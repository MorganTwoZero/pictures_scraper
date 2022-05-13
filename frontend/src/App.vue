<template>  
    <NavBar @update="update"/>
    <div class="main container">
      <router-view :key="$route.fullPath"/>
    </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import NavBar from '@/components/NavBar.vue'
export default {
  components: {
    NavBar
  }, 
  methods: {
    update() {
      axios.get('/update').then(response => {
        console.log(response.data);
      }
      );
    }
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.main {
  padding-top: 5em;
}

.main.container {
    display: flex;
    flex-flow: column;
    align-items: center;
}

.main.container > div {
    margin: 10px;
}
</style>
