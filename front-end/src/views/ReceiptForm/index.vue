<template>
  <div :class="$style.root">
    <div>
      <h2>{{ headers[stepName] }}</h2>

      <el-steps :active="+step - 1" finish-status="success">
        <el-step
          v-for="(title, key) in STEPS_RU"
          :key="key"
          :title="key === stepName ? title : ''"
        />
      </el-steps>

      <template v-if="step !== STEPS.brothers && step !== STEPS.sisters">
        <el-form
          ref="form"
          :model="studentData[stepName]"
          :rules="rules[stepName]"
          :key="step"
        >
          <el-form-item
            v-for="({component, title, props = {}}, key) in fields[stepName]"
            :key="key"
            :prop="key"
          >
            <component
              :is="component"
              :title="title"
              v-bind="props"
              v-model="studentData[stepName][key]"
            />
          </el-form-item>
        </el-form>

        <div
          v-if="step === STEPS.photo && studentData.photo.photo && studentData.photo.photo.length"
          :style="{
            flex: 1,
            background: 'no-repeat center / contain',
            backgroundImage: `url('${getObjUrl(studentData.photo.photo[0].raw)}')`,
            margin: '10px'
          }"
        />
      </template>

      <template v-else>
        <div>
          <el-button
            style="width: 100%"
            icon="el-icon-plus"
            type="primary"
            @click="addTab"
          >
            Добавить {{ tabButtonLabel[stepName] }}
          </el-button>

          <el-tabs v-model="tabsIndex[stepName]" type="card" closable @tab-remove="removeTab">
            <el-tab-pane
              v-for="(item, index) in studentData[stepName]"
              :key="index"
              :label="item.name || `${tabsLabel[stepName]} ${index + 1}`"
              :name="`${index}`"
            >
              <el-form
                v-if="+tabsIndex[stepName] === index"
                ref="form"
                :model="item"
                :rules="rules[stepName]"
              >
                <el-form-item
                  v-for="({component, title, props = {}}, key) in fields[stepName]"
                  :key="key"
                  :prop="key"
                >
                  <component
                    :is="component"
                    :title="title"
                    v-bind="props"
                    v-model="item[key]"
                  />
                </el-form-item>
              </el-form>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div v-if="!studentData[stepName].length">
          Добавьте {{ tabsLabelMany[stepName]}} (при наличии)
        </div>
      </template>
    </div>

    <div>
      <el-button v-if="step !== 1" @click="prev">
        Назад
      </el-button>

      <el-button
        v-if="step !== STEPS.military"
        @click="next"
        type="primary"
      >
        Дальше
      </el-button>
      <el-button v-else type="primary" @click="submit">
        Отправить форму
      </el-button>
    </div>
  </div>
</template>

<script>
import { DateInput, FileInput, TextInput, SelectInput } from '@/common/inputs'
import allowMobileView from '@/utils/allowMobileView'
import { addStudent } from '@/api/students'

const STEPS = {
  campus: 1,
  about: 2,
  birthInfo: 3,
  contactInfo: 4,
  passport: 5,
  recruitmentOffice: 6,
  universityInfo: 7,
  photo: 8,
  mother: 9,
  father: 10,
  brothers: 11,
  sisters: 12,
  military: 13,
}

const STEPS_RU = {
  campus: 'Кампус',
  about: 'Общая',
  birthInfo: 'Рождение',
  contactInfo: 'Контакты',
  passport: 'Паспорт',
  recruitmentOffice: 'Военкомат',
  universityInfo: 'Университет',
  photo: 'Фото',
  mother: 'Мать',
  father: 'Отец',
  brothers: 'Братья',
  sisters: 'Сестры',
  military: 'Направление ВУЦ'
}

const getRelationData = (rel) => {
  return {
    surname: {component: 'TextInput', title: `Фамилия ${rel}`, props: { onlyChars: true }},
    name: {component: 'TextInput', title: `Имя ${rel}`, props: { onlyChars: true }},
    patronymic: {component: 'TextInput', title: `Отчество ${rel} (при наличии)`, props: { onlyChars: true }},
    citizenship: {component: 'TextInput', title: `Гражданство ${rel}`, props: { onlyChars: true }},
    permanent_address: {component: 'TextInput', title: `Адрес постоянной регистрации ${rel}`},
    date: {component: 'DateInput', title: `Дата рождения ${rel}`},
    country: {component: 'TextInput', title: `Страна рождения ${rel}`, props: { onlyChars: true }},
    city: {component: 'TextInput', title: `Город рождения ${rel}`},
    personal_email: {component: 'TextInput', title: `Личная почта ${rel}`},
    personal_phone_number: {component: 'TextInput', title: `Номер телефона ${rel}`},
  }
}

export default {
  name: 'ReceiptForm',
  components: { DateInput, FileInput, TextInput, SelectInput },
  data() {
    const required = { required: true, message: "Обязательное поле" };
    const mailValidator = {validator: (rule, value, cb) => {
      if (value && !/@.+\..+/.test(value)) {
        cb(new Error('Введите корректный email'))
      } else {
        cb()
      }
    }}
    const corpMailValidator = {validator: (rule, value, cb) => {
      if (value && !/[A-Za-z0-9_]*@edu\.hse\.ru$/.test(value)) {
        cb(new Error('Введите корректный email'))
      } else {
        cb()
      }
    }}
    const phoneValidator = {validator: (rule, value, cb) => {
      if (value && !/^\+?\d{10}$/.test(value)) {
        cb(new Error('Введите корректный телефон'))
      } else {
        cb()
      }
    }}

    const campus = {
      mil_campus: {component: 'SelectInput', title: 'Кампус', props: {
        options: ['Москва', 'Санкт-Петербург', 'Нижний Новгород', 'Пермь'],
      }},
    }

    const about = {
      surname: {component: 'TextInput', title: 'Фамилия', props: { onlyChars: true }},
      name: {component: 'TextInput', title: 'Имя', props: { onlyChars: true }},
      patronymic: {component: 'TextInput', title: 'Отчество (при наличии)', props: { onlyChars: true }},
      citizenship: {component: 'TextInput', title: 'Гражданство', props: { onlyChars: true }},
      permanent_address: {component: 'TextInput', title: 'Адрес постоянной регистрации'},
      surname_genitive: {component: 'TextInput', title: 'Фамилия в родительном падеже', props: { onlyChars: true }},
      name_genitive: {component: 'TextInput', title: 'Имя в родительном падеже', props: { onlyChars: true }},
      patronymic_genitive: {component: 'TextInput', title: 'Отчество в родительном падеже (при наличии)', props: { onlyChars: true }},
    }

    const birthInfo = {
      date: {component: 'DateInput', title: 'Дата'},
      country: {component: 'TextInput', title: 'Страна'},
      city: {component: 'TextInput', title: 'Город'},
    }

    const contactInfo = {
      corporate_email: {component: 'TextInput', title: 'Корпоративная почта'},
      personal_email: {component: 'TextInput', title: 'Личная почта'},
      personal_phone_number: {component: 'TextInput', title: 'Номер телефона'},
    }

    const passport = {
      series: {component: 'TextInput', title: 'Серия'},
      code: {component: 'TextInput', title: 'Номер'},
      ufms_name: {component: 'TextInput', title: 'Отделение выдачи'},
      ufms_code: {component: 'TextInput', title: 'Код отделения'},
      issue_date: {component: 'DateInput', title: 'Дата выдачи'},
    }

    const recruitmentOffice = {
      city: {component: 'TextInput', title: 'города'},
      district: {component: 'TextInput', title: 'района'},
    }

    const universityInfo = {
      card_id: {component: 'TextInput', title: 'Номер студенческого билета'},
      program: {component: 'TextInput', title: 'Образовательная программа'},
      group: {component: 'TextInput', title: 'Номер группы'},
    }

    const MILS = [
      {
        milgroup: 'ВКС',
        milspecialty: 'Математическое и программное обеспечение ВРК'
      },
      {
        milgroup: 'РВСН',
        milspecialty: 'Залупа какая-то'
      }
    ]

    const military = {
      military: {component: 'SelectInput', title: 'Направление ВУЦ', props: {
        options: MILS.map(item => ({
          label: item.milspecialty,
          value: item,
        }))
      }}
    }

    const rules = {
        campus: ['mil_campus']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        about: ['surname', 'name', 'citizenship', 'surname_genitive', 'name_genitive']
          .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
        birthInfo: ['date', 'country', 'city']
          .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
        passport: ['series', 'code', 'ufms_name', 'ufms_code', 'issue_date']
          .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
        recruitmentOffice: ['city', 'district']
          .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
        universityInfo: ['card_id', 'program', 'group_title']
          .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
        contactInfo: { personal_email: [mailValidator], corporate_email: [required, corpMailValidator], personal_phone_number: [phoneValidator] },
        mother: {
          ...[/* 'surname', 'name', 'citizenship', 'date', 'country', 'city' */]
            .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
          ...{personal_email: [mailValidator], personal_phone_number: [phoneValidator]}
        },
        father: {
          ...[/* 'surname', 'name', 'citizenship', 'date', 'country', 'city' */]
            .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
          ...{personal_email: [mailValidator], personal_phone_number: [phoneValidator]}
        },
        brothers: {
          ...['surname', 'name', 'citizenship', 'date', 'country', 'city']
            .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
          ...{personal_email: [mailValidator], personal_phone_number: [phoneValidator]}
        },
        sisters: {
          ...['surname', 'name', 'citizenship', 'date', 'country', 'city']
            .reduce((memo, item) => ({...memo, [item]: [required]}), {}),
          ...{personal_email: [mailValidator], personal_phone_number: [phoneValidator]}
        },
        photo: { photo: [required] },
        military: { military: [required] }
    }
    return {
      studentData: {
        campus: Object.keys(campus).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        about: Object.keys(about).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        birthInfo: Object.keys(birthInfo).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        passport: Object.keys(passport).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        recruitmentOffice: Object.keys(recruitmentOffice).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        universityInfo: Object.keys(universityInfo).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        contactInfo: Object.keys(contactInfo).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        mother: Object.keys(getRelationData('матери')).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        father: Object.keys(getRelationData('отца')).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        brothers: [],
        sisters: [],
        photo: { photo: null },
        military: Object.keys(military).reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
      },
      fields: {
        campus,
        about,
        birthInfo,
        passport,
        recruitmentOffice,
        universityInfo,
        contactInfo,
        mother: getRelationData('матери'),
        father: getRelationData('отца'),
        brothers: getRelationData('брата'),
        sisters: getRelationData('сестры'),
        photo: { photo: {component: 'FileInput', title: 'Загрузите фотографию', props: { filesTypes: ['.png', '.jpg', '.jpeg']}} },
        military,
      },

      headers: {
        campus: 'Город обучения',
        about: 'Данные о вас',
        birthInfo: 'Информация о рождении',
        contactInfo: 'Контактная информация',
        passport: 'Данные паспорта',
        recruitmentOffice: 'Состою на воинском учете в военном комиссариате',
        universityInfo: 'Информация о ВУЗе',
        photo: 'Фотография',
        mother: 'Данные о матери (При необходимости оставьте поля пустыми)',
        father: 'Данные об отце (При необходимости оставьте поля пустыми)',
        brothers: 'Данные о братьях',
        sisters: 'Данные о сестрах',
        military: 'Направление в ВУЦ',
      },

      step: STEPS.campus,
      STEPS,
      STEPS_RU,
      tabsIndex: {
        brothers: '',
        sisters: '',
      },

      tabsLabel: {
        brothers: 'Брат',
        sisters: 'Сестра',
      },

      tabsLabelMany: {
        brothers: 'братьев',
        sisters: 'сестер',
      },
    
      tabButtonLabel: {
        brothers: 'брата',
        sisters: 'сестру',
      },

      relationsLabel: {
        brothers: 'брата',
        sisters: 'сестры',
      },

      rules,
    }
  },

  computed: {
    stepName() {
      return Object.entries(STEPS).find(([, value]) => value === this.step)[0]
    },
  },

  created() { allowMobileView(true)} ,

  destroyed() { allowMobileView(false) },

  methods: {
    getFamilyInit() {
      return {
        rel_status: '',
        birthdate: '',
        citizenship: '',
        pers_mobile: '',
        permanent_address: '',
        place_birth: '',
      }
    },

    convertFamily(data) {
      return {
        surname: data.surname,
        name: data.name,
        patronymic: data.patronymic,
        citizenship: data.citizenship,
        permanent_address: data.permanent_address,
        contact_info: {
          personal_email: data.personal_email,
          personal_phone_number: data.personal_phone_number,
        },
        birth_info: {
          date: data.date,
          country: data.country,
          city: data.city,
        },
      }
    },

    validate() {
      let isValid = true
      const ref = this.$refs.form


      const formValidate = (valid) => {
        if (!valid && isValid) {
          this.$message({
            type: 'error',
            message: 'Заполните все обязательные поля',
          })
          isValid = false
        }
      }

      if (ref) {
        if (this.lodash.isArray(ref)) {
          ref.forEach(item => item.validate(formValidate))
        } else {
          ref.validate(formValidate)
        }
      }

      return isValid
    },

    next() {
      const { studentData, stepName } = this
      const data = studentData[stepName] 
      Object.keys(data).forEach(key => {
        if (this.lodash.isString(data[key])) {
          data[key] = data[key].trim()
        }
      })

      if (this.validate()) this.step += 1
    },
    prev() { this.step = (this.step - 1) || 1 },

    addTab() {
      if (this.validate()) {
        this.studentData[this.stepName] = [
          ...this.studentData[this.stepName],
          Object.keys(getRelationData(this.relationsLabel[this.stepName]))
            .reduce((memo, item) => ({ ...memo, [item]: '' }), {}),
        ]
        this.tabsIndex[this.stepName] = `${this.studentData[this.stepName].length - 1}`
      }
    },
    removeTab(index) {
      const newArr = [...this.studentData[this.stepName]]
      newArr.splice(+index, 1)
      this.studentData[this.stepName] = newArr
      this.tabsIndex = {
        ...this.tabsIndex,
        [this.stepName]: +this.tabsIndex[this.stepName]
          ? `${+this.tabsIndex[this.stepName] - 1}`
          : '0',
      }
    },
    getObjUrl(file) {
      return URL.createObjectURL(file)
    },

    submit() {
      if (this.validate()) {
        const family = []

        if (Object.values(this.studentData.father).filter(Boolean).length) {
          family.push({
            ...this.convertFamily(this.studentData.father),
            type: 'FA',
          })
        }

        if (Object.values(this.studentData.mother).filter(Boolean).length) {
          family.push({
            ...this.convertFamily(this.studentData.mother),
            type: 'MO',
          })
        }

        this.studentData.brothers.forEach(brother => family.push({
          ...this.convertFamily(brother),
          type: 'BR',
        }))

        this.studentData.sisters.forEach(sister => family.push({
          ...this.convertFamily(sister),
          type: 'SI',
        }))

        const reader = new FileReader()

        console.log(this.studentData.photo.photo)

        const data = {
          ...this.studentData.about,
          ...this.studentData.campus,
          ...JSON.parse(this.studentData.military.military),
          birth_info: this.studentData.birthInfo,
          contact_info: this.studentData.contactInfo,
          passport: this.studentData.passport,
          recruitment_office: this.studentData.recruitmentOffice,
          university_info: this.studentData.universityInfo,
          family
        }

        reader.onload = () => {
          data.image = reader.result

          addStudent(data)
        }

        reader.readAsDataURL(this.studentData.photo.photo[0].raw)
      } 
    }
  }
}
</script>

<style lang="scss" module>
.root {
  display: flex;
  max-width: 600px;
  min-height: 80vh;
  margin: auto;
  padding: 20px 10px 0;
  flex-direction: column;
  justify-content: space-between;
}

</style>
