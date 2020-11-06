<template>
  <div class="root">
    <div style="{position: relative}">
      <div class="addModal" v-if="opened" v-on:closeModal="closeModal">
        <slot></slot>
      </div>
      <div
          v-if="opened"
          class="background"
          @click="closeModal"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalWindow",
  props: {
    opened: {
      type: Boolean,
      required: true
    }
  },
  mounted() {
    // this.stopScrolling()
  },
  methods: {
    stopScrolling() {
      document.getElementById("main-container").classList.add("stop-scrolling");
    },
    startScrolling() {
      document
          .getElementById("main-container")
          .classList.remove("stop-scrolling");
    },
    closeModal() {
      this.$emit("closeModal");
      this.startScrolling()
    },
  },
  watch: {
    opened(val) {
     if (val) this.stopScrolling()
    },
  },
}
</script>

<style scoped lang="scss">
  .addModal {
    margin-top: 50px;
    position: fixed;
    top: 50%;
    left: calc(50%);
    transform: translate(calc(-0%), -50%);
    width: 50vw;
    height: 100%;
    background-color: white;
    padding: 50px 60px;
    border: 1px solid #ccc;
    z-index: 203;
    overflow-y: scroll;
  }
  .root {
    position: absolute;
    width: 100vw;
    height: 100vh;
  }
  .background {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: black;
    opacity: 0.7;
    z-index: 201;
    height: 100vh;
  }
</style>
