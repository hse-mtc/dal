<template>
  <div>
        <el-col :offset="2" :span="20" class="Absence">
            <el-row class="pageTitle">
                <h1>{{this.$route.meta.title}}</h1>
            </el-row>
            <el-tabs stretch>
                <el-tab-pane label="Пропуски">
                    <el-row class="filterRow" :gutter="20">
                        <el-col :span="5">
                            <el-input clearable placeholder="Поиск..." v-model="filter.search" v-on:clear="onFilter" v-on:keyup.native.enter="onFilter"></el-input>
                        </el-col>
                        <el-col :span="4">
                            <el-select v-model="filter.type" clearable placeholder="Выберите тип причины" v-on:change="onFilter"
                            style="display: block">
                                <el-option
                                v-for="item in types"
                                :key="item"
                                :label="item"
                                :value="item">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="4">
                            <el-select v-model="filter.status" clearable placeholder="Выберите статус" v-on:change="onFilter"
                            style="display: block">
                                <el-option
                                v-for="item in statuses"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="4">
                            <el-select v-model="filter.mg" value-key="milgroup" clearable placeholder="Выберите взвод" v-on:change="onFilter"
                            style="display: block">
                                <el-option
                                    v-for="item in milgroups"
                                    :key="item.milgroup"
                                    :label="item.milgroup"
                                    :value="item">
                                    <span style="float: left">{{ item.milgroup }}</span>
                                    <span style="float: right; color: #8492a6; font-size: 13px">{{ item.milfaculty }}</span>
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="5">
                            <el-date-picker
                                v-model="filter.dateRange"
                                type="daterange"
                                align="right"
                                unlink-panels
                                range-separator="по"
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
                            sortable
                            label="Тип причины"> 
                                <template slot-scope="scope">
                                    <el-tag
                                    :type="scope.row.absenceType === 'Неуважительная' ? 'danger' : 
                                        (scope.row.absenceType === 'Опоздание' ? 'warning' : 'success')"
                                    disable-transitions>{{scope.row.absenceType}}</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column
                            prop="studentid.fullname"
                            sortable
                            show-overflow-tooltip
                            label="ФИО"/>
                            <el-table-column
                            prop="studentid.milgroup.milgroup"
                            sortable
                            label="Взвод"/>
                            <el-table-column
                            prop="reason"
                            sortable
                            label="Причина"/>
                            <el-table-column
                            prop="comment"
                            label="Комментарий"/>
                        </el-table>
                    </el-row>
                </el-tab-pane>
                <el-tab-pane label="Журнал">
                    <el-table
                    :data="journal.students"
                    style="width: 100%"
                    max-height="680"
                    stripe
                    border>
                        <el-table-column
                        width="250"
                        prop="fullname"
                        label="ФИО"
                        show-overflow-tooltip
                        fixed/>
                        <el-table-column
                        v-for="d in dates"
                        :key="d"
                        :label="d"
                        align="center">
                        <template slot-scope="scope">
                            <el-popover
                                v-if="scope.row.absences[d] !== undefined" 
                                placement="top"
                                width="400"
                                trigger="hover">
                                <el-form label-position="right" label-width="150px" size="mini" :model="scope.row.absences[d]">
                                    <el-form-item label="Тип причины: ">
                                        <el-tag
                                        :type="scope.row.absences[d].absenceType === 'Неуважительная' ? 'danger' : 
                                        (scope.row.absences[d].absenceType === 'Опоздание' ? 'warning' : 'success')"
                                        disable-transitions>
                                            {{scope.row.absences[d].absenceType}}
                                        </el-tag>
                                    </el-form-item>
                                    <el-form-item label="Причина: ">
                                        {{scope.row.absences[d].reason}}
                                    </el-form-item>
                                    <el-form-item label="Комментарий: ">
                                        {{scope.row.absences[d].comment}}
                                    </el-form-item>
                                </el-form>
                                <i slot="reference"
                                :class="scope.row.absences[d].status === 'Открыт' ? 'el-icon-circle-close' : 'el-icon-circle-check'" 
                                :style="scope.row.absences[d].status === 'Открыт' ? 'color: red' : 'color: green'" />
                            </el-popover>
                        </template>
                        </el-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </el-col>
  </div>
</template>

<script>
import { getAbsence } from '@/api/absence'
import { Message } from 'element-ui';
import moment from 'moment'

export default {
    name: 'Absence',
    components: {
        
    },
    data() {
        return {
            filter: {
                type: null,
                status: null,
                dateRange: [moment().format('YYYY-MM-DD'), moment().format('YYYY-MM-DD')],
                search: null,
                mg: null
            },
            absences: [],
            types: [
                'Уважительная',
                'Неуважительная',
                'Опоздание',
            ],
            statuses: [
                {
                    id: 0,
                    name: 'Закрыт'
                },
                {
                    id: 1,
                    name: 'Открыт'
                }
            ],
            milgroups: [
                {
                    milgroup: "1807",
                    milfaculty: "ВКС",
                },
                {
                    milgroup: "1808",
                    milfaculty: "ВКС",
                },
                {
                    milgroup: "1809",
                    milfaculty: "ВКС",
                },
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

            dates: [
                '04.09.20',
                '11.09.20',
                '18.09.20',
                '25.09.20',
                '01.10.20',
                '08.10.20',
                '15.10.20',
                '22.10.20',
                '29.10.20',
                '05.11.20',
                '12.11.20',
                '19.11.20',
                '26.11.20',
                '03.12.20',
                '10.12.20',
            ],
            journal: {
                milgroup: {
                    milgroup: '1809',
                    milfaculty: 'ВКС',
                },
                students: [
                    {
                        id: 1,
                        fullname: 'Хромов Григорий Александрович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: 'Не захотел'
                            }
                        }
                    },
                    {
                        id: 2,
                        fullname: 'Кацевалов Артем Сергеевич',
                        absences: {
                            '11.09.20': {
                                absenceType: 'Уважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Коронавирус'
                            },
                            '15.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 3,
                        fullname: 'Кацевалов Григорий Александрович',
                        absences: {
                            '11.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 4,
                        fullname: 'Иванов Иван Иванович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Уважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 5,
                        fullname: 'Исаков Владислав Евгеньевич',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '11.09.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 6,
                        fullname: 'Хромов Григорий Александрович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 7,
                        fullname: 'Хромов Григорий Александрович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 8,
                        fullname: 'Хромов Григорий Александрович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 9,
                        fullname: 'Хромов Григорий Александрович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                    {
                        id: 10,
                        fullname: 'Хромов Григорий Александрович',
                        absences: {
                            '04.09.20': {
                                absenceType: 'Неуважительная',
                                status: 'Закрыт',
                                reason: 'Болезнь',
                                comment: 'Немножко приболел'
                            },
                            '22.10.20': {
                                absenceType: 'Уважительная',
                                status: 'Открыт',
                                reason: 'Прогул',
                                comment: ''
                            }
                        }
                    },
                ],
            }
        }
    },
    created() {
        this.onFilter();
    },
    methods: {
        onFilter(){
            getAbsence({
                date_from: this.filter.dateRange[0], 
                date_to: this.filter.dateRange[1], 
                absenceType: this.filter.type, 
                status: this.filter.status,
                name: this.filter.search,
                milgroup: this.filter.mg
            }).then(response => {
                this.absences = response.data.absences;
                console.log(this.absences);
            }).catch(() => {
                Message('Ошибка получения пропусков!');
            });
        },
    },
}
</script>

<style scoped lang="scss">
  @import "style";
</style>
