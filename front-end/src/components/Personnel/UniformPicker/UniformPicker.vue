<template>
  <div
    v-loading="loading"
    class="text-center"
  >
    <div v-if="!milfacultiesFiltered">
      Циклы не существуют, либо у Вас нет прав.
    </div>

    <el-tabs
      v-else
      type="border-card"
    >
      <el-tab-pane
        v-for="milfaculty in milfacultiesFiltered"
        :key="milfaculty.id"
        :label="milfaculty.title"
      >
        <div class="image-container">
          <img src="@/assets/uniform-picker/base.svg" alt="Ошибка">
          <!-- Headdress -->
          <img :src="HEADDRESSES[uniform.headdress]" alt="" class="above">
          <!-- Outerwear -->
          <img :src="OUTERWEARS[uniform.outerwear]" alt="" class="above">
          <el-button
            v-if="hasPermission(getPermissions(milfaculty.id, 'patch'))"
            icon="el-icon-caret-left"
            circle
            class="top-left"
            @click="cycleThroughHeaddresses"
          />
          <el-button
            v-if="hasPermission(getPermissions(milfaculty.id, 'patch'))"
            icon="el-icon-caret-left"
            circle
            class="left"
            @click="cycleThroughOuterwears"
          />
          <el-button
            v-if="hasPermission(getPermissions(milfaculty.id, 'patch'))"
            icon="el-icon-caret-right"
            circle
            class="top-right"
            @click="cycleThroughHeaddresses"
          />
          <el-button
            v-if="hasPermission(getPermissions(milfaculty.id, 'patch'))"
            icon="el-icon-caret-right"
            circle
            class="right"
            @click="cycleThroughOuterwears"
          />
        </div>
        <AZGuard :permissions="getPermissions(milfaculty.id, 'patch')">
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
import { hasPermission } from "@/utils/permissions";

import { UserModule, ReferenceModule } from "@/store";
import { HEADDRESSES, OUTERWEARS } from "@/utils/enums";

export default {
  name: "UniformPicker",

  data() {
    return {
      HEADDRESSES,
      OUTERWEARS,
      uniform: {},
      fetchingData: false,
    };
  },

  computed: {
    userMilfaculty() {
      return UserModule.personMilfaculty;
    },
    milfaculties() {
      return ReferenceModule.milfaculties;
    },
    milfacultiesFiltered() {
      return this.milfaculties.filter(x => hasPermission(this.getPermissions(x.id, "get")));
    },
    loading() {
      return this.fetchingData;
    },
  },

  async created() {
    this.fetchingData = true;
    await ReferenceModule.fetchMilfaculties();
    this.fetchingData = false;

    await this.fetchUniform(this.milfaculties ? this.milfaculties[0].id : null);
  },

  methods: {
    hasPermission,
    getPermissions(milfaculty, method) {
      return [
        `uniforms.${method}.all`,
        {
          codename: `uniforms.${method}.milfaculty`,
          validator: () => +this.userMilfaculty === milfaculty,
        },
      ];
    },

    async fetchUniform(milfaculty) {
      if (!milfaculty) {
        return;
      }

      let response;
      try {
        response = await getUniforms({ milfaculty });
      } catch (err) {
        getError("информации о форме одежды", err.response.status);
        return;
      }

      if (response.data.length > 0) {
        [this.uniform] = response.data;
        return;
      }

      // Create uniform if it does not exist.
      try {
        response = await createUniform({
          headdress: "CA",
          outerwear: "JA",
          milfaculty,
        });
      } catch (e) {
        postError("формы одежды", e.response?.status);
        return;
      }

      this.uniform = response.data;
    },

    cycleThroughHeaddresses() {
      const keys = Object.keys(HEADDRESSES);
      const nextIndex = keys.indexOf(this.uniform.headdress) + 1;
      this.uniform.headdress = keys[nextIndex % keys.length];
    },
    cycleThroughOuterwears() {
      const keys = Object.keys(OUTERWEARS);
      const nextIndex = keys.indexOf(this.uniform.outerwear) + 1;
      this.uniform.outerwear = keys[nextIndex % keys.length];
    },

    async confirmUniform() {
      try {
        await changeUniform(
          {
            headdress: this.uniform.headdress,
            outerwear: this.uniform.outerwear,
          },
          this.uniform.id,
        );
        patchSuccess("формы одежды");
      } catch (err) {
        patchError("формы одежды", err.response.status);
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
