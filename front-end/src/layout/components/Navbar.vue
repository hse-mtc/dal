<template>
  <div class="mynavbar">
    <div
      class="burger"
      :title="isCollapse ? 'Развернуть меню' : 'Свернуть меню'"
      @click="toggleSideBar"
    >
      <Hamburger :is-active="sidebar.opened" class="hamburger-container" />
    </div>
    <Breadcrumb class="breadcrumb-container" />

    <div class="right-menu">
      <el-popover>
        <div class="teachers">
          Teachers
        </div>
        <div class="students">
          Students
        </div>
        <el-badge slot="reference" :is-dot="birthdays.length" class="birthdays">
          <button>
            <SvgIcon icon-class="cake" />
            <span class="text">Дни рождения</span>
          </button>
        </el-badge>
      </el-popover>
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper m-0" style="font-size: 19px">
          <!--          <img :src="avatar+'?imageView2/1/w/80/h/80'" class="user-avatar">-->
          {{ email }}
          <i class="el-icon-caret-bottom" />
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/">
            <el-dropdown-item> Домой </el-dropdown-item>
          </router-link>
          <el-dropdown-item v-if="personType && personId">
            <span style="display: block" @click="profile">Мой профиль</span>
          </el-dropdown-item>
          <el-dropdown-item divided>
            <span style="display: block" @click="logout">Выход</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import Breadcrumb from "@/components/Breadcrumb";
import Hamburger from "@/components/Hamburger";
import { surnameWithInitials } from "@/utils/person";
import { AppModule, UserModule } from "@/store";

export default {
  components: {
    Breadcrumb,
    Hamburger,
  },
  computed: {
    sidebar() {
      return AppModule.sidebar;
    },
    email() {
      return UserModule.email;
    },
    personType() {
      return UserModule.personType;
    },
    personId() {
      return UserModule.personId;
    },
    isCollapse() {
      return !this.sidebar.opened;
    },
    birthdays() {
      return ["s"];
    },
  },
  methods: {
    surnameWithInitials,
    logout() {
      UserModule.logout();
      window.location.href = "/login";
    },
    profile() {
      if (this.personType && this.personId) {
        const name = this.personType.charAt(0).toUpperCase() + this.personType.slice(1);
        this.$router.push({
          name,
          params: { [`${this.personType}Id`]: this.personId },
        });
      }
    },
    toggleSideBar() {
      AppModule.toggleSideBar();
    },
  },
};
</script>

<style lang="scss" scoped>
.mynavbar {
  display: flex;
  height: 56px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  background-color: #2d3746;
  color: #fff !important;

  .breadcrumb-container {
    height: 56px;
    display: flex;
    align-items: center;
    align-items: center;
    float: left;
    color: #fff;
    color: #fff !important;
  }

  .right-menu {
    margin-right: 120px;
    margin-left: auto;
    height: 100%;
    line-height: 56px;
    display: flex;
    align-items: center;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #fff !important;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;
        color: #fff !important;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
}

.burger {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 20px;
  justify-content: space-between;
  cursor: pointer;

  &:hover {
    background-color: #263445;
  }
}

.birthdays {
  height: 30px;
  margin-right: 20px;

  button {
    cursor: pointer;
    border-radius: 100px;
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    color: white;
    outline: none !important;
    transition: 0.2s;
    display: flex;
    align-items: center;

    .text {
      margin-left: 10px;
    }

    &:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    &:focus {
      background: rgba(255, 255, 255, 0.2);
    }
  }
}
</style>
