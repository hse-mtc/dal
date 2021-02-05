<template>
  <div class="wrapper">
    <div
      :id="`loader__${data.id}`"
      class="file-img"
      @click="$router.push(`/library/book/${data.id}`)"
    >
      <div class="lds-dual-ring" />
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
      <div @click="$router.push(`/library/book/${data.id}`)">
        <CustomText style="cursor: pointer" variant="header">{{
          data.title
        }}</CustomText>
        <CustomText
          style="cursor: pointer"
          variant="sub-header"
          :color="COLORS.gray_2"
          :mt="SIZES.s"
          :mb="SIZES.m"
        >
          <template v-for="item in data.authors">
            {{ item.surname }} {{ item.name }} {{ item.patronymic }},
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
        <div class="button" @click.prevent="downloadFile(data.file, data.id)">
          <CustomText :mt="SIZES.m" :color="COLORS.darkBlue" variant="paragraph">
            Скачать
          </CustomText>
        </div>

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
import { COLORS, SIZES } from "@/utils/appConsts";
import axios from "axios";
export default {
  name: "Book",
  components: { CustomText },
  props: {
    data: {
      type: Object,
      required: true
    },
    onEdit: { type: Function }
  },
  data() {
    return {
      SIZES,
      COLORS,
      loading: false,
    };
  },
  methods: {
    async downloadFile(file, id) {
      document.getElementById(`loader__${id}`).classList.add("loading");
      let data;
      try {
        ({ data } = await axios.get(file.content, { responseType: "blob" }));
      } catch (error) {
        console.log("Failed to download Book.file: ", error);
        document.getElementById(`loader__${id}`).classList.remove("loading");
        return;
      }

      const create = document.createElement.bind(document);
      const link = create("a");

      const blob = new Blob([data]);
      link.href = URL.createObjectURL(blob);
      link.download = file.name;

      link.click();
      URL.revokeObjectURL(link.href);
      document.getElementById(`loader__${id}`).classList.remove("loading");
    },
  },
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

.content {
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

    &:first-child {
      margin-right: 20px;
    }
  }
}
</style>
