export const STEPS = {
  about: "about",
  birthInfo: "birthInfo",
  passport: "passport",
  universityInfo: "universityInfo",
  recruitmentOffice: "recruitmentOffice",
  contactInfo: "contactInfo",
  photo: "photo",
  mother: "mother",
  father: "father",
  brothers: "brothers",
  sisters: "sisters",
  milspecialty: "milspecialty",
};

export const ABOUT = {
  surname: {
    component: "TextInput",
    title: "Фамилия",
    props: { onlyChars: true, placeholder: "Чехов" },
  },
  name: {
    component: "TextInput",
    title: "Имя",
    props: { onlyChars: true, placeholder: "Антон" },
  },
  patronymic: {
    component: "TextInput",
    title: "Отчество (при наличии)",
    props: { onlyChars: true, placeholder: "Павлович" },
  },
  citizenship: {
    component: "TextInput",
    title: "Гражданство",
    props: { onlyChars: true, placeholder: "РФ" },
  },
  permanent_address: {
    component: "TextInput",
    title: "Адрес постоянной регистрации",
  },
  surname_genitive: {
    component: "TextInput",
    title: "Фамилия в родительном падеже",
    props: { onlyChars: true, placeholder: "Чехова" },
  },
  name_genitive: {
    component: "TextInput",
    title: "Имя в родительном падеже",
    props: { onlyChars: true, placeholder: "Антона" },
  },
  patronymic_genitive: {
    component: "TextInput",
    title: "Отчество в родительном падеже (при наличии)",
    props: { onlyChars: true, placeholder: "Павловича" },
  },
};

export const BIRTH_INFO = {
  date: { component: "DateInput", title: "Дата" },
  country: {
    component: "TextInput",
    title: "Страна",
    props: { placeholder: "Россия" },
  },
  city: {
    component: "TextInput",
    title: "Город",
    props: { placeholder: "Владимир" },
  },
};

export const CONTACT_INFO = {
  corporate_email: {
    component: "TextInput",
    title: "Корпоративная почта",
    props: { placeholder: "apchekhov@edu.hse.ru" },
  },
  personal_email: {
    component: "TextInput",
    title: "Личная почта",
    props: { placeholder: "chekhov@writers.ru" },
  },
  personal_phone_number: {
    component: "TextInput",
    title: "Номер телефона",
    props: { placeholder: "+79095050011" },
  },
};

export const PASSPORT = {
  series: {
    component: "TextInput",
    title: "Серия",
    props: { placeholder: "1234" },
  },
  code: {
    component: "TextInput",
    title: "Номер",
    props: { placeholder: "567890" },
  },
  ufms_name: {
    component: "TextInput",
    title: "Паспорт выдан",
    props: {
      placeholder: "Отделом УФМС России по гор. Таганрог по району Светлый",
    },
  },
  issue_date: { component: "DateInput", title: "Дата выдачи" },
  ufms_code: {
    component: "TextInput",
    title: "Код подразделения",
    props: { placeholder: "700-007" },
  },
};

export const RECRUITMENT_OFFICE = {
  title: {
    component: "TextInput",
    title: "Состою на воинском учете в военном комиссариате...",
    props: {
      isTextArea: true,
      placeholder:
        "городов Одинцово, Звенигород, Краснознаменск и Одинцовского городского округа",
    },
  },
};

export const UNIVERSITY_INFO = {
  campus: {
    component: "SelectInput",
    title: "Кампус",
    props: {
      options: [
        {
          value: "MO",
          label: "Москва",
        },
        {
          value: "SP",
          label: "Санкт-Петербург",
        },
        {
          value: "NN",
          label: "Нижний Новгород",
        },
        {
          value: "PE",
          label: "Пермь",
        },
      ],
    },
  },
  card_id: {
    component: "TextInput",
    title: "Номер студенческого билета",
    props: { placeholder: "М123БМИЭФ321" },
  },
  program: {
    component: "TextInput",
    title: "Код образовательной программы",
    props: { placeholder: "01.02.03" },
  },
  group: {
    component: "TextInput",
    title: "Номер группы",
    props: { placeholder: "БИТ 123" },
  },
};

export const MILSPECIALTY = {
  milspecialty: {
    component: "SelectInput",
    title: "Желаемая военная специальность",
    props: { options: [] },
  },
};

export const PHOTO = {
  photo: {
    component: "FileInput",
    title: "Загрузите фотографию",
    props: { filesTypes: [".png", ".jpg", ".jpeg"] },
  },
};

export const getRelationData = (rel) => {
  return {
    surname: {
      component: "TextInput",
      title: `Фамилия ${rel}`,
      props: { onlyChars: true },
    },
    name: {
      component: "TextInput",
      title: `Имя ${rel}`,
      props: { onlyChars: true },
    },
    patronymic: {
      component: "TextInput",
      title: `Отчество ${rel} (при наличии)`,
      props: { onlyChars: true },
    },
    citizenship: {
      component: "TextInput",
      title: `Гражданство ${rel}`,
      props: { onlyChars: true, placeholder: "РФ" },
    },
    permanent_address: {
      component: "TextInput",
      title: `Адрес постоянной регистрации ${rel}`,
    },
    date: { component: "DateInput", title: `Дата рождения ${rel}` },
    country: {
      component: "TextInput",
      title: `Страна рождения ${rel}`,
      props: { onlyChars: true },
    },
    city: { component: "TextInput", title: `Город рождения ${rel}` },
    personal_email: { component: "TextInput", title: `Личная почта ${rel}` },
    personal_phone_number: {
      component: "TextInput",
      title: `Номер телефона ${rel}`,
    },
  };
};

export const STEPS_RU = {
  about: "Общее",
  birthInfo: "Рождение",
  passport: "Паспорт",
  universityInfo: "Университет",
  recruitmentOffice: "Военкомат",
  contactInfo: "Контакты",
  photo: "Фото",
  mother: "Мать",
  father: "Отец",
  brothers: "Братья",
  sisters: "Сёстры",
  milspecialty: "ВУС",
};

export const HEADERS_BY_STEPS = {
  about: "Общие сведения",
  birthInfo: "Информация о рождении",
  contactInfo: "Контактная информация",
  passport: "Паспортные данные",
  recruitmentOffice: "Военный комиссариат",
  universityInfo: "Информация о ВУЗе",
  photo: "Фотография",
  mother: "Данные о матери (При необходимости оставьте ВСЕ поля пустыми)",
  father: "Данные об отце (При необходимости оставьте ВСЕ поля пустыми)",
  brothers: "Данные о братьях",
  sisters: "Данные о сёстрах",
  milspecialty: "Желаемая военная специальность",
};
