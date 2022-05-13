import 'bootstrap/dist/css/bootstrap.css';
import * as bootstrap from 'bootstrap';
import axios from 'axios';

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000';  // the FastAPI backend

createApp(App).use(router).use(bootstrap).mount('#app')