<template>
  <el-footer class="my-footer" height="20px">
    &copy; 2018 Avri Li. Licensed under MIT.
  </el-footer>
</template>

<script>
  export default {
    components: {
    },
    data(){
      return {}
    },
    methods: {}
  }

</script>

<style scoped>
  .my-footer {
    position: fixed;
    text-align: center;
    bottom: 0;
    width: 100%;
    background: #4788c7;
    /*background: rgb(84, 92, 100);*/
    opacity: 0.8;
    color: azure;
    line-height: 20px;
    font-size: smaller;
    z-index: 10;
  }
</style>
