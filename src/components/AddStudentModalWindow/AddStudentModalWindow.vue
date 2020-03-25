<template>
    <div class="addModal">
        <el-form ref="form" :model="form" label-width="250px">
            <el-form-item label="Фото">
                <el-upload
                    class="avatar-uploader"
                    action="https://jsonplaceholder.typicode.com/posts/"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :before-upload="beforeAvatarUpload">
                    <img v-if="form.foto" :src="form.foto" class="avatar">
                    <i v-else class="el-icon-picture-outline avatar-uploader-icon"></i>
                    </el-upload>
            </el-form-item>

            <el-form-item label="Фамилия">
                <el-input clearable v-model="form.surname" placeholder="Введите фамилию"></el-input>
            </el-form-item>

            <el-form-item label="Имя">
                <el-input clearable placeholder="Введите имя" v-model="form.name"></el-input>
            </el-form-item>

            <el-form-item label="Отчество">
                <el-input clearable v-model="form.patronymic" placeholder="Введите отчество"></el-input>
            </el-form-item>
            
            <el-form-item label="Взвод">
                <el-select v-model="form.milgroup" placeholder="Выберите взвод">
                    <el-option
                            v-for="item in milgroups"
                            :key="item"
                            :value="item"
                            :label="item"
                    />
                </el-select>
            </el-form-item>
            <el-form-item label="Образовательная программа">
                <el-select v-model="form.program" placeholder="Выберите программу">
                    <el-option
                            v-for="item in programs"
                            :key="item"
                            :value="item"
                            :label="item"
                    />
                </el-select>
            </el-form-item>

            <el-form-item label="Дата рождения">
                    <el-date-picker
                            v-model="form.birthdate"
                            type="date"
                            placeholder="Выберите дату рождения"
                            format="dd.MM.yyyy">
                    </el-date-picker>
            </el-form-item>
            
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Отправить</el-button>
                <el-button @click="closeModal">Отменить</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    import moment from 'moment'
    import EventBus from '../EventBus';

    export default {
        name: "AddStudentModalWindow",
        data() {
            return {
                form: {
                    surname: '',
                    name: '',
                    patronymic: '',
                    milgroup: '',
                    milfaculty: '',
                    birthdate: '',
                    program: '',
                    code: '',
                    foto: null,
                    status: 'Обучается'
                },
                milgroups: [/* ...this.$store.getters.milgroups */"1807", "1808", "1809"],
                programs: [/* ...this.$store.getters.programs */"Информатика и вычислительная техника", "Программная инженерия", "Машиностроение"],
                statuses: ["Обучается", "Отчислен", "Завершил"]
            }
        },
        created() {
            this.fetchData()
        },
        updated() {
            console.log(this.form.fileList)
        },
        methods: {
            fetchData() {
                
            },
            handleAvatarSuccess(res, file) {
                this.form.foto = URL.createObjectURL(file.raw);
                console.log("handleAvatarSuccess -> this.form.foto", this.form.foto)
            },
            beforeAvatarUpload(file) {
                const isJPG = file.type === 'image/jpeg';
                const isLt2M = file.size / 1024 / 1024 < 2;

                if (!isJPG) {
                    this.$message.error('Avatar picture must be JPG format!');
                }
                if (!isLt2M) {
                    this.$message.error('Avatar picture size can not exceed 2MB!');
                }
                return isJPG && isLt2M;
            },
            onSubmit() {
                if (this.form.title !== '') {
                    let formData = new FormData();
                    this.$route.query.section === 'scienceArticles' ? formData.append('category', 'Article') : formData.append('category', 'Research')
                    formData.append('title', this.form.title);

                    if (this.form.annotation !== '') formData.append('annotation', this.form.annotation);

                    if (this.form.author !== '') {
                        if (this.form.author === -1) {
                            formData.append('authorName', this.form.newAuthorName);
                            formData.append('authorLastName', this.form.newAuthorLastName);
                            formData.append('authorPatronymic', this.form.newAuthorPatronymic);
                        } else {
                            formData.append('authorId', this.form.author);
                        }
                    }

                    if (this.form.publisher !== '') {
                        if (this.form.publisher === -1) {
                            formData.append('newPublisher', this.form.newPublisher);
                        } else {
                            formData.append('publisherId', this.form.publisher);
                        }
                    }

                    if (this.form.publicationDate !== '') {
                        formData.append('date', moment(this.form.publicationDate).format('DD.MM.YYYY'));
                    }

                    if (this.form.selectedTags.length !== 0) {
                        formData.append('keywords', JSON.stringify( this.form.selectedTags));
                    }

                    if (this.form.fileList.length !== 0) {
                        formData.append('file', this.form.fileList[0].raw);
                        /* uploadDocs(formData)
                            .then(function(){
                            EventBus.$emit('UPDATE_EVENT');
                            self.$emit('closeModal');
                            }).catch(function(){
                                console.log('FAILURE!!');
                            }); */
                    } else {
                        this.$message.error(`Приложите файл`);
                    }

                    for (var key of formData.entries()) {
                        console.log(key[0] + ', ' + key[1])
                    }


                } else {
                    this.$message.error(`Заполните название документа`);
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
