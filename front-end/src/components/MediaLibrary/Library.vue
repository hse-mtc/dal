<template>
  <div class="root">
    <PageHeader
      title="Электронная медиатека"
      button="+ Добавить видео"
      :click="openCreateModal"
      :permissions="['books.post.self']"
    />

    <VideoModal
      v-if="showModal"
      :init-data="modalData"
      :is-changing="!!changingId"
      @close-modal="closeModal"
      @save="saveVideo"
    />

    <div class="toolbar">
      <div class="searchWrap">
        <SearchBar
          placeholder="Введите название видео"
          :search="searchVideos"
          :delete="clearSearch"
        />
      </div>

      <div class="toolbarMeta">
        <CustomText variant="paragraph">
          Найдено: {{ count || 0 }}
        </CustomText>
        <el-select v-model="sort" placeholder="Сортировка" class="sortSelect">
          <el-option
            v-for="item in sortTypes"
            :key="item.key"
            :label="item.label"
            :value="item.key"
          />
        </el-select>
      </div>
    </div>

    <div v-loading="loading" class="loader" />

    <div v-if="!loading && videos.length === 0" class="empty">
      <CustomText variant="header">
        Пока нет загруженных видео
      </CustomText>
      <CustomText variant="paragraph" :color="'#667085'">
        Добавь первый ролик, и он появится здесь отдельной карточкой.
      </CustomText>
    </div>

    <div v-for="item in videos" :key="item.id" class="listItem">
      <VideoCard :data="item" :on-edit="() => openEditModal(item)" />
    </div>
  </div>
</template>

<script>
import PageHeader from "@/common/PageHeader";
import SearchBar from "@/common/SearchBar";
import CustomText from "@/common/CustomText";
import { SIZES } from "@/utils/appConsts";
import {
  editVideo,
  getVideos,
  uploadVideo,
} from "@/api/videos";
import VideoCard from "@/components/MediaLibrary/VideoCard.vue";
import VideoModal from "@/components/MediaLibrary/VideoModal.vue";
import { UserModule } from "@/store";

const getInitialData = () => ({
  title: "",
  annotation: "",
  video: [],
});

export default {
  name: "MediaLibrary",
  components: {
    CustomText,
    SearchBar,
    PageHeader,
    VideoCard,
    VideoModal,
  },
  data() {
    return {
      SIZES,
      loading: false,
      videos: [],
      count: null,
      limit: 10,
      showModal: false,
      changingId: null,
      modalData: getInitialData(),
      sortTypes: [
        { key: "-upload_date", label: "По дате ↓" },
        { key: "upload_date", label: "По дате ↑" },
        { key: "title", label: "По названию ↑" },
        { key: "-title", label: "По названию ↓" },
      ],
    };
  },
  computed: {
    userId() { return UserModule.userId; },
    sort: {
      get() {
        return this.$route.query.sort || "-upload_date";
      },
      set(value) {
        this.$router.push({ query: { ...this.$route.query, sort: value } });
      },
    },
    search: {
      get() {
        return this.$route.query.search || "";
      },
      set(value) {
        this.$router.push({ query: { ...this.$route.query, search: value } });
      },
    },
  },
  watch: {
    $route() {
      this.videos = [];
      this.count = null;
      this.fetchData();
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    getInitialData,
    async fetchData() {
      if (this.loading) {
        return;
      }

      if (this.videos.length >= this.count && this.count !== null) {
        return;
      }

      this.loading = true;
      try {
        const { data } = await getVideos(this.lodash.pickBy({
          ordering: this.sort,
          search: this.search,
          limit: this.limit,
          offset: this.videos.length,
        }));
        this.count = data.count;
        this.videos = [...this.videos, ...data.results];
      } finally {
        this.loading = false;
      }
    },
    searchVideos(value) {
      this.search = value;
    },
    clearSearch() {
      this.search = "";
    },
    openCreateModal() {
      this.changingId = null;
      this.modalData = getInitialData();
      this.showModal = true;
    },
    openEditModal(video) {
      this.changingId = video.id;
      this.modalData = {
        title: video.title,
        annotation: video.annotation,
        video: video.file?.content
          ? [{ name: video.file.name, url: `/media/${video.file.content}` }]
          : [],
      };
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    createPayload(values) {
      const payload = new FormData();
      payload.append("data", JSON.stringify({
        title: values.title,
        annotation: values.annotation,
        user: this.userId,
      }));
      if (values.video?.[0]?.raw) {
        payload.append("content", values.video[0].raw);
      }
      return payload;
    },
    async saveVideo(values) {
      const payload = this.createPayload(values);
      if (this.changingId) {
        await editVideo(this.changingId, payload);
      } else {
        await uploadVideo(payload);
      }
      this.closeModal();
      this.videos = [];
      this.count = null;
      this.fetchData();
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.root {
}

.hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 28px;
}

.heroTitle {
  margin-bottom: 10px;
}

.heroText {
  max-width: 760px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-end;
  margin-bottom: 24px;
}

.searchWrap {
  flex: 1;
}

.toolbarMeta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.sortSelect {
  width: 220px;
}

.loader {
  min-height: 24px;
}

.listItem + .listItem {
  margin-top: 18px;
}

.empty {
  padding: 48px 32px;
  border: 1px dashed #cbd5e1;
  border-radius: 20px;
  background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
}

@media screen and (max-width: 992px) {
  .hero,
  .toolbar,
  .toolbarMeta {
    flex-direction: column;
    align-items: stretch;
  }

  .sortSelect {
    width: 100%;
  }
}
</style>
