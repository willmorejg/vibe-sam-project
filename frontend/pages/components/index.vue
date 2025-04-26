<template>
  <div>
    <div class="d-flex justify-content-between align-items-center page-title">
      <h1>Components Management</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <i class="bi bi-plus-circle me-2"></i>Create New Component
      </button>
    </div>
    
    <!-- Search and filters -->
    <div class="mb-3">
      <input type="text" class="form-control" v-model="searchQuery" placeholder="Search components...">
    </div>
    
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
    </div>
    
    <!-- Empty state -->
    <div v-else-if="filteredComponents.length === 0" class="alert alert-info">
      No components found. Use the "Create New Component" button above to add your first component.
    </div>
    
    <!-- Components list -->
    <div v-else class="card">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>System</th>
              <th>Properties</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="component in filteredComponents" :key="component.id">
              <td>{{ component.name }}</td>
              <td>{{ component.description || 'N/A' }}</td>
              <td>{{ getSystemName(component.system_id) }}</td>
              <td>{{ getPropertiesCount(component.properties) }}</td>
              <td>{{ formatDate(component.created_at) }}</td>
              <td>
                <div class="btn-group">
                  <button class="btn btn-sm btn-outline-primary" @click="editComponent(component)">
                    <i class="bi bi-pencil me-1"></i>Edit
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(component)">
                    <i class="bi bi-trash me-1"></i>Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Create Component Modal -->
    <div class="modal" :class="{ show: showCreateModal }" 
         :style="{ display: showCreateModal ? 'block' : 'none' }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New Component</h5>
            <button type="button" class="btn-close" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createComponent">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" class="form-control" v-model="newComponent.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="newComponent.description" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">System</label>
                <select class="form-select" v-model="newComponent.system_id">
                  <option value="">None</option>
                  <option v-for="system in systems" :key="system.id" :value="system.id">
                    {{ system.name }}
                  </option>
                </select>
                <div class="form-text" v-if="systems.length === 0">
                  No systems available. <NuxtLink to="/systems">Create a system first</NuxtLink>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Properties (JSON)</label>
                <textarea 
                  class="form-control json-input"
                  v-model="propertiesJson"
                  rows="5"
                  placeholder='{"key1": "value1", "key2": "value2"}'
                ></textarea>
                <div class="form-text">Enter properties as valid JSON object</div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="showCreateModal = false">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                  <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                  Create Component
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="show" v-if="showCreateModal"></div>
    </div>
    
    <!-- Edit Component Modal -->
    <div class="modal" :class="{ show: editingComponent !== null }" tabindex="-1" 
         :style="{ display: editingComponent !== null ? 'block' : 'none' }">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Component</h5>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateComponent" v-if="editingComponent">
              <!-- Basic Information -->
              <div class="mb-4">
                <h6>Basic Information</h6>
                <hr>
                
                <div class="mb-3">
                  <label class="form-label">Name</label>
                  <input type="text" class="form-control" v-model="editingComponent.name" required>
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea class="form-control" v-model="editingComponent.description" rows="3"></textarea>
                </div>
                
                <div class="mb-3">
                  <label class="form-label">System</label>
                  <select class="form-select" v-model="editingComponent.system_id">
                    <option value="">None</option>
                    <option v-for="system in systems" :key="system.id" :value="system.id">
                      {{ system.name }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- Properties -->
              <div class="mb-4">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <h6>Properties</h6>
                  <button type="button" class="btn btn-sm btn-outline-primary" @click="addProperty">
                    <i class="bi bi-plus-circle me-2"></i>Add Property
                  </button>
                </div>
                <hr>
                
                <div v-if="!hasProperties" class="text-center py-4 text-muted">
                  <i class="bi bi-card-list d-block mb-2" style="font-size: 1.5rem;"></i>
                  <p>No properties defined yet</p>
                </div>
                
                <div v-else>
                  <div v-for="(value, key) in editingComponent.properties" :key="key" class="property-item">
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
                          v-model="editingComponent.properties[key]" 
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
                <h6>Metadata</h6>
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
                <h6>Component Information</h6>
                <hr>
                
                <div class="row">
                  <div class="col-md-4">
                    <p><strong>ID:</strong> {{ editingComponent.id }}</p>
                  </div>
                  <div class="col-md-4">
                    <p><strong>Created:</strong> {{ formatDate(editingComponent.created_at) }}</p>
                  </div>
                  <div class="col-md-4">
                    <p><strong>Updated:</strong> {{ formatDate(editingComponent.updated_at) }}</p>
                  </div>
                </div>
              </div>
              
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="cancelEdit">
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                  <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="show" v-if="editingComponent !== null"></div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div class="modal" :class="{ show: componentToDelete !== null }" tabindex="-1"
         :style="{ display: componentToDelete !== null ? 'block' : 'none' }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="componentToDelete = null"></button>
          </div>
          <div class="modal-body">
            <p v-if="componentToDelete">Are you sure you want to delete the component "{{ componentToDelete.name }}"?</p>
            <p class="text-danger"><i class="bi bi-exclamation-triangle me-2"></i>This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="componentToDelete = null">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="deleteComponent" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              Delete
            </button>
          </div>
        </div>
      </div>
      <div class="show" v-if="componentToDelete !== null"></div>
    </div>
    
    <!-- Toast Notifications -->
    <ToastNotification ref="toast" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, ComponentItem, ComponentBase, System } from '~/composables/useApi'

const { componentsApi, systemsApi } = useApi()

// State
const components = ref<ComponentItem[]>([])
const systems = ref<System[]>([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const showCreateModal = ref(false)
const componentToDelete = ref<ComponentItem | null>(null)
const isSubmitting = ref(false)
const editingComponent = ref<ComponentItem | null>(null)
const propertyKeys = ref<Record<string, string>>({})
const toast = ref<any>(null)

const newComponent = ref<ComponentBase>({
  name: '',
  description: '',
  system_id: '',
  properties: {}
})

const propertiesJson = ref('{}')

// Computed
const filteredComponents = computed(() => {
  if (!searchQuery.value) return components.value
  
  const query = searchQuery.value.toLowerCase()
  return components.value.filter(component => 
    component.name.toLowerCase().includes(query) || 
    (component.description && component.description.toLowerCase().includes(query))
  )
})

const hasProperties = computed(() => {
  return editingComponent.value?.properties && 
         Object.keys(editingComponent.value.properties).length > 0
})

const metadataJson = computed({
  get: () => {
    try {
      return JSON.stringify(editingComponent.value?.metadata || {}, null, 2)
    } catch (e) {
      return '{}'
    }
  },
  set: (val: string) => {
    try {
      if (editingComponent.value) {
        editingComponent.value.metadata = JSON.parse(val)
      }
    } catch (e) {
      // Invalid JSON - will be caught on save
    }
  }
})

// Methods
const fetchData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const [componentsData, systemsData] = await Promise.all([
      componentsApi.getAll(),
      systemsApi.getAll()
    ])
    
    components.value = componentsData
    systems.value = systemsData
  } catch (err: any) {
    error.value = err.message || 'Failed to load data'
    components.value = []
    systems.value = []
  } finally {
    loading.value = false
  }
}

const getSystemName = (systemId?: string) => {
  if (!systemId) return 'None'
  const system = systems.value.find(s => s.id === systemId)
  return system ? system.name : 'Unknown'
}

const createComponent = async () => {
  isSubmitting.value = true
  
  try {
    // Parse properties JSON
    try {
      newComponent.value.properties = JSON.parse(propertiesJson.value)
    } catch (e) {
      alert('Invalid JSON in properties field. Please check the format and try again.')
      isSubmitting.value = false
      return
    }
    
    // Set system_id to undefined if empty string to avoid API validation errors
    if (newComponent.value.system_id === '') {
      newComponent.value.system_id = undefined
    }
    
    await componentsApi.create(newComponent.value)
    await fetchData()
    
    // Reset form and close modal
    newComponent.value = { name: '', description: '', system_id: '', properties: {} }
    propertiesJson.value = '{}'
    showCreateModal.value = false
    
    // Show success toast
    toast.value.addToast({
      type: 'success',
      title: 'Success',
      message: 'Component created successfully'
    })
  } catch (err: any) {
    toast.value.addToast({
      type: 'danger',
      title: 'Error',
      message: err.message || 'Failed to create component'
    })
  } finally {
    isSubmitting.value = false
  }
}

const editComponent = (component: ComponentItem) => {
  // Clone the component to avoid modifying the original directly
  editingComponent.value = JSON.parse(JSON.stringify(component))
  
  // Initialize property keys
  propertyKeys.value = {}
  if (editingComponent.value.properties) {
    Object.keys(editingComponent.value.properties).forEach(key => {
      propertyKeys.value[key] = key
    })
  }
}

const cancelEdit = () => {
  editingComponent.value = null
  propertyKeys.value = {}
}

const updateComponent = async () => {
  if (!editingComponent.value) return
  
  isSubmitting.value = true
  
  try {
    // Validate metadata JSON
    try {
      if (typeof editingComponent.value.metadata === 'string') {
        editingComponent.value.metadata = JSON.parse(editingComponent.value.metadata as unknown as string)
      }
    } catch (e) {
      toast.value.addToast({
        type: 'danger',
        title: 'Validation Error',
        message: 'Invalid metadata JSON. Please check the format and try again.'
      })
      isSubmitting.value = false
      return
    }
    
    // Update properties with new keys
    if (editingComponent.value.properties) {
      const updatedProperties: Record<string, any> = {}
      
      Object.entries(editingComponent.value.properties).forEach(([oldKey, value]) => {
        const newKey = propertyKeys.value[oldKey] || oldKey
        updatedProperties[newKey] = value
      })
      
      editingComponent.value.properties = updatedProperties
    }
    
    // Set system_id to undefined if empty string
    if (editingComponent.value.system_id === '') {
      editingComponent.value.system_id = undefined
    }
    
    const componentToUpdate = {
      name: editingComponent.value.name,
      description: editingComponent.value.description,
      system_id: editingComponent.value.system_id,
      properties: editingComponent.value.properties,
      metadata: editingComponent.value.metadata
    }
    
    await componentsApi.update(editingComponent.value.id, componentToUpdate)
    await fetchData()
    
    // Close the modal
    editingComponent.value = null
    
    // Show success toast
    toast.value.addToast({
      type: 'success',
      title: 'Success',
      message: 'Component updated successfully'
    })
  } catch (err: any) {
    toast.value.addToast({
      type: 'danger',
      title: 'Error',
      message: err.message || 'Failed to update component'
    })
  } finally {
    isSubmitting.value = false
  }
}

const confirmDelete = (component: ComponentItem) => {
  componentToDelete.value = component
}

const deleteComponent = async () => {
  if (!componentToDelete.value) return
  
  isSubmitting.value = true
  
  try {
    await componentsApi.delete(componentToDelete.value.id)
    await fetchData()
    componentToDelete.value = null
    
    // Show success toast
    toast.value.addToast({
      type: 'success',
      title: 'Success',
      message: 'Component deleted successfully'
    })
  } catch (err: any) {
    toast.value.addToast({
      type: 'danger',
      title: 'Error',
      message: err.message || 'Failed to delete component'
    })
  } finally {
    isSubmitting.value = false
  }
}

const addProperty = () => {
  if (!editingComponent.value) return
  
  if (!editingComponent.value.properties) {
    editingComponent.value.properties = {}
  }
  
  const newKey = `property_${Object.keys(editingComponent.value.properties).length + 1}`
  editingComponent.value.properties[newKey] = ''
  propertyKeys.value[newKey] = newKey
}

const removeProperty = (key: string) => {
  if (!editingComponent.value || !editingComponent.value.properties) return
  
  const { [key]: _, ...rest } = editingComponent.value.properties
  editingComponent.value.properties = rest
  delete propertyKeys.value[key]
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const getPropertiesCount = (properties: Record<string, any> | undefined) => {
  if (!properties) return '0 properties'
  const count = Object.keys(properties).length
  return count === 1 ? '1 property' : `${count} properties`
}

// Initialize
onMounted(fetchData)
</script>

<style scoped>
.modal.show {
  display: block;
}

.modal-backdrop {
  opacity: 0.5;
}
</style>
