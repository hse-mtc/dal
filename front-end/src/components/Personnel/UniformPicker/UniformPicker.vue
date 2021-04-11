<template>
  <div class="text-center">
    <el-tabs type="border-card">
      <el-tab-pane
        v-for="milfaculty in milfaculties"
        :key="milfaculty"
        :label="milfaculty"
      >
        <div>
          <el-button
            icon="el-icon-caret-left"
            circle
            @click="cycleThroughHeaddresses()"
          ></el-button>
          <el-button
            icon="el-icon-caret-left"
            circle
            @click="cycleThroughOuterwears()"
          ></el-button>
          <!-- SVG human image here -->
          <p>
            {{ headdresses[headdress_index] }} +
            {{ outerwears[outerwear_index] }}
          </p>
          <el-button
            icon="el-icon-caret-right"
            circle
            @click="cycleThroughHeaddresses()"
          ></el-button>
          <el-button
            icon="el-icon-caret-right"
            circle
            @click="cycleThroughOuterwears()"
          ></el-button>
        </div>
        <el-button
          icon="el-icon-check"
          type="success"
          style="margin-top: 20px"
          @click="confirmUniform(milfaculty)"
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
      uniforms: {},
      milfaculties: [],
      headdresses: ["CA", "HA"],
      outerwears: ["JA", "PC"],
      headdress_index: 0,
      outerwear_index: 0,
    };
  },
  created() {
    var tmp_milfaculties, tmp_uniforms;

    Promise.all([getMilFaculties(), getUniforms()])
      .then((responses) => {
        tmp_milfaculties = responses[0].data;
        tmp_uniforms = responses[1].data;
        // some processing
        for (var i = 0; i < tmp_uniforms.length; ++i) {
          this.milfaculties.push(tmp_uniforms[i].milfaculty);
          this.uniforms[tmp_uniforms[i].milfaculty] = tmp_uniforms[i];
        }
        this.milfaculties.sort();
        // if there are milfaculties without uniforms, create them
        for (var i = 0; i < tmp_milfaculties.length; ++i) {
          if (!this.milfaculties.includes(tmp_milfaculties[i].milfaculty))
            createUniform({
              headdress: "CA",
              outerwear: "JA",
              milfaculty: tmp_milfaculties[i].milfaculty,
            })
              .then((response) => {
                console.log(
                  `Created uniform for ${milfaculty} with code ${response.status}`
                );
              })
              .catch((err) => {
                postError("формы одежды", err.response.status);
              });
        }
      })
      .catch((errors) => {
        for (var i = 0; i < errors.length; ++i)
          getError("данных", errors[i].response.status);
      });
  },
  methods: {
    cycleThroughHeaddresses() {
      this.headdress_index =
        (this.headdress_index + 1) % this.headdresses.length;
    },
    cycleThroughOuterwears() {
      this.outerwear_index =
        (this.outerwear_index + 1) % this.outerwears.length;
    },
    confirmUniform(milfaculty) {
      changeUniform(
        {
          headdress: this.headdresses[this.headdress_index],
          outerwear: this.outerwears[this.outerwear_index],
        },
        this.uniforms[milfaculty].id
      )
        .then((response) => {
          patchSuccess("формы одежды");
        })
        .catch((err) => {
          patchError("формы одежды", err.response.status);
        });
    },
  },
};
</script>
