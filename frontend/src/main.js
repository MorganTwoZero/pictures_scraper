import 'bootstrap/dist/css/bootstrap.css';
import * as bootstrap from 'bootstrap';
import axios from 'axios';

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

axios.defaults.withCredentials = true;
console.log(process.env);
if (process.env.NODE_ENV === 'development') {
axios.defaults.baseURL = 'http://localhost:8000/';  // the FastAPI backend
} else {
axios.defaults.baseURL = 'http://192.168.2.1:8000/';  // production
}

createApp(App).use(router).use(bootstrap).mount('#app')