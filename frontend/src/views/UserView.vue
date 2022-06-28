<template>
  <div class="settings">
    {{user}}
    <div>
      <form @submit.prevent="submit">
        <div>
          <label for="authors_blacklist">Authors blacklist:</label>
          <input type="text" name="authors_blacklist" v-model="form.authors_blacklist">
        </div>
        <div>
          <label for="tags_blacklist">Tags blacklist:</label>
          <input type="text" name="tags_blacklist" v-model="form.tags_blacklist" >
        </div>
        <div>
          <label for="twitter_header">Twitter header:</label>
          <input type="text" name="twitter_header" v-model="form.twitter_header">
          <div>
            Example:
              {'cookie': 'auth_token=269bcbc4...6f168; ct0=bd58...e66', 'authorization': 'Bearer AAA...nhjdP0', 'x-csrf-token': 'bd58...e66'}
              <br>
              check your .json xhr request in devtools on twitter
          </div>
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'

import { useStore } from '@/store'
import { reactive } from 'vue'
import { onMounted } from 'vue'

const store = useStore()

const form = reactive({
  user: store.user,
  twitter_header: "",
  authors_blacklist: "",
  tags_blacklist: "",
})

let user = reactive({
  user: "",
  twitter_header: "",
  authors_blacklist: "",
  tags_blacklist: "",
})

function submit() {
  store.Settings(form).then(() => {
    fetchSettings()
  })
}

function fetchSettings() {
    axios.get('/user')
      .then(response => {
        form.twitter_header = response.data.twitter_header,
        form.authors_blacklist = response.data.authors_blacklist,
        form.tags_blacklist = response.data.tags_blacklist,
        user.user = response.data.user,
        user.twitter_header = response.data.twitter_header,
        user.authors_blacklist = response.data.authors_blacklist,
        user.tags_blacklist = response.data.tags_blacklist
      })
}

onMounted(() => {
  fetchSettings()
})
</script>

<style scoped>
* {
  box-sizing: border-box;
  max-width: 90%;
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
