import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css';
import {Dropdown} from 'bootstrap';

import axios from 'axios';

import Toast, { POSITION } from "vue-toastification";
import "vue-toastification/dist/index.css";

axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;  // the FastAPI backend

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

const app = createApp(App)
app.use(router, Dropdown)
app.use(Toast, {position: POSITION.BOTTOM_RIGHT});
app.use(pinia)
app.mount('#app')