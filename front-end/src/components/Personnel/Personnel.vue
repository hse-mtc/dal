<template>
  <div>
    <el-col :offset="2" :span="20" class="Personnel">
      <el-row class="pageTitle">
        <h1>{{ this.$route.meta.title }}</h1>
      </el-row>
      <el-tabs value="students" stretch>
        <el-tab-pane name="students" label="Студенты">
          <Students />
        </el-tab-pane>
        <el-tab-pane name="teachers" label="Преподаватели">
          <Teachers />
        </el-tab-pane>
        <el-tab-pane name="uniform" label="Текущая форма одежды">
          <UniformPicker />
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </div>
</template>

<script>
import UniformPicker from "@/components/Personnel/UniformPicker/UniformPicker";
import Students from "./Students/Students.vue";
import Teachers from "./Teachers/Teachers.vue";

export default {
  name: "Personnel",
  components: {
    UniformPicker,
    Students,
    Teachers,
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
