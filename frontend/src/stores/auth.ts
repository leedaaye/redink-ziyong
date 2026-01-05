import { defineStore } from 'pinia'
import axios from 'axios'

const TOKEN_KEY = 'redink_access_token'
const API_BASE_URL = '/api'

interface AuthState {
  token: string | null
  isAuthenticated: boolean
  isValidating: boolean
  user: { username: string } | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem(TOKEN_KEY),
    isAuthenticated: false,
    isValidating: false,
    user: null
  }),

  actions: {
    setToken(token: string) {
      this.token = token
      localStorage.setItem(TOKEN_KEY, token)
    },

    clearToken() {
      this.token = null
      this.isAuthenticated = false
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
    },

    async validateToken(): Promise<boolean> {
      if (!this.token) {
        this.isAuthenticated = false
        return false
      }

      this.isValidating = true
      try {
        const response = await axios.get(`${API_BASE_URL}/auth/validate`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })

        if (response.data.success) {
          this.isAuthenticated = true
          this.user = response.data.user
          return true
        } else {
          this.clearToken()
          return false
        }
      } catch {
        this.clearToken()
        return false
      } finally {
        this.isValidating = false
      }
    },

    async login(token: string): Promise<{ success: boolean; error?: string }> {
      this.setToken(token)
      const valid = await this.validateToken()
      if (!valid) {
        return { success: false, error: '访问令牌无效' }
      }
      return { success: true }
    },

    logout() {
      this.clearToken()
    }
  }
})
