import {
  applicantSchema, fieldError, normalizeApplicant, validateApplicant, applicantApiErrors, MAX_PHOTO_SIZE_BYTES,
} from "../applicantValidation";

const relative = () => ({
  surname: "Иванов",
  name: "Иван",
  patronymic: "",
  citizenship: "РФ",
  permanent_address: "Москва",
  date: "1970-01-01",
  country: "Россия",
  place: "Москва",
  personal_email: "",
  personal_phone_number: "",
});

const questionnaire = () => ({
  about: {
    surname: "Иванов",
    name: "Иван",
    patronymic: "",
    surname_genitive: "Иванова",
    name_genitive: "Ивана",
    patronymic_genitive: "",
    citizenship: "РФ",
    nationality: "Русский",
    marital_status: "Холост",
    permanent_address: "",
  },
  birthInfo: { date: "2005-01-01", country: "Россия", place: "Москва" },
  passport: {
    series: "1234", code: "123456", ufms_code: "123-456", ufms_name: "МВД", issue_date: "2020-01-01",
  },
  personalDocumentsInfo: { tax_id: "771234567890", insurance_number: "123-456-789 00" },
  universityInfo: {
    campus: "MO", program: 1, card_id: "123", group: "БИВ123", graduation_year: 2029,
  },
  recruitmentOffice: { title: "Военкомат Москвы" },
  contactInfo: { personal_email: "", personal_phone_number: "" },
  mother: {},
  father: {},
  brothers: [],
  sisters: [],
  photo: { photo: [{ raw: new File(["photo"], "photo.png", { type: "image/png" }) }] },
  milspecialty: { milspecialty: 1 },
  agreement: { agreement: true, isDataCorrect: true },
});

test("accepts a complete questionnaire with optional fields and relatives empty", () => {
  expect(validateApplicant(questionnaire())).toEqual([]);
});

test("validates every field, including fields on unmounted steps and every sibling", () => {
  const data = questionnaire();
  data.about.name = " ";
  data.passport.code = "abc";
  data.brothers = [relative(), { ...relative(), name: "123" }];
  data.sisters = [{ ...relative(), place: "" }];
  const errors = validateApplicant(data);
  expect(errors).toEqual(expect.arrayContaining([
    expect.objectContaining({ step: "about", field: "name" }),
    expect.objectContaining({ step: "passport", field: "code" }),
    expect.objectContaining({ step: "brothers", index: 1, field: "name" }),
    expect.objectContaining({ step: "sisters", index: 0, field: "place" }),
  ]));
});

test("validates father even when mother's phone is present", () => {
  const data = questionnaire();
  data.mother = { ...relative(), personal_phone_number: "+79001234567" };
  data.father = { ...relative(), name: "" };
  expect(validateApplicant(data)).toEqual([
    expect.objectContaining({ step: "father", field: "name" }),
  ]);
});

test("requires a phone for one of the supplied parents", () => {
  const data = questionnaire();
  data.mother = relative();
  expect(validateApplicant(data)).toEqual([
    expect.objectContaining({ step: "mother", field: "personal_phone_number" }),
  ]);
});

test.each(["+79001234567", "79001234567", "89001234567"])("accepts phone %s", phone => {
  expect(fieldError(phone, applicantSchema.contactInfo.personal_phone_number)).toBe("");
});

test.each(["7abcdefghij", "+7900 1234567", "9001234567", "790012345678"])("rejects phone %s", phone => {
  expect(fieldError(phone, applicantSchema.contactInfo.personal_phone_number)).not.toBe("");
});

test.each(["@example.ru", "a@@example.ru", "a@exam ple.ru", "a@example"])("rejects email %s", email => {
  expect(fieldError(email, applicantSchema.contactInfo.personal_email)).not.toBe("");
});

test.each(["Анна-Мария", "O’Connor", "李", "Де Ла Круз"])("accepts name %s", name => {
  expect(fieldError(name, applicantSchema.about.name)).toBe("");
});

test.each(["2023-02-29", "2020-02-30", "2099-01-01", "0000-01-01"])("rejects date %s", date => {
  expect(fieldError(date, applicantSchema.birthInfo.date)).not.toBe("");
});

test("checks passport chronology", () => {
  const data = questionnaire();
  data.passport.issue_date = "2000-01-01";
  expect(validateApplicant(data)).toEqual([
    expect.objectContaining({ step: "passport", field: "issue_date" }),
  ]);
});

test("checks optional text lengths, year, selection and both consents", () => {
  const data = questionnaire();
  data.about.patronymic = "а".repeat(65);
  data.about.permanent_address = "а".repeat(129);
  data.universityInfo.graduation_year = "2029abc";
  data.universityInfo.program = "abc";
  data.agreement = { agreement: false, isDataCorrect: "true" };
  expect(validateApplicant(data).map(error => error.field)).toEqual([
    "patronymic", "permanent_address", "program", "graduation_year", "agreement", "isDataCorrect",
  ]);
});

test.each([[[]], [[{ raw: new File([], "empty.png", { type: "image/png" }) }]],
  [[{ raw: new File(["pdf"], "photo.pdf", { type: "application/pdf" }) }]]])("rejects invalid photo %j", files => {
  expect(fieldError(files, applicantSchema.photo.photo)).not.toBe("");
});

test("accepts a photo at 2 MiB and rejects a photo one byte over the limit", () => {
  const file = size => [{ raw: new File([new Uint8Array(size)], "photo.png", { type: "image/png" }) }];
  expect(fieldError(file(MAX_PHOTO_SIZE_BYTES), applicantSchema.photo.photo)).toBe("");
  expect(fieldError(file(MAX_PHOTO_SIZE_BYTES + 1), applicantSchema.photo.photo))
    .toBe("Размер фотографии не должен превышать 2 МБ");
});

test("trims nested relatives without modifying original data or File instances", () => {
  const data = questionnaire();
  data.brothers = [{ ...relative(), name: " Иван " }];
  const normalized = normalizeApplicant(data);
  expect(normalized.brothers[0].name).toBe("Иван");
  expect(data.brothers[0].name).toBe(" Иван ");
  expect(normalized.photo.photo[0].raw).toBe(data.photo.photo[0].raw);
});

test("maps nested API errors to the correct relative tab and field", () => {
  const family = [{ type: "FA" }, { type: "MO" }, { type: "BR" }, { type: "BR" }, { type: "SI" }];
  expect(applicantApiErrors({
    family: [{}, {}, {}, { contact_info: { personal_phone_number: ["Неверный телефон"] } }],
    passport: { series: ["Введите 4 цифры"] },
    image: ["Неверное изображение"],
  }, family)).toEqual([
    {
      step: "brothers", index: 1, field: "personal_phone_number", message: "Неверный телефон",
    },
    {
      step: "passport", index: null, field: "series", message: "Введите 4 цифры",
    },
    {
      step: "photo", index: null, field: "photo", message: "Неверное изображение",
    },
  ]);
});

test("keeps account errors visible without linking to a missing field", () => {
  const [error] = applicantApiErrors({ contact_info: { corporate_email: ["Неверный email"] } });
  expect(error.step).toBeNull();
  expect(error.message).toBe("Email учётной записи: Неверный email");
});

test("does not expose English or HTML server diagnostics", () => {
  expect(applicantApiErrors("<html>Server error</html>")).toEqual([]);
  expect(applicantApiErrors({ detail: "Internal validation error" })[0].message)
    .toBe("Проверьте значение поля и попробуйте ещё раз");
});
