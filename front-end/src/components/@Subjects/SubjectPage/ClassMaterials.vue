<template>
  <div :class="[$style.root, { [$style.highlight]: highlight }]">
    <div
      :class="$style.header"
      @click="opened = !opened"
    >
      <span :class="$style.title">{{ title }}</span>

      <i
        :class="[
          opened ? 'el-icon-arrow-up' : 'el-icon-arrow-down',
          $style.arrow,
        ]"
      />
    </div>

    <div v-if="opened" :class="$style.content">
      <div :class="$style.add">
        <AZGuard
          :permissions="['class-materials.post.all', {
            codename: 'class-materials.post.self',
            validator: () => userId === subjectOwnerId,
          }]"
        >
          <el-button
            type="text"
            :class="$style.addButton"
            @click="dialogVisible = true"
          >
            + Добавить материал
          </el-button>
        </AZGuard>

        <el-dialog
          :visible.sync="dialogVisible"
          width="350px"
          :before-close="handleClose"
        >
          <FileInput
            v-model="newFiles"
            title="Не более 3х"
            :limit="3"
          />

          <el-checkbox v-model="visibleToStudents" label="доступно для студентов" style="margin-top: 20px" />

          <span slot="footer" class="dialog-footer">
            <el-button @click="cancelFile">Отмена</el-button>

            <el-button type="primary" @click="saveFile">Сохранить</el-button>
          </span>
        </el-dialog>
      </div>

      <div v-if="materials.length" :class="$style.files">
        <div
          v-for="material in materials"
          :key="material.id"
          :class="$style.file"
        >
          <svg-icon
            :icon-class="material.file.extension || 'new-file'"
            :class="$style.fileExtIcon"
          />

          <div :class="$style.fileTitle">
            {{ material.title }}
          </div>

          <div :class="$style.fileControls">
            <el-popover placement="bottom" trigger="click">
              <div
                :style="{
                  textAlign: 'center',
                  margin: 0,
                  padding: 0,
                  fontSize: '15px',
                }"
              >
                <AZGuard
                  :permissions="['class-materials.delete.all', {
                    codename: 'class-materials.delete.self',
                    validator: () => userId === subjectOwnerId,
                  }]"
                >
                  <div
                    style="cursor: pointer"
                    @click="deleteMaterial(material.id)"
                  >
                    Удалить
                  </div>
                </AZGuard>

                <DownloadFile
                  :url="material.file.content"
                  :file-name="material.file.name"
                >
                  Скачать
                </DownloadFile>
              </div>

              <svg-icon
                slot="reference"
                icon-class="greyKebab"
                :class="$style.fileControlsIcon"
              />
            </el-popover>
          </div>
        </div>
      </div>
      <span v-else :class="$style.filesEmptyText">
        Здесь пока нет материалов
      </span>
    </div>
  </div>
</template>

<script>
import {
  Component,
  ModelSync,
  Prop,
  Vue,
  Watch,
} from "vue-property-decorator";

import _isArray from "lodash/isArray";

import { SubjectsModule, UserModule } from "@/store";
import { getDeleteRequest } from "@/utils/mutators";
import { addTopicFile, deleteMaterial } from "@/api/material";
import { downloadError } from "@/utils/message";
import DownloadFile from "@/common/DownloadFile/index.vue";
import { FileInput } from "@/common/inputs";

@Component({
  name: "ClassMaterials",
  components: {
    DownloadFile,
    FileInput,
  },
})
class ClassMaterials extends Vue {
  @ModelSync("isOpen", "change", { default: false }) opened
  @Prop({ default: "" }) title
  @Prop({ default: "" }) code
  @Prop({ type: Array, required: true }) materials
  @Prop({ required: true }) topicId
  @Prop({ type: Boolean }) highlight

  dialogVisible = false

  newFiles = []

  visibleToStudents = false;

  get subjectOwnerId() { return SubjectsModule.currentSubject.user.id; }
  get userId() { return UserModule.userId; }

  async deleteMaterial(id) {
    await this.$confirm(
      "Вы уверены, что хотите удалить материал? Это действие не обратимо.",
      "Подтверждение",
      {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      },
    );

    getDeleteRequest(
      deleteMaterial,
      data => { this.materials = data; },
      "materials",
      "материал",
    ).call(this, id);
  }

  async handleClose(done) {
    await this.$confirm("Вы уверены?", "", {
      confirmButtonText: "Да",
      cancelButtonText: "Отменить",
      type: "warning",
    });

    done();
  }

  cancelFile() {
    this.newFiles = [];
    this.dialogVisible = false;
  }

  async saveFile() {
    this.dialogVisible = false;
    const formData = new FormData();

    this.newFiles.forEach(file => {
      formData.append("content", file.raw);
      formData.append(
        "data",
        JSON.stringify({
          type: this.code,
          topic: this.topicId,
          visible_to_students: this.visibleToStudents,
        }),
      );
    });

    try {
      const { data } = await addTopicFile(formData);
      const files = _isArray(data) ? data : [data];

      this.materials.push(...files);
    } catch (e) {
      downloadError("файла", e.response?.status);
    }

    this.newFiles = [];
  }
}

export default ClassMaterials;
</script>

<style lang="scss" module>
.root {
  position: relative;

  &::after {
    transition: 0.5s;
    display: block;
    position: absolute;
    content: "";
    top: -10px;
    bottom: -10px;
    left: -10px;
    right: -10px;
    background-color: #000;
    border-radius: 10px;
    opacity: 0;
    z-index: -1;
  }

  &.highlight::after {
    opacity: 0.2;
    z-index: 1;
  }
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  padding: 5px;
  font-size: 14px;
  color: #0c4b9a;
  border-bottom: 1px solid #e5e5e5;
  cursor: pointer;
}

.files {
  display: flex;
  flex-wrap: wrap;

  @media screen and (max-width: 1024px) {
    flex-direction: column;
  }

  .file {
    display: flex;
    align-items: center;
    position: relative;
    margin-top: 10px;
    padding: 30px 15px;
    width: calc(50% - 10px);
    border: 1px solid #e5e5e5;
    border-radius: 12px;

    &:nth-child(2n) {
      margin-left: 20px;
    }

    @media screen and (max-width: 1024px) {
      width: 100%;

      &:nth-child(2n) {
        margin-left: 0;
      }
    }

    &ExtIcon {
      font-size: 48px;
      margin-right: 15px;
    }

    &Controls {
      position: absolute;
      top: 14px;
      right: 14px;

      &Icon {
        font-size: 25px;
      }
    }
  }

  &EmptyText {
    display: block;
    margin-top: 10px;
  }
}

.addButton {
  display: block;
  margin: 20px 0 0 auto;
  font-size: 18px;
  color: #0c4b9a;
}
</style>
