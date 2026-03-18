<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <MediaLibraryComponent />
    </el-col>
  </el-row>
</template>

<script>
import MediaLibraryComponent from "@/components/MediaLibrary/Library.vue";

export default {
  name: "MediaLibraryView",
  components: {
    MediaLibraryComponent,
  },
};
</script>
