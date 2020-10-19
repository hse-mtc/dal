<template>
  <div class="class-materials file-group" v-show="hasMaterials">
    <div class="class-materials-title file-section-title" @click="toggleFiles">
      <div>{{ title }}</div>
      <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="files-dropdown">
    </div>

    <div class="files" style="display: none">
      <div class="file" v-for="(material, index) in materials" :key="index">
        <div class="file-icon"><img src="../../assets/subject/iconPowerPoint.svg" alt="" class="kebab"></div>
        <div class="file-title">{{ material.title }}</div>

        <div class="file-kebab">
          <el-popover placement="bottom" trigger="click">
            <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
              <div style="cursor:pointer;">Действие 1</div>
              <div style="cursor:pointer;">Действие 2</div>
            </div>

            <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
              <img src="../../assets/subject/greyKebab.svg" alt="" class="kebab">
            </div>
          </el-popover>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    materials: {
      type: Array,
      required: true,
    }
  },

  methods: {
    toggleFiles(event) {
      if (event.target.closest('.file-group').children[1].style.display === 'none') {
        event.target.closest('.file-group').children[1].style.display = 'flex'
        event.target.closest('.file-section-title').children[1].style.transform = 'rotate(180deg)'
      } else {
        event.target.closest('.file-group').children[1].style.display = 'none'
        event.target.closest('.file-section-title').children[1].style.transform = 'rotate(0deg)'
      }
    }
  },

  computed: {
    hasMaterials() {
      return this.materials && this.materials.length > 0
    }
  }
}
</script>

<style scoped lang="scss">
@import "style";
</style>
