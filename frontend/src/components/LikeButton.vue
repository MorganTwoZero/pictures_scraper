<template>
    <div v-if="isLikeable">
        <button @click="like" class="btn btn-primary">Like</button>
    </div>
</template>

<script setup>
import { defineProps } from 'vue'

import { useStore } from '@/store'

import axios from 'axios';


const post_link = defineProps({
    post_link: {
        type: String,
        required: true,
    }
})
const store = useStore()


const isLikeable = post_link.post_link.includes('twitter.com') && store.isAuthenticated

function like(e) {
    e.preventDefault();
    axios.get('/like', {
        params: {
            post_link: post_link.post_link
        }
    })
    e.target.innerText = 'Liked'
    e.target.blur()
    e.target.disabled = true
    e.target.classList.add('btn-success')
}
</script>