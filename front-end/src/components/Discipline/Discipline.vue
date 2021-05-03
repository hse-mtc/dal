<template>
  <div>
    <el-col :offset="2" :span="20" class="Discipline">
      <el-row class="pageTitle">
        <h1>{{ $route.meta.title }}</h1>
      </el-row>
      <el-tabs stretch>
        <el-tab-pane label="Поощрения">
          <Encouragement />
        </el-tab-pane>
        <el-tab-pane label="Взыскания">
          <Punishment />
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </div>
</template>

<script>
import Punishment from "./Punishment/Punishment.vue";
import Encouragement from "./Encouragement/Encouragement.vue";

export default {
  name: "Discipline",
  components: {
    Punishment,
    Encouragement,
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
