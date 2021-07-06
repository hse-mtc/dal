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
        class="document-card"
      >
        <div
          v-if="yearChanged(index)"
          class="cool-hr d-flex align-items-center"
        >
          <hr class="mr-3">
          {{ year(document) }}
          <hr class="ml-3">
        </div>

        <el-col :span="23">
          <div class="d-flex">
            <div>
              {{ document.publication_date | moment }}
            </div>

            <div class="ml-5" style="color: #76767a">
              {{ publisherNames(document.publishers) }}
            </div>
          </div>

          <div class="document-card-title">
            {{ document.title }}
          </div>

          <div
            class="document-card-authors"
          >
            <template v-for="(author, authorIndex) in document.authors">
              <span
                v-if="getAuthor(author)"
                :key="author"
              >
                {{ `${authorIndex > 0 ? ', ' : ''} ${getAuthor(author)}` }}
              </span>
            </template>
          </div>

          <div class="document-card-annotation">
            {{ document.annotation }}
          </div>

          <div class="document-card-tags">
            <el-tag
              v-for="(tag, tagIndex) in document.tags"
              :key="tagIndex"
              class="document-card-tag"
            >
              {{ tag }}
            </el-tag>
          </div>
        </el-col>

        <el-col :span="1" class="d-flex justify-content-end mt-4">
          <el-popover placement="bottom" trigger="hover">
            <div
              style="text-align: center; margin: 0; padding: 0; font-size: 15px"
            >
              <DownloadFile
                v-if="$route.query.category !== 'bin'"
                :url="document.file.content"
                :file-name="document.file.name"
              >
                Скачать
              </DownloadFile>
              <div v-if="$route.query.category !== 'bin'" style="cursor: pointer" @click="editPaper(document.id)">
                Редактировать
              </div>
              <div
                v-if="$route.query.category !== 'bin'"
                style="cursor: pointer"
                @click="toggleBinStatus(document.id, true)"
              >
                Переместить в корзину
              </div>
              <div
                v-if="$route.query.category === 'bin'"
                style="cursor: pointer"
                @click="toggleBinStatus(document.id, false)"
              >
                Восстановить
              </div>
              <div v-if="$route.query.category === 'bin'" style="cursor: pointer" @click="deletePaper(document.id)">
                Удалить
              </div>
            </div>

            <div
              slot="reference"
              class="d-flex justify-content-center"
              style="width: 10px; cursor: pointer"
            >
              <img src="../../assets/scienceWorks/popover.svg" alt="">
            </div>
          </el-popover>
        </el-col>
      </el-row>
    </div>
    <div v-else-if="!loading" class="my-document">
      Документы не найдены
    </div>
    <div v-loading="loading" class="requests__loader" />
  </div>
</template>

<script>
import moment from "moment";

import { getPapers, patchPaper } from "@/api/papers";
import { deleteDocument } from "@/api/delete";

import { scrollMixin } from "@/mixins/scrollMixin";
import DownloadFile from "@/common/DownloadFile/index.vue";
import { surnameWithInitials } from "@/utils/person";
import { AppModule, PapersModule } from "@/store";
import EventBus from "../EventBus";

export default {
  name: "PaperSerp",
  components: { DownloadFile },
  filters: {
    moment(date) {
      return moment(date).format("DD MMMM YYYY");
    },
  },
  mixins: [scrollMixin],
  props: {
    isMyDocuments: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      count: null,
      limit: 10,
      loading: false,
      documents: [],
      paperToEdit: {},
    };
  },
  computed: {
    userId() { return AppModule.userId; },
    authors() { return PapersModule.authors; },
    publishers() { return PapersModule.publishers; },
  },
  watch: {
    $route() {
      this.count = null;
      this.documents = [];
      this.fetchData();
    },
  },
  async mounted() {
    await this.fetchData();
    EventBus.$on("UPDATE_EVENT", () => {
      this.documents = [];
      this.fetchData();
    });
  },
  methods: {
    moment,
    getAuthor(id) {
      const author = this.authors.find(item => item.id === id);
      if (!author) return "";

      return surnameWithInitials(author);
    },
    publisherNames(ids) {
      return this.publishers
        .filter(p => ids.includes(p.id))
        .map(p => p.name)
        .join(", ");
    },
    loadMore() {
      if (!this.loading) {
        this.fetchData();
      }
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

    async toggleBinStatus(id, status) {
      try {
        const data = { is_binned: status };
        const formData = new FormData();
        formData.set("data", JSON.stringify(data));
        await patchPaper(id, formData);
        this.removePaperFromList(id);
        this.$message({
          type: "success",
          message: status
            ? "Документ перемещен в корзину"
            : "Документ восстановлен",
        });
      } catch (error) {
        console.log("[ERROR]: ", error);
        this.$message({
          type: "error",
          message: status
            ? "Не удалось переместить файл в корзину"
            : "Не удалось восстановить файл",
        });
      }
    },

    removePaperFromList(id) {
      this.documents = this.lodash.filter(
        this.documents,
        paper => paper.id !== id,
      );
      this.count -= 1;
    },

    editPaper(id) {
      const paperToEdit = this.documents.find(paper => paper.id === id);
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
        // TODO(TmLev): better error handling.
        console.log("Failed to delete Paper: ", error);
        return;
      }

      this.removePaperFromList(id);

      this.$message({
        type: "success",
        message: "Удаление завершено",
      });
    },

    async fetchData() {
      if (!this.$route.query.category && !this.isMyDocuments) {
        return;
      }

      if (this.documents.length < this.count || this.count === null) {
        this.loading = true;

        try {
          const { data } = await getPapers(
            this.lodash.pickBy({
              limit: this.limit,
              offset: this.documents.length,
              user: this.isMyDocuments ? this.userId : undefined,
              ...this.$route.query,
            }),
          );

          this.documents = [...this.documents, ...data.results];
          this.count = data.count > 0 ? data.count : null;
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
@import "serp";
</style>
