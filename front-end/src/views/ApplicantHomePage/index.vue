<template>
  <div>
    <el-row>
      <el-col :span="20" :offset="2">
        <PageHeader title="Личный кабинет абитуриента" />
        <div v-if="personType === ''">
          <div style="margin-bottom: 15px">
            Чтобы подать заявку на поступление в Военный учебный центр НИУ ВШЭ, пройдите форму по кнопке ниже
          </div>
          <router-link to="/applicant-form/">
            <el-button type="primary">
              Пройти форму
            </el-button>
          </router-link>
        </div>
        <div v-if="personType === 'applicant'">
          <div v-if="stages.length === 0">
            Подождите, загрузка данных...
          </div>
          <div v-for="(stage, i) in stages" :key="i">
            <div class="h4" style="margin-top: 30px">
              {{ stage.name }}
            </div>
            <div style="border-bottom: 1px solid lightgray; margin-bottom: 30px">
              <el-row
                v-for="(field, index) in stage.fields"
                :key="index"
                class="tableForm"
              >
                <el-col :span="12" style="padding: 15px">
                  {{ field.name }}
                </el-col>
                <el-col :span="12" class="contentcol" style="padding: 15px; min-height: 54px">
                  <div v-if="field.name !== 'Фото'">
                    {{ field.content }}
                  </div>
                  <div v-if="field.name === 'Фото' && !field.content.photo[0].base" style="font-style: italic">
                    Ошибка загрузки фото
                  </div>
                  <div
                    v-if="
                      field.name === 'Фото' &&
                        field.content.photo &&
                        field.content.photo.length &&
                        field.content.photo[0].base
                    "
                    :style="{
                      width: '100%',
                      height: '300px',
                      background: 'no-repeat center / contain',
                      backgroundImage: `url('${getObjUrl(
                        field.content.photo[0].raw,
                      )}')`,
                      margin: '10px auto',
                    }"
                  />
                </el-col>
              </el-row>
            </div>
          </div>
          <div class="buttons">
            <div style="margin-bottom: 30px">
              <router-link to="/applicant-form/">
                <el-button type="primary">
                  Исправить форму
                </el-button>
              </router-link>
            </div>
            <div style="margin-bottom: 30px; margin-left: 30px">
              <el-button
                type="primary"
                native-type="submit"
                @click="resubmitDocs"
              >
                Отправить повторно документы
              </el-button>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PageHeader from "@/common/PageHeader";
import { UserModule } from "@/store";
import { findApplicant, resumbmitApplicantDocs } from "@/api/applicants";
import { dataURLtoFile } from "@/constants/applicantForm";
import { CAMPUSES } from "@/utils/enums";

export default {
  name: "ApplicantHomePage",
  components: {
    PageHeader,
  },
  data() {
    return {
      stages: [],
    };
  },
  computed: {
    personId() { return UserModule.personId; },
    personType() { return UserModule.personType; },
  },
  mounted() {
    if (this.personType === "applicant") {
      this.fetchDocs();
    }
  },
  methods: {
    getObjUrl(file) {
      return URL.createObjectURL(file);
    },

    getFormattedProgram(program) {
      return `${program.code} – ${program.title}`;
    },

    async resubmitDocs() {
      const data = await resumbmitApplicantDocs();
      if (data.status === 200) {
        this.$message({
          type: "success",
          message: "Документы отправлены на вашу почту.",
          duration: 3000,
        });
      }
    },

    async fetchDocs() {
      const dataRequest = await findApplicant(this.personId);
      const { data } = dataRequest;
      this.stages = [
        {
          name: "Общие сведения",
          fields: [
            {
              name: "Фамилия Имя Отчество",
              content: data.fullname,
            },
            {
              name: "Гражданство",
              content: data.citizenship,
            },
            {
              name: "Национальность",
              content: data.nationality,
            },
            {
              name: "Семейное положение",
              content: data.marital_status,
            },
            {
              name: "Адрес постоянной регистрации",
              content: data.permanent_address,
            },
          ],
        },
        {
          name: "Информация о рождении",
          fields: [
            {
              name: "Дата",
              content: data.birth_info.date,
            },
            {
              name: "Страна",
              content: data.birth_info.country,
            },
            {
              name: "Город",
              content: data.birth_info.place,
            },
          ],
        },
        {
          name: "Паспортные данные",
          fields: [
            {
              name: "Серия",
              content: data.passport.series,
            },
            {
              name: "Номер",
              content: data.passport.code,
            },
            {
              name: "Паспорт выдан",
              content: data.passport.ufms_name,
            },
            {
              name: "Дата выдачи",
              content: data.passport.issue_date,
            },
            {
              name: "Код подразделения",
              content: data.passport.ufms_code,
            },
          ],
        },
        // TODO(kateR): Убрать костыль и сделать так, чтобы для старых абитуриентов (у которых не было ИНН и
        // СНИЛС в форме)подставлялись пустые строки с бэка
        {
          name: "ИНН и СНИЛС",
          fields: [
            {
              name: "ИНН",
              content: data.personal_documents_info ? data.personal_documents_info.tax_id : "",
            },
            {
              name: "СНИЛС",
              content: data.personal_documents_info ? data.personal_documents_info.insurance_number : "",
            },
          ],
        },
        {
          name: "Информация о ВУЗе",
          fields: [
            {
              name: "Кампус",
              content: CAMPUSES[data.university_info.program.faculty.campus],
            },
            {
              name: "Номер студенческого билета",
              content: data.university_info.card_id,
            },
            {
              name: "Образовательная программа",
              content: this.getFormattedProgram(data.university_info.program),
            },
            {
              name: "Номер группы",
              content: data.university_info.group,
            },
            {
              name: "Год окончания ВУЗа",
              content: data.university_info.graduation_year,
            },
          ],
        },
        {
          name: "Военный комиссариат",
          fields: [
            {
              name: "Состою на воинском учете в военном комиссариате...",
              content: data.recruitment_office,
            },
            {
              name: "Желаемая военная специальность",
              content: data.milspecialty.title,
            },
          ],
        },
        {
          name: "Контактная информация",
          fields: [
            {
              name: "Корпоративная почта",
              content: data.contact_info.corporate_email,
            },
            {
              name: "Личная почта",
              content: data.contact_info.personal_email,
            },
            {
              name: "Номер телефона",
              content: data.contact_info.personal_phone_number,
            },
          ],
        },
        {
          name: "Фотография",
          fields: [
            {
              name: "Фото",
              content: {
                photo: [
                  {
                    name: "photo.png",
                    percentage: 0,
                    raw: dataURLtoFile(`data:image/png;base64,${data.photo}`, "photo.png"),
                    status: "ready",
                    base: data.photo,
                  },
                ],
              },
            },
          ],
        },
      ];
      if (data.family) {
        console.log(dataURLtoFile(`data:image/png;base64,${data.photo}`, "photo.png"));
        let counter = 0;
        while (counter < data.family.length) {
          const type = [];
          switch (data.family[counter].type) {
            case "FA":
              type.push(" об отце", " отца");
              break;
            case "MO":
              type.push(" о матери", " матери");
              break;
            case "BR":
              type.push(" о брате", " брата");
              break;
            case "SI":
              type.push(" о сестре", " сестры");
              break;
            default:
              break;
          }
          this.stages.push({
            name: `Данные${type[0]}`,
            fields: [
              {
                name: `Фамилия${type[1]}`,
                content: data.family[counter].surname,
              },
              {
                name: `Имя${type[1]}`,
                content: data.family[counter].name,
              },
              {
                name: `Отчество${type[1]}`,
                content: data.family[counter].patronymic,
              },
              {
                name: `Гражданство${type[1]}`,
                content: data.family[counter].citizenship,
              },
              {
                name: `Адрес постоянной регистрации${type[1]}`,
                content: data.family[counter].permanent_address,
              },
              {
                name: `Дата рождения${type[1]}`,
                content: data.family[counter].birth_info?.date,
              },
              {
                name: `Страна рождения${type[1]}`,
                content: data.family[counter].birth_info?.country,
              },
              {
                name: `Город рождения${type[1]}`,
                content: data.family[counter].birth_info?.place,
              },
              {
                name: `Личная почта${type[1]}`,
                content: data.family[counter].contact_info?.personal_email,
              },
              {
                name: `Номер телефона${type[1]}`,
                content: data.family[counter].contact_info?.personal_phone_number,
              },
            ],
          });
          // eslint-disable-next-line no-plusplus
          counter++;
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.tableForm {
  border: 1px solid lightGray;
  border-bottom: 0;
  background-color: $subMenuActiveText;
}

.contentcol {
  border-left: 1px solid lightgray;
  background-color: white;
}

.buttons {
  display: flex;
}

</style>
