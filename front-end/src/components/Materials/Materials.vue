<template>
  <el-col :offset="2" :span="20" class="scienceWork">
    <el-row class="pageTitle">
      <el-col>
        <div class="d-flex align-items-center">
          <img src="../../assets/scienceWorks/previous.svg" v-if="subjectId !== undefined" @click="backToSubjects" style="position: absolute; left: -40px; cursor: pointer" height="22px" alt="назад">
          {{subject}}
        </div>
      </el-col>
    </el-row>
    <el-row class="search" v-if="subjectId === undefined" >
      <el-col :span="23">
        <SearchForSubjects placeholder="Введите название предмета" />
        <Subjects />
      </el-col>
    </el-row>
    <el-row class="search" v-else>
      <el-col :span="4">
        <div class="parts">
          <div class="parts-all">Все разделы</div>
          <div v-for="(part, index) in subjectInfo" :key="index" class="part" @click="selectPart" :id="index+1">
            {{part.title}}
          </div>
        </div>
      </el-col>
      <el-col :span="17" :offset="1">
        <SearchForMaterials placeholder="Введите название темы или документа" />
        <div class="main-parts">
          <div v-for="(mainPart, index) in  subjectInfo" :key="index" class="main-part" :id="'part-'+(index+1)">
            <div class="main-part-title" @click="togglePart">
              <div>{{mainPart.title}}</div>
              <div class="">
                <el-popover
                        placement="bottom"
                        trigger="click"
                >
                  <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                    <div style="cursor:pointer;">Действие 1</div>
                    <div style="cursor:pointer;">Действие 2</div>
                  </div>
                  <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
                    <img src="../../assets/scienceWorks/popover.svg" alt="" class="kebab">
                  </div>
                </el-popover>
              </div>
            </div>
            <SubjectTopic :data="mainPart.topics" />
          </div>
        </div>
      </el-col>
    </el-row>
  </el-col>
</template>

<script>
import SearchForMaterials from '../Search/SearchForMaterials'
import SearchForSubjects from "../Search/SearchForSubjects";
import Subjects from '../Subjects/Subjects'
import SubjectFiles from '../SubjectFiles/SubjectFiles'
import {getSubject} from '../../api/subject'
import {getSubjects} from '../../api/subjects'
import SubjectTopic from '../SubjectTopic/SubjectTopic'

export default {
  name: '',
  components: {
    SearchForMaterials,
    SearchForSubjects,
    Subjects,
    SubjectFiles,
    SubjectTopic
  },
  data() {
    return {
      subject: "Учебно-методические материалы",
      subjectId: undefined,
      subjects: this.$store.getters.subjects,
      subjectInfo: undefined
    }
  },
  created() {
    if (this.$route.query.subjectId) {
      this.setSubject(this.$route.query.subjectId)
    }
  },
  updated() {
    if (this.$route.query.subjectId === undefined) {
      this.subject = "Учебно-методические материалы"
    }
    if (document.querySelector('.part')) {
      // document.querySelector('.part').classList.add('part-selected')
    }

  },
  methods: {
    togglePart(event) {
      if (event.target.className !== 'kebab') {
        if (event.target.closest('.main-part').children[1].style.display !== 'none') {
          event.target.closest('.main-part').children[1].style.display = 'none'
        } else {
          event.target.closest('.main-part').children[1].style.display = 'block'
        }
      }
    },
    selectPart(event) {
      // document.querySelector('.part-selected').classList.remove('part-selected')
      // event.target.classList.add('part-selected')
      document.getElementById('part-' + event.target.id).children[1].style.display = 'block'
      document.getElementById('part-' + event.target.id).scrollIntoView(true)
    },
    findSubjectInSubjects(subjects) {
      subjects.forEach(item => {
        if (item.id == this.subjectId) {
          this.subject = item.title
          getSubject({id: item.id}).then(response => {
            this.subjectInfo = response.data.sections
          }).catch(() => {
            // eslint-disable-next-line no-console
            console.log('Данные по предмету не указаны')
          })
        }
      })
    },
    setSubject(subjectId) {
      this.subjectId = subjectId
      if (this.$store.getters.subjects.length === 0) {
        getSubjects().then(response => {
          this.findSubjectInSubjects(response.data)
        }).catch(() => {
          // eslint-disable-next-line no-console
          console.log('Данные по предметам не указаны')
        })
      } else {
        this.findSubjectInSubjects(this.$store.getters.subjects)
      }
    },
    backToSubjects() {
      this.$router.push({
        query: {
          subjectId: undefined
        }
      })
      this.subject = "Учебно-методические материалы"
    }
  },
  watch: {
    '$route'(to, from) {
      this.setSubject(this.$route.query.subjectId)
    }
  },
}
</script>

<style scoped lang="scss">
  @import "style";
</style>
