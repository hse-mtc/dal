import { ref, reactive, onMounted, watch } from 'vue';
import { Form, Select, Checkbox, Input } from 'element-ui';

export default {
  name: 'MilitaryOfficeSelector',
  props: {
    value: {
      type: Object,
      default: () => ({
        militaryOfficeId: null,
        customMilitaryOffice: null
      })
    }
  },
  setup(props, { emit }) {
    const militaryOffices = ref([]);
    const loading = ref(false);
    const customOffice = ref(false);

    // Check if we have a custom military office value
    watch(() => props.value, (newValue) => {
      if (newValue?.customMilitaryOffice) {
        customOffice.value = true;
      }
    }, { immediate: true });

    onMounted(() => {
      // Fetch military offices from the API
      loading.value = true;
      fetch('/api/military-offices/')
        .then(response => response.json())
        .then(data => {
          militaryOffices.value = data;
          loading.value = false;
        })
        .catch(error => {
          console.error('Error fetching military offices:', error);
          loading.value = false;
        });
    });

    const handleCustomCheckboxChange = (isChecked) => {
      customOffice.value = isChecked;
      
      // If unchecked, reset the custom value
      if (!isChecked) {
        emit('input', { militaryOfficeId: props.value?.militaryOfficeId || null, customMilitaryOffice: null });
      } else {
        // If checked, clear the selected dropdown value
        emit('input', { militaryOfficeId: null, customMilitaryOffice: '' });
      }
    };

    const handleCustomNameChange = (name) => {
      emit('input', { militaryOfficeId: null, customMilitaryOffice: name });
    };

    const handleSelectChange = (selectedId) => {
      emit('input', { militaryOfficeId: selectedId, customMilitaryOffice: null });
    };

    return {
      militaryOffices,
      loading,
      customOffice,
      handleCustomCheckboxChange,
      handleCustomNameChange,
      handleSelectChange
    };
  },
  render() {
    return (
      <div>
        <Form.Item label="Военкомат">
          <Select
            v-model={this.value?.militaryOfficeId}
            filterable
            placeholder="Выберите военкомат"
            loading={this.loading}
            disabled={this.customOffice}
            onChange={this.handleSelectChange}
            clearable
          >
            {this.militaryOffices.map(office => (
              <Select.Option key={office.id} value={office.id}>
                {office.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item>
          <Checkbox
            value={this.customOffice}
            onChange={this.handleCustomCheckboxChange}
          >
            Моего военкомата нет в списке
          </Checkbox>
        </Form.Item>

        {this.customOffice && (
          <Form.Item label="Название военкомата">
            <Input
              placeholder="Введите название военкомата"
              value={this.value?.customMilitaryOffice || ''}
              onChange={e => this.handleCustomNameChange(e.target.value)}
            />
          </Form.Item>
        )}
      </div>
    );
  }
};