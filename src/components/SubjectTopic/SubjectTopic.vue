<template>
    <div class="topics" style="display: none">
        <div v-for="(topic, index) in data" :key="index" class="topic">
            <div class="topic-title">
                <div>Тема №{{index + 1}}</div>
                <div class="topic-download-all">Скачать все материалы архивом</div>
            </div>
            <div class="topic-content">
                {{topic.title}}
            </div>
            <div class="topic-files">
                <div class="lectures file-group">
                    <div class="lectures-title file-section-title" @click="toggleFiles">
                        <div>Лекции</div>
                        <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="files-dropdown">
                    </div>
                    <div class="files" style="display: none">
                        <div class="file" v-for="(lecture, index) in topic.lectures" :key="index">
                            <div class="file-icon"><img src="../../assets/subject/iconPowerPoint.svg" alt="" class="kebab"></div>
                            <div class="file-title">{{lecture.name}}</div>
                            <div class="file-kebab">
                                <el-popover
                                        placement="bottom"
                                        trigger="click"
                                >
                                    <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                                        <div style="cursor:pointer;">Действие 1</div>
                                        <div style="cursor:pointer;">Действие 2</div>
                                    </div>
                                    <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
                                        <img src="../../assets/subject/greyKebab.svg" alt="" class="kebab">
                                    </div>
                                </el-popover>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="seminars file-group">
                    <div class="seminars-title file-section-title" @click="toggleFiles">
                        <div>Семинары</div>
                        <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="files-dropdown">
                    </div>
                    <div class="files" style="display: none">
                        <div class="file" v-for="(seminar, index) in topic.seminars" :key="index">
                            <div class="file-icon"><img src="../../assets/subject/iconPowerPoint.svg" alt="" class="kebab"></div>
                            <div class="file-title">{{seminar.name}}</div>
                            <div class="file-kebab">
                                <el-popover
                                        placement="bottom"
                                        trigger="click"
                                >
                                    <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                                        <div style="cursor:pointer;">Действие 1</div>
                                        <div style="cursor:pointer;">Действие 2</div>
                                    </div>
                                    <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
                                        <img src="../../assets/subject/greyKebab.svg" alt="" class="kebab">
                                    </div>
                                </el-popover>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="group-classes file-group">
                    <div class="group-classes-title file-section-title" @click="toggleFiles">
                        <div>Групповые заняти</div>
                        <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="files-dropdown">
                    </div>
                    <div class="files" style="display: none">
                        <div class="file" v-for="(group_class, index) in topic.group_classes" :key="index">
                            <div class="file-icon"><img src="../../assets/subject/iconPowerPoint.svg" alt="" class="kebab"></div>
                            <div class="file-title">{{group_class.name}}</div>
                            <div class="file-kebab">
                                <el-popover
                                        placement="bottom"
                                        trigger="click"
                                >
                                    <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                                        <div style="cursor:pointer;">Действие 1</div>
                                        <div style="cursor:pointer;">Действие 2</div>
                                    </div>
                                    <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
                                        <img src="../../assets/subject/greyKebab.svg" alt="" class="kebab">
                                    </div>
                                </el-popover>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="practice-classes file-group">
                    <div class="practice-classes-title file-section-title" @click="toggleFiles">
                        <div>Практические занятия</div>
                        <img src="../../assets/scienceWorks/dropdown.svg" alt="" class="files-dropdown">
                    </div>
                    <div class="files" style="display: none">
                        <div class="file" v-for="(lecture, index) in topic.lectures" :key="index">
                            <div class="file-icon"><img src="../../assets/subject/iconPowerPoint.svg" alt="" class="kebab"></div>
                            <div class="file-title">{{lecture.name}}</div>
                            <div class="file-kebab">
                                <el-popover
                                        placement="bottom"
                                        trigger="click"
                                >
                                    <div style="text-align: center; margin: 0; padding: 0; font-size: 15px;">
                                        <div style="cursor:pointer;">Действие 1</div>
                                        <div style="cursor:pointer;">Действие 2</div>
                                    </div>
                                    <div slot="reference" class="d-flex justify-content-center" style="width: 10px; cursor: pointer">
                                        <img src="../../assets/subject/greyKebab.svg" alt="" class="kebab">
                                    </div>
                                </el-popover>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
  import moment from 'moment'

  export default {
    name: '',
    components: {},
    props: ['data'],
    data() {
      return {

      }
    },
    methods: {
      toggleFiles(event) {
        if (event.target.closest('.file-group').children[1].style.display === 'none') {
          event.target.closest('.file-group').children[1].style.display = 'flex'
          event.target.closest('.file-section-title').children[1].style.transform = 'rotate(180deg)'
        } else {
          event.target.closest('.file-group').children[1].style.display = 'none'
          event.target.closest('.file-section-title').children[1].style.transform = 'rotate(0deg)'
        }

      }
    },
    mounted() {
    }
  }
</script>

<style scoped lang="scss">
    @import "style";
</style>
