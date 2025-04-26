<template>
  <div>
    <nav class="navbar navbar-expand-lg" :class="colorMode.value === 'dark' ? 'navbar-dark bg-dark' : 'navbar-light bg-light'">
      <div class="container">
        <NuxtLink class="navbar-brand" to="/">VIBE-SAM Project</NuxtLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/systems">Systems</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/components">Components</NuxtLink>
            </li>
          </ul>
          <ColorModeToggle />
        </div>
      </div>
    </nav>
    
    <div class="container page-container">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
// Fix: Use the composable provided by Nuxt instead of direct import
const colorMode = useColorMode();
</script>

<style scoped>
.navbar {
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
}

.nav-link.router-link-active {
  font-weight: bold;
}
</style>
