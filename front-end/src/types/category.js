export const CategoryFilterType = {
  STRING: "string",
  NUMBER: "number",
};

export const createCategoryFilter = (filtername = "", type = CategoryFilterType.STRING) => ({
  filtername,
  type,
});

export const createCategory = (name = "", filters = []) => ({
  name,
  filters,
});
