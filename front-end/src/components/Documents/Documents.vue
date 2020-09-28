<template>
  <div>
    <div v-if="documents.length !== 0" class="my-document">
      <div v-if="count > 5" class="count">
        {{ count }} документов
      </div>
      <div v-else-if="count > 1">
        {{ count }} документа
      </div>
      <div v-else-if="count > 0">
        {{ count }} документ
      </div>

      <div v-for="group in documents" :key="group.year">
        <div class="cool-hr d-flex align-items-center">
          <hr class="mr-3">
          {{ group.year }}
          <hr class="ml-3">
        </div>
        <el-row v-for="(document, index) in group.documents" :key="document.id" class="document-card mt-3 mb-4">
          <el-col :span="2" style="font-size: 22px" class="mt-4">
            № {{ index+1 }}
          </el-col>
          <el-col :span="21">
            <div class="d-flex">
              <div>
                {{ document.publication_date | moment }}
              </div>
              <div class="ml-5" style="color: #76767A">
                <span v-for="(publisher, index) in document.publishers" :key="index">{{ publisher.name }} </span>
              </div>
            </div>
            <div class="document-card-title">{{ document.title }}</div>
            <div v-for="(author, index) in document.authors" :key="index" class="document-card-authors">
              {{ `${author.last_name} ${author.first_name[0]}. ${author.patronymic[0]}.` }}
            </div>
            <div class="document-card-annotation">{{ document.annotation }}</div>
          </el-col>
          <el-col :span="1" class="d-flex justify-content-end mt-4" >
            <el-popover
                    placement="bottom"
                    trigger="click"
            >
              <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                <div style="cursor:pointer;">
                  <form :action="download" method="get">
                    <input :value="document.id" type="hidden" name="id">
                    <button class="download-kebab-button">Скачать</button>
                  </form>
                </div>
                <div style="cursor:pointer;" @click="deleteArticle(document.id)">Удалить</div>
              </div>
              <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
                <img src="../../assets/scienceWorks/popover.svg" alt="">
              </div>
            </el-popover>
          </el-col>
        </el-row>
      </div>

    </div>
    <div v-else class="my-document">
      Документы не найдены
    </div>
  </div>
</template>

<script>
import { getDocuments } from '@/api/documents'
import { deleteDocument } from '@/api/delete'
import EventBus from '../EventBus';
import {baseURL} from '@/utils/request';
import moment from 'moment'
import groupBy from 'lodash/groupBy';
import keys from 'lodash/keys';

export default {
  name: '',
  components: {},
  filters: {
    moment: function(date) {
      return moment(date).format('DD MMMM YYYY')
    }
  },
  data() {
    return {
      documents: [],
      count: undefined,
    }
  },
  watch: {
    '$route'(to, from) {
      this.fetchData()
    }
  },
  created() {
  },
  mounted() {
    this.fetchData()
    const self = this
    EventBus.$on('UPDATE_EVENT', function () {
      console.log('update')
      self.fetchData()
    })
  },
  computed: {
    download() {
      return `${baseURL}/dms/get_file`
    }
  },
  methods: {
    deleteArticle(id) {
      const deletedId = {
        'id': id
      }
      this.$confirm('Вы уверены?', 'Подтвердите действие', {
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отменить',
        type: 'warning'
      })
              .then(() => {
                deleteDocument(deletedId).then(response => {
                  this.documents.forEach(group => {
                    group.documents = group.documents.filter(i => {
                      return i.id !== id
                    })
                  })
                  this.documents = this.documents.filter(group => {
                    return group.documents.length !== 0
                  })
                  console.log('файл удален')
                  this.count = this.count - 1
                }).catch(() => {
                  console.log('Ошибка удаления файла')
                })
                this.$message({
                  type: 'success',
                  message: 'Удаление завершено'
                })
              })
              .catch(() => { })



    },
    fetchData() {
      let author = this.$route.query.author ?  this.$route.query.author :  null
      let place = this.$route.query.place ?  this.$route.query.place :  null
      let start_date = this.$route.query.start_date ?  this.$route.query.start_date :  null
      let end_date = this.$route.query.end_date ?  this.$route.query.end_date :  null
      let text = this.$route.query.text ?  this.$route.query.text :  null
      let category = this.$route.query.section ?  this.$route.query.section :  null
      getDocuments(category, author, place, start_date, end_date, text).then(response => {
        let groupsByYear = groupBy(response.data, function (document) {
          return moment(document.publication_date).year()
        })
        this.documents = keys(groupsByYear).sort().reverse().map(year => ({
          year: year,
          documents: groupsByYear[year],
        }))
        this.count = response.data.length
      }).catch(() => {
        console.log('Данные по документам не указаны')
      })
    },
    moment: function() {
      return moment()
    }
  },
}

</script>

<style scoped lang="scss">
  @import "style";
</style>
