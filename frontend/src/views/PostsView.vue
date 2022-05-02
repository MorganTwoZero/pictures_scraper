<template>
    <div v-for="post in posts" :key="post.post_link">
      <PostsComponent :post="post" />
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
    };
  },
  methods: {
    getMessage() {
      console.log(this.$route);
      axios.get(this.$route.path)
        .then((res) => {
          this.posts = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
}
</script>