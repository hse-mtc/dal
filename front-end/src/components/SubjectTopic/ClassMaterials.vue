<template>
  <div class="class-materials file-group">
    <div class="class-materials-title file-section-title" @click="toggleFiles">
      <div>{{ title }}</div>
      <img
        src="../../assets/scienceWorks/dropdown.svg"
        alt=""
        class="files-dropdown"
      />
    </div>

    <div style="display: none">
      <div class="files" v-if="hasMaterials">
        <div class="file" v-for="(material, index) in materials" :key="index">
          <div class="file-icon">
            <img
              src="../../assets/subject/iconPowerPoint.svg"
              alt=""
              class="kebab"
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
                <div style="cursor: pointer">Скачать</div>
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
          >Здесь пока нет материалов</CustomText
        >
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
      <span>Здесь будет загрузка файлов</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">Отмена</el-button>
        <el-button type="primary" @click="dialogVisible = false"
          >Добавить</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";
import { deleteMaterial } from "@/api/material";

export default {
  components: { CustomText },
  props: {
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
      dialogVisible: false,
    };
  },
  methods: {
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
          this.materials = this.materials.filter((item) => item.id !== id);
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

  computed: {
    hasMaterials() {
      return this.materials && this.materials.length > 0;
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
