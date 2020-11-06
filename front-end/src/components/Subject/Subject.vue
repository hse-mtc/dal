<template>
  <el-col :offset="2" :span="20" class="scienceWork">
    <el-row class="pageTitle">
      <el-col>
        <div class="d-flex align-items-center">
          <img
              src="../../assets/scienceWorks/previous.svg"
              @click="backToSubjects"
              style="position: absolute; left: -40px; cursor: pointer"
              height="22px"
              alt="назад"
          />
          {{ subject }}
        </div>
      </el-col>
    </el-row>
    <el-row class="search">
      <el-col :span="4">
        <div class="parts">
          <div class="parts-all">Все разделы</div>
          <div
              v-for="(part, index) in subjectInfo"
              :key="index"
              class="part"
              @click="selectPart"
              :id="index + 1"
          >
            {{ part.title }}
          </div>
        </div>
      </el-col>
      <el-col :span="17" :offset="1">
        <SearchForMaterials placeholder="Введите название темы или документа"/>
        <div class="main-parts">
          <div
              v-for="(mainPart, index) in subjectInfo"
              :key="index"
              class="main-part"
              :id="'part-' + (index + 1)"
          >
            <div class="main-part-title" @click="togglePart">
              <div>{{ mainPart.title }}</div>
              <div class="">
                <el-popover placement="bottom" trigger="click">
                  <div
                      style="
                        text-align: center;
                        margin: 0;
                        padding: 0;
                        font-size: 15px;
                      "
                  >
                    <div style="cursor: pointer">Действие 1</div>
                    <div style="cursor: pointer">Действие 2</div>
                  </div>
                  <div
                      slot="reference"
                      class="d-flex justify-content-center"
                      style="width: 10px; cursor: pointer"
                  >
                    <img
                        src="../../assets/scienceWorks/popover.svg"
                        alt=""
                        class="kebab"
                    />
                  </div>
                </el-popover>
              </div>
            </div>
            <SubjectTopic :data="mainPart.topics"/>
          </div>
        </div>
      </el-col>
    </el-row>
  </el-col>
</template>

<script>
import SearchForMaterials from "@/components/Search/SearchForMaterials";
import SubjectTopic from "@/components/SubjectTopic/SubjectTopic";
import {getSubject} from "@/api/subject";
import {getSubjects} from "@/api/subjects";
import {mapActions, mapState} from "vuex";

export default {
  name: "Subject",
  mounted() {
    console.log(this.$route.params.subjectId)
    this.setSubject(this.$route.params.subjectId);
  },
  data() {
    return {
      subject: null,
      subjectId: null,
      subjectInfo: null,
    };
  },
  components: {
    SearchForMaterials,
    SubjectTopic,
  },
  computed: {
    ...mapState({
      subjects: (state) => state.subjects.subjects,
    }),
  },
  methods: {
    ...mapActions({
      setSubjects: "subjects/setSubjects",
    }),
    togglePart(event) {
      if (event.target.className !== "kebab") {
        if (
            event.target.closest(".main-part").children[1].style.display !==
            "none"
        ) {
          event.target.closest(".main-part").children[1].style.display = "none";
        } else {
          event.target.closest(".main-part").children[1].style.display =
              "block";
        }
      }
    },
    selectPart(event) {
      document.getElementById(
          "part-" + event.target.id
      ).children[1].style.display = "block";
      document.getElementById("part-" + event.target.id).scrollIntoView(true);
    },
    findSubjectInSubjects(subjects) {
      subjects.forEach((item) => {
        if (item.id == this.subjectId) {
          this.subject = item.title;
          getSubject({ id: item.id })
              .then((response) => {
                this.subjectInfo = response.data.sections;
              })
              .catch(() => {
                // eslint-disable-next-line no-console
                console.log("Данные по предмету не указаны");
              });
        }
      });
    },
    setSubject(subjectId) {
      this.subjectId = subjectId;
      if (this.subjects.length === 0) {
        getSubjects()
            .then((response) => {
              this.setSubjects(response.data)
              this.findSubjectInSubjects(response.data);
            })
            .catch(() => {
              // eslint-disable-next-line no-console
              console.log("Данные по предметам не указаны");
            });
      } else {
        this.findSubjectInSubjects(this.subjects);
      }
    },
    backToSubjects() {
      this.$router.push({ path: `/subjects/`})
    },
  },
}
</script>

<style scoped lang="scss">
 @import "style";
</style>
