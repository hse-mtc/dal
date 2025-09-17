<template>
  <ExpandBox v-if="show" title="Дополнительная информация" @toggled="toggled">
    <div class="extra-info">
      <el-form
        ref="form"
        class="form"
        :model="modifyInfo"
        label-position="right"
        label-width="250px"
        size="mini"
        :disabled="loading"
      >
        <el-form-item class="actions">
          <transition name="el-fade-in" mode="out-in">
            <div v-if="modify">
              <el-button type="primary" plain @click="save">
                Сохранить
              </el-button>
              <el-button type="warning" plain @click="modify = false">
                Отмена
              </el-button>
            </div>
            <template v-else>
              <AZGuard
                :permissions="[
                  'students.patch.all',
                  {
                    codename: 'students.patch.milfaculty',
                    validator: () => milgroup.milfaculty === userMilfaculty,
                  },
                  {
                    codename: 'students.patch.milgroup',
                    validator: () =>
                      userMilgroups.some((x) => x === milgroup.milgroup),
                  },
                  {
                    codename: 'students.patch.self',
                    validator: () => +id === userId,
                  },
                ]"
              >
                <el-button
                  type="info"
                  plain
                  icon="el-icon-edit"
                  @click="startModify"
                >
                  Редактировать
                </el-button>
              </AZGuard>
            </template>
          </transition>
        </el-form-item>
        <el-form-item label="Образовательная программа:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.university_info.program.id"
              value-key="id"
              style="display: block"
            >
              <el-option
                v-for="item in programs"
                :key="item.id"
                :label="item.title"
                :value="item.id"
              />
            </el-select>
            <span v-else class="field-value">
              {{
                displayInfo.university_info.program
                  ? displayInfo.university_info.program.title
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Учебная группа:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.university_info.group"
            />
            <span v-else class="field-value">
              {{
                displayInfo.university_info
                  ? displayInfo.university_info.group
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Номер студенческого билета:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.university_info.card_id"
            />
            <span v-else class="field-value">
              {{
                displayInfo.university_info
                  ? displayInfo.university_info.card_id
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Год окончания ВУЗа:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.university_info.graduation_year"
            />
            <span v-else class="field-value">
              {{
                displayInfo.university_info
                  ? displayInfo.university_info.graduation_year
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Паспорт, серия и номер:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.passport.seriesAndCode"
              v-maska="'#### ######'"
            />
            <span v-else class="field-value">
              {{
                displayInfo.passport
                  ? `${displayInfo.passport.series} ${displayInfo.passport.code}`
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Паспорт, место выдачи:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.passport.ufms_name" />
            <span v-else class="field-value">
              {{
                displayInfo.passport ? displayInfo.passport.ufms_name : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Паспорт, дата выдачи:">
          <transition name="el-fade-in" mode="out-in">
            <el-date-picker
              v-if="modify"
              v-model="modifyInfo.passport.issue_date"
              type="date"
              style="width: 100%;"
              :picker-options="{
                disabledDate(time) {
                  return time.getTime() > Date.now();
                },
                firstDayOfWeek: 1,
              }"
              format="dd.MM.yyyy"
              value-format="yyyy-MM-dd"
            />
            <span v-else class="field-value">
              {{
                displayInfo.passport
                  ? formatDate(displayInfo.passport.issue_date)
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Паспорт, код подразделения:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.passport.ufms_code"
              v-maska="'###-###'"
            />
            <span v-else class="field-value">
              {{
                displayInfo.passport ? displayInfo.passport.ufms_code : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Гражданство:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.citizenship" />
            <span v-else class="field-value">
              {{ displayInfo.citizenship ? displayInfo.citizenship : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Национальность:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.nationality" />
            <span v-else class="field-value">
              {{ displayInfo.nationality ? displayInfo.nationality : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Семейное положение:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.marital_status" />
            <span v-else class="field-value">
              {{ displayInfo.marital_status ? displayInfo.marital_status : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Адрес:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.permanent_address" />
            <span v-else class="field-value">
              {{
                displayInfo.permanent_address
                  ? displayInfo.permanent_address
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="E-mail:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.contact_info.email"
              v-maska="'X*@S*.X*'"
            />
            <span v-else class="field-value">
              {{
                displayInfo.contact_info
                  ? displayInfo.contact_info.email
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
      </el-form>
    </div>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import { findStudentExtra, patchStudent, findStudentBasic } from "@/api/students";
import { getError, patchError } from "@/utils/message";
import moment from "moment";
import { ReferenceModule, UserModule } from "@/store";
import { CAMPUSES } from "@/utils/enums";

export default {
  name: "StudentExtra",
  components: { ExpandBox },
  props: {
    milgroup: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      CAMPUSES,
      modify: false,
      displayInfo: {
        contact_info: {},
        university_info: {
          program: {},
        },
        passport: {},
      },
      modifyInfo: {},
      show: true,
      loading: false,
    };
  },
  computed: {
    programs() {
      return ReferenceModule.programs;
    },
    milspecialties() {
      return ReferenceModule.milspecialties;
    },
    id() {
      return this.$route.params.studentId;
    },
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    userMilgroups() {
      return UserModule.personMilgroups;
    },
    userId() {
      return UserModule.personId;
    },
  },
  async mounted() {
    await this.fetch();
    if (this.displayInfo.passport === null && this.displayInfo.citizenship === "") {
      this.show = false;
    } else {
      this.show = true;
    }
  },
  methods: {
    formatDate: date => moment(date).format("DD.MM.YYYY"),
    async fetch() {
      await this.fetchInfo();
    },
    async fetchInfo() {
      try {
        this.loading = true;
        this.displayInfo = (await findStudentExtra(this.id)).data;
      } catch (err) {
        getError("дополнительной информации о студенте", err.response.status);
      } finally {
        this.loading = false;
      }
    },
    startModify() {
      this.modify = true;
      this.modifyInfo = { ...this.displayInfo };
      if (!this.modifyInfo.university_info) {
        this.$set(this.modifyInfo, "university_info", { program: {} });
      }
      if (!this.modifyInfo.passport) {
        this.$set(this.modifyInfo, "passport", {});
      }
      this.modifyInfo.passport.seriesAndCode = this.displayInfo.passport
        ? `${this.displayInfo.passport.series} ${this.displayInfo.passport.code}`
        : "";
    },
    async save() {
      try {
        this.loading = true;
        const [series, code] = this.modifyInfo.passport.seriesAndCode.split(
          " ",
        );
        this.modifyInfo.passport.series = series;
        this.modifyInfo.passport.code = code;
        const requestBody = { ...this.modifyInfo };
        // eslint-disable-next-line max-len
        const programFiltered = this.programs.filter(program => program.id === this.modifyInfo.university_info.program.id);
        requestBody.university_info.program = { ...programFiltered[0] };
        requestBody.university_info.program = requestBody.university_info.program.id;
        await patchStudent(requestBody);
        this.displayInfo = this.modifyInfo;
        this.displayInfo.university_info = requestBody.university_info;
        this.modify = false;
      } catch (err) {
        patchError("дополнительной информации о студенте", err.response.status);
      } finally {
        await this.fetchInfo();
        this.loading = false;
      }
    },
    async toggled(expanded) {
      if (expanded) {
        await this.fetch();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
