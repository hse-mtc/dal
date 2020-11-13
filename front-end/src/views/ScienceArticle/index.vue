<template>
  <div class="dashboard-container">
    <div class="dashboard-text">{{ name }}, добро пожаловать на сайт.</div>
    <div class="previewer">
      <iframe
        src="../../assets/files/ТСП%20ГЗ%201-2.docx"
        width="100%"
        height="100%"
        frameborder="0"
        >This is an embedded
        <a target="_blank" href="http://office.com">Microsoft Office</a>
        document, powered by
        <a target="_blank" href="http://office.com/webapps">Office Online</a
        >.</iframe
      >
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "ScienceArticle",
  computed: {
    ...mapGetters(["name"]),
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style>
.previewer,
iframe {
  width: 100%;
  height: calc(100vh - 74px);
  padding: 0;
  margin: 0;
}
</style>
