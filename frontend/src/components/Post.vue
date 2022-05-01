<template>
<div type="image" class="{{ post.source }}">
    <a class="image" href="{{ post.post_link }}">
        <div>
            <img src="{{ post.preview_link }}">
        </div>
        <div class="counter_wrapper">
            <div class="images_count">
                {{ post.images_number }}
            </div>
        </div>
    </a>
    <div class="author">
        <a href="{{ post.author_link }}">{{ post.author }}</a>
        <img src="{{ post.author_profile_image }}">
        {{ post.created }}
    </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Post',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      axios.get('/')
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>

<style scoped>
a {
  cursor: pointer;
}
</style>