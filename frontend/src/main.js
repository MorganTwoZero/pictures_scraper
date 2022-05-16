import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css';
import bootstrap from 'bootstrap';
import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;  // the FastAPI backend

createApp(App).use(router).use(bootstrap).mount('#app')