<template>
  <div :class="$style.root" :disabled="isDataLoading" @click="downloadFile">
    <slot />
  </div>
</template>

<script>

import { downloadError } from "@/utils/message";
import request from "@/utils/request";

export default {
  name: "DownloadFile",
  props: {
    url: {
      type: String,
      required: true,
    },
    fileName: {
      type: String,
      default: "",
    },
    requireAuth: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return { isDataLoading: false };
  },
  methods: {
    async downloadFile() {
      if (!this.url || this.isDataLoading) {
        return;
      }

      this.isDataLoading = true;
      let fileUrl = this.url;
      if (this.requireAuth) {
        const res = await request({
          url: this.url,
          method: "GET",
        });
        fileUrl = res.data.content;
      }
      try {
        const link = document.createElement("a");
        link.href = fileUrl;
        link.download = this.fileName;
        link.click();
      } catch (e) {
        downloadError("файла", e.response?.status);
      }

      this.isDataLoading = false;
    },
  },
};
</script>

<style lang="scss" module>
.root {
  cursor: pointer;

  &[disabled] {
    opacity: 0.5;
  }
}
</style>
