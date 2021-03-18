<template>
  <div :class="$style.root">
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
            :label="`${item.name || tabsLabel[stepName]} ${index + 1}`"
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
    
    <div>
      <el-button v-if="step !== 1" @click="prev">
        Назад
      </el-button>

      <el-button
        v-if="step !== STEPS.sisters"
        @click="next"
        type="primary"
      >
        Дальше
      </el-button>
      <el-button v-else @click="submit">
      </el-button>
    </div>
  </div>
</template>

<script>
import { DateInput, FileInput, TextInput } from '@/common/inputs'

const STEPS = {
  about: 1,
  birthInfo: 2,
  contactInfo: 3,
  passport: 4,
  recruitmentOffice: 5,
  universityInfo: 6,
  photo: 7,
  mother: 8,
  father: 9,
  brothers: 10,
  sisters: 11,
}

const getRelationData = (rel) => {
  return {
    surname: {component: 'TextInput', title: `Фамилия ${rel}`},
    name: {component: 'TextInput', title: `Имя ${rel}`},
    patronymic: {component: 'TextInput', title: `Отчество ${rel} (при наличии)`},
    citizenship: {component: 'TextInput', title: `Гражданство ${rel}`},
    permanent_address: {component: 'TextInput', title: `Адрес постоянной регистрации ${rel}`},
    date: {component: 'DateInput', title: `Дата рождения ${rel}`},
    country: {component: 'TextInput', title: `Страна рождения ${rel}`},
    city: {component: 'TextInput', title: `Город рождения ${rel}`},
    personal_email: {component: 'TextInput', title: `Личная почта ${rel}`},
    personal_phone_number: {component: 'TextInput', title: `Номер телефона ${rel}`},
  }
}

export default {
  name: 'ReceiptForm',
  components: { DateInput, FileInput, TextInput },
  data() {
    const required = [{ required: true, message: "Обязательное поле" }];

    const about = {
      surname: {component: 'TextInput', title: 'Фамилия'},
      name: {component: 'TextInput', title: 'Имя'},
      patronymic: {component: 'TextInput', title: 'Отчество (при наличии)'},
      citizenship: {component: 'TextInput', title: 'Гражданство'},
      permanent_address: {component: 'TextInput', title: 'Адрес постоянной регистрации'},
      surname_genitive: {component: 'TextInput', title: 'Фамилия в родительном падеже'},
      name_genitive: {component: 'TextInput', title: 'Имя в родительном падеже'},
      patronymic_genitive: {component: 'TextInput', title: 'Отчество в родительном падеже (при наличии)'},
    }

    const birthInfo = {
      date: {component: 'DateInput', title: 'Дата рождения'},
      country: {component: 'TextInput', title: 'Страна рождения'},
      city: {component: 'TextInput', title: 'Город рождения'},
    }

    const contactInfo = {
      corporate_email: {component: 'TextInput', title: 'Корпоративная почта'},
      personal_email: {component: 'TextInput', title: 'Личная почта'},
      personal_phone_number: {component: 'TextInput', title: 'Номер телефона'},
    }

    const passport = {
      series: {component: 'TextInput', title: 'Серию паспорта'},
      code: {component: 'TextInput', title: 'Номер паспорта'},
      ufms_name: {component: 'TextInput', title: 'Отделения выдавшее паспорт'},
      ufms_code: {component: 'TextInput', title: 'Код отделения выдавшее паспорт'},
      issue_date: {component: 'DateInput', title: 'Дата выдачи паспорта'},
    }

    const recruitmentOffice = {
      city: {component: 'TextInput', title: 'Состою на воинском учете в военном комиссариате города'},
      district: {component: 'TextInput', title: 'Состою на воинском учете в военном комиссариате района'},
    }

    const universityInfo = {
      card_id: {component: 'TextInput', title: 'Номер студенческого билета'},
      program: {component: 'TextInput', title: 'Образовательная программа'},
      group: {component: 'TextInput', title: 'Номер группы'},
    }

    return {
      studentData: {
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
        photo: { photo: null }
      },
      fields: {
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
        photo: { photo: {component: 'FileInput', title: 'Загрузите фотографию', props: { filesTypes: ['.png', '.jpg', '.jpeg']}} }
      },

      step: 1,
      STEPS,
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

      rules: {
        about: ['surname', 'name', 'citizenship', 'surname_genitive', 'name_genitive']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        birthInfo: ['date', 'country', 'city']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        passport: ['series', 'code', 'ufms_name', 'ufms_code', 'issue_date']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        recruitmentOffice: ['city', 'district']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        universityInfo: ['card_id', 'program', 'group_title']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        contactInfo: { personal_email: required },
        mother: ['surname', 'name', 'citizenship', 'date', 'country', 'city']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        father: ['surname', 'name', 'citizenship', 'date', 'country', 'city']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        brothers: ['surname', 'name', 'citizenship', 'date', 'country', 'city']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        sisters: ['surname', 'name', 'citizenship', 'date', 'country', 'city']
          .reduce((memo, item) => ({...memo, [item]: required}), {}),
        photo: { photo: required }
      },
    }
  },

  computed: {
    stepName() {
      return Object.entries(STEPS).find(([, value]) => value === this.step)[0]
    },
  },

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
    onSubmit() {
      this.$refs.form.validate((valid) => {
        console.log('this.formValues.book', this.formValues.book)
        if (!valid || (!this.isChanging && !this.formValues.book.length)) return false

        this.$emit('save', this.formValues)
        this.$emit('close-modal')
      })
    },

    next() {
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
        const father = {
          ...this.convertFamily(this.studentData.father),
          type: 'FA',
        }

        const mother = {
          ...this.convertFamily(this.studentData.mother),
          type: 'MO',
        }
        const brothers = this.studentData.brothers.map(brother => ({
          ...this.convertFamily(brother),
          type: 'BR',
        }))

        const sisters = this.studentData.sisters.map(sister => ({
          ...this.convertFamily(sister),
          type: 'SI',
        }))

        const reader = new FileReader()

        console.log(this.studentData.photo.photo)

        const data = {
          ...this.studentData.about,
          birth_info: this.studentData.birthInfo,
          contact_info: this.studentData.contactInfo,
          passport: this.studentData.passport,
          recruitment_office: this.studentData.recruitmentOffice,
          university_info: this.studentData.universityInfo,
          family: [father, mother, ...brothers, ...sisters]
        }

        reader.onload = () => {
          data.image = reader.result

          console.log(data)
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
  padding-top: 20px;
  flex-direction: column;
  justify-content: space-between;
}
</style>
