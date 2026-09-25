/* global jest */
import { getFormationRosterCount } from "@/api/formations";
import Formations from "./Formations.vue";

jest.mock("@/store", () => ({ UserModule: {}, ReferenceModule: {} }));
jest.mock("@/utils/request", () => jest.fn());

jest.mock("@/api/formations", () => ({
  getFormationRosterCount: jest.fn(),
}));

const makePage = () => ({
  selectedGroup: { id: 1 },
  selectedGroupId: 1,
  report: null,
  canEditReport: true,
  contextKey: "2026-09-25/1",
  form: { roster_count: null, excused_count: 0 },
  setForm(form) { this.form = form; },
});

it("prefills only positive counts and keeps a manual correction made while loading", async() => {
  const page = makePage();
  getFormationRosterCount.mockResolvedValueOnce({ data: { count: 2 } });
  await Formations.methods.prefillRosterCount.call(page);
  expect(page.form.roster_count).toBe(2);

  page.form = { ...page.form, roster_count: null };
  getFormationRosterCount.mockResolvedValueOnce({ data: { count: 0 } });
  await Formations.methods.prefillRosterCount.call(page);
  expect(page.form.roster_count).toBeNull();

  let resolveCount;
  getFormationRosterCount.mockReturnValueOnce(new Promise(resolve => { resolveCount = resolve; }));
  const pending = Formations.methods.prefillRosterCount.call(page);
  page.form = { ...page.form, roster_count: 7 };
  resolveCount({ data: { count: 2 } });
  await pending;
  expect(page.form.roster_count).toBe(7);
});
