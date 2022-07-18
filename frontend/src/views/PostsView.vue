<template>
  <div v-for="post in posts" :key="post.post_link">
    <PostsComponent :post="post" />
  </div>
</template>

<script setup>
import { onBeforeMount, ref } from 'vue'
import router from '@/router'

import PostsComponent from '@/components/PostsComponent.vue'

import axios from 'axios'

let posts = ref([]);
let page = 1;

// eslint-disable-next-line
function debounce(func, wait) {
    let timeout;
    return () => {
        if (timeout) {
            clearTimeout(timeout);
        }
        timeout = setTimeout(func, wait)
    }
}

function getNextPosts() {
    if ((window.innerHeight + Math.ceil(window.scrollY)) >= document.body.offsetHeight) { //ceil for mobile
      axios.get(router.currentRoute.value.fullPath + '?page=' + page).then(response => {
        posts.value = posts.value.concat(response.data);       
        page++;
      });
    }
  }

/*window.onscroll = debounce(getNextPosts, 200);*/
window.onscroll = getNextPosts;

onBeforeMount(() => {
  page = 1;
  axios.get(router.currentRoute.value.fullPath + '?page=' + page)
  .then((res) => {
    posts.value = res.data;
    page++;
  })
  .catch((error) => {
    console.error(error);
  });
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