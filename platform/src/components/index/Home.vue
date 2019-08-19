<template>
  <div class="hello">
    <h1>{{ msg }}</h1>

    <el-card class="box-card" v-if="!user">
      <h3>Sign in</h3>

      <el-input
        class="login"
        placeholder="User Name"
        prefix-icon="fa fa-user-circle"
        v-model="username">
      </el-input>

      <el-input
        class="login"
        placeholder="Password"
        prefix-icon="fa fa-unlock-alt"
        v-model="pwd">
      </el-input>

      <el-button type="primary" @click="login">Login</el-button>
    </el-card>

    <div v-if="user" style="width: 80%;margin: 10px auto;">
      <img src="static/images/welcome-card.gif">
    </div>

  </div>
</template>

<script>
  import Util from '../../utils/utils';

export default {
  name: 'Home',
  data () {
    return {
      msg: 'Welcome to Snack Bar Management',
      username: '',
      pwd: '',
      user: Util.getCookie('user')
    }
  },
  methods: {
    login () {
      var user = Util.getAdmins();
      if(this.username === user.name && this.pwd === user.pwd){
        Util.setCookie('user','Admin');
        window.location.reload()
      }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .login {
    margin-bottom: 15px;
  }
  .box-card {
    width: 400px;
    height: 260px;
    margin: 50px auto;
  }
h1, h2 {
  font-weight: normal;
}

</style>
