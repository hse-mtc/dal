<template>
  <ExpandBox title="Заметки" @toggled="toggled">
    <div v-loading="loading" class="notes">
      <TableEditor
        type="notes"
        :data="notes"
        @addItem="onAddItem"
        @startEdit="onStartEdit"
        @abortEdit="onAbortEdit"
        @submitEdit="onSubmitEdit"
        @delete="onDelete"
      />
    </div>
  </ExpandBox>
</template>

<script>
import ExpandBox from "@/components/ExpandBox/ExpandBox.vue";
import TableEditor from "@/components/Apanel/Dictionaries/TableEditor.vue";
import {
  postError, getError, patchError, deleteError,
} from "@/utils/message";
import {
  findStudentNotes,
  postStudentNote,
  patchStudentNote,
  deleteStudentNote,
} from "@/api/students";
import _omit from "lodash/omit";

export default {
  name: "StudentNotes",
  components: { ExpandBox, TableEditor },
  data() {
    return {
      notes: [],
      loading: false,
      editingItemId: null,
      editingData: null,
      editorDefenition: {
        label: "Заметки",
        async add(data) {
          try {
            this.loading = false;
            await postStudentNote(data);
          } catch (err) {
            postError("заметки о студенте");
          } finally {
            this.loading = false;
          }
        },
        async delete(id) {
          try {
            this.loading = false;
            await deleteStudentNote(id);
          } catch (err) {
            deleteError("заметки о студенте");
          } finally {
            this.loading = false;
          }
        },
        async edit(data) {
          try {
            this.loading = false;
            await patchStudentNote(data);
          } catch (err) {
            patchError("заметки о студенте");
          } finally {
            this.loading = false;
          }
        },
      },
    };
  },
  computed: {
    id() {
      return this.$route.params.studentId;
    },
  },
  methods: {
    async toggled(expanded) {
      if (expanded) {
        await this.fetchInfo();
      }
    },
    async fetchInfo() {
      try {
        this.loading = true;
        this.notes = (await findStudentNotes(this.id)).data;
      } catch (err) {
        getError("заметок о студенте", err.response.status);
      } finally {
        this.loading = false;
      }
    },
    async onAddItem(data) {
      await this.editorDefenition.add({ student: +this.id, ...data });
      await this.fetchInfo();
    },
    async onDelete(id) {
      await this.$confirm("Вы уверены, что хотите удалить?", "Подтверждение", {
        confirmButtonText: "Да",
        cancelButtonText: "Отмена",
        type: "warning",
      });

      await this.editorDefenition.delete(id);
      await this.fetchInfo();
    },
    onStartEdit(id) {
      this.editingItemId = id;
      this.editingData = _omit(
        this.notes.find(item => item.id === id),
        ["id"],
      );
    },
    onAbortEdit() {
      this.editingItemId = null;
      this.editingData = null;
    },
    async onSubmitEdit(data) {
      const res = await this.editorDefenition.edit({
        id: this.editingItemId,
        ...data,
      });
      await this.fetchInfo();

      if (res) {
        this.onAbortEdit();
      }
    },
  },
};
</script>

<style lang="scss" scoped>
@import "style";
</style>
