<template>
  <div style="margin-top: 3rem">
    <Documents class="documents" :isMyDocuments="true" v-on:openPaperModal="openPaperModal"/>
    <UpsertPaperModal
        v-if="paperAction"
        :action="paperAction"
        :paper="paperToEdit"
        v-on:closeModal="closeModal"
    />
    <div
        v-if="paperAction"
        class="background"
        @click="closeModal"
    />
  </div>
</template>

<script>
import Documents from "@/components/Documents/Documents";
import UpsertPaperModal from "@/components/Documents/UpsertPaperModal";

export default {
  name: "MyDocuments",
  components: {
    Documents,
    UpsertPaperModal,
  },
  data() {
    return {
      paperAction: "",
      paperToEdit: {},
    };
  },
  methods: {
    startScrolling() {
      document
          .getElementById("main-container")
          .classList.remove("stop-scrolling");
    },
    stopScrolling() {
      document.getElementById("main-container").classList.add("stop-scrolling");
    },
    openPaperModal(action, paperToEdit = {}) {
      console.log(
          "Open Paper Modal: action = ",
          action,
          " to edit = ",
          paperToEdit
      );
      this.paperAction = action;
      this.paperToEdit = paperToEdit;
      this.stopScrolling();
    },
    // Any modal (paper or category)
    closeModal() {
      console.log("Close modal");
      this.paperAction = "";
      this.paperToEdit = {};
      this.addNewCategory = false;
      this.startScrolling();
    },
  }
}
</script>

<style scoped lang="scss">
.background {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: black;
  opacity: 0.7;
  z-index: 201;
}
</style>
