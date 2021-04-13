<template>
  <div class="text-center">
    <el-tabs type="border-card" @tab-click="handleClick">
      <el-tab-pane
        v-for="milfaculty in milfaculties"
        :key="milfaculty.milfaculty"
        :label="milfaculty.milfaculty"
        v-loading="milfaculty.milfaculty !== uniform.milfaculty"
      >
        <div class="image-container">
          <img src="@/assets/uniform-picker/base.svg" alt="Ошибка" />
          <!-- Headdress -->
          <img :src="headdressesSrc[uniform.headdress]" alt="" class="above" />
          <!-- Outerwear -->
          <img :src="outerwearsSrc[uniform.outerwear]" alt="" class="above" />
          <el-button
            icon="el-icon-caret-left"
            circle
            @click="cycleThroughHeaddresses"
            class="top-left"
          ></el-button>
          <el-button
            icon="el-icon-caret-left"
            circle
            class="left"
            @click="cycleThroughOuterwears"
          ></el-button>
          <el-button
            icon="el-icon-caret-right"
            circle
            @click="cycleThroughHeaddresses"
            class="top-right"
          ></el-button>
          <el-button
            icon="el-icon-caret-right"
            circle
            @click="cycleThroughOuterwears"
            class="right"
          ></el-button>
        </div>
        <el-button icon="el-icon-check" type="success" @click="confirmUniform"
          >Утвердить</el-button
        >
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getMilFaculties } from "@/api/reference-book";
import { getUniforms, createUniform, changeUniform } from "@/api/uniform";
import { getError, postError, patchSuccess, patchError } from "@/utils/message";

export default {
  name: "",
  data() {
    return {
      uniform: {},
      milfaculties: [],
      headdresses: ["CA", "HA"],
      headdressesSrc: {
        CA: require("@/assets/uniform-picker/cap.svg"),
        HA: require("@/assets/uniform-picker/hat.svg"),
      },
      outerwears: ["JA", "PC"],
      outerwearsSrc: {
        JA: "",
        PC: require("@/assets/uniform-picker/pea-coat.svg"),
      },
    };
  },
  methods: {
    fetchUniform(milfaculty) {
      getUniforms({
        milfaculty: milfaculty,
      })
        .then((response) => {
          if (response.data.length === 0) {
            // Create
            createUniform({
              headdress: "CA",
              outerwear: "JA",
              milfaculty: milfaculty,
            })
              .then((resp) => {
                this.uniform = resp.data;
              })
              .catch((err) => {
                postError("формы одежды", err.response.status);
              });
          } else this.uniform = response.data[0];
        })
        .catch((err) => {
          getError("информации о форме одежды", err.response.status);
        });
    },
    handleClick(obj) {
      this.fetchUniform(obj.label);
    },
    cycleThroughHeaddresses() {
      const nextIndex = this.headdresses.indexOf(this.uniform.headdress) + 1;
      this.uniform.headdress = this.headdresses[
        nextIndex % this.headdresses.length
      ];
    },
    cycleThroughOuterwears() {
      const nextIndex = this.outerwears.indexOf(this.uniform.outerwear) + 1;
      this.uniform.outerwear = this.outerwears[
        nextIndex % this.outerwears.length
      ];
    },
    confirmUniform() {
      changeUniform(
        {
          headdress: this.uniform.headdress,
          outerwear: this.uniform.outerwear,
        },
        this.uniform.id
      )
        .then(() => {
          patchSuccess("формы одежды");
        })
        .catch((err) => {
          patchError("формы одежды", err.response.status);
        });
    },
  },
  created() {
    getMilFaculties()
      .then((response) => {
        this.milfaculties = response.data;
        this.fetchUniform(this.milfaculties[0].milfaculty);
      })
      .catch((err) => {
        console.log(err);
        getError("информации о циклах", err.response.status);
      });
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
