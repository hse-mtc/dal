<template>
  <span
    v-if="canPreview"
    :class="$style.trigger"
    @click.stop="open"
  >
    <slot>Предпросмотр</slot>

    <el-dialog
      :visible.sync="visible"
      :title="file.name"
      width="90%"
      top="3vh"
      append-to-body
      :close-on-click-modal="false"
      @closed="onClosed"
      @click.native.stop
    >
      <div
        v-loading="loading"
        :class="$style.viewer"
      >
        <img
          v-if="visible && file.preview_kind === 'image'"
          :src="file.preview_url"
          :alt="file.name"
          :class="$style.image"
          @load="onLoaded"
          @error="onError"
        >

        <video
          v-else-if="visible && file.preview_kind === 'video'"
          :src="file.preview_url"
          :class="$style.video"
          controls
          playsinline
          preload="metadata"
          @loadedmetadata="onLoaded"
          @error="onError"
        >
          Ваш браузер не смог воспроизвести видео.
        </video>

        <audio
          v-else-if="visible && file.preview_kind === 'audio'"
          :src="file.preview_url"
          :class="$style.audio"
          controls
          preload="metadata"
          @loadedmetadata="onLoaded"
          @error="onError"
        >
          Ваш браузер не смог воспроизвести аудио.
        </audio>

        <iframe
          v-else-if="visible"
          :src="file.preview_url"
          :title="`Предпросмотр ${file.name}`"
          :class="$style.frame"
          @load="onLoaded"
        />

        <el-alert
          v-if="error"
          title="Не удалось открыть предпросмотр. Файл можно скачать и открыть на устройстве."
          type="warning"
          :closable="false"
          show-icon
        />
      </div>

      <span slot="footer" :class="$style.footer">
        <DownloadFile
          :url="file.content"
          :file-name="file.name"
        >
          <el-button type="primary" icon="el-icon-download">
            Скачать файл
          </el-button>
        </DownloadFile>
      </span>
    </el-dialog>
  </span>
</template>

<script>
import DownloadFile from "@/common/DownloadFile";

export default {
  name: "FilePreview",
  components: { DownloadFile },
  props: {
    file: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      error: false,
      loading: true,
      visible: false,
    };
  },
  computed: {
    canPreview() {
      return Boolean(this.file.preview_url && this.file.preview_kind);
    },
  },
  methods: {
    open() {
      this.error = false;
      this.loading = true;
      this.visible = true;
    },
    onLoaded() {
      this.loading = false;
    },
    onError() {
      this.loading = false;
      this.error = true;
    },
    onClosed() {
      this.error = false;
      this.loading = true;
    },
  },
};
</script>

<style lang="scss" module>
.trigger {
  display: inline-block;
  cursor: pointer;
}

.viewer {
  display: flex;
  min-height: 65vh;
  align-items: center;
  justify-content: center;
  overflow: auto;
  background: #f5f7fa;
  border-radius: 8px;
}

.frame {
  width: 100%;
  height: 75vh;
  border: 0;
  background: #fff;
}

.image {
  display: block;
  max-width: 100%;
  max-height: 75vh;
  object-fit: contain;
}

.video {
  width: 100%;
  max-height: 75vh;
  background: #111827;
}

.audio {
  width: min(720px, 90%);
}

.footer {
  display: flex;
  justify-content: flex-end;
}
</style>
