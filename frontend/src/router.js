import { createRouter, createWebHashHistory } from 'vue-router'
import PostsView from './views/PostsView.vue'
import AboutView from './views/AboutView.vue'

const routes = [
  {
    path: '',
    redirect: 'honkai',
  },
  {
    path: '/honkai',
    name: 'honkai',
    component: PostsView,
    meta: {title: 'Honkai'},
  },
  {
    path: '/homeline',
    name: 'homeline',
    component: PostsView,
    meta: {title: 'Homeline'},
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: {title: 'About'},
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('./views/LoginView.vue'),
    meta: {title: 'Login'},
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('./views/RegisterView.vue'),
    meta: {title: 'Register'},
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('./views/UserView.vue'),
    meta: {title: 'User'},
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

const DEFAULT_TITLE = 'Картиночки';
router.afterEach((to) => {
    // Use next tick to handle router history correctly
    // see: https://github.com/vuejs/vue-router/issues/914#issuecomment-384477609
        document.title = to.meta.title || DEFAULT_TITLE;
});

export default router
