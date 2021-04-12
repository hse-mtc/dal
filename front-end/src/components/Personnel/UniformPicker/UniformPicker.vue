<template>
  <div class="text-center">
    <el-tabs type="border-card" @tab-click="handleClick">
      <el-tab-pane
        v-for="milfaculty in milfaculties"
        :key="milfaculty.milfaculty"
        :label="milfaculty.milfaculty"
        v-loading="milfaculty.milfaculty !== uniform.milfaculty"
      >
        <div>
          <el-button
            icon="el-icon-caret-left"
            circle
            @click="cycleThroughHeaddresses"
          ></el-button>
          <el-button
            icon="el-icon-caret-left"
            circle
            @click="cycleThroughOuterwears"
          ></el-button>
          <!-- SVG human image here -->
          <p>
            {{ uniform.headdress }} +
            {{ uniform.outerwear }}
          </p>
          <el-button
            icon="el-icon-caret-right"
            circle
            @click="cycleThroughHeaddresses"
          ></el-button>
          <el-button
            icon="el-icon-caret-right"
            circle
            @click="cycleThroughOuterwears"
          ></el-button>
        </div>
        <el-button
          icon="el-icon-check"
          type="success"
          style="margin-top: 20px"
          @click="confirmUniform"
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
      outerwears: ["JA", "PC"],
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
      var headdress_index = this.headdresses.indexOf(this.uniform.headdress);
      headdress_index = (headdress_index + 1) % this.headdresses.length;
      this.uniform.headdress = this.headdresses[headdress_index];
    },
    cycleThroughOuterwears() {
      var outerwear_index = this.outerwears.indexOf(this.uniform.outerwear);
      outerwear_index = (outerwear_index + 1) % this.outerwears.length;
      this.uniform.outerwear = this.outerwears[outerwear_index];
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
