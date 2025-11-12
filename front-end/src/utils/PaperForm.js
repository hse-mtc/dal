import moment from "moment";
import has from "lodash/has";

export default class PaperForm {
  constructor(
    annotation = "",
    authors = [],
    category = "",
    files = [],
    publicationDate = "",
    publishers = [],
    tags = [],
    title = "",
    categoryFilters = {},
  ) {
    this.annotation = annotation;
    this.authors = authors;
    this.category = category;
    this.files = files;
    this.publicationDate = publicationDate;
    this.publishers = publishers;
    this.tags = tags;
    this.title = title;
    this.categoryFilters = categoryFilters;
  }

  getContent(action) {
    if (action === "add" || has(this.files[0], "raw")) {
      return this.files[0].raw;
    }
    return null;
  }

  getData() {
    const data = {
      annotation: this.annotation.trim(),
      authors: this.authors,
      category: this.category,
      publishers: this.publishers,
      tags: this.tags,
      title: this.title.trim(),
    };

    const date = this.publicationDate;
    if (date) {
      data.publication_date = moment(date).format("YYYY-MM-DD");
    }

    if (this.categoryFilters && Object.keys(this.categoryFilters).length > 0) {
      const additional = {};
      Object.keys(this.categoryFilters).forEach(filterName => {
        const filterValue = this.categoryFilters[filterName];
        if (filterValue !== null && filterValue !== undefined && filterValue !== "") {
          additional[filterName] = filterValue;
        }
      });
      if (Object.keys(additional).length > 0) {
        data.additional_fields = additional;
      }
    }

    return data;
  }

  split(action) {
    if (!["add", "edit"].includes(action)) {
      throw new TypeError("PaperForm: unknown action");
    }

    return {
      data: this.getData(),
      content: this.getContent(action),
    };
  }
}
