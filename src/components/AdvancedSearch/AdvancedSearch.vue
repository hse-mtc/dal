<template>
  <div>
    <div class="my-advanced-search" @click="advancedClick">
      <div class="d-flex align-items-center">
        <div class="my-advanced-search-text" style="cursor:pointer;">Расширенный поиск</div>
        <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="my-advanced-search-arrow ml-2">
      </div>
    </div>
    <div class="filters mt-3 pt-3 pb-3">
      <el-row class="">
        <el-col :span="10" :offset="1">
          <div class="filters-title pl-1">Автор</div>
          <el-select v-model="author" placeholder="Все авторы" class="filters-select" @change="selectAuthors()">
            <el-option
              v-for="item in authors"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
        <el-col :span="10" :offset="1">
          <div class="filters-title pl-1">Размещение</div>
          <el-select v-model="placing" placeholder="Все размещения" class="filters-select">
            <el-option
              v-for="item in placings"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-col>
      </el-row>
      <el-row class="mt-3">
        <el-col :offset="1" :span="8">
          <div class="filters-title pl-1">Период публикации</div>
          <el-date-picker
            v-model="valueDate"
            type="daterange"
            align="right"
            start-placeholder="Начало"
            end-placeholder="Конец"
            default-value=""
          />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  components: {},
  data() {
    return {
      authors: [{
        value: 'Option1',
        label: 'Option1'
      }, {
        value: 'Option2',
        label: 'Option2'
      }, {
        value: 'Option3',
        label: 'Option3'
      }, {
        value: 'Option4',
        label: 'Option4'
      }, {
        value: 'Option5',
        label: 'Option5'
      }],
      author: '',
      placings: [{
        value: 'Option1',
        label: 'Option1'
      }, {
        value: 'Option2',
        label: 'Option2'
      }, {
        value: 'Option3',
        label: 'Option3'
      }, {
        value: 'Option4',
        label: 'Option4'
      }, {
        value: 'Option5',
        label: 'Option5'
      }],
      placing: '',
      valueDate: ''
    }
  },
  methods: {
    advancedClick() {
      const filters = document.querySelector('.filters')
      const array = document.querySelector('.my-advanced-search-arrow')
      if (filters.style.display === 'none') {
        filters.style.display = 'block'
        array.style.transform = 'rotate(0deg)'
      } else {
        filters.style.display = 'none'
        array.style.transform = 'rotate(180deg)'
      }
    },
    // selectAuthors() {
    //   console.log(this.$route)
    //   this.$route.query.author = this.author
    // }
  }
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
