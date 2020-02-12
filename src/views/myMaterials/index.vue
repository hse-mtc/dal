<template>
  <div class="dashboard-container">
    <div class="dashboard-text">{{ name }}, добро пожаловать на сайт.</div>
    <div>Страница сейчас находится на стадии разработки, по всем вопросам: <a href="mailto:vmloskutov@edu.hse.ru">vmloskutov@edu.hse.ru</a></div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
