<template>
  <div class="wrapper">
    <div
        :id="`loader__${data.id}`"
        class="file-img"
        @click="$router.push(`/library/book/${data.id}`)"
    >
      <div class="lds-dual-ring"/>
      <img
          class="file-image"
          :src="
          data.cover
            ? data.cover.image
            : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/387928/book%20placeholder.png'
        "
          alt=""
      />
    </div>
    <div class="content">

      <div class="header">
        <div @click="$router.push(`/library/book/${data.id}`)">
          <CustomText style="cursor: pointer" variant="header">{{
              data.title
            }}
          </CustomText>
        </div>
        <img v-if="data.favorite" @click="unsaveBook" src="@/assets/icons/saved.svg" alt=""/>
        <img v-else @click="saveBook" src="@/assets/icons/not-saved.svg" alt=""/>
      </div>
      <div @click="$router.push(`/library/book/${data.id}`)" style="width: 100%">
        <CustomText
            style="cursor: pointer"
            variant="sub-header"
            :color="COLORS.gray_2"
            :mt="SIZES.s"
            :mb="SIZES.m"
        >
          <template v-for="item in data.authors">
            {{getAuthor(item)}},
          </template>
          {{ data.publication_year }} г.
        </CustomText>
        <CustomText
            style="cursor: pointer"
            variant="paragraph"
            :color="COLORS.black_2"
            class="annotation"
        >
          {{ data.annotation }}
        </CustomText>
      </div>
      <div class="buttons">
        <DownloadFile
            :url="data.file.content"
            :fileName="data.file.name"
        >
          <CustomText :mt="SIZES.m" :color="COLORS.darkBlue" variant="paragraph">
            Скачать
          </CustomText>
        </DownloadFile>
        <div class="button" @click="onEdit">
          <CustomText :mt="SIZES.m" :color="COLORS.darkBlue" variant="paragraph">
            Редактировать
          </CustomText>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CustomText from "@/common/CustomText";
import DownloadFile from '@/common/DownloadFile/index.vue'
import {COLORS, SIZES} from "@/utils/appConsts";
import {saveFavBook, unsaveFavBook} from "@/api/books";
import {mapState} from "vuex";

export default {
  name: "Book",
  components: {CustomText, DownloadFile},
  props: {
    data: {
      type: Object,
      required: true
    },
    onEdit: {type: Function}
  },
  data() {
    return {
      SIZES,
      COLORS,
      loading: false,
    };
  },
  computed: {
    ...mapState({
      authors: (state) => state.documents.authors,
    }),
  },
  methods: {
    getAuthor(id) {
      const author = this.authors.find(author => author.id === id)
      return `${author.surname} ${author.name[0]}. ${author.patronymic[0]}.`
    },
    saveBook() {
      saveFavBook({book: this.data.id}).then(() => {
        this.data.favorite = true
      })
    },
    unsaveBook() {
      unsaveFavBook(this.data.id).then(() => {
        this.data.favorite = false
        this.$emit("deleteFavBook", this.data.id);
      })
    }
  }
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.wrapper {
  padding-top: $m;
  padding-bottom: $m;
  display: flex;
  align-items: flex-start;
}

.content {
  width: 100%;
}

.header {
  img {
    cursor: pointer;
  }
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.file-img {
  cursor: pointer;
  border-radius: $s;
  margin-right: $xl;

  .lds-dual-ring {
    display: none;
    width: 120px;
    height: 170px;
  }

  .lds-dual-ring:after {
    content: " ";
    display: block;
    width: 64px;
    height: 64px;
    margin: 8px;
    border-radius: 50%;
    border: 6px solid #0686fe;
    border-color: #0686fe transparent #0686fe transparent;
    animation: lds-dual-ring 1.2s linear infinite;
  }

  @keyframes lds-dual-ring {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
}

.file-image {
  width: 120px;
  height: 170px;
  border-radius: $s;
  object-fit: cover;
}

.annotation {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
}

.loading {
  .lds-dual-ring {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .file-image {
    display: none;
  }
}

.buttons {
  display: flex;

  .button {
    cursor: pointer;
    margin-left: 20px;
  }
}
</style>
