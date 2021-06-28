<template>
  <ExpandBox title="Дополнительная информация" @toggled="toggled">
    <div class="extra-info">
      <el-form
        ref="form"
        class="form"
        :model="modifyInfo"
        label-position="right"
        label-width="150px"
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
        <el-form-item label="ОП:">
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
              {{ displayInfo.university_info.program.program }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Военная специальность:">
          <transition name="el-fade-in" mode="out-in">
            <el-select
              v-if="modify"
              v-model="modifyInfo.milspecialty"
              value-key="status"
              style="display: block"
            >
              <el-option
                v-for="item in milspecialties"
                :key="item"
                :label="item"
                :value="item"
              />
            </el-select>
            <span v-else class="field-value">
              {{ displayInfo.milspecialty }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Паспорт:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.passport"
              v-maska="'#### ######'"
            />
            <span v-else class="field-value">
              {{ displayInfo.birth_info ? displayInfo.passport : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Гражданство:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.citizenship" />
            <span v-else class="field-value">
              {{ displayInfo.birth_info ? displayInfo.citizenship : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Адрес:">
          <transition name="el-fade-in" mode="out-in">
            <el-input v-if="modify" v-model="modifyInfo.permanent_address" />
            <span v-else class="field-value">
              {{ displayInfo.birth_info ? displayInfo.permanent_address : "---" }}
            </span>
          </transition>
        </el-form-item>
        <el-form-item label="Почта:">
          <transition name="el-fade-in" mode="out-in">
            <el-input
              v-if="modify"
              v-model="modifyInfo.contact_info.email"
              v-maska="'X*@S*.X*'"
            />
            <span v-else class="field-value">
              {{ displayInfo.contact_info.email }}
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
import { findStudentExtra, patchStudentExtra } from "@/api/students";
import { getError, patchError } from "@/utils/message";

export default {
  name: "StudentExtra",
  components: { ExpandBox },
  data() {
    return {
      modify: false,
      displayInfo: {},
      modifyInfo: {},
      loading: false,
      id: this.$route.params.studentId,
    };
  },
  computed: {
    ...mapState("reference", ["programs", "milspecialties"]),
  },
  async created() {
    await this.fetchInfo();
    await this.fetchMilgroups();
    await this.fetchStudentPosts();
    await this.fetchStudentStatuses();
  },
  methods: {
    ...mapActions("reference", [
      "fetchPrograms",
      "fetchMilspecialties",
    ]),
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
    },
    async save() {
      try {
        this.loading = true;
        await patchStudentExtra(this.modifyInfo);
        this.displayInfo = this.modifyInfo;
        this.modify = false;
      } catch {
        patchError("дополнительной информации о студенте");
      } finally {
        this.loading = false;
      }
    },
    toggled(expanded) {
      if (expanded) {
        this.fetchInfo();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
