import { CAMPUSES } from "@/utils/enums";

export const STEPS = {
  about: "about",
  birthInfo: "birthInfo",
  passport: "passport",
  personalDocumentsInfo: "personalDocumentsInfo",
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
    component: "text",
    title: "Фамилия",
    props: { onlyChars: true, placeholder: "Чехов" },
  },
  name: {
    component: "text",
    title: "Имя",
    props: { onlyChars: true, placeholder: "Антон" },
  },
  patronymic: {
    component: "text",
    title: "Отчество (при наличии)",
    props: { onlyChars: true, placeholder: "Павлович" },
  },
  citizenship: {
    component: "text",
    title: "Гражданство",
    props: { onlyChars: true, placeholder: "РФ" },
  },
  nationality: {
    component: "text",
    title: "Национальность",
    props: { onlyChars: true, placeholder: "Русский" },
  },
  marital_status: {
    component: "select",
    title: "Семейное положение",
    props: { options: ["Холост", "Женат"], allowCustom: false },
  },
  permanent_address: {
    component: "text",
    title: "Адрес постоянной регистрации",
  },
  surname_genitive: {
    component: "text",
    title: "Фамилия в родительном падеже",
    props: { onlyChars: true, placeholder: "Чехова" },
  },
  name_genitive: {
    component: "text",
    title: "Имя в родительном падеже",
    props: { onlyChars: true, placeholder: "Антона" },
  },
  patronymic_genitive: {
    component: "text",
    title: "Отчество в родительном падеже (при наличии)",
    props: { onlyChars: true, placeholder: "Павловича" },
  },
};

export const BIRTH_INFO = {
  date: { component: "date", title: "Дата" },
  country: {
    component: "text",
    title: "Страна",
    props: {
      placeholder: "Россия",
      annotation: "не более 64х символов",
    },
  },
  place: {
    component: "text",
    title: "Город",
    props: {
      placeholder: "Владимир",
      annotation: "не более 64х символов",
    },
  },
};

export const CONTACT_INFO = {
  personal_email: {
    component: "text",
    title: "Личная почта",
    props: { placeholder: "chekhov@writers.ru" },
  },
  personal_phone_number: {
    component: "text",
    title: "Номер телефона",
    props: { placeholder: "+79095050011" },
  },
};

export const PASSPORT = {
  series: {
    component: "text",
    title: "Серия",
    props: { placeholder: "1234" },
  },
  code: {
    component: "text",
    title: "Номер",
    props: { placeholder: "567890" },
  },
  ufms_name: {
    component: "text",
    title: "Паспорт выдан",
    props: {
      placeholder: "Отделом УФМС России по гор. Таганрог по району Светлый",
    },
  },
  issue_date: { component: "date", title: "Дата выдачи" },
  ufms_code: {
    component: "text",
    title: "Код подразделения",
    props: { placeholder: "700-007" },
  },
};

export const PERSONAL_DOCUMENTS_INFO = {
  tax_id: {
    component: "text",
    title: "ИНН",
    props: {
      placeholder: "771234567890",
    },
  },
  insurance_number: {
    component: "text",
    title: "СНИЛС",
    props: {
      placeholder: "200-200-200 20",
    },
  },
};

export const RECRUITMENT_OFFICE = {
  title: {
    component: "select",
    title: "Военный комиссариат",
    props: {
      options: [],
      allowCustom: true,
    },
  },
};

export const UNIVERSITY_INFO = {
  campus: {
    component: "select",
    title: "Кампус",
    props: {
      options: Object.entries(CAMPUSES)
        .map(([value, label]) => ({ value, label })),
      allowCustom: false,
    },
  },
  card_id: {
    component: "text",
    title: "Номер студенческого билета",
    props: { placeholder: "М123БМИЭФ321" },
  },
  program: {
    component: "select",
    title: "Образовательная программа",
    props: { options: [], allowCustom: false },
  },
  group: {
    component: "text",
    title: "Номер группы",
    props: { placeholder: "БИТ 123" },
  },
  graduation_year: {
    component: "text",
    title: "Год окончания ВУЗа",
    props: { placeholder: new Date().getFullYear() + 3 },
  },
};

export const MILSPECIALTY = {
  milspecialty: {
    component: "select",
    title: "Желаемая военная специальность",
    props: { options: [], allowCustom: false },
  },
};

export const PHOTO = {
  photo: {
    component: "file",
    title: "Загрузите фотографию размером 3x4",
    props: { filesTypes: [".png", ".jpg", ".jpeg"] },
  },
};

export const AGREEMENT = {
  agreement: {
    component: "checkbox",
    title: "Я даю согласие на обработку персональных данных",
  },
  isDataCorrect: {
    component: "checkbox",
    title: "Я подтверждаю правильность введенных данных",
  },
};

export const getRelationData = rel => ({
  surname: {
    component: "text",
    title: `Фамилия ${rel}`,
    props: { onlyChars: true },
  },
  name: {
    component: "text",
    title: `Имя ${rel}`,
    props: { onlyChars: true },
  },
  patronymic: {
    component: "text",
    title: `Отчество ${rel} (при наличии)`,
    props: { onlyChars: true },
  },
  citizenship: {
    component: "text",
    title: `Гражданство ${rel}`,
    props: { onlyChars: true, placeholder: "РФ" },
  },
  permanent_address: {
    component: "text",
    title: `Адрес постоянной регистрации ${rel}`,
  },
  date: { component: "date", title: `Дата рождения ${rel}` },
  country: {
    component: "text",
    title: `Страна рождения ${rel}`,
    props: {
      onlyChars: true,
      annotation: "не более 64х символов",
    },
  },
  place: {
    component: "text",
    title: `Город рождения ${rel}`,
    props: {
      annotation: "не более 64х символов",
    },
  },
  personal_email: { component: "text", title: `Личная почта ${rel}` },
  personal_phone_number: {
    component: "text",
    title: `Номер телефона ${rel}`,
  },
});

export const STEPS_RU = {
  about: "Общее",
  birthInfo: "Рождение",
  passport: "Паспорт",
  personalDocumentsInfo: "ИНН и СНИЛС",
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
  personalDocumentsInfo: "ИНН и СНИЛС",
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

export function dataURLtoFile(dataurl, filename) {
  const arr = dataurl.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  const n = bstr.length;
  const u8arr = new Uint8Array(n);

  for (let i = 0; i < n; i += 1) {
    u8arr[i] = bstr.charCodeAt(i);
  }
  return new File([u8arr], filename, { type: mime });
}

export const devInitData = {
  about: {
    surname: "Фамилия",
    name: "Имя",
    patronymic: "Отчество",
    citizenship: "Гражданство",
    nationality: "Национальность",
    marital_status: "Холост",
    permanent_address: "Адрес постоянной регистрации",
    surname_genitive: "Фамилия в родительном падеже",
    name_genitive: "Имя в родительном падеже",
    patronymic_genitive: "Отчество в родительном падеже",
  },
  birthInfo: {
    date: "2021-04-06",
    country: "Страна",
    place: "Город",
  },
  passport: {
    series: "1234",
    code: "123456",
    ufms_name: "Паспорт выдан",
    issue_date: "2021-04-20",
    ufms_code: "010-191",
  },
  personalDocumentsInfo: {
    tax_id: "771234567890",
    insurance_number: "200-200-200 20",
  },
  recruitmentOffice: { title: "Состою на воинском учете в военном комиссариате" },
  universityInfo: {
    campus: "MO",
    card_id: "Номер студенческого билета",
    program: 1,
    group: "БИВ123",
    graduation_year: new Date().getFullYear() + 3,
  },
  contactInfo: {
    personal_email: "test@mail.ru",
    personal_phone_number: "72345678900",
  },
  mother: {
    surname: "Фамилия матери",
    name: "Имя матери",
    patronymic: "Отчество матери",
    citizenship: "Гражданство матери",
    permanent_address: "Адрес постоянной регистрации матери",
    date: "2021-05-25",
    country: "Страна рождения матери",
    place: "Город рождения матери",
    personal_email: "test@mail.ru",
    personal_phone_number: "89098080022",
  },
  father: {
    surname: "Фамилия отца",
    name: "Имя отца",
    patronymic: "Отчество отца",
    citizenship: "Гражданство отца",
    permanent_address: "Адрес постоянной регистрации отца",
    date: "2021-04-28",
    country: "Страна рождения отца",
    place: "Город рождения отца",
    personal_email: "test@dkcmsdc.sdcjnis",
    personal_phone_number: "+72345678765",
  },
  brothers: [],
  sisters: [],
  photo: {
    photo: [
      {
        name: "1x1_pxl.png",
        percentage: 0,
        raw: dataURLtoFile("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjULHy/A8AAtQBp1XLiUMAAAAASUVORK5CYII=", "1x1_pxl.png"),
        size: 82,
        status: "ready",
      },
    ],
  },
  milspecialty: { milspecialty: 8 },
  agreement: {
    agreement: true,
    isDataCorrect: true,
  },
};
