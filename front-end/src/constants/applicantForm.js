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
  agreement: "agreement",
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
    props: {
      placeholder: "Россия",
      annotation: "не более 64х символов",
    },
  },
  city: {
    component: "TextInput",
    title: "Город",
    props: {
      placeholder: "Владимир",
      annotation: "не более 64х символов",
    },
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
    title: "Загрузите фотографию размером 3x4",
    props: { filesTypes: [".png", ".jpg", ".jpeg"] },
  },
};

export const AGREEMENT = {
  agreement: {
    component: "SingleCheckbox",
    title: "Я даю согласие на обработку персональных данных",
  },
  isDataCorrect: {
    component: "SingleCheckbox",
    title: "Я подтверждаю правильность введенных данных",
  },
};

export const getRelationData = rel => ({
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
    props: {
      onlyChars: true,
      annotation: "не более 64х символов",
    },
  },
  city: {
    component: "TextInput",
    title: `Город рождения ${rel}`,
    props: {
      annotation: "не более 64х символов",
    },
  },
  personal_email: { component: "TextInput", title: `Личная почта ${rel}` },
  personal_phone_number: {
    component: "TextInput",
    title: `Номер телефона ${rel}`,
  },
});

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
  agreement: "Соглашение",
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
  agreement: "Соглашение",
};

export const devInitData = {
  about: {
    surname: "Фамилия",
    name: "Имя",
    patronymic: "Отчество",
    citizenship: "Гражданство",
    permanent_address: "Адрес постоянной регистрации",
    surname_genitive: "Фамилия в родительном падеже",
    name_genitive: "Имя в родительном падеже",
    patronymic_genitive: "Отчество в родительном падеже",
  },
  birthInfo: {
    date: "2021-04-06",
    country: "Страна",
    city: "Город",
  },
  passport: {
    series: "1234",
    code: "123456",
    ufms_name: "Паспорт выдан",
    issue_date: "2021-04-20",
    ufms_code: "010-191",
  },
  recruitmentOffice: { title: "Состою на воинском учете в военном комиссариате" },
  universityInfo: {
    campus: "MO",
    card_id: "Номер студенческого билета",
    program: "01.12.12",
    group: "БИВ123",
  },
  contactInfo: {
    corporate_email: "test@edu.hse.ru",
    personal_email: "test@mail.ru",
    personal_phone_number: "+12345678900",
  },
  mother: {
    surname: "Фамилия матери",
    name: "Имя матери",
    patronymic: "Отчество матери",
    citizenship: "Гражданство матери",
    permanent_address: "Адрес постоянной регистрации матери",
    date: "2021-05-25",
    country: "Страна рождения матери",
    city: "Город рождения матери",
    personal_email: "test@mail.ru",
    personal_phone_number: "",
  },
  father: {
    surname: "Фамилия отца",
    name: "Имя отца",
    patronymic: "Отчество отца",
    citizenship: "Гражданство отца",
    permanent_address: "Адрес постоянной регистрации отца",
    date: "2021-04-28",
    country: "Страна рождения отца",
    city: "Город рождения отца",
    personal_email: "test@dkcmsdc.sdcjnis",
    personal_phone_number: "+12345678765",
  },
  brothers: [],
  sisters: [],
  photo: {
    photo: null,
  },
  milspecialty: { milspecialty: "106646-543" },
  agreement: {
    agreement: true,
    isDataCorrect: true,
  },
};
