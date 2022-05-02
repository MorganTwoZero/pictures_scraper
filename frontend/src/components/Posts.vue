<template>
<a class="image" :href="post.post_link">
    <img :src="post.preview_link">
    <div class="counter_wrapper">
        <div class="images_count">
            {{ post.images_number }}
        </div>
    </div>
</a>
<div class="author">
    <a :href="post.author_link">
        <img :src="post.author_profile_image">
        {{ post.author }}
    </a>
    {{ created }}
</div>
</template>

<script>
export default {
    name: 'PostsComponent',
    props: {
        post: {
            type: Object,
            required: true,
        },
    },
    computed: {
        created() {
            return new Date(this.post.created).toLocaleTimeString('ru');
        },
    },
};
</script>

<style scoped>
img {
    max-width: 90vw;
    max-height: 80vh;
    object-fit: cover;
}

.author {
    max-width: fit-content;
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
    width: max-content;
}
</style>