<template>
  <ExpandBox title="Дополнительная информация" @toggled="toggled">
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
              <el-button
                type="info"
                plain
                icon="el-icon-edit"
                @click="startModify"
              >
                Редактировать
              </el-button>
            </template>
          </transition>
        </el-form-item>
        <el-form-item label="Образовательная программа:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.university_info.program.code"
              value-key="code"
              style="display: block"
            >
              <el-option
                v-for="item in programs"
                :key="item.code"
                :label="item.program"
                :value="item.code"
              />
            </el-select>
            <span v-else class="field-value">
              {{
                displayInfo.university_info.program
                  ? displayInfo.university_info.program.program
                  : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Кампус:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.university_info.campus"
              value-key="code"
              style="display: block"
            >
              <el-option
                v-for="item in campuses"
                :key="item.code"
                :label="item.title"
                :value="item.code"
              />
            </el-select>
            <span v-else class="field-value">
              {{
                campuses.some(
                  (x) => x.code === displayInfo.university_info.campus,
                )
                  ? campuses.find(
                    (x) => x.code === displayInfo.university_info.campus,
                  ).title
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
        <el-form-item label="Военная специальность:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.milspecialty"
              value-key="code"
              style="display: block"
            >
              <el-option
                v-for="item in milspecialties"
                :key="item.code"
                :label="item.milspecialty"
                :value="item.code"
              />
            </el-select>
            <span v-else class="field-value">
              {{ displayInfo.milspecialty }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Серия и номер паспорта:">
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
        <el-form-item label="Место выдачи паспорта:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.passport.ufms_name" />
            <span v-else class="field-value">
              {{
                displayInfo.passport ? displayInfo.passport.ufms_name : "---"
              }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Дата выдачи паспорта:">
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
        <el-form-item label="Код подразделения:">
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
import { mapActions, mapState } from "vuex";
import { findStudentExtra, patchStudent } from "@/api/students";
import { getError, patchError } from "@/utils/message";
import moment from "moment";

export default {
  name: "StudentExtra",
  components: { ExpandBox },
  data() {
    return {
      modify: false,
      displayInfo: {
        contact_info: {},
        university_info: {
          program: {},
        },
        passport: {},
      },
      modifyInfo: {},
      loading: false,
      id: this.$route.params.studentId,
      campuses: [
        {
          code: "MO",
          title: "Москва",
        },
        {
          code: "SP",
          title: "Санкт-Петербург",
        },
        {
          code: "NN",
          title: "Нижний Новгород",
        },
        {
          code: "PE",
          title: "Пермь",
        },
      ],
    };
  },
  computed: {
    ...mapState("reference", ["programs", "milspecialties"]),
  },
  methods: {
    ...mapActions("reference", ["fetchPrograms", "fetchMilspecialties"]),
    formatDate: date => moment(date).format("DD.MM.YYYY"),
    async fetch() {
      await this.fetchInfo();
      await this.fetchPrograms();
      await this.fetchMilspecialties();
    },
    async fetchInfo() {
      try {
        this.loading = true;
        this.displayInfo = (await findStudentExtra(this.id)).data;
      } catch (err) {
        getError("дополнительной информации о студенте", err);
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
        requestBody.university_info.program = this.modifyInfo.university_info.program.code;
        console.log("🚀 > requestBody", requestBody);
        await patchStudent(requestBody);
        this.displayInfo = this.modifyInfo;
        this.modify = false;
      } catch {
        patchError("дополнительной информации о студенте");
      } finally {
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
