<template>
  <el-header class="no-padding" width="100%">

    <el-menu class="el-menu-demo" mode="horizontal" background-color="#4788c7" text-color="#fff" active-text-color="#ffd04b"
             :router="true" :default-active="$route.path" :class="[scrolled ? 'scrolled-header' : 'un-scroll-header']">

      <div class="header-logo-box"><img src="../../assets/logo1.png" class="header-logo"></div>

      <el-menu-item index="1" route="/">Home</el-menu-item>
      <el-menu-item index="2" route="/product">Product Manage</el-menu-item>
      <!--<el-submenu index="2">
        <template slot="title">About</template>
        <el-menu-item index="2-1">选项1</el-menu-item>
        <el-menu-item index="2-2">选项2</el-menu-item>
        <el-menu-item index="2-3">选项3</el-menu-item>
      </el-submenu>-->
      <el-menu-item index="3" route="/lucky-draw">Lucky Draw</el-menu-item>
    </el-menu>

    <div v-if="user" style="float:right;position: fixed;top: 10px;right: 10px;">
      <span style="color: #ffffff;">Welcome, {{user}} </span>
      <el-button icon="fa fa-sign-out" @click="logout" circle style="font-size: large;color: rgb(71, 136, 199);"></el-button>
    </div>

  </el-header>
</template>

<script>
  import Util from '../../utils/utils';

  export default {
    components: {},
    data(){
      return {
        activeIndex: '1',
        scrolled: false,
        user: Util.getCookie('user')
      }
    },
    props:[],
    methods: {
      logout(){
        Util.delCookie('user')
        window.location.replace('/')
      },
      handleScroll () {
        this.scrolled = window.scrollY > 540;
      }
    },
    mounted(){
      this.$nextTick(function () {
//        window.addEventListener('scroll', this.handleScroll);
      })
    }
  }

</script>


<style scoped>
  .header-logo-box {
    display: inline-block;
    float: left;
    background: #ffffff;
    border-radius: 50%;
    margin-left: 80px;
    margin-right: 10px;
  }
  .header-logo {
    width: 50px;
    display: inline-block;
    padding: 5px;
    float: left;
  }
  .un-scroll-header {
    position: relative;
    opacity: 1;
  }
  .scrolled-header {
    transition: opacity .8s;
    position: fixed;
    opacity: 0.8;
    top:0;
    z-index: 2;
    width: 100%;
    border: 0;
  }
</style>
