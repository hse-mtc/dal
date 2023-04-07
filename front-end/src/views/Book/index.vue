<template>
  <el-row>
    <el-col :span="20" :offset="2">
      <div class="book-header" @click="$router.push(`${prevRoute.path}`)">
        <img src="@/assets/icons/arrow-back.svg" alt="">
        <CustomText
          variant="label-1"
          :color="COLORS.gray_2"
        >
          Все учебники
        </CustomText>
      </div>
      <div v-loading="loading" class="my-loading">
        <div v-if="book" class="wrapper">
          <div :id="`loader__${book.id}`" class="file-img">
            <div class="lds-dual-ring" />
            <img
              class="file-image"
              :src="
                book.cover
                  ? 'media/' + book.cover.image
                  : require('@/assets/icons/book-cover-placeholder.png')
              "
              alt=""
            >
          </div>
          <div class="content">
            <div class="content-title">
              <CustomText
                variant="page-header-1"
                :mb="SIZES.m"
              >
                {{ book.title }}
              </CustomText>
              <AZGuard
                :permissions="['books.delete.all', {
                  codename: 'books.delete.self',
                  validator: () => userId === book.user_id,
                }]"
              >
                <CtaButton
                  background="#fff"
                  color="#0061D9"
                  border="1px solid #0061D9"
                  @click="handleDelete"
                >
                  <div style="display: flex; align-items: center">
                    <svg-icon
                      icon-class="close"
                      style="font-size: 24px; margin-right: 8px"
                      @click="deleteSection"
                    />

                    Удалить
                  </div>
                </CtaButton>
              </AZGuard>
            </div>
            <CustomText
              v-for="authorId in book.authors"
              :key="authorId"
              :custom-style="{ fontWeight: 'normal' }"
              variant="header"
              :color="COLORS.gray_2"
            >
              {{
                surnameWithInitials(authors.filter((a) => a.id === authorId)[0])
              }}
            </CustomText>
            <div class="additional-info">
              <CustomText
                :custom-style="{ fontWeight: 'normal' }"
                variant="header"
              >
                {{
                  publishers.filter((p) => p.id === book.publishers[0])[0].name
                }}
              </CustomText>
              <template v-if="book.page_count">
                <img src="@/assets/icons/dot.svg" alt="">
                <CustomText
                  :custom-style="{ fontWeight: 'normal' }"
                  variant="header"
                >
                  {{ book.page_count }} печат. страниц
                </CustomText>
              </template>
              <template v-if="book.publication_year">
                <img src="@/assets/icons/dot.svg" alt="">
                <CustomText
                  :custom-style="{ fontWeight: 'normal' }"
                  variant="header"
                >
                  {{ book.publication_year }} г.
                </CustomText>
              </template>
            </div>

            <DownloadFile
              class="cta"
              :url="book.file.content"
              :file-name="book.file.name"
            >
              Скачать
            </DownloadFile>

            <CustomText
              variant="header"
              :mt="SIZES.xxxl"
              :mb="SIZES.m"
            >
              О книге
            </CustomText>
            <CustomText variant="paragraph">
              {{ book.annotation }}
            </CustomText>

            <CustomText
              variant="header"
              :mt="SIZES.xxxl"
              :mb="SIZES.m"
            >
              Предметы
            </CustomText>
            <div class="subjects">
              <div
                v-for="subjectId in book.subjects"
                :key="subjectId"
                class="subject"
              >
                <CustomText variant="label-1" :color="COLORS.gray_4">
                  {{ getSubjectTitle(subjectId) }}
                </CustomText>
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
import DownloadFile from "@/common/DownloadFile/index.vue";
import { COLORS, SIZES } from "@/utils/appConsts";
import { getBook, deleteBook } from "@/api/books";
import { surnameWithInitials } from "@/utils/person";
import CtaButton from "@/common/CtaButton";
import {PapersModule, ReferenceModule, SubjectsModule, UserModule} from "@/store";

export default {
  name: "Book",
  components: { CtaButton, CustomText, DownloadFile },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      // eslint-disable-next-line no-param-reassign
      vm.prevRoute = from;
    });
  },
  data() {
    return {
      SIZES,
      COLORS,
      book: null,
      loading: true,
      prevRoute: null,
    };
  },
  computed: {
    subjects() { return SubjectsModule.subjects; },
    authors() { return PapersModule.authors; },
    publishers() { return PapersModule.publishers; },
    userId() { return UserModule.userId; },
    milspecialties() { return ReferenceModule.milspecialties; }
  },
  created() {
    this.fetchData();
  },
  methods: {
    surnameWithInitials,
    getSubjectTitle(subjectId) {
      const subject = this.subjects.find(item => item.id === subjectId);
      return `${subject.title} ${this.milspecialties.find(x => x.id === subject.milspecialty).code}`;
    },
    fetchData() {
      this.loading = true;
      getBook(this.$route.params.id).then(res => {
        this.book = res.data;
        this.loading = false;
      });
    },
    handleDelete() {
      this.$confirm(
        "Вы уверены, что хотите удалить эту книгу?",
        "Подтверждение",
        {
          confirmButtonText: "Да",
          cancelButtonText: "Отмена",
          type: "warning",
        },
      )
        .then(() => {
          deleteBook(this.$route.params.id).then(() => {
            this.$message({
              type: "success",
              message: "Удаление завершено",
            });
            this.$router.push(`${this.prevRoute.path}`);
          });
        })
        .catch(() => {
          this.$message.error("Ошибка удаления");
        });
    },
  },
};
</script>

<style scoped lang="scss">
@import "@/styles/variables.scss";

.content-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

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
  width: 100%;
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
  margin-right: $m;
}
</style>
