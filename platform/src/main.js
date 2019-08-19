// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import 'font-awesome/less/font-awesome.less'

import ElementUI from 'element-ui';
Vue.use(ElementUI);

import axios from 'axios'
Vue.prototype.$http = axios

Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App},
  template: '<App/>',
})


import 'element-ui/lib/theme-chalk/index.css';
import 'assets/css/common.less'
