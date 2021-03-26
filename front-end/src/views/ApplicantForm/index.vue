<template>
  <div :class="$style.root">
    <template v-if="!formSubmitted">
      <div>
        <h2>{{ headers[step] }}</h2>

        <el-steps
          :active="stepIndex"
          finish-status="success"
          :align-center="true"
        >
          <el-step v-for="(title, key) in STEPS_RU" :key="key" />
        </el-steps>
        <center>{{ STEPS_RU[step] }}</center>
      </div>

      <template v-if="step !== STEPS.brothers && step !== STEPS.sisters">
        <el-form
          ref="form"
          :model="studentData[step]"
          :rules="rules[step]"
          :key="step"
        >
          <el-form-item
            v-for="({ component, title, props = {} }, key) in fields[step]"
            :key="key"
            :prop="key"
          >
            <component
              :is="component"
              :title="title"
              v-bind="props"
              v-model="studentData[step][key]"
            />
          </el-form-item>
        </el-form>

        <div
          v-if="
            step === STEPS.photo &&
            studentData.photo.photo &&
            studentData.photo.photo.length
          "
          :style="{
            flex: 1,
            background: 'no-repeat center / contain',
            backgroundImage: `url('${getObjUrl(
              studentData.photo.photo[0].raw
            )}')`,
            margin: '10px',
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
            Добавить {{ tabButtonLabel[step] }}
          </el-button>

          <el-tabs
            v-model="tabsIndex[step]"
            type="card"
            closable
            @tab-remove="removeTab"
          >
            <el-tab-pane
              v-for="(item, index) in studentData[step]"
              :key="index"
              :label="item.name || `${tabsLabel[step]} ${index + 1}`"
              :name="`${index}`"
            >
              <el-form
                v-if="+tabsIndex[step] === index"
                ref="form"
                :model="item"
                :rules="rules[step]"
              >
                <el-form-item
                  v-for="({ component, title, props = {} }, key) in fields[
                    step
                  ]"
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

        <div v-if="!studentData[step].length">
          Добавьте {{ tabsLabelMany[step] }} (при наличии)
        </div>
      </template>

      <div>
        <el-button v-if="step !== firstStep" @click="prev"> Назад </el-button>

        <el-button v-if="step !== lastStep" @click="next" type="primary">
          Дальше
        </el-button>
        <el-button
          v-else
          type="primary"
          v-loading="isSubmitting"
          @click="submit"
        >
          Отправить форму
        </el-button>
      </div>
    </template>

    <template v-else>
      <div :class="$style.thanks">
        <h2>Форма успешно отправлена</h2>
      </div>
    </template>
  </div>
</template>

<script>
import {
  DateInput,
  FileInput,
  TextInput,
  SelectInput,
  SingleCheckbox,
} from "@/common/inputs";
import allowMobileView from "@/utils/allowMobileView";
import { addStudent } from "@/api/students";
import {
  ABOUT,
  BIRTH_INFO,
  CONTACT_INFO,
  PASSPORT,
  RECRUITMENT_OFFICE,
  UNIVERSITY_INFO,
  MILSPECIALTY,
  PHOTO,
  AGREEMENT,
  HEADERS_BY_STEPS,
  STEPS_RU,
  getRelationData,
  STEPS,
} from "@/constants/applicantForm";

import { getReferenceMilSpecialties } from "@/api/reference-book";

export default {
  name: "ApplicantForm",
  components: { DateInput, FileInput, TextInput, SelectInput, SingleCheckbox },

  data() {
    const createData = (fields) =>
      Object.keys(fields).reduce(
        (memo, item) => ({
          ...memo,
          [item]: "",
        }),
        {}
      );

    return {
      studentData: {
        about: createData(ABOUT),
        birthInfo: createData(BIRTH_INFO),
        passport: createData(PASSPORT),
        recruitmentOffice: createData(RECRUITMENT_OFFICE),
        universityInfo: createData(UNIVERSITY_INFO),
        contactInfo: createData(CONTACT_INFO),
        mother: createData(getRelationData("матери")),
        father: createData(getRelationData("отца")),
        brothers: [],
        sisters: [],
        photo: { photo: null },
        milspecialty: createData(MILSPECIALTY),
        agreement: createData(AGREEMENT),
      },
      fields: {
        about: ABOUT,
        birthInfo: BIRTH_INFO,
        passport: PASSPORT,
        recruitmentOffice: RECRUITMENT_OFFICE,
        universityInfo: UNIVERSITY_INFO,
        contactInfo: CONTACT_INFO,
        mother: getRelationData("матери"),
        father: getRelationData("отца"),
        brothers: getRelationData("брата"),
        sisters: getRelationData("сестры"),
        photo: PHOTO,
        milspecialty: MILSPECIALTY,
        agreement: AGREEMENT,
      },

      formSubmitted: false,
      isSubmitting: false,
      headers: HEADERS_BY_STEPS,

      step: STEPS.about,
      STEPS,
      STEPS_RU,

      tabsIndex: {
        brothers: "",
        sisters: "",
      },

      tabsLabel: { brothers: "Брат", sisters: "Сестра" },
      tabsLabelMany: { brothers: "братьев", sisters: "сестёр" },
      tabButtonLabel: { brothers: "брата", sisters: "сестру" },
      relationsLabel: { brothers: "брата", sisters: "сёстры" },
    };
  },

  computed: {
    firstStep() {
      return Object.keys(STEPS)[0];
    },
    lastStep() {
      const stepsNames = Object.keys(STEPS);
      return stepsNames[stepsNames.length - 1];
    },
    stepIndex() {
      return Object.keys(STEPS).indexOf(this.step);
    },
    campus() {
      return this.studentData.universityInfo.campus;
    },
    rules() {
      const required = { required: true, message: "Обязательное поле" };

      const getValidator = (regExp, msg) => ({
        validator: (rule, value, cb) => {
          if (value && !regExp.test(value)) {
            cb(new Error(msg));
          } else {
            cb();
          }
        },
      });

      const mailValidator = getValidator(/@.+\..+/, "Введите корректную почту");
      const corpMailValidator = getValidator(
        /[A-Za-z0-9._%+-]+@edu\.hse\.ru$/,
        "Почта должна оканчиваться на @edu.hse.ru"
      );
      const phoneValidator = getValidator(
        /^\+?\d{11}$/,
        "Введите корректный номер телефона"
      );
      const makeRequired = (fields) =>
        fields.reduce((memo, item) => ({ ...memo, [item]: [required] }), {});

      const relationFields = {
        ...makeRequired([
          "surname",
          "name",
          "citizenship",
          "date",
          "country",
          "city",
        ]),
        personal_email: [mailValidator],
        personal_phone_number: [phoneValidator],
      };

      const fatherFields = {
        ...relationFields,
      };

      if (!this.studentData.mother.personal_phone_number) {
        fatherFields.personal_phone_number = [
          {
            required: true,
            message: "Укажите номер матери или отца",
          },
          phoneValidator,
        ];
      }

      const withFaterRules = Object.values(this.studentData.father).filter(
        Boolean
      ).length;
      const withMotherRules = Object.values(this.studentData.mother).filter(
        Boolean
      ).length;

      return {
        about: makeRequired([
          "surname",
          "name",
          "citizenship",
          "surname_genitive",
          "name_genitive",
        ]),
        birthInfo: makeRequired(["date", "country", "city"]),
        passport: {
          ...makeRequired(["ufms_name", "issue_date"]),
          series: [
            required,
            getValidator(/^\d{4}$/, "Введите серию паспорта в формате 1234"),
          ],
          code: [
            required,
            getValidator(/^\d{6}$/, "Введите номер паспорта в формате 567890"),
          ],
          ufms_code: [
            required,
            getValidator(
              /^\d{3}-\d{3}$/,
              "Введите код подразделения в формате 700-007 "
            ),
          ],
        },
        recruitmentOffice: makeRequired(["title"]),
        universityInfo: {
          ...makeRequired(["campus", "card_id", "program", "group_title"]),
          program: [
            required,
            getValidator(
              /^\d\d.\d\d.\d\d$/,
              "Введите код программы в формате 01.02.03"
            ),
          ],
        },
        contactInfo: {
          personal_email: [mailValidator],
          corporate_email: [required, corpMailValidator],
          personal_phone_number: [phoneValidator],
        },
        mother: withMotherRules ? relationFields : {},
        father: withFaterRules ? fatherFields : {},
        brothers: relationFields,
        sisters: relationFields,
        photo: { photo: [required] },
        milspecialty: { milspecialty: [required] },
        agreement: { agreement: [required], isDataCorrect: [required] },
      };
    },
  },

  created() {
    allowMobileView(true);
  },

  destroyed() {
    allowMobileView(false);
  },

  methods: {
    fillMilspecialtyOptions(data) {
      this.fields.milspecialty.milspecialty.props.options = data.map(
        (item) => ({
          label: item.milspecialty
            ? `${item.code} - ${item.milspecialty}`
            : item.code,
          value: item.code,
        })
      );
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
      };
    },

    validate() {
      let isValid = true;
      const ref = this.$refs.form;

      const formValidate = (valid) => {
        if (!valid && isValid) {
          this.$message({
            type: "error",
            message: "Заполните все обязательные поля",
          });
          isValid = false;
        }
      };

      if (ref) {
        if (this.lodash.isArray(ref)) {
          ref.forEach((item) => item.validate(formValidate));
        } else {
          ref.validate(formValidate);
        }
      }

      return isValid;
    },

    next() {
      const { studentData, step } = this;
      const data = studentData[step];

      Object.keys(data).forEach((key) => {
        if (this.lodash.isString(data[key])) {
          data[key] = data[key].trim();
        }
      });

      if (this.validate()) {
        const stepsKeys = Object.keys(STEPS);
        const stepIndex = stepsKeys.indexOf(step);
        this.step = stepsKeys[stepIndex + 1] || stepsKeys[stepsKeys.length - 1];
      }
    },

    prev() {
      const stepsKeys = Object.keys(STEPS);
      const stepIndex = stepsKeys.indexOf(this.step);
      const newIndex = stepIndex >= 1 ? stepIndex - 1 : 0;
      this.step = stepsKeys[newIndex];
    },

    addTab() {
      const { step } = this;

      if (this.validate()) {
        this.studentData[step] = [
          ...this.studentData[step],
          Object.keys(getRelationData(this.relationsLabel[step])).reduce(
            (memo, item) => ({ ...memo, [item]: "" }),
            {}
          ),
        ];
        this.tabsIndex[step] = `${this.studentData[step].length - 1}`;
      }
    },

    removeTab(index) {
      const { step } = this;

      const newArr = [...this.studentData[step]];
      newArr.splice(+index, 1);
      this.studentData[step] = newArr;
      this.tabsIndex = {
        ...this.tabsIndex,
        [step]: +this.tabsIndex[step] ? `${+this.tabsIndex[step] - 1}` : "0",
      };
    },

    getObjUrl(file) {
      return URL.createObjectURL(file);
    },

    submit() {
      if (this.validate()) {
        const family = [];

        if (Object.values(this.studentData.father).filter(Boolean).length) {
          family.push({
            ...this.convertFamily(this.studentData.father),
            type: "FA",
          });
        }

        if (Object.values(this.studentData.mother).filter(Boolean).length) {
          family.push({
            ...this.convertFamily(this.studentData.mother),
            type: "MO",
          });
        }

        this.studentData.brothers.forEach((brother) =>
          family.push({
            ...this.convertFamily(brother),
            type: "BR",
          })
        );

        this.studentData.sisters.forEach((sister) =>
          family.push({
            ...this.convertFamily(sister),
            type: "SI",
          })
        );

        const reader = new FileReader();

        console.log(this.studentData.photo.photo);

        const data = {
          ...this.studentData.about,
          ...this.studentData.milspecialty,
          birth_info: this.studentData.birthInfo,
          contact_info: this.studentData.contactInfo,
          passport: this.studentData.passport,
          recruitment_office: this.studentData.recruitmentOffice,
          university_info: this.studentData.universityInfo,
          family,
        };

        this.isSubmitting = true;

        reader.onload = async () => {
          data.image = reader.result;

          try {
            await addStudent(data);
            this.formSubmited = true;
          } catch (e) {
            this.$message({
              type: "error",
              message: "Не удалось отправить форму",
            });
          }

          this.isSubmitting = false;
          this.formSubmitted = true;
        };

        reader.readAsDataURL(this.studentData.photo.photo[0].raw);
      }
    },
  },

  watch: {
    async campus(nextValue) {
      const { data } = await getReferenceMilSpecialties(nextValue);
      this.fillMilspecialtyOptions(data);
    },
  },
};
</script>

<style lang="scss" module>
.root {
  display: flex;
  max-width: 600px;
  min-height: 80vh;
  margin: auto;
  padding: 20px 10px;
  flex-direction: column;
  justify-content: space-between;
}

.thanks {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}
</style>
