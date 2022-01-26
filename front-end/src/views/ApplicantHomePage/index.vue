<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <PageHeader title="Личный кабинет абитуриента" />
      <div style="margin-bottom: 15px">
        Чтобы подать заявку на поступление в Военный учебный центр НИУ ВШЭ, пройдите форму по кнопке ниже
      </div>
      <router-link to="/applicant-form/">
        <el-button type="primary">Пройти форму</el-button>
      </router-link>
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
