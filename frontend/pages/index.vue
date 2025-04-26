<template>
  <div>
    <div class="card">
      <div class="card-body">
        <h1 class="card-title">VIBE-SAM Management</h1>
        <p class="card-text">A comprehensive management system for components and systems.</p>
        <hr>
        <p>Choose an option below to get started:</p>
      </div>
    </div>
    
    <div class="row mt-4">
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h2 class="card-title">Systems</h2>
            <p class="card-text">Manage systems and their properties. Create, update, delete and view system details.</p>
            <div class="mt-auto">
              <NuxtLink to="/systems" class="btn btn-primary">
                <i class="bi bi-gear me-2"></i>Manage Systems
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 mb-4">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <h2 class="card-title">Components</h2>
            <p class="card-text">Manage components and their associations with systems. Create, update, delete and view component details.</p>
            <div class="mt-auto">
              <NuxtLink to="/components" class="btn btn-primary">
                <i class="bi bi-cpu me-2"></i>Manage Components
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
