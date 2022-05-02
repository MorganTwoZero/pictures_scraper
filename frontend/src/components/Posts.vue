<template>
<div type="image" class="post.source">
    <a class="image" :href="post.post_link">
        <img :src="post.preview_link">
        <div class="counter_wrapper">
            <div class="images_count">
                {{post.images_number}}
            </div>
        </div>
    </a>
    <div class="author">
        <a :href="post.author_link">
            <img :src="post.author_profile_image">
            {{post.author}}
        </a>
        {{post.created}}
    </div>
</div>
</template>

<script>
export default {
  name: 'PostsComponent',
  props: {
    post : {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
div[type="image"] {
    border-radius: 2px;
    padding: 10px;
    border: 1px solid rgb(0, 0, 0);
    width: max-content;
    height: max-content;
}

img {
    max-width: 90vw;
    max-height: 80vh;
    object-fit: cover;
}

.author img {
    width: 50px;
}

.counter_wrapper {
    position: absolute;
    right: 0px;
    padding: 4px 4px 0px;
}

.images_count {
    display: flex;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
    height: 20px;
    min-width: 20px;
    color: rgb(255, 255, 255);
    font-weight: bold;
    background: rgba(0, 0, 0, 0.32);
    border-radius: 10px;
    font-size: 10px;
    line-height: 10px;
}

.image {
    position: relative;
    display: flex;
    margin-bottom: 10px;
}
</style>