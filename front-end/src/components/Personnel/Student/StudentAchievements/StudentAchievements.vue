<template>
  <ExpandBox title="Умения и достижения" @toggled="toggled">
    <div class="achievements-info">
      <div class="achievements-table">
        <div class="title">
          Умения
        </div>
        <el-tag
          v-for="skill in skills"
          :key="skill"
          closable
          :disable-transitions="false"
          effect="plain"
          @close="handleClose(skill)"
        >
          {{ skillsOptions.find((x) => x.id === skill).title }}
        </el-tag>
        <el-select
          v-if="selectVisible"
          ref="newSkillSelect"
          v-model="newSkillValue"
          class="input-new-skill"
          size="small"
          automatic-dropdown
          @change="handleSelectConfirm"
        >
          <el-option
            v-for="option in skillsOptionsFiltered"
            :key="option.id"
            :label="option.title"
            :value="option.id"
          />
        </el-select>
        <el-button
          v-else-if="skillsOptionsFiltered.length"
          class="button-new-skill"
          size="mini"
          icon="el-icon-plus"
          @click="showSelect"
        />
        <div class="separator" />
      </div>
      <div class="achievements-table">
        <div class="title">
          Достижения
          <el-button
            size="mini"
            type="text"
            icon="el-icon-plus"
            style="float: right;"
            @click="showDialog"
          >
            Добавить
          </el-button>
        </div>
        <PrimeTable
          :value="achievements"
          scroll-height="200px"
          scrollable
          class="p-datatable-striped p-datatable-gridlines p-datatable-sm"
        >
          <PrimeColumn
            :field="dateField"
            header="Дата"
            column-key="date"
            header-style="width: 100px"
            body-style="width: 100px"
          />
          <PrimeColumn header="Тип" column-key="achievement_type">
            <template #body="{ data }">
              <el-tag :type="tagVariantByType(data.achievement_type)">
                {{ data.achievement_type }}
              </el-tag>
            </template>
          </PrimeColumn>
          <PrimeColumn
            column-key="text"
            header="Описание"
            :field="(row) => row.text"
          />
          <PrimeColumn
            column-key="buttons"
            header-style="width: 50px;"
            body-style="width: 50px;"
          >
            <template #body="{ data }">
              <el-button
                size="mini"
                icon="el-icon-delete"
                type="danger"
                circle
                @click="handleDelete(data.id)"
              />
            </template>
          </PrimeColumn>
          <template #empty>
            Нет данных.
          </template>
        </PrimeTable>
        <div class="separator" />
      </div>
    </div>
    <el-dialog
      title="Новое достижение"
      :visible.sync="dialogVisible"
      width="30%"
    >
      <el-form
        label-position="right"
        label-width="100px"
        size="mini"
        :model="editAchievement"
      >
        <el-form-item label="Дата:">
          <el-date-picker
            v-model="editAchievement.date"
            type="date"
            style="width: 100%;"
            :picker-options="{
              disabledDate(time) {
                return time.getTime() > Date.now();
              },
            }"
            format="dd.MM.yyyy"
            value-format="yyyy-MM-dd"
            placeholder="Выберите дату"
          />
        </el-form-item>
        <el-form-item label="Тип: ">
          <el-select
            v-model="editAchievement.achievement_type"
            placeholder="Выберите тип"
            style="display: block"
          >
            <el-option
              v-for="item in achievementTypes"
              :key="item.achievement_type"
              :label="item.achievement_type"
              :value="item.achievement_type"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Описание: ">
          <el-input
            v-model="editAchievement.text"
            placeholder="Введите описание"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="primary" :loading="loading" @click="handleAccept()">
          Применить
        </el-button>
      </span>
    </el-dialog>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import moment from "moment";
import {
  getAchievement,
  postAchievement,
  deleteAchievement,
} from "@/api/achievement";
import { getError, postError, deleteError } from "@/utils/message";
import { patchStudent, findStudentSkills } from "@/api/students";
import { ReferenceModule } from "@/store";

export default {
  name: "StudentAchievements",
  components: { ExpandBox },
  data() {
    return {
      achievements: [],
      skills: [],
      loading: false,
      selectVisible: false,
      newSkillValue: "",
      dialogVisible: false,
      editAchievement: {},
    };
  },
  computed: {
    id() {
      return this.$route.params.studentId;
    },
    skillsOptions() { return ReferenceModule.skills; },
    achievementTypes() { return ReferenceModule.achievementTypes; },
    skillsOptionsFiltered() {
      return this.skillsOptions.filter(
        x => !this.skills.some(y => x.id === y),
      );
    },
  },
  methods: {
    dateField: row => (moment(row.date).isValid()
      ? moment(row.date).format("DD.MM.YYYY")
      : "---"),
    tagVariantByType(type) {
      switch (type) {
        case "Спортивные":
          return "danger";
        case "Научные":
          return "primary";
        default:
          return "";
      }
    },
    async fetchInfo() {
      try {
        this.loading = true;
        await ReferenceModule.fetchSkills();
        await ReferenceModule.fetchAchievementTypes();
        this.achievements = (await getAchievement({ student: this.id })).data;
        this.skills = (
          await findStudentSkills(this.id)
        ).data.student_skills.map(x => x.id);
      } catch (err) {
        getError("информации о достижениях студента", err.response.status);
      } finally {
        this.loading = false;
      }
    },
    async toggled(expanded) {
      if (expanded) {
        await this.fetchInfo();
      }
    },

    async handleClose(removedSkill) {
      const skills = this.skills.filter(x => x !== removedSkill);
      await this.updateSkills(skills);
    },
    showSelect() {
      this.selectVisible = true;
      this.$nextTick(() => {
        this.$refs.newSkillSelect.focus();
      });
    },
    async handleSelectConfirm() {
      const { newSkillValue } = this;
      if (newSkillValue) {
        const skills = [...this.skills, newSkillValue];
        await this.updateSkills(skills);
      }
      this.selectVisible = false;
      this.newSkillValue = "";
    },
    async updateSkills(skills) {
      await patchStudent({ id: this.id, student_skills: skills });
      this.skills = skills;
    },

    showDialog() {
      this.dialogVisible = true;
      this.editAchievement = { student: this.id };
    },
    async handleAccept() {
      try {
        this.loading = true;
        await postAchievement(this.editAchievement);
        this.dialogVisible = false;
        await this.fetchInfo();
      } catch (err) {
        postError("достижения студента", err.response.status);
      } finally {
        this.loading = false;
      }
    },
    async handleDelete(id) {
      try {
        this.loading = true;
        await deleteAchievement(id);
        await this.fetchInfo();
      } catch (err) {
        deleteError("достижения студента", err.response.status);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
