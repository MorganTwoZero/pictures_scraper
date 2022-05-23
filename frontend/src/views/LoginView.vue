<template>
  <div class="login">
    <div>
      <form @submit.prevent="submit">
        <div>
          <label for="username">Username:</label>
          <input type="text" name="username" v-model="form.username" autocomplete="username">
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" name="password" v-model="form.password" autocomplete="current-password">
        </div>
        <button type="submit">Submit</button>
      </form>
      <p v-if="showError.e" id="error">Username or Password is incorrect</p>
    </div>
  </div>
</template>
<script setup>
import { useStore } from '@/store'
import { reactive } from 'vue'
import router from '@/router'

const store = useStore()
let showError = reactive({ e: false })

const form = {
  username: "",
  password: "",
}

function submit() {
  store.LogIn(form).then(() => {
    showError.e = false;
    router.push('/')
  }, error => {
    console.log('error', error);
    showError.e = true;
  })
}
</script>
<style scoped>
* {
  box-sizing: border-box;
}

label {
  padding: 12px 12px 12px 0;
  display: inline-block;
}

button[type=submit] {
  background-color: #4CAF50;
  color: white;
  padding: 12px 20px;
  cursor: pointer;
  border-radius: 30px;
}

button[type=submit]:hover {
  background-color: #45a049;
}

input {
  margin: 5px;
  box-shadow: 0 0 15px 4px rgba(0, 0, 0, 0.06);
  padding: 10px;
  border-radius: 30px;
}

#error {
  color: red;
}
</style>
