<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <div class="book-header" @click="$router.go(-1)">
        <img src="@/assets/icons/arrow-back.svg" alt="">
        <CustomText variant="label-1" :color="COLORS.gray_2">Все учебники</CustomText>
      </div>
      <div class="my-loading" v-loading="loading">
        <div class="wrapper" v-if="book">
          <div :id="`loader__${book.id}`" class="file-img">
            <div class="lds-dual-ring" />
            <img class="file-image" :src="book.cover ? book.cover.image : 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/387928/book%20placeholder.png'" alt="">
          </div>
          <div class="content">
            <CustomText variant="page-header-1" :mb="SIZES.m">{{book.title}}</CustomText>
            <CustomText :custom-style="{fontWeight: 'normal'}" variant="header" :color="COLORS.gray_2" v-for="item in book.authors" :key="item.id" >
              {{item.surname}} {{item.name}} {{item.patronymic}}
            </CustomText>
            <div class="additional-info">

              <CustomText :custom-style="{fontWeight: 'normal'}" variant="header">{{book.publishers[0].name}}</CustomText>
              <template v-if="book.pagesCount">
                <img src="@/assets/icons/dot.svg" alt="">
                <CustomText :custom-style="{fontWeight: 'normal'}" variant="header">{{book.pagesCount}} печат. страниц</CustomText>
              </template>
              <template v-if="book.publication_year">
                <img src="@/assets/icons/dot.svg" alt="">
                <CustomText :custom-style="{fontWeight: 'normal'}" variant="header">{{book.publication_year}} г.</CustomText>
              </template>
            </div>

            <div class="cta" @click.prevent="downloadFile(book.file, book.id)">
              Скачать
            </div>

            <CustomText variant="header" :mt="SIZES.xxxl" :mb="SIZES.m">О книге</CustomText>
            <CustomText variant="paragraph">{{book.annotation}}</CustomText>

            <CustomText variant="header" :mt="SIZES.xxxl" :mb="SIZES.m">Предметы</CustomText>
            <div class="subjects">
              <div class="subject" v-for="item in book.subjects" :key="item.id">
                <CustomText variant="label-1" :color="COLORS.gray_4">{{item.title}}</CustomText>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>


import CustomText from "@/common/CustomText";
import {COLORS, SIZES} from "@/utils/appConsts";
import {getBook} from "@/api/books";
import axios from "axios";

export default {
  name: "Book",
  components: {CustomText},
  computed: {},
  created() {
    this.fetchData()
  },
  data() {
    return {
      SIZES,
      COLORS,
      book: null,
      loading: true
    }
  },
  methods: {
    fetchData() {
      this.loading = true
      getBook(this.$route.params.id)
          .then(res => {
            console.log('[BOOK]: ', res.data)
            this.book = res.data
            this.loading = false
          })
    },
    async downloadFile(file, id) {
      document.getElementById(`loader__${id}`).classList.add('loading')
      let data;
      try {
        ({ data } = await axios.get(file.content, { responseType: "blob" }));
      } catch (error) {
        console.log("Failed to download Book.file: ", error);
        document.getElementById(`loader__${id}`).classList.remove('loading')
        return;
      }

      const create = document.createElement.bind(document);
      const link = create("a");

      const blob = new Blob([data]);
      link.href = URL.createObjectURL(blob);
      link.download = file.name;

      link.click();
      URL.revokeObjectURL(link.href);
      document.getElementById(`loader__${id}`).classList.remove('loading')
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.book-header {
  cursor: pointer;
  padding-top: $xl;
  padding-bottom: $xl;
  display: flex;
  align-items: center;

  img {
    margin-right: $s;
  }
}

.wrapper {
  display: flex;
}

.my-loading {
  min-height: 50vh;

}

.content {
  padding-top: $l;
}

.additional-info {
  margin-top: $l;
  margin-bottom: $l;
  display: flex;
  img {
    margin-right: $l;
    margin-left: $l;
  }
}

.file-image {
  width: 179px;
  height: 254px;
  border-radius: $s;
  margin-right: $xxl;
  object-fit: cover;
}

.file-img {
  cursor: pointer;
  border-radius: $s;
  margin-right: $xl;

  .lds-dual-ring {
    display: none;
    width: 179px;
    height: 254px;
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

.loading {
  .lds-dual-ring {
    margin-right: $xl;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .file-image {
    display: none;
  }
}

.cta {
  cursor: pointer;
  color: white;
  width: max-content;
  background: $darkBlue;
  border-radius: $xs;
  padding: 14px 51px;
}

.subjects {
  display: flex;
  align-items: center;
}

.subject {
  background: $lightGray;
  border-radius: $xs;
  padding: 6px 8px;
  margin-right: $m;;
}
</style>
