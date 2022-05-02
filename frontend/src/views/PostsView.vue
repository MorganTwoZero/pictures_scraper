<template>
    <div v-for="post in posts" :key="post.post_link">
      <PostsComponent :post="post"/>
    </div>
</template>
<script>

import PostsComponent from '@/components/Posts.vue'
import axios from 'axios';
export default {
  name: 'PostsView',
  components: {
    PostsComponent,
  },
  data() {
    return {
      posts: [],
      page: 1,
    };
  },
  methods: {
    getMessage() {
      axios.get(this.$route.path + '?page=' + this.page + '&offset=5')
        .then((res) => {
          this.posts = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getNextPosts() {
      window.onscroll = () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
          this.page++;
          axios.get(this.$route.path + '?page=' + this.page + '&offset=5').then(response => {
            this.posts = this.posts.concat(response.data);
            });
          }
        }
    },
  },
  beforeMount() {
    this.getMessage();
  },
  mounted() {
    this.getNextPosts();
  },
}
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