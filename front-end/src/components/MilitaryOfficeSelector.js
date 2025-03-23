import React, { useState, useEffect } from 'react';
import { Select, Checkbox, Input, Form, Space } from 'antd';

const MilitaryOfficeSelector = ({ value, onChange }) => {
  const [militaryOffices, setMilitaryOffices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [customOffice, setCustomOffice] = useState(false);

  useEffect(() => {
    // Check if we have a custom military office value
    if (value?.customMilitaryOffice) {
      setCustomOffice(true);
    }
  }, [value]);

  useEffect(() => {
    // Fetch military offices from the API
    setLoading(true);
    fetch('/api/military-offices/')
      .then(response => response.json())
      .then(data => {
        setMilitaryOffices(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching military offices:', error);
        setLoading(false);
      });
  }, []);

  const handleCustomCheckboxChange = (e) => {
    const isChecked = e.target.checked;
    setCustomOffice(isChecked);
    
    // If unchecked, reset the custom value
    if (!isChecked) {
      onChange({ militaryOfficeId: value?.militaryOfficeId || null, customMilitaryOffice: null });
    } else {
      // If checked, clear the selected dropdown value
      onChange({ militaryOfficeId: null, customMilitaryOffice: '' });
    }
  };

  const handleCustomNameChange = (e) => {
    const name = e.target.value;
    onChange({ militaryOfficeId: null, customMilitaryOffice: name });
  };

  const handleSelectChange = (selectedId) => {
    onChange({ militaryOfficeId: selectedId, customMilitaryOffice: null });
  };

  return (
    <Space direction="vertical" style={{ width: '100%' }}>
      <Form.Item label="Военкомат">
        <Select
          showSearch
          placeholder="Выберите военкомат"
          optionFilterProp="children"
          loading={loading}
          disabled={customOffice}
          onChange={handleSelectChange}
          value={customOffice ? null : value?.militaryOfficeId}
          allowClear
          style={{ width: '100%' }}
          filterOption={(input, option) =>
            option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
          }
        >
          {militaryOffices.map(office => (
            <Select.Option key={office.id} value={office.id}>
              {office.name}
            </Select.Option>
          ))}
        </Select>
      </Form.Item>

      <Form.Item>
        <Checkbox 
          checked={customOffice} 
          onChange={handleCustomCheckboxChange}
        >
          Моего военкомата нет в списке
        </Checkbox>
      </Form.Item>

      {customOffice && (
        <Form.Item label="Название военкомата">
          <Input 
            placeholder="Введите название военкомата"
            value={value?.customMilitaryOffice || ''}
            onChange={handleCustomNameChange}
          />
        </Form.Item>
      )}
    </Space>
  );
};

export default MilitaryOfficeSelector;
