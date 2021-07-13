<template>
  <div class="text-center">
    <el-tabs type="border-card">
      <el-tab-pane
        v-for="milfaculty in milfaculties"
        :key="milfaculty.id"
        :label="milfaculty.title"
      >
        <div class="image-container">
          <img src="@/assets/uniform-picker/base.svg" alt="Ошибка">
          <!-- Headdress -->
          <img :src="HEAD_DRESSES[uniform.headdress]" alt="" class="above">
          <!-- Outerwear -->
          <img :src="OUTERWEARS[uniform.outerwear]" alt="" class="above">
          <AZGuard :permissions="getPermissions(milfaculty.milfaculty)">
            <el-button
              icon="el-icon-caret-left"
              circle
              class="top-left"
              @click="cycleThroughHeaddresses"
            />
            <el-button
              icon="el-icon-caret-left"
              circle
              class="left"
              @click="cycleThroughOuterwears"
            />
            <el-button
              icon="el-icon-caret-right"
              circle
              class="top-right"
              @click="cycleThroughHeaddresses"
            />
            <el-button
              icon="el-icon-caret-right"
              circle
              class="right"
              @click="cycleThroughOuterwears"
            />
          </AZGuard>
        </div>
        <AZGuard :permissions="getPermissions(milfaculty.id)">
          <el-button
            icon="el-icon-check"
            type="success"
            @click="confirmUniform"
          >
            Утвердить
          </el-button>
        </AZGuard>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { getUniforms, createUniform, changeUniform } from "@/api/uniform";
import {
  getError, postError, patchSuccess, patchError,
} from "@/utils/message";

import { UserModule, ReferenceModule } from "@/store";
import { HEAD_DRESSES, OUTERWEARS } from "@/utils/enums";

export default {
  name: "",
  data() {
    return {
      HEAD_DRESSES,
      OUTERWEARS,
      uniform: {},
    };
  },
  computed: {
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    milfaculties() {
      return ReferenceModule.milfaculties;
    },
  },
  created() {
    this.fetchUniform();
  },
  methods: {
    getPermissions(milfaculty) {
      return [
        "uniforms.patch.all",
        {
          codename: "uniforms.patch.milfaculty",
          validator: () => this.userMilfaculty === milfaculty,
        },
      ];
    },
    fetchUniform(milfaculty) {
      getUniforms({
        milfaculty,
      })
        .then(response => {
          if (response.data.length === 0) {
            // Create
            createUniform({
              headdress: "CA",
              outerwear: "JA",
              milfaculty,
            })
              .then(resp => {
                this.uniform = resp.data;
              })
              .catch(err => {
                postError("формы одежды", err.response.status);
              });
          } else {
            [this.uniform] = response.data;
          }
        })
        .catch(err => {
          getError("информации о форме одежды", err.response.status);
        });
    },
    cycleThroughHeaddresses() {
      const keys = Object.keys(HEAD_DRESSES);
      const nextIndex = keys.indexOf(this.uniform.headdress) + 1;
      this.uniform.headdress = keys[nextIndex % keys.length];
    },
    cycleThroughOuterwears() {
      const keys = Object.keys(OUTERWEARS);
      const nextIndex = keys.indexOf(this.uniform.outerwear) + 1;
      this.uniform.outerwear = keys[nextIndex % keys.length];
    },
    confirmUniform() {
      changeUniform(
        {
          headdress: this.uniform.headdress,
          outerwear: this.uniform.outerwear,
        },
        this.uniform.id,
      )
        .then(() => {
          patchSuccess("формы одежды");
        })
        .catch(err => {
          patchError("формы одежды", err.response.status);
        });
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
