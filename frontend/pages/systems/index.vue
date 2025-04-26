<template>
  <div>
    <div class="d-flex justify-content-between align-items-center page-title">
      <h1>Systems Management</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <i class="bi bi-plus-circle me-2"></i>Create New System
      </button>
    </div>
    
    <!-- Search and filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="input-group">
          <span class="input-group-text"><i class="bi bi-search"></i></span>
          <input 
            type="text" 
            class="form-control" 
            v-model="searchQuery" 
            placeholder="Search systems by name or description..."
          >
        </div>
      </div>
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
    <div v-else-if="filteredSystems.length === 0" class="card">
      <div class="card-body empty-state">
        <i class="bi bi-inbox"></i>
        <h3>No systems found</h3>
        <p>No data is available. Use the "Create New System" button above to add your first system.</p>
        <button class="btn btn-primary mt-3" @click="showCreateModal = true">
          <i class="bi bi-plus-circle me-2"></i>Create New System
        </button>
      </div>
    </div>
    
    <!-- Systems list -->
    <div v-else class="card">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Properties</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="system in filteredSystems" :key="system.id">
              <td>{{ system.name }}</td>
              <td>{{ system.description || 'N/A' }}</td>
              <td>{{ getPropertiesCount(system.properties) }}</td>
              <td>{{ formatDate(system.created_at) }}</td>
              <td>
                <div class="btn-group">
                  <button class="btn btn-sm btn-outline-primary" @click="editSystem(system)">
                    <i class="bi bi-pencil me-1"></i>Edit
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="confirmDelete(system)">
                    <i class="bi bi-trash me-1"></i>Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Create System Modal -->
    <div class="modal" :class="{ show: showCreateModal }" 
         :style="{ display: showCreateModal ? 'block' : 'none' }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Create New System</h5>
            <button type="button" class="btn-close" @click="showCreateModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createSystem">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" class="form-control" v-model="newSystem.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="newSystem.description" rows="3"></textarea>
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
                  Create System
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class="show" v-if="showCreateModal"></div>
    </div>
    
    <!-- Edit System Modal -->
    <div class="modal" :class="{ show: editingSystem !== null }" tabindex="-1" 
         :style="{ display: editingSystem !== null ? 'block' : 'none' }">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit System</h5>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateSystem" v-if="editingSystem">
              <!-- Basic Information -->
              <div class="mb-4">
                <h6>Basic Information</h6>
                <hr>
                
                <div class="mb-3">
                  <label class="form-label">Name</label>
                  <input type="text" class="form-control" v-model="editingSystem.name" required>
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea class="form-control" v-model="editingSystem.description" rows="3"></textarea>
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
                  <div v-for="(value, key) in editingSystem.properties" :key="key" class="property-item">
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
                          v-model="editingSystem.properties[key]" 
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
              
              <!-- System Information -->
              <div class="mb-4">
                <h6>System Information</h6>
                <hr>
                
                <div class="row">
                  <div class="col-md-4">
                    <p><strong>ID:</strong> {{ editingSystem.id }}</p>
                  </div>
                  <div class="col-md-4">
                    <p><strong>Created:</strong> {{ formatDate(editingSystem.created_at) }}</p>
                  </div>
                  <div class="col-md-4">
                    <p><strong>Updated:</strong> {{ formatDate(editingSystem.updated_at) }}</p>
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
      <div class="show" v-if="editingSystem !== null"></div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div class="modal" :class="{ show: systemToDelete !== null }" tabindex="-1"
         :style="{ display: systemToDelete !== null ? 'block' : 'none' }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Delete</h5>
            <button type="button" class="btn-close" @click="systemToDelete = null"></button>
          </div>
          <div class="modal-body">
            <p v-if="systemToDelete">Are you sure you want to delete the system "{{ systemToDelete.name }}"?</p>
            <p class="text-danger"><i class="bi bi-exclamation-triangle me-2"></i>This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="systemToDelete = null">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="deleteSystem" :disabled="isSubmitting">
              <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
              Delete
            </button>
          </div>
        </div>
      </div>
      <div class="show" v-if="systemToDelete !== null"></div>
    </div>
    
    <!-- Toast Notifications -->
    <ToastNotification ref="toast" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useApi, System, SystemBase } from '~/composables/useApi'

const { systemsApi } = useApi()

// State
const systems = ref<System[]>([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const showCreateModal = ref(false)
const systemToDelete = ref<System | null>(null)
const isSubmitting = ref(false)
const editingSystem = ref<System | null>(null)
const propertyKeys = ref<Record<string, string>>({})
const toast = ref<any>(null)

const newSystem = ref<SystemBase>({
  name: '',
  description: '',
  properties: {}
})

const propertiesJson = ref('{}')

// Computed properties
const filteredSystems = computed(() => {
  if (!searchQuery.value) return systems.value
  
  const query = searchQuery.value.toLowerCase()
  return systems.value.filter(system => 
    system.name.toLowerCase().includes(query) || 
    (system.description && system.description.toLowerCase().includes(query))
  )
})

const hasProperties = computed(() => {
  return editingSystem.value?.properties && 
         Object.keys(editingSystem.value.properties).length > 0
})

const metadataJson = computed({
  get: () => {
    try {
      return JSON.stringify(editingSystem.value?.metadata || {}, null, 2)
    } catch (e) {
      return '{}'
    }
  },
  set: (val: string) => {
    try {
      if (editingSystem.value) {
        editingSystem.value.metadata = JSON.parse(val)
      }
    } catch (e) {
      // Invalid JSON - will be caught on save
    }
  }
})

// Methods
const fetchSystems = async () => {
  loading.value = true
  error.value = ''
  
  try {
    systems.value = await systemsApi.getAll()
  } catch (err: any) {
    error.value = err.message || 'Failed to load systems'
    systems.value = []
  } finally {
    loading.value = false
  }
}

const createSystem = async () => {
  isSubmitting.value = true
  
  try {
    // Parse properties JSON
    try {
      newSystem.value.properties = JSON.parse(propertiesJson.value)
    } catch (e) {
      alert('Invalid JSON in properties field. Please check the format and try again.')
      isSubmitting.value = false
      return
    }
    
    await systemsApi.create(newSystem.value)
    await fetchSystems()
    
    // Reset form and close modal
    newSystem.value = { name: '', description: '', properties: {} }
    propertiesJson.value = '{}'
    showCreateModal.value = false
    
    // Show success toast instead of alert
    toast.value.addToast({
      type: 'success',
      title: 'Success',
      message: 'System created successfully'
    })
  } catch (err: any) {
    // Show error toast instead of alert
    toast.value.addToast({
      type: 'danger',
      title: 'Error',
      message: err.message || 'Failed to create system'
    })
  } finally {
    isSubmitting.value = false
  }
}

const editSystem = (system: System) => {
  // Clone the system to avoid modifying the original directly
  editingSystem.value = JSON.parse(JSON.stringify(system))
  
  // Initialize property keys
  propertyKeys.value = {}
  if (editingSystem.value.properties) {
    Object.keys(editingSystem.value.properties).forEach(key => {
      propertyKeys.value[key] = key
    })
  }
}

const cancelEdit = () => {
  editingSystem.value = null
  propertyKeys.value = {}
}

const updateSystem = async () => {
  if (!editingSystem.value) return
  
  isSubmitting.value = true
  
  try {
    // Validate metadata JSON
    try {
      if (typeof editingSystem.value.metadata === 'string') {
        editingSystem.value.metadata = JSON.parse(editingSystem.value.metadata as unknown as string)
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
    if (editingSystem.value.properties) {
      const updatedProperties: Record<string, any> = {}
      
      Object.entries(editingSystem.value.properties).forEach(([oldKey, value]) => {
        const newKey = propertyKeys.value[oldKey] || oldKey
        updatedProperties[newKey] = value
      })
      
      editingSystem.value.properties = updatedProperties
    }
    
    const systemToUpdate = {
      name: editingSystem.value.name,
      description: editingSystem.value.description,
      properties: editingSystem.value.properties,
      metadata: editingSystem.value.metadata
    }
    
    await systemsApi.update(editingSystem.value.id, systemToUpdate)
    await fetchSystems()
    
    // Close the modal
    editingSystem.value = null
    
    // Show success toast
    toast.value.addToast({
      type: 'success',
      title: 'Success',
      message: 'System updated successfully'
    })
  } catch (err: any) {
    toast.value.addToast({
      type: 'danger',
      title: 'Error',
      message: err.message || 'Failed to update system'
    })
  } finally {
    isSubmitting.value = false
  }
}

const confirmDelete = (system: System) => {
  systemToDelete.value = system
}

const deleteSystem = async () => {
  if (!systemToDelete.value) return
  
  isSubmitting.value = true
  
  try {
    await systemsApi.delete(systemToDelete.value.id)
    await fetchSystems()
    systemToDelete.value = null
    
    // Show success toast
    toast.value.addToast({
      type: 'success',
      title: 'Success',
      message: 'System deleted successfully'
    })
  } catch (err: any) {
    toast.value.addToast({
      type: 'danger',
      title: 'Error',
      message: err.message || 'Failed to delete system'
    })
  } finally {
    isSubmitting.value = false
  }
}

const addProperty = () => {
  if (!editingSystem.value) return
  
  if (!editingSystem.value.properties) {
    editingSystem.value.properties = {}
  }
  
  const newKey = `property_${Object.keys(editingSystem.value.properties).length + 1}`
  editingSystem.value.properties[newKey] = ''
  propertyKeys.value[newKey] = newKey
}

const removeProperty = (key: string) => {
  if (!editingSystem.value || !editingSystem.value.properties) return
  
  const { [key]: _, ...rest } = editingSystem.value.properties
  editingSystem.value.properties = rest
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
onMounted(fetchSystems)
</script>

<style scoped>
.modal.show {
  display: block;
}

.modal-backdrop {
  opacity: 0.5;
}
</style>
