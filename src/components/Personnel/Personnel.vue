<template>
  <div>
    <el-col :offset="2" :span="21" class="Personnel">
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
					<el-input placeholder="Введите ФИО" v-model="fioFilter" v-on:keyup.native.enter="onFilter"></el-input>
				</el-col>
				<el-col :span="6" class="filter" v-if="selectedSection=='students'">
					<el-select v-model="selectedMG" clearable placeholder="Выберите взвод" v-on:change="onFilter">
						<el-option
						v-for="item in mgs"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
				<el-col :span="4" class="filter" v-if="selectedSection=='students'">
					<el-select v-model="selectedStatus" clearable placeholder="Выберите статус" v-on:change="onFilter">
						<el-option
						v-for="item in statuses"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
			</el-row>
			<el-row class="table">
				<el-table 
					height="600px"
					:data="studentsData" 
					v-if="selectedSection=='students'" 
					:default-sort = "{prop: 'milgroup', order: 'ascending'}" 
					stripe>
					<el-table-column width="400px" sortable
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
					<el-table-column width="400px"
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
    <AddModalWindow v-if="addModal" v-on:closeModal="closeModal" />
    <div v-if="addModal" class="background" @click="closeModal"></div>
  </div>
</template>

<script>
import { getStudent } from '@/api/student'
import AddModalWindow from "../AddModalWindow/AddModalWindow";
import axios from 'axios'

export default {
	name: '',
	components: {
		AddModalWindow
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

			/* axios.get(`http://localhost:8000/api/students/?
						${this.fioFilter != '' ? `name=${this.fioFilter}` : ''}&
						${this.selectedMG != null ? `milgroup=${this.selectedMG}` : ''}&
						${this.selectedStatus != null ? `status=${this.selectedStatus}` : ''}`)
			.then(response => {
				this.studentsData = response.data.students;
			}); */
		},
		fetchData(){

			/* axios.get('http://localhost:8000/api/students/')
			.then(response => {
				this.studentsData = response.data.students;
			}); */

			getStudent().then(response => {
				this.studentsData = response.students;
			}).catch((err) => {
                console.log(err)
			})
		}
	}
}
</script>

<style scoped lang="scss">
	@import "style"
</style>
