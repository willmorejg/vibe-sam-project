import axios from 'axios'

export interface SystemBase {
  name: string
  description?: string
  properties?: Record<string, any>
  metadata?: Record<string, any>
}

export interface System extends SystemBase {
  id: string
  created_at: string
  updated_at: string
}

export interface ComponentBase {
  name: string
  description?: string
  system_id?: string
  properties?: Record<string, any>
  metadata?: Record<string, any>
}

// Renamed from 'Component' to 'ComponentItem' to avoid conflict with Vue's Component
export interface ComponentItem extends ComponentBase {
  id: string
  created_at: string
  updated_at: string
}

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseUrl
  
  const api = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json'
    }
  })
  
  const handleError = (error: any): never => {
    console.error('API Error:', error)
    let message = 'An error occurred while communicating with the server.'
    
    if (error.response) {
      if (error.response.data?.detail) {
        message = error.response.data.detail
      } else {
        message = `Server error: ${error.response.status}`
      }
    } else if (error.request) {
      message = 'No response from server. Please check your connection.'
    } else if (error.message) {
      message = error.message
    }
    
    throw new Error(message)
  }
  
  // Systems API
  const systemsApi = {
    getAll: async () => {
      try {
        const response = await api.get<System[]>('/systems/')
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    get: async (id: string) => {
      try {
        const response = await api.get<System>(`/systems/${id}`)
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    create: async (system: SystemBase) => {
      try {
        const response = await api.post<System>('/systems/', system)
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    update: async (id: string, system: SystemBase) => {
      try {
        const response = await api.put<System>(`/systems/${id}`, system)
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    delete: async (id: string) => {
      try {
        await api.delete(`/systems/${id}`)
        return true
      } catch (error) {
        return handleError(error)
      }
    }
  }
  
  // Components API
  const componentsApi = {
    getAll: async () => {
      try {
        const response = await api.get<ComponentItem[]>('/components/')
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    get: async (id: string) => {
      try {
        const response = await api.get<ComponentItem>(`/components/${id}`)
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    create: async (component: ComponentBase) => {
      try {
        const response = await api.post<ComponentItem>('/components/', component)
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    update: async (id: string, component: ComponentBase) => {
      try {
        const response = await api.put<ComponentItem>(`/components/${id}`, component)
        return response.data
      } catch (error) {
        return handleError(error)
      }
    },
    
    delete: async (id: string) => {
      try {
        await api.delete(`/components/${id}`)
        return true
      } catch (error) {
        return handleError(error)
      }
    }
  }
  
  return {
    systemsApi,
    componentsApi
  }
}
