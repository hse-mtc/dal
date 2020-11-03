import moment from "moment"
import has from "lodash/has"

export default class PaperForm {
  constructor(
      annotation = "",
      authors = [],
      category = "",
      files = [],
      publication_date = "",
      publishers = [],
      tags = [],
      title = "",
  ) {
    this.annotation = annotation
    this.authors = authors
    this.category = category
    this.files = files
    this.publication_date = publication_date
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

    const date = this.publication_date || ""
    if (date !== "") {
      data.publication_date = moment(date).format("YYYY-MM-DD")
    }

    return data
  }

  split(action) {
    if (["add", "edit"].indexOf(action) === -1) {
      throw TypeError("PaperForm: unknown action")
    }

    return {
      data: this.getData(),
      content: this.getContent(action),
    }
  }
}

