import { getCoords } from "@/utils/functions";
import { throttle } from "lodash";

export const scrollMixin = {
  mounted() {
    window.addEventListener("scroll", this.onScroll);
  },

  beforeDestroy() {
    window.removeEventListener("scroll", this.onScroll);
  },
  methods: {
    onScroll: throttle(function throttledOnScroll() {
      const { top } = getCoords(this.$el);
      const delta = 100;
      if (
        window.pageYOffset + window.document.documentElement.clientHeight
        >= this.$el.clientHeight + top - delta
      ) {
        this.loadMore();
      }
    }, 200),
  },
};
