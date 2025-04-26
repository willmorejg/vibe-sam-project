// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@nuxt/ui',
    '@nuxtjs/color-mode'
  ],

  // Configure color mode
  colorMode: {
    preference: 'dark', // default value of $colorMode.preference
    fallback: 'dark',   // fallback value if not system preference found
    hid: 'nuxt-color-mode-script',
    globalName: '__NUXT_COLOR_MODE__',
    componentName: 'ColorScheme',
    classPrefix: '',
    classSuffix: '',
    storageKey: 'nuxt-color-mode'
  },

  css: [
    'bootstrap/dist/css/bootstrap.min.css',
    'bootstrap-icons/font/bootstrap-icons.css',
    '~/assets/css/main.css'
  ],

  // Ensure Bootstrap is correctly loaded
  app: {
    baseURL: '/ui/',
    head: {
      title: 'VIBE-SAM Management',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Management system for components and systems' }
      ],
      script: [
        {
          src: 'https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js',
          body: true
        },
        {
          src: 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js',
          body: true
        }
      ]
    }
  },

  ssr: false,

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    }
  },

  typescript: {
    strict: true
  },

  ui: {
    global: true,
    icons: ['heroicons', 'bi']
  },

  compatibilityDate: '2025-04-26'
})