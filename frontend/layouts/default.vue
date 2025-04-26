<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <NuxtLink class="navbar-brand" to="/">VIBE-SAM Project</NuxtLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/systems">Systems</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/components">Components</NuxtLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    
    <div class="container page-container">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.navbar {
  margin-bottom: 20px;
}

.nav-link.router-link-active {
  font-weight: bold;
}
</style>
