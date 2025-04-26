<template>
  <div>
    <!-- Modal -->
    <div 
      class="modal" 
      tabindex="-1" 
      :class="{'show': modelValue}" 
      :style="{'display': modelValue ? 'block' : 'none'}"
      @click.self="$emit('update:modelValue', false)"
    >
      <div class="modal-dialog" :class="size ? `modal-${size}` : ''">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ title }}</h5>
            <button 
              type="button" 
              class="btn-close" 
              @click="$emit('update:modelValue', false)"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <slot></slot>
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Backdrop -->
    <div 
      v-if="modelValue"
      class="show"
      @click="$emit('update:modelValue', false)"
    ></div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: '', // options: 'sm', 'lg', 'xl'
    validator: (val: string) => ['', 'sm', 'lg', 'xl'].includes(val)
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.modal.show {
  background-color: rgba(0, 0, 0, 0.3);
  overflow-y: auto;
}
</style>
