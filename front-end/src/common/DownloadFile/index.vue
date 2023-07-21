<template>
  <div :class="$style.root" :disabled="isDataLoading" @click="downloadFile">
    <slot />
  </div>
</template>

<script>

import { downloadError } from "@/utils/message";

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

      try {
        const link = document.createElement("a");
        link.href = this.url;
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
