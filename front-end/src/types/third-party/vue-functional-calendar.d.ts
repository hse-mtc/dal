// FIXME(TmLev): Properly type `FunctionalCalender` and remove @ts-ignore
// comment near `Vue.use(FunctionalCalendar)`.
declare module "vue-functional-calendar" {
  import { PluginObject } from "vue";

  class FunctionalCalendar extends PluginObject {
  }

  export default FunctionalCalendar;
}
