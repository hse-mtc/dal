<template>
  <div>
    <el-col :offset="1" :span="22" class="Discipline">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-tabs stretch>
        <el-tab-pane
          v-if="hasPermission(getPermissions('encouragements'))"
          label="Поощрения"
        >
          <Encouragement />
        </el-tab-pane>
        <el-tab-pane
          v-if="hasPermission(getPermissions('punishments'))"
          label="Взыскания"
        >
          <Punishment />
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </div>
</template>

<script>
import { hasPermission } from "@/utils/permissions";
import Punishment from "./Punishment/Punishment.vue";
import Encouragement from "./Encouragement/Encouragement.vue";

export default {
  name: "Discipline",
  components: {
    Punishment,
    Encouragement,
  },
  methods: {
    hasPermission,
    getPermissions(entity) {
      return [
        `${entity}.get.all`,
        `${entity}.get.milfaculty`,
        `${entity}.get.milgroup`,
        `${entity}.get.self`,
      ];
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
