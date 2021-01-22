<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <LibraryComponent/>
    </el-col>
  </el-row>
</template>

<script>

import LibraryComponent from "@/components/Library/Library";

export default {
  name: "Library",
  components: {
    LibraryComponent
  },
  computed: {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style></style>
