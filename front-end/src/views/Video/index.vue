<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <div v-loading="loading" class="wrapper">
        <template v-if="video">
          <div class="backLink" @click="$router.push('/media-library/')">
            <img src="@/assets/icons/arrow-back.svg" alt="">
            <CustomText variant="label-1" :color="'#667085'">
              Все видео
            </CustomText>
          </div>

          <div class="hero">
            <div>
              <CustomText variant="page-header-1" :mb="SIZES.s" class="title">
                {{ video.title }}
              </CustomText>
              <CustomText variant="paragraph" :color="'#667085'">
                Если встроенный плеер не воспроизводит ролик, откройте файл напрямую в новой вкладке.
              </CustomText>
            </div>

            <a
              :href="videoUrl"
              target="_blank"
              rel="noopener noreferrer"
              class="actionLink"
            >
              <CtaButton background="#fff" color="#0f62fe" border="1px solid #bcd1ff">
                Открыть файл
              </CtaButton>
            </a>
          </div>

          <div class="playerCard">
            <video
              class="player"
              controls
              playsinline
              preload="metadata"
            >
              <source :src="videoUrl" :type="videoMimeType">
              Ваш браузер не смог воспроизвести видео.
            </video>
          </div>

          <div class="infoGrid">
            <div class="infoCard">
              <CustomText variant="header" :mb="SIZES.s">
                О видео
              </CustomText>
              <CustomText variant="paragraph">
                {{ video.annotation || "Описание пока не добавлено." }}
              </CustomText>
            </div>

            <div class="infoCard">
              <CustomText variant="header" :mb="SIZES.s">
                Файл
              </CustomText>
              <CustomText variant="paragraph" :color="'#667085'">
                {{ video.file.name }}
              </CustomText>
            </div>
          </div>
        </template>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CustomText from "@/common/CustomText";
import CtaButton from "@/common/CtaButton";
import { COLORS, SIZES } from "@/utils/appConsts";
import { getVideo } from "@/api/videos";

export default {
  name: "VideoView",
  components: { CtaButton, CustomText },
  data() {
    return {
      COLORS,
      SIZES,
      loading: true,
      video: null,
    };
  },
  computed: {
    videoUrl() {
      const content = this.video?.file?.content || "";
      if (!content) {
        return "";
      }
      if (content.startsWith("http://") || content.startsWith("https://")) {
        return content;
      }
      if (content.startsWith("/")) {
        return `${window.location.origin}${content}`;
      }
      return `${window.location.origin}/media/${content}`;
    },
    videoMimeType() {
      const name = this.video?.file?.name || "";
      const ext = name.split(".").pop()?.toLowerCase();
      const types = {
        mp4: "video/mp4",
        webm: "video/webm",
        mov: "video/quicktime",
        avi: "video/x-msvideo",
        mkv: "video/x-matroska",
      };
      return types[ext] || "video/mp4";
    },
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const { data } = await getVideo(this.$route.params.id);
      this.video = data;
      this.loading = false;
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.wrapper {
  min-height: 50vh;
  padding: 24px 0 56px;
}

.player {
  width: 100%;
  max-height: 72vh;
  background: #111827;
  border-radius: 18px;
}

.backLink {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  margin-bottom: 28px;
}

.hero {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  align-items: flex-start;
  margin-bottom: 24px;
}

.playerCard {
  padding: 20px;
  border-radius: 24px;
  background:
    radial-gradient(circle at top, rgba(87, 143, 255, 0.18), transparent 32%),
    linear-gradient(180deg, #0c1424 0%, #101828 100%);
  box-shadow: 0 24px 60px rgba(16, 24, 40, 0.2);
}

.infoGrid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 18px;
  margin-top: 22px;
}

.infoCard {
  padding: 22px;
  border-radius: 18px;
  border: 1px solid #e5ebf3;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.actionLink {
  text-decoration: none;
}

@media screen and (max-width: 992px) {
  .hero,
  .infoGrid {
    grid-template-columns: 1fr;
    flex-direction: column;
  }
}
</style>
