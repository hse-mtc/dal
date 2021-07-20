<template>
  <div class="birthday-item-wrapper">
    <router-link class="name" :to="`/${type}/${person.id}`" @click.native="$emit('clicked')">
      {{ person.full_name }}
    </router-link>
    <div class="description">
      <span class="date"> {{ formatDate(person.birthday) }} </span>
      <span class="age">
        Исполняется
        <span class="value">{{ person.how_old_will_be }}</span>
        <SvgIcon icon-class="cake" />
      </span>
    </div>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "BirthdayItem",
  props: {
    person: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  methods: {
    formatDate: d => moment(d).format("DD MMMM"),
  },
};
</script>

<style lang="scss" scoped>
.birthday-item-wrapper {
  padding: 5px;

  .name {
    font-size: 1.2em;
    font-weight: 600;
    transition: .2s;
  }

  .description {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .date {
    }

    .age {
      .value {
        font-weight: 500;
      }
    }
  }
}
</style>
