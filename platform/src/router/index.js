import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/index/Home'
import Product from '@/components/index/Products'
import LuckyDraw from '@/components/index/LuckyDraw'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },{
      path: '/product',
      name: 'Product',
      component: Product
    },{
      path: '/lucky-draw',
      name: 'LuckyDraw',
      component: LuckyDraw
    }
  ]
})
