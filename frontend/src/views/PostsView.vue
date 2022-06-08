<template>
  <div v-for="post in posts" :key="post.post_link">
    <PostsComponent :post="post" />
  </div>
</template>

<script setup>
import { onBeforeMount, onMounted, ref } from 'vue'
import router from '@/router'

import PostsComponent from '@/components/PostsComponent.vue'

import axios from 'axios'

let posts = ref([]);
let page = 1;

function getMessage() {
  axios.get(router.currentRoute.value.fullPath + '?page=' + page + '&offset=5')
    .then((res) => {
      posts.value = res.data;
    })
    .catch((error) => {
      console.error(error);
    });
}

function getNextPosts() {
  window.onscroll = () => {
    if ((window.innerHeight + Math.ceil(window.scrollY)) >= document.body.offsetHeight) { //ceil for mobile
      page++;
      axios.get(router.currentRoute.value.fullPath + '?page=' + page + '&offset=5').then(response => {
        posts.value = posts.value.concat(response.data);
      });
    }
  }
}

onBeforeMount(() => {
  getMessage();
})

onMounted(() => {
  getNextPosts();
})
</script>

<style scoped>
div {
  border-radius: 2px;
  padding: 10px;
  border: 1px solid rgb(0, 0, 0);
  width: max-content;
  height: max-content;
}
</style>