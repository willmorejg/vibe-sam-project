<template>
  <div class="toast-container position-fixed top-0 end-0 p-3">
    <div v-for="(toast, index) in toasts" :key="index" 
         class="toast show" 
         :class="`bg-${toast.type} text-white`" 
         role="alert" 
         aria-live="assertive" 
         aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">{{ toast.title }}</strong>
        <button type="button" class="btn-close" @click="removeToast(index)"></button>
      </div>
      <div class="toast-body">
        {{ toast.message }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Toast {
  type: 'success' | 'danger' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

const toasts = ref<Toast[]>([])

// Function to add a toast
const addToast = (toast: Toast) => {
  toasts.value.push(toast)
  
  // Auto remove toast after specified duration (default: 5000ms)
  setTimeout(() => {
    removeToast(toasts.value.length - 1)
  }, toast.duration || 5000)
}

// Function to remove a toast
const removeToast = (index: number) => {
  toasts.value.splice(index, 1)
}

// Expose functions to the parent component
defineExpose({
  addToast
})
</script>

<style scoped>
.toast-container {
  z-index: 1100;
}

.toast {
  min-width: 250px;
}
</style>
