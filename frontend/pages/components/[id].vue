<template>
  <div>
    <!-- Loading state -->
    <div v-if="loading" class="d-flex justify-content-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
      <div class="mt-3">
        <NuxtLink to="/components" class="btn btn-primary">
          <i class="bi bi-arrow-left me-2"></i>Back to Components
        </NuxtLink>
      </div>
    </div>
    
    <!-- Component details -->
    <div v-else>
      <div class="d-flex justify-content-between align-items-center page-title">
        <h1>Edit Component</h1>
        <NuxtLink to="/components" class="btn btn-outline-secondary">
          <i class="bi bi-arrow-left me-2"></i>Back to Components
        </NuxtLink>
      </div>
      
      <div class="card mb-4">
        <div class="card-body">
          <form @submit.prevent="updateComponent">
            <!-- Basic Information -->
            <div class="mb-4">
              <h4>Basic Information</h4>
              <hr>
              
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" class="form-control" v-model="component.name" required>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="component.description" rows="3"></textarea>
              </div>
              
              <div class="mb-3">
                <label class="form-label">System</label>
                <select class="form-select" v-model="component.system_id">
                  <option value="">None</option>
                  <option v-for="system in systems" :key="system.id" :value="system.id">
                    {{ system.name }}
                  </option>
                </select>
                <div class="form-text" v-if="systems.length === 0">
                  No systems available. <NuxtLink to="/systems">Create a system first</NuxtLink>
                </div>
              </div>
            </div>
            
            <!-- Properties -->
            <div class="mb-4">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <h4>Properties</h4>
                <button type="button" class="btn btn-sm btn-outline-primary" @click="addProperty">
                  <i class="bi bi-plus-circle me-2"></i>Add Property
                </button>
              </div>
              <hr>
              
              <div v-if="!hasProperties" class="empty-state py-4">
                <i class="bi bi-card-list"></i>
                <p>No properties defined yet</p>
                <button type="button" class="btn btn-outline-primary" @click="addProperty">
                  <i class="bi bi-plus-circle me-2"></i>Add First Property
                </button>
              </div>
              
              <div v-else>
                <div v-for="(value, key) in component.properties" :key="key" class="property-item">
                  <div class="row">
                    <div class="col-md-5 mb-3">
                      <label class="form-label">Property Name</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        v-model="propertyKeys[key]" 
                        placeholder="Property name"
                      >
                    </div>
                    <div class="col-md-5 mb-3">
                      <label class="form-label">Property Value</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        v-model="component.properties[key]" 
                        placeholder="Property value"
                      >
                    </div>
                    <div class="col-md-2 mb-3">
                      <label class="form-label">&nbsp;</label>
                      <button 
                        type="button" 
                        class="btn btn-outline-danger form-control" 
                        @click="removeProperty(key)"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Metadata -->
            <div class="mb-4">
              <h4>Metadata</h4>
              <hr>
              
              <div class="mb-3">
                <label class="form-label">Metadata (JSON)</label>
                <textarea 
                  class="form-control json-input" 
                  v-model="metadataJson" 
                  rows="5"
                  placeholder='{"key1": "value1", "key2": "value2"}'
                ></textarea>
                <div class="form-text">Enter metadata as valid JSON object</div>
              </div>
            </div>
            
            <!-- Component Information -->
            <div class="mb-4">
              <h4>Component Information</h4>
              <hr>
              
              <div class="row">
                <div class="col-md-4">
                  <p><strong>ID:</strong> {{ component.id }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Created:</strong> {{ formatDate(component.created_at) }}</p>
                </div>
                <div class="col-md-4">
                  <p><strong>Updated:</strong> {{ formatDate(component.updated_at) }}</p>
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="d-flex justify-content-end">
              <NuxtLink to="/components" class="btn btn-secondary me-2">
                Cancel
              </NuxtLink>
              <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, ComponentItem, System } from '~/composables/useApi'

const route = useRoute()
const { componentsApi, systemsApi } = useApi()

// State
const component = ref<ComponentItem>({
  id: '',
  name: '',
  description: '',
  system_id: '',
  properties: {},
  metadata: {},
  created_at: '',
  updated_at: ''
})

const systems = ref<System[]>([])
const propertyKeys = ref<Record<string, string>>({})
const loading = ref(true)
const error = ref('')
const isSubmitting = ref(false)

// Computed
const hasProperties = computed(() => {
  return component.value.properties && Object.keys(component.value.properties).length > 0
})

const metadataJson = computed({
  get: () => {
    try {
      return JSON.stringify(component.value.metadata || {}, null, 2)
    } catch (e) {
      return '{}'
    }
  },
  set: (val: string) => {
    try {
      component.value.metadata = JSON.parse(val)
    } catch (e) {
      // Invalid JSON - will be caught on save
    }
  }
})

// Methods
const fetchData = async () => {
  const id = route.params.id as string
  if (!id) {
    error.value = 'No component ID provided'
    loading.value = false
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    const [componentData, systemsData] = await Promise.all([
      componentsApi.get(id),
      systemsApi.getAll()
    ])
    
    component.value = componentData
    systems.value = systemsData
    
    // Initialize properties if not defined
    if (!component.value.properties) {
      component.value.properties = {}
    }
    
    // Initialize property keys
    propertyKeys.value = {}
    Object.keys(component.value.properties).forEach(key => {
      propertyKeys.value[key] = key
    })
    
  } catch (err: any) {
    error.value = err.message || 'Failed to load component'
  } finally {
    loading.value = false
  }
}

const updateComponent = async () => {
  isSubmitting.value = true
  
  try {
    // Validate metadata JSON
    try {
      if (typeof component.value.metadata === 'string') {
        component.value.metadata = JSON.parse(component.value.metadata as unknown as string)
      }
    } catch (e) {
      alert('Invalid metadata JSON. Please check the format and try again.')
      isSubmitting.value = false
      return
    }
    
    // Update properties with new keys
    if (component.value.properties) {
      const updatedProperties: Record<string, any> = {}
      
      Object.entries(component.value.properties).forEach(([oldKey, value]) => {
        const newKey = propertyKeys.value[oldKey] || oldKey
        updatedProperties[newKey] = value
      })
      
      component.value.properties = updatedProperties
    }
    
    // Set system_id to undefined if empty string
    if (component.value.system_id === '') {
      component.value.system_id = undefined
    }
    
    const componentToUpdate = {
      name: component.value.name,
      description: component.value.description,
      system_id: component.value.system_id,
      properties: component.value.properties,
      metadata: component.value.metadata
    }
    
    await componentsApi.update(component.value.id, componentToUpdate)
    await fetchData()
    
    // Show success message
    alert('Component updated successfully!')
    
  } catch (err: any) {
    alert(err.message || 'Failed to update component')
  } finally {
    isSubmitting.value = false
  }
}

const addProperty = () => {
  if (!component.value.properties) {
    component.value.properties = {}
  }
  
  const newKey = `property_${Object.keys(component.value.properties).length + 1}`
  component.value.properties[newKey] = ''
  propertyKeys.value[newKey] = newKey
}

const removeProperty = (key: string) => {
  if (component.value.properties) {
    const { [key]: _, ...rest } = component.value.properties
    component.value.properties = rest
    delete propertyKeys.value[key]
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

// Initialize
onMounted(fetchData)
</script>
