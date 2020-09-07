<template>
    <div class="addModal">
        <el-form ref="form" :model="form" label-width="175px">
            <el-form-item label="Название категории">
                <el-input v-model="form.title" placeholder="Введите название"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Добавить</el-button>
                <el-button @click="closeModal">Отменить</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import EventBus from '../EventBus';
    import {addPaperCategories} from "../../api/paper_categories";

    export default {
        name: "AddCategoryModalWindow",
        data() {
            return {
                form: {
                    title: ''
                }
            }
        },
        created() {
        },
        updated() {
        },
        methods: {
            onSubmit() {
                const self = this
                if (this.form.title.trim() !== '') {
                    addPaperCategories(this.form.title)
                        .then(function(){
                            EventBus.$emit('UPDATE_CATEGORY');
                            self.$emit('closeModal');
                        })
                }
            },
            closeModal() {
                this.$emit('closeModal');
            }
        }
    }
</script>

<style scoped lang="scss">
    @import "style.scss";
</style>
