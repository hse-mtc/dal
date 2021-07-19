<template>
  <div>
    <el-col :offset="1" :span="22" class="Personnel">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-tabs stretch>
        <el-tab-pane
          v-if="hasPermission(getPermissions('students'))"
          label="Студенты"
        >
          <Students />
        </el-tab-pane>
        <el-tab-pane
          v-if="hasPermission(getPermissions('teachers'))"
          label="Преподаватели"
        >
          <Teachers />
        </el-tab-pane>
        <el-tab-pane
          v-if="hasPermission(getPermissions('uniforms'))"
          label="Текущая форма одежды"
        >
          <UniformPicker />
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </div>
</template>

<script>
import UniformPicker from "@/components/Personnel/UniformPicker/UniformPicker";
import { hasPermission } from "@/utils/permissions";
import Students from "./Students/Students.vue";
import Teachers from "./Teachers/Teachers.vue";

export default {
  name: "Personnel",
  components: {
    UniformPicker,
    Students,
    Teachers,
  },
  methods: {
    hasPermission,
    getPermissions(entity) {
      return [
        `${entity}.get.all`,
        `${entity}.get.milfaculty`,
        `${entity}.get.milgroup`,
      ];
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
