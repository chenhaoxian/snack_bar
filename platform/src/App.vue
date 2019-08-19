<template>
  <div id="app">
    <MyHeader></MyHeader>
    <!--<img src="./assets/logo.png">-->
    <router-view/>
    <MyFooter></MyFooter>
  </div>
</template>

<script>
  import MyFooter from '../src/components/common/MyFooter.vue';
  import MyHeader from '../src/components/common/MyHeader.vue';

  export default {
    name: 'App',
    components: {
      MyHeader, MyFooter
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    height: 100%;
  }
</style>
