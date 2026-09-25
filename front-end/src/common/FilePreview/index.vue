<template>
  <span
    v-if="canPreview"
    :class="$style.trigger"
    @click.stop="open"
  >
    <slot>Показать</slot>

    <el-dialog
      ref="dialog"
      :visible.sync="visible"
      :title="file.name"
      custom-class="file-preview-dialog"
      fullscreen
      append-to-body
      :close-on-click-modal="false"
      @closed="onClosed"
      @click.native.stop
    >
      <div
        v-loading="loading"
        :class="$style.viewer"
      >
        <div
          v-if="visible && isPresentation"
          :class="$style.presentation"
        >
          <img
            v-if="slideUrl"
            :src="slideUrl"
            :alt="`${file.name}, слайд ${currentPage}`"
            :class="$style.slide"
            @load="onLoaded"
            @error="onError"
          >

          <el-button
            :class="[$style.slideArrow, $style.slideArrowLeft]"
            :disabled="loading || currentPage <= 1"
            icon="el-icon-arrow-left"
            circle
            aria-label="Предыдущий слайд"
            @click="previousSlide"
          />
          <el-button
            :class="[$style.slideArrow, $style.slideArrowRight]"
            :disabled="loading || (pageCount > 0 && currentPage >= pageCount)"
            icon="el-icon-arrow-right"
            circle
            aria-label="Следующий слайд"
            @click="nextSlide"
          />
        </div>

        <img
          v-else-if="visible && file.preview_kind === 'image'"
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
          :class="$style.errorAlert"
          title="Не удалось открыть предпросмотр. Файл можно скачать и открыть на устройстве."
          type="warning"
          :closable="false"
          show-icon
        />
      </div>

      <span slot="footer" :class="$style.footer">
        <span v-if="isPresentation" :class="$style.navigation">
          <el-button
            icon="el-icon-arrow-left"
            :disabled="loading || currentPage <= 1"
            @click="previousSlide"
          >
            Назад
          </el-button>
          <strong :class="$style.pageCounter">
            {{ currentPage }} / {{ pageCount || "…" }}
          </strong>
          <el-button
            :disabled="loading || (pageCount > 0 && currentPage >= pageCount)"
            @click="nextSlide"
          >
            Вперёд
            <i class="el-icon-arrow-right el-icon-right" />
          </el-button>
          <span :class="$style.keyboardHint">Можно использовать клавиши ← →</span>
        </span>

        <span :class="$style.footerActions">
          <el-button
            v-if="browserFullscreenSupported"
            icon="el-icon-full-screen"
            @click="toggleBrowserFullscreen"
          >
            {{ nativeFullscreen ? "Выйти из полного экрана" : "Во весь экран" }}
          </el-button>

          <DownloadFile
            :url="file.content"
            :file-name="file.name"
          >
            <el-button type="primary" icon="el-icon-download">
              Скачать файл
            </el-button>
          </DownloadFile>
        </span>
      </span>
    </el-dialog>
  </span>
</template>

<script>
import axios from "axios";

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
      currentPage: 1,
      error: false,
      loading: true,
      nativeFullscreen: false,
      pageCount: 0,
      slideRequestId: 0,
      slideUrl: "",
      visible: false,
    };
  },
  computed: {
    browserFullscreenSupported() {
      return Boolean(document.fullscreenEnabled || document.webkitFullscreenEnabled);
    },
    canPreview() {
      return Boolean(this.file.preview_url && this.file.preview_kind);
    },
    isPresentation() {
      return this.file.preview_kind === "presentation";
    },
  },
  mounted() {
    document.addEventListener("fullscreenchange", this.onFullscreenChange);
    document.addEventListener("webkitfullscreenchange", this.onFullscreenChange);
  },
  beforeDestroy() {
    this.exitBrowserFullscreen();
    this.unbindKeyboard();
    this.releaseSlideUrl();
    document.removeEventListener("fullscreenchange", this.onFullscreenChange);
    document.removeEventListener("webkitfullscreenchange", this.onFullscreenChange);
  },
  methods: {
    open() {
      this.error = false;
      this.loading = true;
      this.visible = true;
      this.bindKeyboard();
      if (this.isPresentation) {
        this.loadSlide(1);
      }
    },
    async loadSlide(pageNumber) {
      if (pageNumber < 1 || (this.pageCount && pageNumber > this.pageCount)) {
        return;
      }

      const requestId = this.slideRequestId + 1;
      this.slideRequestId = requestId;
      this.error = false;
      this.loading = true;

      try {
        const response = await axios.get(
          `${this.file.preview_url}&page=${pageNumber}`,
          {
            responseType: "blob",
            timeout: 65000,
          },
        );
        if (requestId !== this.slideRequestId) {
          return;
        }

        const nextSlideUrl = URL.createObjectURL(response.data);
        this.releaseSlideUrl();
        this.slideUrl = nextSlideUrl;
        this.currentPage = pageNumber;
        this.pageCount = Number(response.headers["x-preview-page-count"]) || 0;
      } catch (error) {
        if (requestId === this.slideRequestId) {
          this.onError();
        }
      }
    },
    previousSlide() {
      if (!this.loading) {
        this.loadSlide(this.currentPage - 1);
      }
    },
    nextSlide() {
      if (!this.loading) {
        this.loadSlide(this.currentPage + 1);
      }
    },
    handleKeydown(event) {
      if (!this.visible || !this.isPresentation) {
        return;
      }

      if (["ArrowLeft", "PageUp"].includes(event.key)) {
        event.preventDefault();
        this.previousSlide();
      } else if (["ArrowRight", "PageDown", " "].includes(event.key)) {
        event.preventDefault();
        this.nextSlide();
      } else if (event.key === "Home") {
        event.preventDefault();
        this.loadSlide(1);
      } else if (event.key === "End" && this.pageCount) {
        event.preventDefault();
        this.loadSlide(this.pageCount);
      }
    },
    bindKeyboard() {
      window.addEventListener("keydown", this.handleKeydown);
    },
    unbindKeyboard() {
      window.removeEventListener("keydown", this.handleKeydown);
    },
    releaseSlideUrl() {
      if (this.slideUrl) {
        URL.revokeObjectURL(this.slideUrl);
        this.slideUrl = "";
      }
    },
    toggleBrowserFullscreen() {
      const fullscreenElement = document.fullscreenElement
        || document.webkitFullscreenElement;
      if (fullscreenElement) {
        const exitFullscreen = document.exitFullscreen
          || document.webkitExitFullscreen;
        if (exitFullscreen) {
          exitFullscreen.call(document);
        }
        return;
      }

      const dialog = this.$refs.dialog.$el.querySelector(".el-dialog");
      const requestFullscreen = dialog.requestFullscreen
        || dialog.webkitRequestFullscreen;
      if (requestFullscreen) {
        requestFullscreen.call(dialog);
      }
    },
    exitBrowserFullscreen() {
      const fullscreenElement = document.fullscreenElement
        || document.webkitFullscreenElement;
      const dialogRoot = this.$refs.dialog && this.$refs.dialog.$el;
      if (
        !fullscreenElement
        || !dialogRoot
        || !dialogRoot.contains(fullscreenElement)
      ) {
        return;
      }

      const exitFullscreen = document.exitFullscreen
        || document.webkitExitFullscreen;
      if (exitFullscreen) {
        exitFullscreen.call(document);
      }
    },
    onFullscreenChange() {
      this.nativeFullscreen = Boolean(
        document.fullscreenElement || document.webkitFullscreenElement,
      );
    },
    onLoaded() {
      this.loading = false;
    },
    onError() {
      this.loading = false;
      this.error = true;
    },
    onClosed() {
      this.exitBrowserFullscreen();
      this.slideRequestId += 1;
      this.unbindKeyboard();
      this.releaseSlideUrl();
      this.currentPage = 1;
      this.pageCount = 0;
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
  position: relative;
  display: flex;
  height: 100%;
  min-height: 0;
  align-items: center;
  justify-content: center;
  overflow: auto;
  background: #f5f7fa;
  border-radius: 8px;
}

.errorAlert {
  position: absolute;
  top: 20px;
  left: 50%;
  z-index: 5;
  width: calc(100% - 40px);
  max-width: 720px;
  transform: translateX(-50%);
}

.frame {
  width: 100%;
  height: 100%;
  border: 0;
  background: #fff;
}

.image {
  display: block;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.video {
  width: 100%;
  max-height: 100%;
  background: #111827;
}

.audio {
  width: min(720px, 90%);
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.footerActions,
.navigation {
  display: flex;
  align-items: center;
  gap: 12px;
}

.footerActions {
  margin-left: auto;
}

.pageCounter {
  min-width: 72px;
  text-align: center;
}

.keyboardHint {
  margin-left: 8px;
  color: #909399;
  font-size: 13px;
}

.presentation {
  position: relative;
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  background: #111827;
}

.slide {
  display: block;
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.35);
}

.slideArrow {
  position: absolute;
  top: 50%;
  z-index: 2;
  width: 48px;
  height: 48px;
  border: 0;
  background: rgba(255, 255, 255, 0.9);
  transform: translateY(-50%);
}

.slideArrowLeft {
  left: 20px;
}

.slideArrowRight {
  right: 20px;
}

:global(.file-preview-dialog) {
  display: flex;
  height: 100%;
  flex-direction: column;
  overflow: hidden;
  background: #fff;
}

:global(.file-preview-dialog .el-dialog__body) {
  min-height: 0;
  flex: 1;
  padding: 0 20px;
  overflow: hidden;
}

:global(.file-preview-dialog .el-dialog__footer) {
  padding: 12px 20px;
}

@media (max-width: 900px) {
  .keyboardHint {
    display: none;
  }

  .footer {
    align-items: stretch;
    flex-direction: column;
  }

  .footerActions {
    margin-left: 0;
    justify-content: flex-end;
  }
}
</style>
