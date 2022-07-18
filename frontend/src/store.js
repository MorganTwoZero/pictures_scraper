import { defineStore } from 'pinia'
import axios from 'axios';

export const useStore = defineStore({
    id: 'auth',
    state: () => ({
        user: document.cookie.split('; ').forEach(cookie => {
            const [key, value] = cookie.split('=');
            if (key === 'username') {
                return value;
            }
        }),
        lastUpdate: null,
    }),
    persist: true,
    getters: {
        isAuthenticated: state => !!state.user,
        User: state => state.user,
        LastUpdate: state => state.lastUpdate,
    },
    actions: {
        async lastUpdateSetter() {
            axios.get('update/last_update').then(res => {
                this.lastUpdate = new Date(res.data).toLocaleTimeString('ru')
              })
        },
        async Register(form) {
            return new Promise((resolve, reject) => {
                axios({
                    method: 'post',
                    url: 'register',
                    data: `username=${form.username}&password=${form.password}`,
                }).then(() => {
                    resolve();
                }).catch((err) => {
                    reject(err);
                });
            })
        },
        async LogIn(form) {
            return new Promise((resolve, reject) => {
                axios({
                    method: 'post',
                    url: 'login',
                    data: `username=${form.username}&password=${form.password}`
                }).then(response => {
                    if (response.status == 200) {
                        this.$patch({ user: form.username });
                        resolve();
                    }
                }).catch(err => {
                    console.log(err)
                    reject(err);
                });
            })
        },

        async LogOut() {
            this.$patch({ user: null })
            await axios.get('logout');
        },

        async Settings(form) {
            return new Promise((resolve, reject) => {
                axios({
                    method: 'post',
                    url: 'settings',
                    data: form
                }).then(response => {
                    if (response.status == 200) {
                        resolve();
                    }
                }).catch(err => {
                    console.log(err)
                    reject(err);
                });
            })
        },
    }
})