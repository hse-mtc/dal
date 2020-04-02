<template>
    <div class="addModal">
        <el-form ref="form" :model="form" :rules="rules" label-width="250px">
            <el-form-item label="Фото">
                <el-upload
                    class="avatar-uploader"
                    action="https://jsonplaceholder.typicode.com/posts/"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :before-upload="beforeAvatarUpload">
                    <img v-if="form.photo" :src="form.photo" class="avatar">
                    <i v-else class="el-icon-picture-outline avatar-uploader-icon"></i>
                    </el-upload>
            </el-form-item>

            <el-form-item label="Фамилия" prop="surname">
                <el-input clearable v-model="form.surname" placeholder="Введите фамилию"></el-input>
            </el-form-item>

            <el-form-item label="Имя" prop="name">
                <el-input clearable placeholder="Введите имя" v-model="form.name"></el-input>
            </el-form-item>

            <el-form-item label="Отчество" prop="patronymic">
                <el-input clearable v-model="form.patronymic" placeholder="Введите отчество"></el-input>
            </el-form-item>
            
            <el-form-item label="Взвод" prop="milgroup">
                <el-select v-model="form.milgroup" value-key="milgroup" placeholder="Выберите взвод">
                    <el-option
                        v-for="item in milgroups"
                        :key="item.milgroup"
                        :label="item.milgroup"
                        :value="item">
                        <span style="float: left">{{ item.milgroup }}</span>
                        <span style="float: right; color: #8492a6; font-size: 13px">{{ item.milfaculty }}</span>
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="Образовательная программа" prop="program">
                <el-select v-model="form.program" value-key="code" placeholder="Выберите программу">
                    <el-option
                        v-for="item in programs"
                        :key="item.code"
                        :label="item.program"
                        :value="item">
                        <span style="float: left">{{ item.program }}</span>
                        <span style="float: right; color: #8492a6; font-size: 13px">{{ item.code }}</span>
                    </el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="Дата рождения" prop="birthdate">
                    <el-date-picker
                            v-model="form.birthdate"
                            type="date"
                            placeholder="Выберите дату рождения"
                            format="dd.MM.yyyy"
                            value-format="dd.MM.yyyy">
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
import { putStudent } from '../../api/student';

    export default {
        name: "AddStudentModalWindow",
        data() {
            return {
                form: {
                    milgroup: null,
                    program: null,
                    birthdate: '',
                    surname: '',
                    name: '',
                    patronymic: '',
                    photo: null,
                    status: 'Обучается'
                },
                rules: {
                    surname: [
                        { required: true, message: 'Пожалуйста, введите фамилию', trigger: 'blur' }
                    ],
                    name: [
                        { required: true, message: 'Пожалуйста, введите имя', trigger: 'blur' }
                    ],
                    milgroup: [
                        { required: true, message: 'Пожалуйста, выберите взвод', trigger: 'change' }
                    ],
                    program: [
                        { required: true, message: 'Пожалуйста, выберите обр. программу', trigger: 'change' }
                    ],
                    birthdate: [
                        { type: 'string', required: true, message: 'Пожалуйста, выберите дату рождения', trigger: 'change' }
                    ]
                },
                milgroups: [/* ...this.$store.getters.milgroups */{milgroup: 1807, milfaculty: "ВКС"}, {milgroup: 1808, milfaculty: "ВКС"}, {milgroup: 1809, milfaculty: "ВКС"}, {milgroup: 1810, milfaculty: "РВСН"}],
                programs: [/* ...this.$store.getters.programs */{program: "Информатика и вычислительная техника", code: "09.03.01"}, {program: "Программная инженерия", code: "09.03.04"}, {program: "Машиностроение", code: "05.02.02"}],
                statuses: ["Обучается", "Отчислен", "Завершил"]
            }
        },
        created() {
            this.fetchData()
        },
        methods: {
            fetchData() {
                
            },
            handleAvatarSuccess(res, file) {
                this.form.foto = URL.createObjectURL(file.raw);
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
                this.$refs['form'].validate((valid) => {
                    if (valid){
                        putStudent(this.form)
                        .then(() => {
                            this.$message.success('Новый студент успешно добавлен.');
                            this.closeModal();
                        })
                        .catch(() => {
                            this.$message.error('Ошибка при добавлении студента.');
                        });
                    }
                });
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
