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
        <el-table :data="achievements" max-height="200" size="mini">
          <el-table-column prop="date" label="Дата" :formatter="formatDate" />
          <el-table-column label="Тип">
            <template slot-scope="{ row }">
              <el-tag :type="tagVariantByType(row.achievement_type)">
                {{ row.achievement_type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="text" label="Описание" show-overflow-tooltip />
          <el-table-column width="40px">
            <template slot-scope="scope">
              <el-button
                size="mini"
                icon="el-icon-delete"
                type="danger"
                circle
                @click="handleDelete(scope.row.id)"
              />
            </template>
          </el-table-column>
        </el-table>
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
import { mapActions, mapState } from "vuex";

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
    ...mapState({
      skillsOptions: state => state.reference.skills,
      achievementTypes: state => state.reference.achievementTypes,
    }),
    skillsOptionsFiltered() {
      return this.skillsOptions.filter(
        x => !this.skills.some(y => x.id === y),
      );
    },
  },
  methods: {
    ...mapActions("reference", ["fetchSkills", "fetchAchievementTypes"]),
    formatDate: row => (moment(row.date).isValid()
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
        await this.fetchSkills();
        await this.fetchAchievementTypes();
        this.achievements = (await getAchievement({ student: this.id })).data;
        this.skills = (
          await findStudentSkills(this.id)
        ).data.student_skills.map(x => x.id);
      } catch (err) {
        getError("информации о достижениях студента", err);
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
      } catch {
        postError("достижения студента");
      } finally {
        this.loading = false;
      }
    },
    async handleDelete(id) {
      try {
        this.loading = true;
        await deleteAchievement(id);
        await this.fetchInfo();
      } catch {
        deleteError("достижения студента");
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
