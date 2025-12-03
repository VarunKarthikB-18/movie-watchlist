<template>
  <form @submit.prevent="handleRegister" class="form">
    <div class="form-group">
      <label for="email">Email</label>
      <input 
        id="email"
        v-model="email" 
        type="email" 
        placeholder="you@example.com"
        required>
    </div>
    
    <div class="form-group">
      <label for="password">Password</label>
      <input 
        id="password"
        v-model="password" 
        type="password" 
        placeholder="••••••"
        required>
    </div>
    
    <div class="form-group">
      <label for="password-confirm">Confirm Password</label>
      <input 
        id="password-confirm"
        v-model="passwordConfirm" 
        type="password" 
        placeholder="••••••"
        required>
    </div>
    
    <button type="submit" :disabled="loading" class="btn-primary">
      {{ loading ? 'Registering...' : 'Register' }}
    </button>
    
    <div v-if="error" class="form-error">{{ error }}</div>
  </form>
</template>

<script>
import { ref } from 'vue'
import { register, login } from '../services/auth.js'

export default {
  emits: ['register'],
  setup(props, { emit }) {
    const email = ref('')
    const password = ref('')
    const passwordConfirm = ref('')
    const loading = ref(false)
    const error = ref('')

    const handleRegister = async () => {
      error.value = ''
      
      if (password.value !== passwordConfirm.value) {
        error.value = 'Passwords do not match'
        return
      }
      
      if (password.value.length < 6) {
        error.value = 'Password must be at least 6 characters'
        return
      }
      
      loading.value = true
      
      try {
        await register(email.value, password.value)
        // Auto-login after successful registration
        await login(email.value, password.value)
        emit('register')
      } catch (err) {
        error.value = err.response?.data?.msg || 'Registration failed. Please try again.'
      } finally {
        loading.value = false
      }
    }

    return {
      email,
      password,
      passwordConfirm,
      loading,
      error,
      handleRegister
    }
  }
}
</script>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: 600;
  color: #333;
  font-size: 0.95em;
}

input {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1em;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-primary {
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-error {
  color: #ff6b6b;
  font-size: 0.9em;
  background: #ffe0e0;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
}
</style>
