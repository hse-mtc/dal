import Vue from "vue";

import localeLangRu from "element-ui/lib/locale/lang/ru-RU";
import locale from "element-ui/lib/locale";
import "element-ui/lib/theme-chalk/index.css";
import "element-ui/lib/theme-chalk/display.css";

import {
  Drawer,
  Pagination,
  Dialog,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Menu,
  Submenu,
  MenuItem,
  Input,
  InputNumber,
  Radio,
  RadioGroup,
  Checkbox,
  Switch,
  Select,
  Option,
  Button,
  DatePicker,
  TimePicker,
  Popover,
  Tooltip,
  Breadcrumb,
  BreadcrumbItem,
  Form,
  FormItem,
  Tabs,
  TabPane,
  Tag,
  Tree,
  Alert,
  Icon,
  Row,
  Col,
  Upload,
  Steps,
  Step,
  Transfer,
  Loading,
  MessageBox,
  Message,
  Notification,
  Scrollbar,
  Autocomplete,
  Badge,
  Divider,
} from "element-ui";

locale.use(localeLangRu);

Vue.use(Alert);
Vue.use(Autocomplete);
Vue.use(Badge);
Vue.use(Breadcrumb);
Vue.use(BreadcrumbItem);
Vue.use(Button);
Vue.use(Checkbox);
Vue.use(Col);
Vue.use(DatePicker);
Vue.use(Dialog);
Vue.use(Divider);
Vue.use(Drawer);
Vue.use(Dropdown);
Vue.use(DropdownItem);
Vue.use(DropdownMenu);
Vue.use(Form);
Vue.use(FormItem);
Vue.use(Icon);
Vue.use(Input);
Vue.use(InputNumber);
Vue.use(Menu);
Vue.use(MenuItem);
Vue.use(Option);
Vue.use(Pagination);
Vue.use(Popover);
Vue.use(Radio);
Vue.use(RadioGroup);
Vue.use(Row);
Vue.use(Select);
Vue.use(Step);
Vue.use(Steps);
Vue.use(Submenu);
Vue.use(Switch);
Vue.use(TabPane);
Vue.use(Tabs);
Vue.use(Tag);
Vue.use(TimePicker);
Vue.use(Tooltip);
Vue.use(Transfer);
Vue.use(Tree);
Vue.use(Upload);

// FIXME(TmLev): Existing code should work, but doesn't for some reason.
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
Vue.use(Scrollbar);

Vue.use(Loading.directive);

Vue.prototype.$loading = Loading.service;
Vue.prototype.$msgbox = MessageBox;
Vue.prototype.$alert = MessageBox.alert;
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$prompt = MessageBox.prompt;
Vue.prototype.$notify = Notification;
Vue.prototype.$message = Message;
