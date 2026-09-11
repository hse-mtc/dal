/* global jest */
import { mount, createLocalVue } from "@vue/test-utils";
import ElementUI from "element-ui";
import lodash from "lodash";
import GenericForm from "@/common/Form/index.vue";
import { devInitData } from "@/constants/applicantForm";
import { normalizeApplicant } from "@/utils/applicantValidation";
import { postApplicant } from "@/api/applicants";
import ApplicantForm from "../index.vue";

jest.mock("@/store", () => ({ UserModule: { email: "user@example.ru", personId: null } }));
jest.mock("@/utils/enums", () => ({ CAMPUSES: { MO: "Москва" } }));
// Pop-up positioning is outside these tests; keep the real form and text inputs.
jest.mock("@/common/inputs/Select.vue", () => ({ render: h => h("div") }));
jest.mock("@/common/inputs/Date.vue", () => ({ render: h => h("div") }));
jest.mock("@/utils/allowMobileView", () => ({ __esModule: true, default: jest.fn() }));
jest.mock("@/api/applicants", () => ({ postApplicant: jest.fn(), putApplicant: jest.fn() }));
jest.mock("@/api/reference-book", () => ({
  getAvailableForApplicantsProgramsByCampus: jest.fn(() => Promise.resolve({ data: [] })),
  getMilSpecialtiesSelectableByProgram: jest.fn(() => Promise.resolve({ data: [] })),
  getRecruitmentOffices: jest.fn(() => Promise.resolve({ data: [] })),
}));

const localVue = createLocalVue();
localVue.use(ElementUI);
let wrapper;
const flush = () => new Promise(resolve => setTimeout(resolve, 0));

beforeEach(async() => {
  jest.spyOn(window, "scrollTo").mockImplementation(() => undefined);
  Element.prototype.scrollIntoView = jest.fn();
  wrapper = mount(ApplicantForm, {
    localVue,
    mocks: { $route: { query: {}, hash: "" }, lodash },
    stubs: { "router-link": true },
  });
  wrapper.setData({ disableWatchers: true, applicantData: normalizeApplicant(devInitData), step: "agreement" });
  await wrapper.vm.$nextTick();
  wrapper.setData({ disableWatchers: false });
  jest.spyOn(window, "FileReader").mockImplementation(() => ({
    result: "data:image/png;base64,test",
    readAsDataURL() { this.onload(); },
  }));
});

afterEach(() => {
  wrapper.destroy();
  jest.restoreAllMocks();
});

test("submit revalidates hidden steps, displays inline errors and focuses the first field", async() => {
  wrapper.vm.applicantData.passport.series = "abcd";
  wrapper.vm.submit();
  await flush();
  expect(postApplicant).not.toHaveBeenCalled();
  expect(wrapper.vm.step).toBe("passport");
  expect(wrapper.find("[role=\"alert\"]").text()).toContain("Введите 4 цифры серии паспорта");
  const field = wrapper.find("[data-field=\"series\"]");
  expect(field.find(".el-form-item__error").text()).toBe("Введите 4 цифры серии паспорта");
  expect(Element.prototype.scrollIntoView).toHaveBeenCalled();
});

test("server errors appear under fields and preserve entered values", async() => {
  postApplicant.mockRejectedValue({ response: { status: 400, data: { passport: { code: ["Неверный номер паспорта"] } } } });
  wrapper.vm.submit();
  await flush();
  expect(postApplicant).toHaveBeenCalledTimes(1);
  expect(postApplicant.mock.calls[0][0].agreement).toBe(true);
  expect(wrapper.vm.step).toBe("passport");
  expect(wrapper.find("[data-field=\"code\"] .el-form-item__error").text()).toBe("Неверный номер паспорта");
  expect(wrapper.vm.applicantData.passport.code).toBe(devInitData.passport.code);
  expect(wrapper.vm.isSubmitting).toBe(false);
});

test("network errors remain readable and permit retry", async() => {
  postApplicant.mockRejectedValue(new Error("Network Error"));
  wrapper.vm.submit();
  await flush();
  expect(wrapper.find("[role=\"alert\"]").text()).toContain("Проверьте подключение к интернету");
  expect(wrapper.vm.isSubmitting).toBe(false);
  expect(wrapper.vm.formSubmitted).toBe(false);
});

test("a valid questionnaire is submitted once and shows success", async() => {
  postApplicant.mockResolvedValue({ data: {} });
  wrapper.vm.submit();
  wrapper.vm.submit();
  await flush();
  expect(postApplicant).toHaveBeenCalledTimes(1);
  expect(wrapper.vm.formSubmitted).toBe(true);
  expect(wrapper.text()).toContain("Форма успешно отправлена");
});

test("editing a field clears its stale error", async() => {
  wrapper.setData({
    step: "passport",
    validationErrors: [
      {
        step: "passport", index: null, field: "series", message: "Введите 4 цифры серии паспорта",
      },
    ],
  });
  await wrapper.vm.$nextTick();
  const input = wrapper.find("[data-field=\"series\"] input");
  input.element.value = "4321";
  input.trigger("input");
  await flush();
  expect(wrapper.vm.validationErrors).toEqual([]);
  expect(wrapper.vm.applicantData.passport.series).toBe("4321");
});

test("an error link opens the second sibling tab", async() => {
  const brother = { ...devInitData.mother };
  wrapper.vm.applicantData.brothers = [brother, { ...brother, name: "123" }];
  wrapper.vm.submit();
  await flush();
  expect(wrapper.vm.step).toBe("brothers");
  expect(wrapper.vm.tabsIndex.brothers).toBe("1");
  expect(wrapper.find(GenericForm).props("errors").name).toContain("Используйте буквы");
  expect(postApplicant).not.toHaveBeenCalled();
});
