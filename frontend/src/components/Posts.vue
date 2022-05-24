<template>
    <a @click="toClipboard" class="image" :href="post.post_link">
        <img class="preview_link" :src="post.preview_link">
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
import axios from 'axios';

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
    methods: {
        toClipboard(e) {
                e.preventDefault();
                let text = '';
                if (this.post.post_link.startsWith('https://twitter.com/')) {
                    text = `<${this.post.post_link}> ${this.post.preview_link}?name=orig`;
                } else if (this.post.post_link.startsWith('https://www.pixiv.net')) {
                    text = `<${this.post.post_link}> https://honkai-pictures.ru/api/embed/${this.post.post_link.slice(-8)}`;
                } else {
                    text = `<${this.post.post_link}> ${this.post.preview_link.replace(/\?.*/, '')}`;
                }
                navigator.clipboard.writeText(text);
        },
        pixivLink() {
            if (this.post.post_link.startsWith('https://www.pixiv.net/')) {
                axios({
                    method: 'get',
                    url: `/embed/${this.post.post_link.slice(-8)}.jpg`,
                    responseType: 'blob',
                }).then(res => {
                    let img = document.querySelector(`.preview_link[src="${this.post.preview_link}"]`)
                    let imageType = this.post.preview_link.slice(-3);
                    let file = new File([res.data], { type: `image/${imageType}` });
                    img.src = URL.createObjectURL(file);
                });
            }
        },
    },
    beforeMount() {
        this.pixivLink();
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