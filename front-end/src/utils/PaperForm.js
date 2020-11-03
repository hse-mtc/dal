import moment from "moment"
import has from "lodash/has"

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
  ) {
    this.annotation = annotation
    this.authors = authors
    this.category = category
    this.files = files
    this.publicationDate = publicationDate
    this.publishers = publishers
    this.tags = tags
    this.title = title
  }

  getContent(action) {
    if (action === "add" || has(this.files[0], "raw")) {
      return this.files[0].raw
    } else {
      return null
    }
  }

  getData() {
    const data = {
      annotation: this.annotation.trim(),
      authors: this.authors,
      category: this.category,
      publishers: this.publishers,
      tags: this.tags,
      title: this.title.trim(),
    }

    const date = this.publicationDate
    if (date) {
      data.publication_date = moment(date).format("YYYY-MM-DD")
    }

    return data
  }

  split(action) {
    if (!["add", "edit"].includes(action)) {
      throw new TypeError("PaperForm: unknown action")
    }

    return {
      data: this.getData(),
      content: this.getContent(action),
    }
  }
}

