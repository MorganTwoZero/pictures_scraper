import { defineStore } from 'pinia'
import axios from 'axios';

export const useStore = defineStore({
    id: 'auth',
    state: () => ({
        user: null,
    }),
    persist: true,
    getters: {
        isAuthenticated: state => !!state.user,
        User: state => state.user,
    },
    actions: {
        async Register(form) {
            const data = {
                ...form,
            }
            return new Promise((resolve, reject) => {
                axios({
                    method: 'post',
                    url: 'register',
                    data: data
                }).then(() => {
                    this.LogIn(data);
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