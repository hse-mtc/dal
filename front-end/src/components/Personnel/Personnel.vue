<template>
  <div>
    <el-col :offset="2" :span="20" class="Personnel">
		<el-row class="pageTitle">
			<h1>{{this.$route.meta.title}}</h1>
		</el-row>
		<el-tabs v-model="selectedSection" @tab-click="onFilter" stretch>
			<el-tab-pane name="students" label="Студенты">
				<el-row class="filterRow" :gutter="20" style="margin-bottom: 15px">
					<el-col :span="8">
						<el-input clearable placeholder="Поиск..." v-model="filterS.search" v-on:clear="onFilter" v-on:keyup.native.enter="onFilter"></el-input>
					</el-col>
					<el-col :span="7">
						<el-select v-model="filterS.milgroup" value-key="milgroup" clearable placeholder="Выберите взвод" v-on:change="onFilter"
						style="display: block">
							<el-option
								v-for="item in milgroups"
								:key="item.milgroup"
								:value="item.milgroup">
								<span style="float: left">{{ item.milgroup }}</span>
								<span style="float: right; color: #8492a6; font-size: 13px">{{ item.milfaculty }}</span>
							</el-option>
						</el-select>
					</el-col>
					<el-col :span="7">
						<el-select v-model="filterS.status" clearable placeholder="Выберите статус" v-on:change="onFilter"
						style="display: block">
							<el-option
							v-for="item in statuses"
							:key="item"
							:label="item"
							:value="item">
							</el-option>
						</el-select>
					</el-col>
					<el-col :span="2">
						<el-button type="text" @click="clearFilter">Сбросить</el-button>
					</el-col>
				</el-row>
				<el-row class="addRow">
					<el-col :span="24">
						<el-button 
							class="addBtn" 
							type="primary" 
							icon="el-icon-plus" 
							@click="openModal">
							Новый студент
						</el-button>
					</el-col>
				</el-row>
				<el-row class="table">
					<el-table
						max-height="600px"
						:data="studentsData" 
						:default-sort = "{prop: 'milgroup.milgroup', order: 'ascending'}" 
						stripe>
						<el-table-column width="300px" sortable show-overflow-tooltip
							prop="fullname"
							label="ФИО">
						</el-table-column>
						<el-table-column sortable 
							prop="milgroup.milgroup"
							label="Взвод">
						</el-table-column>
						<el-table-column
							prop="milgroup.milfaculty"
							label="Цикл">
						</el-table-column>
						<el-table-column width="300px" show-overflow-tooltip
							prop="program.program"
							label="Программа">
						</el-table-column>
						<el-table-column
							prop="birthdate"
							label="Дата рождения">
						</el-table-column>
						<el-table-column
							prop="status"
							label="Статус">
						</el-table-column>
						<el-table-column
							label=""
							width="115px">
							<template slot-scope="scope">
								<el-button
								size="mini"
								icon="el-icon-edit"
								type="info"
								circle
								@click="onEdit(scope.row)"></el-button>
								<el-button
								size="mini"
								icon="el-icon-delete"
								type="danger"
								circle
								@click="onDelete(scope.row.id)"></el-button>
							</template>
						</el-table-column>
						</el-table>
					</el-row>
				</el-tab-pane>
			<el-tab-pane name="teachers" label="Преподаватели">
				<el-row class="filterRow" :gutter="20" style="margin-bottom: 15px">
					<el-col :span="8">
						<el-input clearable placeholder="Поиск..." v-model="filterT.search" v-on:clear="onFilter" v-on:keyup.native.enter="onFilter"></el-input>
					</el-col>
					<el-col :span="7">
						<el-select v-model="filterT.milfaculty" clearable placeholder="Выберите цикл" v-on:change="onFilter"
						style="display: block">
							<el-option
								v-for="item in milfaculties"
								:key="item"
								:label="item"
								:value="item">
							</el-option>
						</el-select>
					</el-col>
					<el-col :offset="7" :span="2">
						<el-button type="text" @click="clearFilter">Сбросить</el-button>
					</el-col>
				</el-row>
				<el-row class="addRow">
					<el-col :span="24">
						<el-button 
							class="addBtn" 
							type="primary" 
							icon="el-icon-plus" 
							@click="openModal">
							Новый преподаватель
						</el-button>
					</el-col>
				</el-row>
				<el-row class="table">
					<el-table 
						max-height="600px"
						:data="teachersData" 
						:default-sort = "{prop: 'milgroup.milgroup', order: 'ascending'}" 
						stripe>
						<el-table-column width="400px"
							prop="fullname"
							label="ФИО">
						</el-table-column>
						<el-table-column
							prop="milfaculty"
							label="Цикл">
						</el-table-column>
						<el-table-column
							prop="rank"
							label="Звание">
						</el-table-column>
						<el-table-column
							prop="post"
							label="Должность">
						</el-table-column>
						<el-table-column
							prop="milgroup.milgroup"
							label="Прикр. взвод">
						</el-table-column>
						<el-table-column
							label=""
							width="115px">
							<template slot-scope="scope">
								<el-button
								size="mini"
								icon="el-icon-edit"
								type="info"
								circle
								@click="onEdit(scope.row)"></el-button>
								<el-button
								size="mini"
								icon="el-icon-delete"
								type="danger"
								circle
								@click="onDelete(scope.row.id)"></el-button>
							</template>
						</el-table-column>
					</el-table>
				</el-row>
			</el-tab-pane>
		</el-tabs>
    </el-col>
    <AddStudentModalWindow v-if="addModal" v-on:closeModal="closeModal" v-on:submitModal="clearFilter" v-bind:student="editStudent"/>
    <div v-if="addModal" class="background" @click="closeModal"></div>
  </div>
</template>

<script>
import { getStudent, deleteStudent } from '@/api/student'
import { getTeacher, deleteTeacher } from '@/api/teacher'
import AddStudentModalWindow from "../AddStudentModalWindow/AddStudentModalWindow";
import { Message } from 'element-ui';
import moment from 'moment'

export default {
	name: '',
	components: {
		AddStudentModalWindow
	},
	data() {
		return {
			filterS: {
				search: null,
				milgroup: null,
				status: null,
			},
			filterT: {
				search: null,
				milfaculty: null,
			},
			studentsData: [], teachersData: [],
			addModal: false,
			statuses: ["Обучается", "Отчислен", "Завершил"],
			milgroups: [
                {
                    milgroup: 1807,
                    milfaculty: "ВКС",
                },
                {
                    milgroup: 1808,
                    milfaculty: "ВКС",
                },
                {
                    milgroup: 1809,
                    milfaculty: "ВКС",
                },
			],
			milfaculties: [
				"Разведка",
				"Сержанты",
				"ВКС",
				"РВСН"
			],
			editStudent: null,
			selectedSection: 'students',
		}
	},
	created() {
		this.onFilter();
	},
	methods: {
		closeModal() {
			this.addModal = false
			document.getElementById('main-container').classList.remove('stop-scrolling')
			this.editStudent = null;
		},
		openModal() {
			this.addModal = true
			document.getElementById('main-container').classList.add('stop-scrolling')
		},
		onFilter(){
			if (this.selectedSection == 'students'){
				getStudent({ 
					search: this.filterS.search, 
					milgroup: this.filterS.milgroup,
					status: this.filterS.status,
				}).then(response => {
					this.studentsData = response.data;
					this.studentsData.forEach(x => {
						x.birthdate = moment(x.birthdate).format('DD.MM.yyyy');
					});
				}).catch(() => {
					this.$message.error('Ошибка получения списка студентов!');
				})
			}
			else if (this.selectedSection == 'teachers'){
				getTeacher({ 
					search: this.filterT.search, 
					milfaculty: this.filterT.milfaculty,
				}).then(response => {
					this.teachersData = response.data;
				}).catch(() => {
					this.$message.error('Ошибка получения списка преподавателей!');
				})
			}
		},
		clearFilter(){
			if (this.selectedSection == 'students'){
				this.filterS.search = null; 
				this.filterS.milgroup = null;
				this.filterS.status = null;
			}
			else if (this.selectedSection == 'teachers'){
				this.filterT.search = null;
				this.filterT.milfaculty = null;
			}
			this.onFilter();
		},
		onDelete(id){
			if (this.selectedSection == 'students'){
				this.$confirm('Вы уверены, что хотите удалить студента?', 'Подтверждение', {
					confirmButtonText: 'Да',
					cancelButtonText: 'Отмена',
					type: 'warning'
				})
				.then(() => {
					deleteStudent(id).then(() => {
						this.onFilter();
						this.$message.success('Студент удален.');
					}).catch(() => {
						this.$message.error('Ошибка при удалении.');  
					});
				});
			}
			else if (this.selectedSection == 'teachers'){
				this.$confirm('Вы уверены, что хотите удалить преподавателя?', 'Подтверждение', {
					confirmButtonText: 'Да',
					cancelButtonText: 'Отмена',
					type: 'warning'
				}).then(() => {
					deleteTeacher(id).then(() => {
						this.onFilter();
						this.$message.success('Преподаватель удален.');
					}).catch(() => {
						this.$message.error('Ошибка при удалении.');  
					});
				});
			}
		},
		onEdit(row){
			this.editStudent = row;
			this.openModal();
		}
	}
}
</script>

<style scoped lang="scss">
	@import "style"
</style>
