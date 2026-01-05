<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="/logo-banner.png" alt="红墨" class="login-logo" />
        <p class="login-subtitle">请输入访问令牌以继续</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="token">访问令牌</label>
          <input
            id="token"
            v-model="token"
            type="password"
            placeholder="请输入您的访问令牌"
            :disabled="loading"
            autocomplete="off"
            autofocus
          />
        </div>

        <p v-if="error" class="error-message">{{ error }}</p>

        <button type="submit" class="login-btn" :disabled="loading || !token.trim()">
          <span v-if="loading">验证中...</span>
          <span v-else>登录</span>
        </button>
      </form>

      <div class="login-footer">
        <p>访问令牌由管理员分配</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const token = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!token.value.trim()) return

  loading.value = true
  error.value = ''

  const result = await authStore.login(token.value.trim())

  if (result.success) {
    router.push('/')
  } else {
    error.value = result.error || '登录失败'
  }

  loading.value = false
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  height: 48px;
  margin-bottom: 16px;
}

.login-subtitle {
  color: #666;
  font-size: 14px;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--primary, #e74c3c);
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.form-group input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 13px;
  margin: 0;
  padding: 8px 12px;
  background: #fef2f2;
  border-radius: 6px;
}

.login-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary, #e74c3c) 0%, #ff6b6b 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
}

.login-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 24px;
  text-align: center;
}

.login-footer p {
  color: #999;
  font-size: 12px;
  margin: 0;
}
</style>
