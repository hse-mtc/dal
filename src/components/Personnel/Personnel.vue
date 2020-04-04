<template>
  <div>
    <el-col :offset="1" :span="22" class="Personnel">
		<el-row class="pageTitle">
			<el-col>
			Личный состав ВУЦ
			</el-col>
		</el-row>
		<el-row class="selectPers">
			<el-col :span="4">
				<div id="students" class="selectPers-item selected" @click="selectClick($event)">
					Студенты
				</div>
			</el-col>
			<el-col :span="5" :offset="1">
				<div id="teachers" class="selectPers-item" @click="selectClick($event)">
					Преподаватели
				</div>
			</el-col>
		</el-row>
		<el-row>
			<el-row class="search">
				<el-col :span="10" class="filter">
					<el-input clearable placeholder="Введите ФИО" v-model="fioFilter" v-on:clear="onFilter" v-on:keyup.native.enter="onFilter"></el-input>
				</el-col>
				<el-col :span="3" class="filter" v-if="selectedSection=='students'">
					<el-select v-model="selectedMG" clearable placeholder="Выберите взвод" v-on:change="onFilter">
						<el-option
						v-for="item in mgs"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
				<el-col :span="7" class="filter" v-if="selectedSection=='students'">
					<el-select v-model="selectedStatus" clearable placeholder="Выберите статус" v-on:change="onFilter">
						<el-option
						v-for="item in statuses"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
				<el-col :span="1" class="filter">
					<el-button type="text" @click="clearFilter">Сбросить</el-button>
				</el-col>
			</el-row>
			<el-row class="addRow">
				<el-col :span="24">
					<el-button 
						class="addBtn" 
						type="primary" 
						icon="el-icon-plus" 
						v-if="selectedSection=='students'"
						@click="openModal">
						Новый студент
					</el-button>
					<el-button 
						class="addBtn" 
						type="primary" 
						icon="el-icon-plus" 
						v-if="selectedSection=='teachers'"	
						@click="openModal">
						Новый преподаватель
					</el-button>
				</el-col>
			</el-row>
			<el-row class="table">
				<el-table
					height="600px"
					:data="studentsData" 
					v-if="selectedSection=='students'" 
					:default-sort = "{prop: 'milgroup.milgroup', order: 'ascending'}" 
					stripe>
					<el-table-column width="350px" sortable show-overflow-tooltip
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
						label="">
						<template slot-scope="scope">
							<el-button
							size="mini"
							icon="el-icon-edit"
							@click="onEdit(scope.row)"></el-button>
							<el-button
							size="mini"
							icon="el-icon-delete"
							type="danger"
							@click="onDelete(scope.row.id)"></el-button>
						</template>
						</el-table-column>
				</el-table>
				<el-table :data="teachersData" v-if="selectedSection=='teachers'">
					<el-table-column width="400px"
						prop="name"
						label="ФИО">
					</el-table-column>
					<el-table-column
						prop="mf"
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
						prop="mg"
						label="Прикр. взвод">
					</el-table-column>
				</el-table>
			</el-row>
		</el-row>
    </el-col>
    <AddStudentModalWindow v-if="addModal" v-on:closeModal="closeModal" v-on:submitModal="clearFilter" v-bind:student="editStudent"/>
    <div v-if="addModal&&selectedSection=='students'" class="background" @click="closeModal"></div>
  </div>
</template>

<script>
import { getStudent, deleteStudent } from '@/api/student'
import AddStudentModalWindow from "../AddStudentModalWindow/AddStudentModalWindow";

export default {
	name: '',
	components: {
		AddStudentModalWindow
	},
	data() {
		return {
			studentsData: [], teachersData: [],
			calendarData: undefined,
			addModal: false,
			statuses: ["Обучается", "Отчислен", "Завершил"], selectedStatus: null,
			mgs: ["1807", "1808", "1809"], selectedMG: null,
			selectedSection: "students",
			fioFilter: "",
			editStudent: null
		}
	},
	created() {
		this.$router.replace({ name: 'Personnel', query: { section: 'students' }});
		this.fetchData();
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
		selectClick(event) {
			Array.from(document.getElementsByClassName(event.target.className)).forEach(item => item.classList.remove('selected'))
			event.target.classList.add('selected')
			this.$router.replace({ name: 'Personnel', query: { section: event.target.id }})
			this.selectedSection = event.target.id
		},
		onFilter(){
			let params = {};
			if (this.fioFilter != '') params['name'] = this.fioFilter;
			if (this.selectedMG != null) params['milgroup'] = this.selectedMG;
			if (this.selectedStatus != null) params['status'] = this.selectedStatus;
			getStudent(params).then(response => {
				this.studentsData = response.students;
			}).catch((err) => {
				console.log(err)
			})
		},
		clearFilter(){
			this.fioFilter = "";
			this.selectedMG = null;
			this.selectedStatus = null;
			getStudent().then(response => {
				this.studentsData = response.students;
			}).catch((err) => {
				console.log(err)
			})
		},
		fetchData(){
			getStudent().then(response => {
				this.studentsData = response.students;
			}).catch((err) => {
                console.log(err)
			})
		},
		onDelete(id){
			this.$confirm('Вы уверены, что хотите удалить студента?', 'Подтверждение', {
				confirmButtonText: 'Да',
				cancelButtonText: 'Отмена',
				type: 'warning'
			}).then(() => {
				deleteStudent(id).then(() => {
					this.fetchData();
					this.$message.success('Студент удален.');
				}).catch(() => {
					this.$message.error('Ошибка при удалении.');  
				});
			});
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
