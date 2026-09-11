const empty = value => value === null || value === undefined || value === "";
export const MAX_PHOTO_SIZE_BYTES = 2 * 1024 * 1024;
const text = (max, required = true, name = false) => ({ max, required, name });
const names = {
  surname: text(64, true, true),
  name: text(64, true, true),
  patronymic: text(64, false, true),
};
const birth = { date: { required: true, date: true }, country: text(64), place: text(64) };
const contacts = {
  personal_email: { max: 254, email: true },
  personal_phone_number: { phone: true },
};
const relative = {
  ...names,
  citizenship: text(64),
  permanent_address: text(128),
  ...birth,
  ...contacts,
};

export const applicantSchema = {
  about: {
    ...names,
    surname_genitive: text(64, true, true),
    name_genitive: text(64, true, true),
    patronymic_genitive: text(64, false, true),
    citizenship: text(64),
    nationality: text(64),
    marital_status: { required: true, choices: ["Холост", "Женат"] },
    permanent_address: text(128, false),
  },
  birthInfo: birth,
  passport: {
    series: { required: true, pattern: /^\d{4}$/, format: "Введите 4 цифры серии паспорта" },
    code: { required: true, pattern: /^\d{6}$/, format: "Введите 6 цифр номера паспорта" },
    ufms_code: { required: true, pattern: /^\d{3}-\d{3}$/, format: "Введите код подразделения в формате 123-456" },
    ufms_name: text(255),
    issue_date: { required: true, date: true },
  },
  personalDocumentsInfo: {
    tax_id: { required: true, pattern: /^\d{12}$/, format: "Введите 12 цифр ИНН" },
    insurance_number: {
      required: true, pattern: /^\d{3}-\d{3}-\d{3} \d{2}$/, format: "Введите СНИЛС в формате 123-456-789 00",
    },
  },
  universityInfo: {
    campus: { required: true, choices: ["MO", "SP", "NN", "PE", "VA"] },
    program: { required: true, id: true },
    card_id: text(32),
    group: text(32),
    graduation_year: { required: true, pattern: /^[1-9]\d{3}$/, format: "Введите год из 4 цифр, например 2029" },
  },
  recruitmentOffice: { title: text(255) },
  contactInfo: contacts,
  photo: { photo: { required: true, photo: true } },
  mother: relative,
  father: relative,
  brothers: relative,
  sisters: relative,
  milspecialty: { milspecialty: { required: true, id: true } },
  agreement: {
    agreement: { consent: true },
    isDataCorrect: { consent: true },
  },
};

export function normalizeApplicant(value) {
  if (typeof value === "string") {
    return value.trim();
  }
  if (Array.isArray(value)) {
    return value.map(normalizeApplicant);
  }
  // Keep File and upload objects intact.
  if (value && Object.getPrototypeOf(value) === Object.prototype) {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, normalizeApplicant(item)]));
  }
  return value;
}

const hasRelative = value => Object.values(value || {}).some(item => !empty(item));

export function fieldError(value, rule) {
  if (rule.consent) {
    return value === true ? "" : "Для отправки формы необходимо поставить галочку";
  }
  if (empty(value) || (Array.isArray(value) && !value.length)) {
    return rule.required ? "Заполните обязательное поле" : "";
  }
  if (rule.photo) {
    const file = Array.isArray(value) && value.length === 1 && value[0].raw;
    if (!file || file.size <= 0 || !["image/jpeg", "image/png"].includes(file.type)) {
      return "Загрузите одну непустую фотографию в формате JPG или PNG";
    }
    if (file.size > MAX_PHOTO_SIZE_BYTES) {
      return "Размер фотографии не должен превышать 2 МБ";
    }
    return "";
  }
  if (rule.id) {
    return /^[1-9]\d*$/.test(String(value)) ? "" : "Выберите значение из списка";
  }
  if (rule.choices && !rule.choices.includes(value)) {
    return "Выберите значение из списка";
  }
  if (typeof value !== "string" && typeof value !== "number") {
    return "Введите корректное значение";
  }
  const input = String(value);
  if (rule.max && Array.from(input).length > rule.max) {
    return `Допустимо не более ${rule.max} символов`;
  }
  if (rule.name && !/^[\p{L}\p{M}]+(?:[ '\u2019-][\p{L}\p{M}]+)*$/u.test(input)) {
    return "Используйте буквы; между частями имени допустимы пробел, дефис или апостроф";
  }
  if (rule.email && !/^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/.test(input)) {
    return "Введите email в формате name@example.ru";
  }
  if (rule.phone && !/^(?:\+7|7|8)\d{10}$/.test(input)) {
    return "Введите 11 цифр телефона, начиная с 7 или 8; также можно указать +7";
  }
  if (rule.pattern && !rule.pattern.test(input)) {
    return rule.format;
  }
  if (rule.date) {
    const parsed = new Date(`${input}T00:00:00Z`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(input) || Number.isNaN(parsed.getTime())
      || parsed.toISOString().slice(0, 10) !== input || input.startsWith("0000")) {
      return "Введите существующую дату в формате ДД.ММ.ГГГГ";
    }
    const today = new Date();
    const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    if (input > localToday) {
      return "Дата не может быть в будущем";
    }
  }
  return "";
}

export function validateApplicant(source, steps = Object.keys(applicantSchema)) {
  const data = normalizeApplicant(source);
  const errors = [];
  const add = (step, index, field, message) => {
    if (message) {
      errors.push({
        step, index, field, message,
      });
    }
  };
  steps.forEach(step => {
    const multiple = ["brothers", "sisters"].includes(step);
    const rows = multiple ? data[step] || [] : [data[step] || {}];
    rows.forEach((row, rowIndex) => {
      if (["mother", "father"].includes(step) && !hasRelative(row)) {
        return;
      }
      Object.entries(applicantSchema[step]).forEach(([field, rule]) => {
        add(step, multiple ? rowIndex : null, field, fieldError(row[field], rule));
      });
    });
  });
  if (steps.includes("passport") && data.passport && data.birthInfo
    && data.passport.issue_date && data.birthInfo.date && data.passport.issue_date < data.birthInfo.date) {
    add("passport", null, "issue_date", "Дата выдачи паспорта не может быть раньше даты рождения");
  }
  if (steps.includes("father") && (hasRelative(data.mother) || hasRelative(data.father))
    && !(data.mother || {}).personal_phone_number && !(data.father || {}).personal_phone_number) {
    add(hasRelative(data.mother) ? "mother" : "father", null, "personal_phone_number", "Укажите телефон хотя бы одного из родителей");
  }
  return errors;
}

const apiSteps = {
  birth_info: "birthInfo",
  contact_info: "contactInfo",
  personal_documents_info: "personalDocumentsInfo",
  university_info: "universityInfo",
  passport: "passport",
};
const familySteps = {
  MO: "mother", FA: "father", BR: "brothers", SI: "sisters",
};

export function applicantApiErrors(payload, family = []) {
  const errors = [];
  const visit = (value, path = []) => {
    if (Array.isArray(value)) {
      value.forEach((item, index) => visit(item, typeof item === "object" ? [...path, index] : path));
      return;
    }
    if (value && typeof value === "object") {
      Object.entries(value).forEach(([key, item]) => visit(item, [...path, key]));
      return;
    }
    let step = apiSteps[path[0]];
    let field = path[path.length - 1];
    let index = null;
    if (path[0] === "family") {
      const member = family[path[1]];
      step = member && familySteps[member.type];
      if (["brothers", "sisters"].includes(step)) {
        index = family.slice(0, path[1]).filter(item => item.type === member.type).length;
      }
    } else if (path[0] === "recruitment_office") {
      step = "recruitmentOffice";
      field = "title";
    } else if (["image", "photo"].includes(path[0])) {
      step = "photo";
      field = "photo";
    } else if (path[0] === "milspecialty") {
      step = "milspecialty";
    } else if (["agreement", "isDataCorrect"].includes(path[0])) {
      step = "agreement";
    } else if (Object.keys(applicantSchema.about).includes(path[0])) {
      step = "about";
    }
    // Corporate email comes from the account and has no editable form field.
    const accountEmail = field === "corporate_email";
    const message = typeof value === "string" && /[а-яё]/i.test(value)
      ? value : "Проверьте значение поля и попробуйте ещё раз";
    errors.push({
      step: accountEmail ? null : step,
      field,
      index,
      message: accountEmail ? `Email учётной записи: ${message}` : message,
    });
  };
  if (payload && typeof payload === "object") {
    visit(payload);
  }
  return errors;
}
