<template>
    <div class="topics" style="display: none">
        <div v-for="({
            title,
            class_materials: {lectures, seminars, groups, practices}
        }, index) in data" :key="index" class="topic">
            <div class="topic-title">
                <div>Тема №{{index + 1}}</div>
                <div class="topic-download-all">Скачать все материалы архивом</div>
            </div>

            <div class="topic-content">
                {{title}}
            </div>

            <div class="topic-files">
              <ClassMaterials title="Лекции" :materials="lectures" />
              <ClassMaterials title="Семинары" :materials="seminars" />
              <ClassMaterials title="Групповые занятия" :materials="groups" />
              <ClassMaterials title="Практические занятия" :materials="practices" />
            </div>
        </div>
    </div>
</template>

<script>
import ClassMaterials from "./ClassMaterials";

export default {
  name: '',
  components: {ClassMaterials},
  props: ['data'],
  data() {
    return {}
  },
}
</script>

<style scoped lang="scss">
    @import "style";
</style>
