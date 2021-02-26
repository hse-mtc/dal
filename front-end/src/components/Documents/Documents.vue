<template>
  <div>
    <div v-if="documents.length !== 0" class="my-document">
      <div class="count">
        {{ count || 0 }}
        {{ `документ${(count > 4 && "ов") || (count > 1 && "а") || ""}` }}
      </div>

      <el-row
          v-for="(document, index) in documents"
          :key="document.id"
          class="document-card mt-3 mb-4"
      >
        <div
            v-if="yearChanged(index)"
            class="cool-hr d-flex align-items-center"
        >
          <hr class="mr-3"/>
          {{ year(document) }}
          <hr class="ml-3"/>
        </div>

        <el-col :span="2" style="font-size: 22px" class="mt-4">
          № {{ index + 1 }}
        </el-col>

        <el-col :span="21">
          <div class="d-flex">
            <div>
              {{ document.publication_date | moment }}
            </div>

            <div class="ml-5" style="color: #76767a">
              <span
                  v-for="publisher in document.publishers"
                  :key="publisher.id"
              >
                {{ publisher.name }}
              </span>
            </div>
          </div>

          <div class="document-card-title">{{ document.title }}</div>

          <div
              v-for="author in document.authors"
              :key="author.id"
              class="document-card-authors"
          >
            {{
              `${author.surname} ${author.name[0]}. ${author.patronymic[0]}.`
            }}
          </div>

          <div class="document-card-annotation">
            {{ document.annotation }}
          </div>
        </el-col>

        <el-col :span="1" class="d-flex justify-content-end mt-4">
          <el-popover placement="bottom" trigger="hover">
            <div
                style="text-align: center; margin: 0; padding: 0; font-size: 15px"
            >
              <DownloadFile
                  :url="document.file.content"
                  :fileName="document.file.name"
              >
                Скачать
              </DownloadFile>
              <div style="cursor: pointer" @click="editPaper(document.id)">
                Редактировать
              </div>
              <div style="cursor: pointer" @click="deletePaper(document.id)">
                Удалить
              </div>
            </div>

            <div
                slot="reference"
                class="d-flex justify-content-center"
                style="width: 10px; cursor: pointer"
            >
              <img src="../../assets/scienceWorks/popover.svg" alt=""/>
            </div>
          </el-popover>
        </el-col>
      </el-row>
    </div>
    <div v-else-if="!loading" class="my-document">Документы не найдены</div>
    <div v-loading="loading" class="requests__loader"></div>
  </div>
</template>

<script>
import moment from "moment";

import { getPapers } from "@/api/papers";
import { deleteDocument } from "@/api/delete";

import EventBus from "../EventBus";
import {scrollMixin} from "@/mixins/scrollMixin";
import DownloadFile from '@/common/DownloadFile/index.vue'
import {mapState} from "vuex";

export default {
  name: "",
  components: {DownloadFile},
  props: {
    isMyDocuments: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      userId: (state) => state.app.userId,
    }),
  },
  filters: {
    moment: function (date) {
      return moment(date).format("DD MMMM YYYY");
    },
  },
  watch: {
    $route() {
      this.count = null;
      this.documents = [];
      this.fetchData();
    },
  },
  mixins: [scrollMixin],
  data() {
    return {
      count: null,
      limit: 10,
      loading: false,
      documents: [],
      paperToEdit: {},
    };
  },
  async mounted() {
    await this.fetchData();
    EventBus.$on("UPDATE_EVENT", () => {
      this.documents = []
      this.fetchData();
    });
  },
  methods: {
    moment,
    loadMore() {
      this.fetchData();
    },
    yearChanged(index) {
      if (index === 0) {
        return true;
      }

      const prev = this.year(this.documents[index - 1]);
      const curr = this.year(this.documents[index]);

      return prev !== curr;
    },

    year(document) {
      return moment(document.publication_date).year();
    },

    editPaper(id) {
      const paperToEdit = this.documents.find((paper) => paper.id === id);
      this.$emit("openPaperModal", "edit", paperToEdit);
    },

    async deletePaper(id) {
      await this.$confirm("Вы уверены?", "Подтвердите действие", {
        confirmButtonText: "Удалить",
        cancelButtonText: "Отменить",
        type: "warning",
      });

      try {
        await deleteDocument(id);
      } catch (error) {
        console.log("Failed to delete Paper: ", error);
        return;
      }

      this.documents = this.lodash.filter(this.documents, (paper) => paper.id !== id);

      this.$message({
        type: "success",
        message: "Удаление завершено",
      });
    },

    async fetchData() {
      if (this.documents.length < this.count || this.count === null) {
        this.loading = true;
        const authors = this.$route.query.author;
        const publishers = this.$route.query.publishers;
        const start_date = this.$route.query.start_date;
        const end_date = this.$route.query.end_date;
        const text = this.$route.query.text;
        const category = this.$route.query.category;

        try {
          const { data } = await getPapers(this.lodash.pickBy({
            category,
            authors,
            publishers,
            start_date,
            end_date,
            search: text,
            limit: this.limit,
            offset: this.documents.length,
            user: this.isMyDocuments ? this.userId : undefined
          }))

          this.documents = [...this.documents, ...data.results];
          this.count = data.count;
          this.loading = false;
        } catch (error) {
          console.log("Failed to fetch Papers: ", error);
        }
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "style";
</style>
