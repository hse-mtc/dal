/* eslint max-classes-per-file: ["error", 2] */

import { ElementUIComponent } from "element-ui";

declare module "element-ui" {
  class ElScrollbar extends ElementUIComponent {
    /** Native type */
    native: boolean

    /** WrapStyle type */
    wrapStyle: any

    /** WrapClass type */
    wrapClass: any

    /** ViewClass type */
    viewClass: any

    /** ViewStyle type */
    viewStyle: any

    /** Noresize type */
    noresize: boolean

    /** Tag type */
    tag: string
  }

  export class Scrollbar extends ElScrollbar {}
}
