import { mount, createLocalVue } from "@vue/test-utils";
import { Input } from "element-ui";
import { TextInput } from "@/common/inputs";

describe("Text input", () => {
  // Нужен, если используются глобальные компоненты,плагины и т.д
  // Использование такое же (по идее) как и у Vue при настройке проекта
  // Думаю стоит вынести создание и настройку в отдельный файл,
  // чтобы не дублировать одно и то же
  const localVue = createLocalVue();
  localVue.use(Input);

  // Есть еще shallowMount, если не нужно рендерить дочерние компоненты
  const factory = props => mount(TextInput, {
    props,
    localVue,
  });

  it("input test", () => {
    const wrapper = factory({
      modelValue: "123",
    });

    // Находим ноду инпута
    const input = wrapper.find("input");
    // Меняем значение в инпуте
    input.element.value = "1234";
    // Тригерим событие ввода, так как при изменении value напрямую оно не срабатывает
    input.trigger("input");
    // Триггер на инпуте инициирует события в el-input, а затем и в TextInput
    expect(wrapper.emitted().change[0]).toEqual(["1234"]);
  });
});
