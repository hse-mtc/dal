import { mount, createLocalVue } from "@vue/test-utils";
import { Button, Input } from "element-ui";
import FormationHeadcount from "./FormationHeadcount.vue";

const localVue = createLocalVue();
localVue.use(Button);
localVue.use(Input);

const makeForm = (readonly = false) => mount({
  components: { FormationHeadcount },
  data() {
    return {
      counts: {
        roster_count: 29, excused_count: 2, unexcused_count: 1, unknown_count: 1, comment: "",
      },
      group: { id: 1, title: "1801" },
      readonly,
    };
  },
  template: `<FormationHeadcount v-model="counts" :group="group" date="2026-09-25"
    :wizard="readonly" :disabled="readonly" />`,
}, { localVue });

describe("Formation headcount", () => {
  let wrapper;
  beforeEach(() => { wrapper = makeForm(); });
  afterEach(() => { wrapper.destroy(); });

  it("recalculates present after all-present, plus and minus and saves that number", async() => {
    const allPresent = wrapper.findAll("button").wrappers.find(button => button.text() === "Все в строю");
    allPresent.trigger("click");
    await localVue.nextTick();
    expect(wrapper.find("output").text()).toBe("29");
    wrapper.find("[aria-label=\"Увеличить: Причина не выяснена\"]").trigger("click");
    await localVue.nextTick();
    expect(wrapper.find("output").text()).toBe("28");
    wrapper.find(".formation-save button").trigger("click");
    expect(wrapper.find(FormationHeadcount).emitted().save[0][0].present_count).toBe(28);
    wrapper.find("[aria-label=\"Уменьшить: Причина не выяснена\"]").trigger("click");
    await localVue.nextTick();
    expect(wrapper.find("output").text()).toBe("29");
  });

  it("caps directly entered absences and prevents incrementing past the roster", async() => {
    const input = wrapper.find("[aria-label=\"Причина не выяснена\"]");
    input.setValue("99");
    await localVue.nextTick();
    expect(input.element.value).toBe("26");
    expect(wrapper.find("output").text()).toBe("0");
    expect(wrapper.find("[aria-label=\"Увеличить: Уважительная причина\"]").element.disabled).toBe(true);
    input.setValue("99");
    await localVue.nextTick();
    expect(input.element.value).toBe("26");
  });

  it("blocks saving an invalid roster without discarding the absence breakdown", async() => {
    wrapper.find("[aria-label=\"По списку\"]").setValue("3");
    await localVue.nextTick();
    expect(wrapper.find(".formation-save button").element.disabled).toBe(true);
    expect(wrapper.find("[role=\"alert\"]").text()).toContain("не меньше 4");
    wrapper.find("[aria-label=\"По списку\"]").setValue("30");
    await localVue.nextTick();
    expect(wrapper.find("output").text()).toBe("26");
    expect(wrapper.find(".formation-save button").element.disabled).toBe(false);
  });

  it("lets a read-only user browse all steps while keeping editing disabled", async() => {
    wrapper.destroy();
    wrapper = makeForm(true);
    const next = wrapper.find(".formation-wizard-actions button");
    expect(next.element.disabled).toBe(false);
    expect(next.element.closest("fieldset[disabled]")).toBeNull();
    next.trigger("click");
    await localVue.nextTick();
    expect(wrapper.find(".formation-reasons").exists()).toBe(true);
    expect(wrapper.find(".formation-stepper button").element.disabled).toBe(true);
    wrapper.findAll(".formation-wizard-actions button").at(1).trigger("click");
    await localVue.nextTick();
    expect(wrapper.find("#formation-comment").exists()).toBe(true);
    expect(wrapper.find(".formation-save button").element.disabled).toBe(true);
    wrapper.find(".formation-wizard-actions button").trigger("click");
    await localVue.nextTick();
    expect(wrapper.find(".formation-reasons").exists()).toBe(true);
  });
});
