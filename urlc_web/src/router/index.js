import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from '../store'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path:'/login',
    name:'login',
    component: () => import('../views/Login'),
    meta:{
      title:"登陆",
      authenticate:false
    }
  },
  {
    path:'/urils',
    name:'base',
    component: () => import('../views/Base'),
    children:[
      {
        path: 'about',
        name: 'about',
        component: () => import('../views/AboutView.vue'),
        meta:{
          title:"主页展示",
          authenticate:false
        }
      },
      {
        path: 'index',
        name: 'index',
        query:{
          title:'name'
        },
        component: () => import('../views/Index.vue')
      },
      {
        path: 'music',
        name: 'music',
        component: () => import('../views/Music.vue')
      },
      {
        path: 'host',
        name: 'host',
        component: () => import('../views/Host.vue'),
        meta:{
          title:"主机管理",
          authenticate:true
        }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to,from,next)=>{
  document.title = to.meta.title
  if (to.meta.authenticate && store.getters.token == ''){
    next({'name':'login'})
  }else{
    next()
  }
  
  
})
export default router
