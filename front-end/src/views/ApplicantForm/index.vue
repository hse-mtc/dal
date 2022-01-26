<template>
  <div :class="$style.root">
    <template v-if="!formSubmitted">
      <div :class="$style.header">
        <h2 :class="$style.title">
          {{ headers[step] }}
        </h2>

        <el-steps
          :active="stepIndex"
          finish-status="success"
          :align-center="true"
        >
          <el-step
            v-for="(title, key) in STEPS_RU"
            :key="key"
            @click.native="goToStep(key)"
          />
        </el-steps>
      </div>

      <template v-if="step !== STEPS.brothers && step !== STEPS.sisters">
        <GenericForm
          :key="step"
          ref="form"
          v-model="applicantData[step]"
          :rules="rules[step]"
          :fields="fields[step]"
        >
          <template #buttons>
            {{ null }}
          </template>
        </GenericForm>

        <div
          v-if="
            step === STEPS.photo &&
              applicantData.photo.photo &&
              applicantData.photo.photo.length
          "
          :style="{
            width: '300px',
            height: '400px',
            background: 'no-repeat center / contain',
            backgroundImage: `url('${getObjUrl(
              applicantData.photo.photo[0].raw,
            )}')`,
            margin: '10px auto',
          }"
        />
      </template>

      <template v-else>
        <div>
          <el-button
            style="width: 100%"
            icon="el-icon-plus"
            type="primary"
            :style="{ sdhbchbsc: 3 }"
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
              v-for="(item, index) in applicantData[step]"
              :key="index"
              :label="item.name || `${tabsLabel[step]} ${index + 1}`"
              :name="`${index}`"
            >
              <GenericForm
                v-if="+tabsIndex[step] === index"
                ref="form"
                :key="`${step}-${index}`"
                v-model="applicantData[step][index]"
                :rules="rules[step]"
                :fields="fields[step]"
              >
                <template #buttons>
                  {{ null }}
                </template>
              </GenericForm>
            </el-tab-pane>
          </el-tabs>
        </div>

        <div v-if="!applicantData[step].length">
          Добавьте {{ tabsLabelMany[step] }} (при наличии)
        </div>
      </template>

      <div>
        <el-button v-if="step !== firstStep" @click="prev">
          Назад
        </el-button>

        <el-button
          v-if="step !== lastStep"
          type="primary"
          native-type="submit"
          @click="next"
        >
          Дальше
        </el-button>
        <el-button
          v-else
          v-loading="isSubmitting"
          type="primary"
          native-type="submit"
          @click="submit"
        >
          Отправить форму
        </el-button>
      </div>

      <div :class="$style.footer">
        <p :class="$style.footerText">
          При возникновении технических трудностей обращайтесь по адресу
          <a href="mailto:dal.mec.hse@gmail.com">dal.mec.hse@gmail.com</a>. В
          письме подробно опишите ситуацию и проблему, с которой Вы столкнулись.
        </p>
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
  Component, Ref, Vue, Watch,
} from "vue-property-decorator";
import _pick from "lodash/pick";
import _omit from "lodash/omit";

import GenericForm from "@/common/Form/index.vue";

import allowMobileView from "@/utils/allowMobileView";
import { postApplicant } from "@/api/applicants";

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

import { getMilSpecialties, getProgramsByCampus } from "@/api/reference-book";
import copyToClipboard from "@/utils/copyToClipboard";
import {getUser} from "@/api/user";

const createData = fields => Object.keys(fields).reduce(
  (memo, item) => ({
    ...memo,
    [item]: "",
  }),
  {},
);

@Component({
  name: "ApplicantForm",
  components: { GenericForm },
})
class ApplicantForm extends Vue {
  @Ref() form

  data() {
    return {
      applicantData: __DEV__ && ("fill" in this.$route.query)
        // eslint-disable-next-line global-require, @typescript-eslint/no-var-requires
        ? require("@/constants/applicantForm").devInitData
        : {
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
    };
  }

  fields = {
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
  }

  formSubmitted = false
  isSubmitting = false
  headers = HEADERS_BY_STEPS

  step = STEPS.about
  STEPS= STEPS
  STEPS_RU = STEPS_RU

  tabsIndex = {
    brothers: "",
    sisters: "",
  }

  tabsLabel = { brothers: "Брат", sisters: "Сестра" }
  tabsLabelMany = { brothers: "братьев", sisters: "сестёр" }
  tabButtonLabel = { brothers: "брата", sisters: "сестру" }
  relationsLabel = { brothers: "брата", sisters: "сёстры" }

  get firstStep() { return Object.keys(STEPS)[0]; }

  get lastStep() {
    const stepsNames = Object.keys(STEPS);
    return stepsNames[stepsNames.length - 1];
  }

  get stepIndex() { return Object.keys(STEPS).indexOf(this.step); }
  get campus() { return this.applicantData.universityInfo.campus; }

  get rules() {
    const required = { required: true, message: "Обязательное поле" };
    const requiredBool = {
      required: true,
      message: "Обязательное поле",
      validator: (rule, value, cb) => {
        if (!value) {
          cb(new Error("Обязательное поле"));
        } else {
          cb();
        }
      },
    };

    const getValidator = (regExp, msg) => ({
      validator: (rule, value, cb) => {
        if (value && !regExp.test(value)) {
          cb(new Error(msg));
        } else {
          cb();
        }
      },
    });

    const getMaxLengthValidator = max => ({
      max,
      message: `Максимальное количество символов - ${max}`,
    });

    const mailValidator = getValidator(/@.+\..+/, "Введите корректную почту");
    const corpMailValidator = getValidator(
      /[A-Za-z0-9._%+-]+@edu\.hse\.ru$/,
      "Почта должна оканчиваться на @edu.hse.ru",
    );
    const phoneValidator = getValidator(
      /^\+?\d{11}$/,
      "Введите корректный номер телефона",
    );
    const makeRequired = fields => fields.reduce((memo, item) => ({
      ...memo,
      [item]: [required],
    }), {});

    const relationFields = {
      ...makeRequired([
        "surname",
        "name",
        "citizenship",
        "permanent_address",
        "date",
      ]),
      city: [required, getMaxLengthValidator(64)],
      country: [required, getMaxLengthValidator(64)],
      personal_email: [mailValidator],
      personal_phone_number: [phoneValidator],
    };

    const withMotherRules = Object.values(this.applicantData.mother).filter(
      Boolean,
    ).length;

    const withFatherRules = Object.values(this.applicantData.father).filter(
      Boolean,
    ).length;

    const motherFatherPhone = [
      {
        required: true,
        message: withFatherRules
          ? "Укажите номер матери или отца"
          : "Укажите номер матери",
      },
      phoneValidator,
    ];

    let fatherFields = {};

    if (!withMotherRules) {
      if (withFatherRules) {
        fatherFields = {
          ...relationFields,
          personal_phone_number: motherFatherPhone,
        };
      }
    } else if (!this.applicantData.mother.personal_phone_number) {
      if (withFatherRules) {
        fatherFields = {
          ...relationFields,
          personal_phone_number: motherFatherPhone,
        };
      } else {
        fatherFields = {
          personal_phone_number: motherFatherPhone,
        };
      }
    }

    return {
      about: makeRequired([
        "surname",
        "name",
        "citizenship",
        "surname_genitive",
        "name_genitive",
      ]),
      birthInfo: {
        ...makeRequired(["date"]),
        country: [required, getMaxLengthValidator(64)],
        city: [required, getMaxLengthValidator(64)],
      },
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
            "Введите код подразделения в формате 700-007 ",
          ),
        ],
      },
      recruitmentOffice: makeRequired(["title"]),
      universityInfo: {
        ...makeRequired(["campus", "card_id", "program", "group"]),
        program: [
          required,
        ],
      },
      contactInfo: {
        personal_email: [mailValidator],
        corporate_email: [required, corpMailValidator],
        personal_phone_number: [phoneValidator],
      },
      mother: withMotherRules ? relationFields : {},
      father: fatherFields,
      brothers: relationFields,
      sisters: relationFields,
      photo: { photo: [required] },
      milspecialty: { milspecialty: [required] },
      agreement: { agreement: [requiredBool], isDataCorrect: [requiredBool] },
    };
  }

  created() { allowMobileView(true); }

  destroyed() { allowMobileView(false); }

  goToStep(key) {
    if (this.$route.hash === "#activate-god-mode") {
      this.step = key;
    }
  }

  fillMilspecialtyOptions(data) {
    this.fields.milspecialty.milspecialty.props.options = data.map(
      item => ({
        label: item.title
          ? `${item.code} - ${item.title}`
          : item.code,
        value: item.id,
      }),
    );
  }

  fillProgramOptions(data) {
    this.fields.universityInfo.program.props.options = data.map(
      item => ({
        label: item.code,
        value: item.id,
      }),
    );
  }

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
        place: data.place,
      },
    };
  }

  validate() {
    let isValid = true;

    const formValidate = valid => {
      if (!valid && isValid) {
        this.$message({
          type: "error",
          message: "Заполните все обязательные поля",
        });
        isValid = false;
      }
    };

    if (this.form) {
      if (this.lodash.isArray(this.form)) {
        this.form.forEach(item => {
          formValidate(item.validate());
        });
      } else {
        formValidate(this.form.validate());
      }
    }

    return isValid;
  }

  next() {
    const { applicantData, step } = this;
    const data = applicantData[step];

    Object.keys(data).forEach(key => {
      if (this.lodash.isString(data[key])) {
        data[key] = data[key].trim();
      }
    });

    if (this.validate()) {
      const stepsKeys = Object.keys(STEPS);
      const stepIndex = stepsKeys.indexOf(step);
      this.step = stepsKeys[stepIndex + 1] || stepsKeys[stepsKeys.length - 1];
    }
  }

  prev() {
    const stepsKeys = Object.keys(STEPS);
    const stepIndex = stepsKeys.indexOf(this.step);
    const newIndex = stepIndex >= 1 ? stepIndex - 1 : 0;
    this.step = stepsKeys[newIndex];
  }

  addTab() {
    const { step } = this;

    if (this.validate()) {
      this.applicantData[step] = [
        ...this.applicantData[step],
        Object.keys(getRelationData(this.relationsLabel[step])).reduce(
          (memo, item) => ({ ...memo, [item]: "" }),
          {},
        ),
      ];
      this.tabsIndex[step] = `${this.applicantData[step].length - 1}`;
    }
  }

  removeTab(index) {
    const { step } = this;

    const newArr = [...this.applicantData[step]];
    newArr.splice(+index, 1);
    this.applicantData[step] = newArr;
    this.tabsIndex = {
      ...this.tabsIndex,
      [step]: +this.tabsIndex[step] ? `${+this.tabsIndex[step] - 1}` : "0",
    };
  }

  getObjUrl(file) {
    return URL.createObjectURL(file);
  }

  submit() {
    if (this.validate()) {
      const family = [];

      if (Object.values(this.applicantData.father).filter(Boolean).length) {
        family.push({
          ...this.convertFamily(this.applicantData.father),
          type: "FA",
        });
      }

      if (Object.values(this.applicantData.mother).filter(Boolean).length) {
        family.push({
          ...this.convertFamily(this.applicantData.mother),
          type: "MO",
        });
      }

      this.applicantData.brothers.forEach(brother => family.push({
        ...this.convertFamily(brother),
        type: "BR",
      }));

      this.applicantData.sisters.forEach(sister => family.push({
        ...this.convertFamily(sister),
        type: "SI",
      }));

      const reader = new FileReader();

      const data = {
        ...this.applicantData.about,
        ...this.applicantData.milspecialty,
        birth_info: this.applicantData.birthInfo,
        contact_info: this.applicantData.contactInfo,
        passport: this.applicantData.passport,
        recruitment_office: this.applicantData.recruitmentOffice.title,
        university_info: this.applicantData.universityInfo,
        family,
        generate_documents: true,
      };

      reader.onload = async() => {
        data.image = reader.result;
        const user = await getUser();
        data.contact_info.corporate_email = user.data.email;

        try {
          await postApplicant(data);
          this.formSubmitted = true;
        } catch (e) {
          if (e.response.status < 500) {
            this.$alert(
              "Проверьте правильность заполненных данных. Если проблема не решится, отправьте текст ошибки нам на почту: <a href=\"mailto:dal.mec.hse@gmail.com\">dal.mec.hse@gmail.com</a>",
              "Не удалось отправить форму",
              {
                confirmButtonText: "Скопировать текст ошибки",
                type: "error",
                dangerouslyUseHTMLString: true,
                callback: async action => {
                  const dataToCopy = e.response
                    ? _pick(e.response, ["config", "data"])
                    : { config: e.config };

                  dataToCopy.config.data = _omit(JSON.parse(dataToCopy.config.data), ["image"]);
                  if (action !== "cancel") {
                    if (await copyToClipboard(JSON.stringify(dataToCopy, null, 4))) {
                      this.$message({
                        type: "success",
                        message: "Текст скопирован",
                      });
                    } else {
                      this.$message({
                        type: "error",
                        message: "Текст не скопирован",
                      });
                    }
                  }
                },
              },
            );
          } else {
            this.$message({
              type: "error",
              message: "Ошибка сервера",
            });
          }
        }

        reader.onerror = () => {
          this.isSubmitting = false;
          console.error("Ошибка чтения файла:", reader.error);
          this.$message({
            type: "error",
            message: "Ошибка чтения файла",
          });
        };

        this.isSubmitting = false;
      };

      try {
        this.isSubmitting = true;
        reader.readAsDataURL(this.applicantData.photo.photo[0].raw);
      } catch (e) {
        this.isSubmitting = false;
        console.error("Ошибка чтения файла:", e);
        this.$message({
          type: "error",
          message: "Ошибка чтения файла",
        });
      }
    }
  }

  @Watch("applicantData.universityInfo.campus")
  async onCampusChange() {
    try {
      const { data } = await getProgramsByCampus(
        this.applicantData.universityInfo.campus,
      );
      this.fillProgramOptions(data);
      this.applicantData.universityInfo.program = this.fields.universityInfo.program.props.options[0].value;
    } catch (e) {
      this.$message({
        type: "error",
        duration: 1000 * 5,
        message: "Ошибка загрузки данных. Вернитесь к предыдущему шагу и заново перейдите на текущий шаг",
      });
    }
  }

  @Watch("step")
  async onStepChange(nextValue) {
    window.scrollTo({
      left: 0,
      top: 0,
    });
    if (nextValue === STEPS.universityInfo && this.applicantData.universityInfo.campus) {
      const { data } = await getProgramsByCampus(
        this.applicantData.universityInfo.campus,
      );
      this.fillProgramOptions(data);
    }
    if (nextValue === STEPS.milspecialty) {
      try {
        const { data } = await getMilSpecialties(
          this.applicantData.universityInfo.campus,
        );
        this.fillMilspecialtyOptions(data);
      } catch (e) {
        this.$message({
          type: "error",
          duration: 1000 * 5,
          message: "Ошибка загрузки данных. Вернитесь к предыдущему шагу и заново перейдите на текущий шаг",
        });
      }
    }
  }
}

export default ApplicantForm;
</script>

<style lang="scss" module>
.header {
  margin-bottom: 30px;

  .title {
    margin-bottom: 20px;
  }
}

.root {
  display: flex;
  max-width: 600px;
  min-height: 100vh;
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
  text-align: center;
}

.footer {
  margin-top: 35px;
  border-top: 1px solid #cfc8c8;
  color: #cfc8c8;
  padding-top: 10px;

  a {
    color: #5a96d6;
  }
}

:global(.el-message-box) {
  width: auto !important;
}
</style>
