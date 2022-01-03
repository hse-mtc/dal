<template>
  <div id="app" :style="{ minWidth: width }">
    <router-view />
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

const WHITELIST = [
  "Register", "Login", "ApplicantForm", "Subjects", "Subject",
];

@Component({
  name: "App",

  metaInfo() {
    const width = WHITELIST.includes(this.$route.name!) ? "device-width" : 1200;
    return {
      meta: [
        {
          name: "viewport",
          content: `width=${width}, initial-scale=1`,
        },
      ],
    };
  },
})
class App extends Vue {
  get width(): number {
    return WHITELIST.includes(this.$route.name!) ? 0 : 1200;
  }

  @Watch("width")
  onWidthChange(newWidth: number): void {
    document.getElementById("app")!.style.minWidth = `${newWidth}px`;
  }
}

export default App;
</script>
