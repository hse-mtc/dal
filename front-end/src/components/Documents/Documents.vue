<template>
  <div>
    <div v-if="documents.length !== 0" class="my-document">
      <div class="count">
        {{ count }} {{ "документ" + (count > 5 ? "ов" : count > 1 ? "а" : "") }}
      </div>

      <div v-for="group in documents" :key="group.year">
        <div class="cool-hr d-flex align-items-center">
          <hr class="mr-3">
          {{ group.year }}
          <hr class="ml-3">
        </div>

        <el-row v-for="(document, index) in group.documents" :key="document.id" class="document-card mt-3 mb-4">
          <el-col :span="2" style="font-size: 22px" class="mt-4">
            № {{ index + 1 }}
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

          <el-col :span="1" class="d-flex justify-content-end mt-4">
            <el-popover
                placement="bottom"
                trigger="hover"
            >
              <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                <div style="cursor:pointer;" @click.prevent="downloadFile(document.file)">Скачать</div>
                <div style="cursor:pointer;" @click="editPaper(document.id)">Редактировать</div>
                <div style="cursor:pointer;" @click="deletePaper(document.id)">Удалить</div>
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
import axios from "axios"
import moment from 'moment'
import groupBy from 'lodash/groupBy'
import keys from 'lodash/keys'

import {getDocuments} from '@/api/documents'
import {deleteDocument} from '@/api/delete'

import EventBus from '../EventBus'

export default {
  name: '',

  filters: {
    moment: function (date) {
      return moment(date).format('DD MMMM YYYY')
    }
  },
  watch: {
    '$route': 'fetchData',
  },

  data() {
    return {
      documents: [],
      count: undefined,
      paperToEdit: {},
    }
  },

  async mounted() {
    await this.fetchData()
    const self = this
    EventBus.$on('UPDATE_EVENT', () => {
      self.fetchData()
    })
  },

  methods: {
    moment,

    async downloadFile(file) {
      let data
      try {
        data = (await axios.get(file.content, {responseType: 'blob'})).data
      } catch (error) {
        console.log("Failed to download Paper.file: ", error)
        return
      }

      const create = document.createElement.bind(document)
      const link = create('a')

      const blob = new Blob([data])
      link.href = URL.createObjectURL(blob)
      link.download = file.name

      link.click()
      URL.revokeObjectURL(link.href)
    },

    editPaper(id) {
      const allDocs = this.documents.map(group => group.documents).flat(1)
      const paperToEdit = allDocs.find(paper => paper.id === id)
      this.$emit("openPaperModal", "edit", paperToEdit)
    },

    async deletePaper(id) {
      await this.$confirm('Вы уверены?', 'Подтвердите действие', {
        confirmButtonText: 'Удалить',
        cancelButtonText: 'Отменить',
        type: 'warning'
      })

      try {
        await deleteDocument(id)
      } catch (error) {
        console.log("Failed to delete Paper: ", error)
        return
      }

      this.documents.forEach(group => {
        group.documents = group.documents.filter(paper => paper.id !== id)
      })
      this.documents = this.documents.filter(group => group.documents.length)
      this.count = this.count - 1

      this.$message({
        type: 'success',
        message: 'Удаление завершено'
      })
    },

    async fetchData() {
      let author = this.$route.query.author ? this.$route.query.author : null
      let place = this.$route.query.place ? this.$route.query.place : null
      let start_date = this.$route.query.start_date ? this.$route.query.start_date : null
      let end_date = this.$route.query.end_date ? this.$route.query.end_date : null
      let text = this.$route.query.text ? this.$route.query.text : null
      let category = this.$route.query.category ? this.$route.query.category : null

      let papers
      try {
        papers = (await getDocuments(category, author, place, start_date, end_date, text)).data
      } catch (error) {
        console.log("Failed to fetch Papers: ", error)
        return
      }

      const groupsByYear = groupBy(papers, (paper) => {
        return moment(paper.publication_date).year()
      })
      this.documents = keys(groupsByYear).sort().reverse().map((year) => ({
        year: year,
        documents: groupsByYear[year],
      }))
      this.count = papers.length
    },
  },
}

</script>

<style scoped lang="scss">
@import "style";
</style>
