<template>
  <div id="app" :style="{ minWidth: width }">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      whiteList: ["SignUp", "Login", "ApplicantForm"],
    };
  },
  computed: {
    width() {
      return this.whiteList.includes(this.$route.name) ? 0 : 1200;
    },
  },
  metaInfo() {
    return {
      meta: [
        {
          name: "viewport",
          content: `width=${
            this.whiteList.includes(this.$route.name) ? "device-width" : "1200"
          }, initial-scale=1`,
        },
      ],
    };
  },
  watch: {
    width(nextWidth) {
      document.getElementById("app").style.minWidth = nextWidth;
    },
  },
};
</script>
