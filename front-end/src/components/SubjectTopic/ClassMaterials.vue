<template>
  <div class="class-materials file-group">
    <div class="class-materials-title file-section-title" @click="toggleFiles">
      <div>{{ titles[title] }}</div>
      <img
        src="../../assets/scienceWorks/dropdown.svg"
        alt=""
        class="files-dropdown"
      />
    </div>

    <div style="display: none">
      <div class="files" v-if="hasMaterials">
        <div
          class="file"
          v-for="(material, index) in displayMaterials"
          :key="index"
        >
          <div class="file-icon">
            <img
              :src="
                require(`../../assets/extensions-icon/${
                  Object.keys(icons).includes(material.file.extension)
                    ? icons[material.file.extension]
                    : 'new-file'
                }.svg`)
              "
              alt=""
              class="kebab"
              width="48px"
              height="48px"
            />
          </div>
          <div class="file-title">{{ material.title }}</div>

          <div class="file-kebab">
            <el-popover placement="bottom" trigger="click">
              <div
                style="
                  text-align: center;
                  margin: 0;
                  padding: 0;
                  font-size: 15px;
                "
              >
                <div
                  v-if="isOwner"
                  style="cursor: pointer"
                  @click="deleteMaterial(material.id)"
                >
                  Удалить
                </div>
                <DownloadFile
                  :url="material.file.content"
                  :fileName="material.file.name"
                >
                  Скачать
                </DownloadFile>
              </div>

              <div
                slot="reference"
                class="d-flex justify-content-center"
                style="width: 10px; cursor: pointer"
              >
                <img
                  src="../../assets/subject/greyKebab.svg"
                  alt=""
                  class="kebab"
                />
              </div>
            </el-popover>
          </div>
        </div>
      </div>
      <div v-else class="pt-2 pl-2">
        <CustomText v-if="!isOwner" variant="paragraph"
          >Здесь пока нет материалов
        </CustomText>
      </div>
      <CustomText
        v-if="isOwner"
        class="mt-3 mb-1"
        variant="paragraph"
        color="#0C4B9A"
        :custom-style="{
          cursor: 'pointer',
          display: 'flex',
          justifyContent: 'center',
        }"
      >
        <div @click="dialogVisible = true">+ Добавить материал</div>
      </CustomText>
    </div>
    <el-dialog
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose"
    >
      <el-upload
        ref="upload"
        class="upload-video-upload"
        action="‍"
        :on-remove="handleRemoveFile"
        :before-remove="beforeRemove"
        :on-change="addFile"
        :limit="3"
        :on-exceed="handleExceed"
        :file-list="fileList"
        :auto-upload="false"
        :multiple="true"
      >
        <el-button
          class="upload-button"
          size="small"
          type="primary"
          style="outline: none"
          >Добавить файл
        </el-button>
        <div slot="tip" class="el-upload__tip" />
      </el-upload>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelFile">Отмена</el-button>
        <el-button type="primary" @click="saveFile">Сохранить</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";
import DownloadFile from '@/common/DownloadFile/index.vue'
import { deleteMaterial } from "@/api/material";
import { addTopicFile } from "@/api/subject";

export default {
  components: { CustomText, DownloadFile },
  props: {
    topic: {
      type: Number,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    materials: {
      type: Array,
      required: true,
    },
    isOwner: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      fileList: [],
      displayMaterials: [],
      dialogVisible: false,
      titles: {
        LE: "Лекции",
        SE: "Семианры",
        GR: "Групповые занятия",
        PR: "Практические занятия",
      },
      icons: {
        doc: "doc",
        docx: "doc",
        xsl: "xsl",
        xslx: "xsl.",
        jpg: "jpg",
        jpeg: "jpeg",
        png: "png",
        ppt: "ppt",
        zip: "zip",
        rar: "rar",
        txt: "txt",
        pdf: "pdf",
      },
    };
  },
  computed: {
    hasMaterials() {
      return this.displayMaterials && this.displayMaterials.length > 0;
    },
  },
  mounted() {
    this.displayMaterials = [...this.materials];
  },
  methods: {
    icon(extension) {
      return Object.keys(this.icons).includes(extension)
        ? this.icons[extension]
        : "../../assets/extensions-icon/new-file.svg";
    },
    cancelFile() {
      this.fileList = [];
      this.dialogVisible = false;
    },
    saveFile() {
      this.dialogVisible = false;
      const formData = new FormData();
      this.fileList.forEach((file) => {
        formData.append("content", file.raw);
        formData.append(
          "data",
          JSON.stringify({
            type: this.title,
            topic: this.topic,
          })
        );
      });
      addTopicFile(formData).then((res) => {
        const files = Array.isArray(res.data) ? res.data : [res.data];
        console.log(files);
        files.forEach((file) => {
          this.displayMaterials.unshift(file);
        });
      });
      this.fileList = [];
    },
    handleRemoveFile(file, fileList) {
      this.fileList = this.fileList.filter((item) => item.uid !== file.uid);
    },
    handlePreview(file) {
      console.log(file);
    },
    handleExceed() {
      this.$message.warning(`Вы можете выбрать максимум 3 файлов.`);
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`Удалить ${file.name} ?`);
    },
    addFile(file, fileList) {
      this.fileList.push(file);
    },
    deleteMaterial(id) {
      this.$confirm(
        "Вы уверены, что хотите удалить материал? Это действие не обратимо.",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        }
      ).then(() => {
        deleteMaterial(id).then(() => {
          this.displayMaterials = this.displayMaterials.filter(
            (item) => item.id !== id
          );
        });
      });
    },
    handleClose(done) {
      this.$confirm("Вы уверены?", "", {
        confirmButtonText: "Да",
        cancelButtonText: "Отменить",
        type: "warning",
      })
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    toggleFiles(event) {
      if (
        event.target.closest(".file-group").children[1].style.display === "none"
      ) {
        event.target.closest(".file-group").children[1].style.display = "block";
        event.target.closest(
          ".file-section-title"
        ).children[1].style.transform = "rotate(180deg)";
      } else {
        event.target.closest(".file-group").children[1].style.display = "none";
        event.target.closest(
          ".file-section-title"
        ).children[1].style.transform = "rotate(0deg)";
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
