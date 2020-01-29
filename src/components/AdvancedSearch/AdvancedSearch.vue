<template>
    <div>
        <div class="my-advanced-search" @click="advancedClick">
            <div class="d-flex align-items-center">
                <div class="my-advanced-search-text" style="cursor:pointer;">Расширенный поиск</div>
                <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="my-advanced-search-arrow ml-2">
            </div>
        </div>
        <div class="filters mt-3 pt-3 pb-3" style="display: none">
            <el-row class="">
                <el-col :span="10" :offset="1">
                    <div class="filters-title pl-1">Автор</div>
                    <el-select clearable v-model="author" placeholder="Все авторы" class="filters-select"
                               @change="changeAuthors">
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
                    <el-select clearable v-model="placing" placeholder="Все размещения" class="filters-select"
                               @change="changePlacing">
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
                <el-col :offset="1" :span="10">
                    <div class="filters-title pl-1">Период публикации</div>
                    <el-date-picker
                            v-model="valueDate"
                            type="daterange"
                            align="right"
                            unlink-panels
                            start-placeholder="Начало"
                            end-placeholder="Конец"
                            @change="changeDate"
                    />
                </el-col>
                <el-col :offset="1" :span="8" class="mt-1 d-flex align-items-center">
                    <el-checkbox v-model="checked" @change="showDeleted">Показывать удаленные</el-checkbox>
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
  import { getAuthors } from '@/api/authors'
  import { getPublishPlaces } from '@/api/published_places'
  import moment from 'moment'

  export default {
    name: '',
    components: {},
    data() {
      return {
        authors: [],
        author: '',
        placings: [],
        placing: '',
        valueDate: '',
        checked: false
      }
    },
    methods: {
      showDeleted() {
        if (this.checked) {
          this.$router.push({
            query: {
              text: this.$route.query.text,
              section: this.$route.query.section,
              place: this.$route.query.place,
              author: this.$route.query.author,
              start_date: this.$route.query.start_date,
              end_date: this.$route.query.end_date,
              show: 'all'
            }
          })
        } else {
          this.$router.push({
            query: {
              text: this.$route.query.text,
              section: this.$route.query.section,
              place: this.$route.query.place,
              author: this.$route.query.author,
              start_date: this.$route.query.start_date,
              end_date: this.$route.query.end_date,
              show: 'enabled'
            }
          })
        }
      },
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

      renderQuery(item) {
        let temp = { section: this.$route.query.section }
        if (this.$route.query.place) {
          temp.place = this.$route.query.place
        }
        if (this.$route.query.author) {
          temp.author = this.$route.query.author
        }
        if (this.$route.query.start_date) {
          temp.start_date = this.$route.query.start_date
          temp.end_date = this.$route.query.end_date
        }
        temp[item] = this[temp]
      },

      changeAuthors() {
        if (this.valueDate) {
          let start_date = this.$route.query.start_date
          let end_date = this.$route.query.end_date

          if (this.author && this.$route.query.place) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                author: this.author,
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.author && this.$route.query.place) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (this.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                section: this.$route.query.section,
                author: this.author,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                start_date: start_date,
                end_date: end_date,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          }

        } else {

          if (this.author && this.$route.query.place) {
            this.$router.push({
              query: {
                author: this.author,
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.author && this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (this.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                author: this.author,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          }

        }
      },

      changePlacing() {
        if (this.valueDate) {
          let start_date = this.$route.query.start_date
          let end_date = this.$route.query.end_date

          if (this.$route.query.author && this.placing) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                author: this.$route.query.author,
                section: this.$route.query.section,
                place: this.placing,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && this.placing) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                section: this.$route.query.section,
                place: this.placing,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (this.$route.query.author && !this.placing) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                section: this.$route.query.section,
                author: this.$route.query.author,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && !this.placing) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                start_date: start_date,
                end_date: end_date,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          }

        } else {
          if (this.$route.query.author && this.placing) {
            this.$router.push({
              query: {
                author: this.$route.query.author,
                section: this.$route.query.section,
                place: this.placing,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && this.placing) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                place: this.placing,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (this.$route.query.author && !this.placing) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                author: this.$route.query.author,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && !this.placing) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          }

        }
      },

      changeDate() {
        if (this.valueDate) {
          let start_date = moment(this.valueDate[0]).format('YYYY-MM-DD')
          let end_date = moment(this.valueDate[1]).format('YYYY-MM-DD')

          if (this.$route.query.author && this.$route.query.place) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                author: this.$route.query.author,
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && this.$route.query.place) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (this.$route.query.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                start_date: start_date,
                end_date: end_date,
                section: this.$route.query.section,
                author: this.$route.query.author,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                start_date: start_date,
                end_date: end_date,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          }

        } else {
          if (this.$route.query.author && this.$route.query.place) {
            this.$router.push({
              query: {
                author: this.$route.query.author,
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                place: this.$route.query.place,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (this.$route.query.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                author: this.$route.query.author,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          } else if (!this.$route.query.author && !this.$route.query.place) {
            this.$router.push({
              query: {
                section: this.$route.query.section,
                text: this.$route.query.text ? this.$route.query.text : null,
                show: this.$route.query.show ? this.$route.query.show : 'enabled'
              }
            })
          }

        }
      }
    },
    mounted() {
      getAuthors().then(response => {
        this.authors = response.data
      }).catch(() => {
        console.log('Данные по авторам не указаны')
      })

      getPublishPlaces().then(response => {
        this.placings = response.data
      }).catch(() => {
        console.log('Данные по размещениям не указаны')
      })
    }
  }

</script>

<style scoped lang="scss">
    @import "style";
</style>
