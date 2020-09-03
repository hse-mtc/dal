<template>
  <div>
        <el-col :offset="2" :span="20" class="Absence">
            <el-row class="pageTitle">
                <h1>{{this.$route.meta.title}}</h1>
            </el-row>
            <el-tabs stretch>
                <el-tab-pane label="Пропуски">
                    <el-row class="filterRow" :gutter="20">
                        <el-col :span="6">
                            <el-input clearable placeholder="Поиск..." v-model="search" v-on:clear="onFilter" v-on:keyup.native.enter="onFilter"></el-input>
                        </el-col>
                        <el-col :span="6">
                            <el-select v-model="selectedType" clearable placeholder="Выберите тип причины" v-on:change="onFilter"
                            style="display: block">
                                <el-option
                                v-for="item in types"
                                :key="item"
                                :label="item"
                                :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="6" v-show="false">
                            <el-select v-model="selectedStatus" clearable placeholder="Выберите статус" v-on:change="onFilter"
                            style="display: block">
                                <el-option
                                v-for="item in statuses"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="6">
                            <el-date-picker
                                v-model="selectedDateRange"
                                type="daterange"
                                align="right"
                                unlink-panels
                                range-separator="До"
                                start-placeholder="Начальная дата"
                                end-placeholder="Конечная дата"
                                :picker-options="pickerOptions"
                                v-on:change="onFilter"
                                v-on:clear="onFilter"
                                format="dd.MM.yyyy"
                                value-format="yyyy-MM-dd">
                            </el-date-picker>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-table
                        :data="absences"
                        style="width: 100%"
                        max-height="680"
                        stripe>
                            <el-table-column
                            prop="date"
                            sortable
                            label="Дата"/>
                            <el-table-column
                            prop="absenceType"
                            sortable
                            label="Тип причины"/>
                            <el-table-column
                            prop="studentid.fullname"
                            sortable
                            label="ФИО"/>
                            <el-table-column
                            prop="reason"
                            sortable
                            label="Причина"/>
                            <el-table-column
                            prop="comment"
                            sortable
                            label="Комментарий"/>
                        </el-table>
                    </el-row>
                </el-tab-pane>
                <el-tab-pane label="Журнал">
                    
                </el-tab-pane>
            </el-tabs>
        </el-col>
  </div>
</template>

<script>
import { getAbsence } from '@/api/absence'
import { Message } from 'element-ui';

export default {
    name: 'Absence',
    components: {
        
    },
    data() {
        return {
            selectedType: null,
            selectedStatus: null,
            selectedDateRange: null,
            search: '',
            absences: [],
            types: [
                'Уважительная',
                'Неуважительная',
                'Опоздание',
            ],
            statuses: [
                {
                    id: 1,
                    name: 'Закрыт'
                },
                {
                    id: 2,
                    name: 'Открыт'
                }
            ],
            pickerOptions: {
                shortcuts: [{
                    text: 'Неделя',
                    onClick(picker) {
                    const end = new Date();
                    const start = new Date();
                    start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                    picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: 'Месяц',
                    onClick(picker) {
                    const end = new Date();
                    const start = new Date();
                    start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                    picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '3 месяца',
                    onClick(picker) {
                    const end = new Date();
                    const start = new Date();
                    start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                    picker.$emit('pick', [start, end]);
                    }
                }]
            },
        }
    },
    created() {
        this.fetchData();
    },
    methods: {
        onFilter(){
            const d = this.selectedDateRange == null ? null : this.selectedDateRange[0];
            getAbsence({
                date: d, 
                absenceType: this.selectedType, 
                status: this.selectedStatus,
                name: this.search
            }).then(response => {
                this.absences = response.absences;
                console.log(this.absences);
            }).catch(error => {
                Message('Ошибка получения пропусков!');
            });
        },
        fetchData(){
            getAbsence().then(response => {
                this.absences = response.absences;
                console.log(this.absences);
            }).catch(error => {
                Message('Ошибка получения пропусков!');
            });
        }
    },
}
</script>

<style scoped lang="scss">
  @import "style";
</style>
