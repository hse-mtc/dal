<template>
    <div class="addModal">
        <el-form ref="form" :model="form" label-width="175px">
            <el-form-item label="Название документа">
                <el-input v-model="form.title" placeholder="Введите название"></el-input>
            </el-form-item>

            <el-form-item label="Аннотация">
                <el-input type="textarea" placeholder="Введите текст аннотации" v-model="form.annotation" :autosize="{ minRows: 2}"></el-input>
            </el-form-item>

            <el-form-item label="Автор">
                <el-select clearable v-model="form.author" placeholder="Выберите автора">
                    <el-option
                            v-for="item in authors"
                            :key="item.value"
                            :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <div v-if="form.author === 'Добавить нового'" class="add-author">
                <el-form-item label="Фамилия">
                    <el-input v-model="form.newAuthorLastName" placeholder="Введите фамилию"></el-input>
                </el-form-item>
                <el-form-item label="Имя">
                    <el-input v-model="form.newAuthorName" placeholder="Введите имя"></el-input>
                </el-form-item>
                <el-form-item label="Отчество">
                    <el-input v-model="form.newAuthorPatronymic" placeholder="Введите отчество"></el-input>
                </el-form-item>
            </div>

            <el-form-item label="Размещение">
                <el-select clearable v-model="form.publisher" placeholder="Выберите журнал">
                    <el-option
                            v-for="item in publishers"
                            :key="item.value"
                            :value="item.value"
                    />
                </el-select>
            </el-form-item>

            <div v-if="form.publisher === 'Добавить новое'" class="add-publishers">
                <el-form-item label="Название размещения">
                    <el-input v-model="form.newAuthorName" placeholder="Введите имя"></el-input>
                </el-form-item>
            </div>

            <el-form-item label="Дата публикации">
                    <el-date-picker
                            v-model="form.publicationDate"
                            type="date"
                            placeholder="Выберите дату"
                            format="dd.MM.yyyy">
                    </el-date-picker>
            </el-form-item>

            <el-form-item label="Ключевые слова">
                <tags-input element-id="tags"
                            v-model="form.selectedTags"
                            :existing-tags="existingTags"
                            :typeahead="true"
                            placeholder="Добавить ключевое слово"
                            :typeahead-hide-discard="true">
                </tags-input>
            </el-form-item>

<!--            <el-form-item>-->
<!--                <div class="add-files">-->
<!--                    <div class="add-files-title">Загрузите новый материал</div>-->
<!--                    <div class="add-files-subtitle">Файл в формате: pdf, pptx, doc, docx, xls, xlsx</div>-->
<!--                    <div class="add-files-container">-->
<!--                        <div class="large-12 medium-12 small-12 cell">-->
<!--                            <label>-->
<!--                                <input type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()"/>-->
<!--                            </label>-->
<!--                        </div>-->
<!--                        <div class="large-12 medium-12 small-12 cell">-->
<!--                            <div v-for="(file, key) in form.files" class="file-listing">{{ file.name }} <span class="remove-file" v-on:click="removeFile( key )">Remove</span></div>-->
<!--                        </div>-->
<!--                        <div class="large-12 medium-12 small-12 cell">-->
<!--                            <button v-on:click="addFiles()">Add Files</button>-->
<!--                        </div>-->
<!--                    </div>-->
<!--                </div>-->
<!--            </el-form-item>-->
        </el-form>
    </div>
</template>

<script>
    import {getExistingTags} from "../../api/existingTags";

    export default {
        name: "AddModalWindow",
        data() {
            return {
                form: {
                    title: '',
                    author: '',
                    annotation: '',
                    publicationDate: '',
                    newAuthorName: '',
                    newAuthorLastName: '',
                    newAuthorPatronymic: '',
                    publisher: '',
                    tags: [
                        { name: 'Tag 2', type: 'success' },
                        { name: 'Tag 3', type: 'info' },
                        { name: 'Tag 4', type: 'warning' },
                        { name: 'Tag 5', type: 'danger' }
                    ],
                    selectedTags: [{}],
                    files: []
                },
                existingTags: [
                    { key: 1, value: 'Стратегия' },
                    { key: 2, value: 'Тактика' },
                    { key: 3, value: 'Хуяктика' },
                ],
                authors: [{value: 'Добавить нового'}, ...this.$store.getters.authors],
                publishers: [{value: 'Добавить новое'}, ...this.$store.getters.publishers],
            }
        },
        created() {
            this.fetchData()
        },
        methods: {
            fetchData() {
                getExistingTags()
                    .then(response => {
                        this.existingTags = response.data
                    }).catch(() => {
                    console.log('Данные по тегам не указаны')
                    })
            },
            onSubmit() {
                console.log('submit!');
            },
            addFiles(){
                this.$refs.files.click();
            },
            submitFiles(){

                let formData = new FormData();
                for( var i = 0; i < this.form.files.length; i++ ){
                    let file = this.from.files[i];
                    formData.append('files[' + i + ']', file);
                }
                // axios.post( '/select-files',
                //     formData,
                //     {
                //         headers: {
                //             'Content-Type': 'multipart/form-data'
                //         }
                //     }
                // ).then(function(){
                //     console.log('SUCCESS!!');
                // })
                //     .catch(function(){
                //         console.log('FAILURE!!');
                //     });
            },
            handleFilesUpload(){
                let uploadedFiles = this.$refs.files.files;
                for( var i = 0; i < uploadedFiles.length; i++ ){
                    this.form.files.push( uploadedFiles[i] );
                }
            },
            removeFile( key ){
                this.form.files.splice( key, 1 );
            }
        }
    }
</script>

<style scoped lang="scss">
    @import "style.scss";

    .el-tag + .el-tag {
        margin-left: 10px;
    }
    .button-new-tag {
        margin-left: 10px;
        height: 32px;
        line-height: 30px;
        padding-top: 0;
        padding-bottom: 0;
    }
    .input-new-tag {
        width: 90px;
        margin-left: 10px;
        vertical-align: bottom;
    }
</style>
