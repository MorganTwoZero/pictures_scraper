import 'bootstrap/dist/css/bootstrap.css';
import bootstrap from 'bootstrap'
import axios from 'axios';

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/api';  // the FastAPI backend
// axios.defaults.baseURL = 'http://192.168.2.1:8000/api';  // production

createApp(App).use(router).use(bootstrap).mount('#app')