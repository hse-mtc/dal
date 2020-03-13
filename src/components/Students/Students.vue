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
		<el-row v-if="selectedSection=='students'" class="studentsPage">
			<el-row class="search">
				<el-col :span="7" class="filter">
					<el-input placeholder="Введите ФИО" v-model="SfioFilter" v-on:keyup.native.enter="onEnter"></el-input>
				</el-col>
				<el-col :span="9" class="filter">
					<el-select v-model="SselectedMG" clearable placeholder="Выберите взвод">
						<el-option
						v-for="item in mgs"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
				<el-col :span="4" class="filter">
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
				<el-table id="studentsTable" :data="studentsData">
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
			</el-row>
		</el-row>
		<el-row v-if="selectedSection=='teachers'" class="teachersPage">
			<el-row class="search">
				<el-col :span="7" class="filter">
					<el-input placeholder="Введите ФИО" v-model="TfioFilter"></el-input>
				</el-col>
				<el-col :span="9" class="filter">
					<el-select v-model="TselectedMG" clearable placeholder="Выберите прикр. взвод">
						<el-option
						v-for="item in mgs"
						:key="item"
						:label="item"
						:value="item">
						</el-option>
					</el-select>
				</el-col>
			</el-row>
			<el-row class="table">
				<el-table :data="teachersData">
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
import AddModalWindow from "../AddModalWindow/AddModalWindow";

export default {
	name: '',
	components: {
		AddModalWindow
	},
	data() {
		return {
			studentsData1: [{"name": "Кацевалов Артем Сергеевич", "mg": "1809", "mf": "ВКС", "pr": "Информатика и вычислительная техника", "bdate": "23.02.2000", "status": "Обучается"},
						{"name": "Исаков Владислав Евгеньевич", "mg": "1809", "mf": "ВКС", "pr": "Информатика и вычислительная техника", "bdate": "29.08.1999", "status": "Обучается"},
						{"name": "Хромов Григорий Александрович", "mg": "1809", "mf": "ВКС", "pr": "Информатика и вычислительная техника", "bdate": "04.11.1999", "status": "Обучается"}], studentsData: [],
			
			teachersData: [{"name": "Никандров Игорь Владимирович", "mg": "1809", "mf": "ВКС", "rank": "Подполковник", "post": "Преподаватель"},
						{"name": "Репалов Дмитрий Николаевич", "mg": "1808", "mf": "ВКС", "rank": "Подполковник", "post": "Начальник цикла"},
						{"name": "Пеляк Виктор Степанович", "mg": null, "mf": "ВКС", "rank": "Полковник", "post": "Преподаватель"}],
			calendarData: undefined,
			count: undefined,
			addModal: false,
			statuses: ["Обучается", "Отчислен", "Завершил"], selectedStatus: '',
			mgs: ["1807", "1808", "1809"], SselectedMG: '', TselectedMG: '',
			selectedSection: "students",
			SfioFilter: "", TfioFilter: ""
		}
	},
	created() {
			this.$router.replace({ name: 'Personnel', query: { section: 'students' }})
			this.studentsData = this.studentsData1
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
			this.studentsData = this.studentsData1.filter(x => x["name"].toLowerCase().includes(this.SfioFilter.toLowerCase()));
		}
}
}
</script>

<style scoped lang="scss">
  @import "style"
</style>
