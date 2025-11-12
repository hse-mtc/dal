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
              <AZGuard :permissions="['papers.get.all']">
                <DownloadFile
                  v-if="$route.query.category !== 'bin'"
                  :url="document.file.content"
                  :file-name="document.file.name"
                  class="popover-action"
                >
                  Скачать
                </DownloadFile>
              </AZGuard>
              <AZGuard :permissions="['papers.patch.all']">
                <div
                  v-if="$route.query.category !== 'bin'"
                  class="popover-action"
                  @click="editPaper(document.id)"
                >
                  Редактировать
                </div>
              </AZGuard>
              <AZGuard :permissions="['papers.delete.all']">
                <div
                  v-if="$route.query.category !== 'bin'"
                  class="popover-action"
                  @click="toggleBinStatus(document.id, true)"
                >
                  Переместить в корзину
                </div>
              </AZGuard>
              <AZGuard :permissions="['papers.delete.all']">
                <div
                  v-if="$route.query.category === 'bin'"
                  class="popover-action"
                  @click="toggleBinStatus(document.id, false)"
                >
                  Восстановить
                </div>
              </AZGuard>
              <AZGuard :permissions="['papers.delete.all']">
                <div
                  v-if="$route.query.category === 'bin'"
                  class="popover-action"
                  @click="deletePaper(document.id)"
                >
                  Удалить
                </div>
              </AZGuard>
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

import * as message from "@/utils/message";

import { scrollMixin } from "@/mixins/scrollMixin";
import DownloadFile from "@/common/DownloadFile/index.vue";
import { surnameWithInitials } from "@/utils/person";
import { PapersModule, UserModule } from "@/store";
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
    userId() { return UserModule.userId; },
    authors() { return PapersModule.authors; },
    publishers() { return PapersModule.publishers; },
    categories() { return PapersModule.categories; },
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
      if (author) {
        return surnameWithInitials(author);
      }
      return "";
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
        this.$message.error(
          status
            ? "Не удалось переместить файл в корзину."
            : "Не удалось восстановить файл.",
        );
        console.error("Papers.Serp.toggleBinStatus: ", error);
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
        message.deleteError("статьи", error.response?.status);
        console.error("Papers.Serp.deletePaper: ", error);
        return;
      }

      this.removePaperFromList(id);

      this.$message({
        type: "success",
        message: "Статья удалена.",
      });
    },

    async fetchData() {
      if (!this.$route.query.category && !this.isMyDocuments) {
        return;
      }

      if (this.documents.length < this.count || this.count === null) {
        this.loading = true;

        try {
          const queryParams = {
            limit: this.limit,
            offset: this.documents.length,
            user: this.isMyDocuments ? this.userId : undefined,
            ...this.$route.query,
          };

          const categoryId = queryParams.category;
          const category = this.categories.find(cat => cat.id === categoryId);
          const extraFilters = [];

          if (category && category.filters && category.filters.properties) {
            Object.keys(queryParams).forEach(key => {
              if (key.startsWith("filter_")) {
                const filterName = key.replace("filter_", "");
                const value = queryParams[key];
                const filterDef = category.filters.properties[filterName];

                if (filterDef && value !== undefined && value !== null && value !== "") {
                  if (filterDef.type === "string") {
                    extraFilters.push(`contains|${filterName}|${value}`);
                  } else if (filterDef.type === "integer") {
                    extraFilters.push(`eq|${filterName}|${value}`);
                  } else {
                    extraFilters.push(`eq|${filterName}|${value}`);
                  }
                }
                delete queryParams[key];
              }
            });
          }

          if (extraFilters.length > 0) {
            queryParams.extra_filter = extraFilters.join(",");
          }

          const { data } = await getPapers(
            this.lodash.pickBy(queryParams),
          );

          this.documents = [...this.documents, ...data.results];
          this.count = data.count > 0 ? data.count : null;
          this.loading = false;
        } catch (error) {
          message.getError("статей", error.response?.status);
          console.error("Papers.Serp.fetchData: ", error);
        }
      }
    },
  },
};
</script>

<style scoped lang="scss">
@import "serp";
</style>
