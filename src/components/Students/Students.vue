<template>
  <div>
    <el-col :offset="2" :span="20" class="Personnel">
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
					<el-input placeholder="Введите ФИО" v-model="fioFilter" v-on:keyup.native.enter="onEnter"></el-input>
				</el-col>
				<el-col :span="6" class="filter" v-if="selectedSection=='students'">
					<el-select v-model="selectedMG" clearable placeholder="Выберите взвод">
						<el-option
						v-for="item in mgs"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
				<el-col :span="4" class="filter" v-if="selectedSection=='students'">
					<el-select v-model="selectedStatus" clearable placeholder="Выберите статус">
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
				<el-table :data="studentsData" v-if="selectedSection=='students'">
					<el-table-column width="400px"
						prop="name"
						label="ФИО">
					</el-table-column>
					<el-table-column
						prop="mg"
						label="Взвод">
					</el-table-column>
					<el-table-column
						prop="mf"
						label="Цикл">
					</el-table-column>
					<el-table-column width="400px"
						prop="pr"
						label="Программа">
					</el-table-column>
					<el-table-column
						prop="bdate"
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
import { getStudents } from '@/api/students'
import AddModalWindow from "../AddModalWindow/AddModalWindow";

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
			statuses: ["Обучается", "Отчислен", "Завершил"], selectedStatus: '',
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
		onEnter(){
			getStudents({name: this.fioFilter, milgroup: this.selectedMG}).then(response => {
				this.studentsData = response.data;
			}).catch(() => {
				console.log('Данные по студентам не указаны')
			})
		},
		fetchData(){
			getStudents().then(response => {
				this.studentsData = response.data;
			}).catch(() => {
				console.log('Данные по студентам не указаны')
			})
		}
	}
}
</script>

<style scoped lang="scss">
	@import "style"
</style>
