import { createRouter, createWebHashHistory } from 'vue-router'
import PostsView from '../views/PostsView.vue'

const routes = [
  {
    path: '/',
    redirect: '/honkai',
  },
  {
    path: '/honkai',
    name: 'honkai',
    component: PostsView,
  },
  {
    path: '/homeline',
    name: 'homeline',
    component: PostsView
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
