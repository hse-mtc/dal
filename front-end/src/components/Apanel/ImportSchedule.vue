<template>
  <div>
    <input
      ref="attachmentUpload"
      type="file"
      hidden
      accept="application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      @change="onAttachmentPicked"
    >
    <table>
      <tr>
        <td>
          <el-button
            type="primary"
            @click="onScheduleUpload()"
          >
            Распознать расписание
          </el-button>
          <el-button
            type="primary"
            @click="onSaveParsed()"
          >
            Добавить в базу
          </el-button>
        </td>
      </tr>
      <tr>
        <td class="border-box">
          <pre> {{ parsedSchedule
            ? (pretty(parsedSchedule, 4))
            : "Загрузите файл расписания, нажав на кнопку..."  }} </pre>
        </td>
      </tr>
    </table>
  </div>

</template>

<script>
import { patchError } from "@/utils/message";
import { parseSchedulePost, saveParsedPost } from "@/api/import-schedule";
import { Message } from "element-ui";

export default {
  name: "ImportScheduleComponent",
  filters: {
  },
  data() {
    return {
      parsedSchedule: null,
    };
  },
  methods: {
    pretty(val, indent = 2) {
      let prettyVal = val;
      if (typeof val !== "object") {
        try {
          prettyVal = JSON.parse(val);
        } catch (err) {
          console.warn("value is not JSON");
          return val;
        }
      }
      return JSON.stringify(prettyVal, null, indent);
    },
    onScheduleUpload() {
      this.$data.parsedSchedule = null;
      this.$refs.attachmentUpload.value = null;
      this.$refs.attachmentUpload.click();
    },
    messageImportedLessons(number) {
      Message({
        message: `Успешно добавлено ${number} занятий.`,
        type: "success",
      });
    },
    onAttachmentPicked() {
      const formData = new FormData();
      if (this.$refs.attachmentUpload.files[0]) {
        formData.set("content", this.$refs.attachmentUpload.files[0]);
      }
      try {
        parseSchedulePost(formData)
          .then(blob => {
            this.$data.parsedSchedule = JSON.stringify(blob.data);
          });
      } catch (err) {
        patchError("приложения", err.response?.status);
      }
    },
    onSaveParsed() {
      const requestData = JSON.parse(this.$data.parsedSchedule);
      if (requestData) {
        saveParsedPost(requestData).then(response => {
          this.messageImportedLessons(response.data.created);
        });
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.tab-button {
  width: 196px;
  height: 33px;
  font-family: 'Proxima Nova';
  border-radius: 8px;
  font-style: normal;
  font-weight: normal;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 9px 12px;
  margin-bottom: 8px;
}

.active {
  background: #F6F7FB;
  font-weight: 600;
  font-size: 14px;
  color: #0C4B9A;
}
.not-active {
  border: 1px solid #F2F2F2;
  box-sizing: border-box;
  font-size: 14px;
  color: #858587;
}

.content {
  padding-top: $xl;
}

.el-select {
  width: 100%;
}

.el-transfer {
  display: flex;
  align-items: center;
  justify-content: center;
}

.border-box {
  /* Border styling for the container */
  border: 2px solid #ccc;
  padding: 10px;
  margin-top: 10px;
}

.text {
  /* Styles for the <pre> tag */
  white-space: pre-wrap;
}

/* Additional table styling (optional) */
table {
  width: 100%;
  border-collapse: collapse;
}

td {
  padding: 10px;
}

</style>
