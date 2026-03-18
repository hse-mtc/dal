<template>
  <div class="card">
    <div class="preview" @click="$router.push(`/media-library/video/${data.id}/`)">
      <video
        :src="videoUrl"
        controls
        muted
        playsinline
        preload="metadata"
        @click.stop
      />
    </div>

    <div class="content">
      <div class="topRow">
        <div class="meta">
          <CustomText
            variant="header"
            class="title clickable"
            @click.native="$router.push(`/media-library/video/${data.id}/`)"
          >
            {{ data.title }}
          </CustomText>

          <CustomText variant="paragraph" :color="COLORS.gray_2" class="annotation">
            {{ data.annotation || "Описание пока не добавлено." }}
          </CustomText>
        </div>

        <div class="actions">
          <CustomText
            variant="paragraph"
            :color="COLORS.darkBlue"
            class="clickable action"
            @click.native="$router.push(`/media-library/video/${data.id}/`)"
          >
            Смотреть
          </CustomText>
          <a
            :href="videoUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="actionLink"
          >
            <CustomText variant="paragraph" :color="COLORS.darkBlue" class="action">
              Открыть файл
            </CustomText>
          </a>
          <AZGuard
            :permissions="['videos.patch.all', {
              codename: 'videos.patch.self',
              validator: () => userId === data.user_id,
            }]"
          >
            <CustomText
              variant="paragraph"
              :color="COLORS.darkBlue"
              class="clickable action"
              @click.native="onEdit"
            >
              Редактировать
            </CustomText>
          </AZGuard>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";
import { COLORS } from "@/utils/appConsts";
import { UserModule } from "@/store";

export default {
  name: "VideoCard",
  components: { CustomText },
  props: {
    data: { type: Object, required: true },
    onEdit: { type: Function, required: true },
  },
  data() {
    return {
      COLORS,
    };
  },
  computed: {
    userId() { return UserModule.userId; },
    videoUrl() {
      const content = this.data.file.content || "";
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
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.card {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: $xl;
  padding: $l;
  border: 1px solid #dde4ef;
  border-radius: 20px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  box-shadow: 0 16px 40px rgba(31, 57, 90, 0.08);
}

.preview {
  position: relative;
  width: 100%;
  min-width: 0;
  aspect-ratio: 16 / 9;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  background:
    radial-gradient(circle at top, rgba(73, 127, 255, 0.25), transparent 45%),
    linear-gradient(135deg, #101828 0%, #1d3557 100%);

  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.96;
  }
}

.content {
  width: 100%;
}

.topRow {
  display: flex;
  justify-content: space-between;
  gap: $xl;
}

.meta {
  min-width: 0;
}

.title {
  font-size: 34px;
  line-height: 1.05;
}

.annotation {
  margin-top: 14px;
  max-width: 760px;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 18px;
  margin-top: 18px;
  min-width: 220px;
}

.clickable {
  cursor: pointer;
}

.action {
  font-weight: 600;
}

.actionLink {
  text-decoration: none;
}

@media screen and (max-width: 992px) {
  .card {
    grid-template-columns: 1fr;
  }

  .topRow {
    flex-direction: column;
  }

  .title {
    font-size: 28px;
  }
}
</style>
