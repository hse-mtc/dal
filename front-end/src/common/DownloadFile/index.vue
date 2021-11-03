<template>
  <div :class="$style.root" :disabled="isDataLoading" @click="downloadFile">
    <slot />
  </div>
</template>

<script>
import request from "@/utils/request";

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
        const { data } = await request({
          url: this.url,
          method: "GET",
          responseType: "blob",
        });

        const link = document.createElement("a");
        link.href = URL.createObjectURL(new Blob([data]));
        link.download = this.fileName;
        link.click();
        URL.revokeObjectURL(link.href);
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
