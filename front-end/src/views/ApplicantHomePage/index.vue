<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <PageHeader title="Мои материалы" />
    </el-col>
  </el-row>
</template>

<script>
import PageHeader from "@/common/PageHeader";

export default {
  name: "MyMaterials",
  components: {
    PageHeader,
  },
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";
</style>
