<template>
  <div class="color-mode-toggle">
    <button class="btn" @click="toggleColorMode" :title="buttonTitle">
      <i class="bi" :class="colorModeIcon"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// Fix: Use the composable provided by Nuxt instead of direct import
const colorMode = useColorMode();

const colorModeIcon = computed(() => {
  return colorMode.value === 'dark' ? 'bi-sun' : 'bi-moon';
});

const buttonTitle = computed(() => {
  return colorMode.value === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
});

const toggleColorMode = () => {
  colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark';
};
</script>

<style scoped>
.color-mode-toggle {
  display: inline-block;
}

.color-mode-toggle .btn {
  padding: 0.25rem 0.5rem;
  font-size: 1.2rem;
  color: var(--text-color);
}

.dark-mode .color-mode-toggle .btn {
  color: #f8f9fa;
}

.light-mode .color-mode-toggle .btn {
  color: #212529;
}
</style>
