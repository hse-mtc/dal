<script>
import { hasPermission } from "@/utils/permissions";
import { UserModule } from "@/store";

export default {
  name: "AZGuard",
  props: {
    permissions: {
      type: Array,
      default: () => [],
    },
    disable: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    isSuperuser() {
      return UserModule.isSuperuser;
    },
    disabled() {
      return this.disable && !hasPermission(this.permissions);
    },
  },
  render() {
    return this.isSuperuser || (this.$scopedSlots.default && (this.disable || hasPermission(this.permissions))) ? (
      this.$scopedSlots.default({ disabled: this.disabled })
    ) : null;
  },
};
</script>
