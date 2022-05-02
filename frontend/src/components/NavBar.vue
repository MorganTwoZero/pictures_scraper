<template>
  <header>
    <nav class="navbar navbar-expand-sm navbar-light fixed-top bg-light">
      <div class="container">
        <a class="navbar-brand" href="/">FastAPI + Vue</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav me-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/honkai">Honkai</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/homeline">Homeline</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'NavBar',
}
</script>

<style scoped>
a {
  cursor: pointer;
}
</style>