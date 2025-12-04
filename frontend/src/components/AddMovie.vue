<template>
  <div class="add-movie-card">
    <h2 class="card-title">➕ Add New Movie</h2>
    
    <div class="search-section">
      <div class="search-box">
        <input 
          v-model="searchQuery"
          @keyup.enter="searchTMDB"
          type="text"
          placeholder="Search for a movie..."
          class="search-input">
        <button @click="searchTMDB" class="search-btn" :disabled="!searchQuery || searching">
          {{ searching ? 'Searching...' : '🔍' }}
        </button>
      </div>

      <div v-if="searchResults.length > 0" class="search-results">
        <div 
          v-for="result in searchResults" 
          :key="result.imdbID"
          class="result-item"
          @click="selectFromSearch(result)">
          <img 
            v-if="result.poster_url && result.poster_url !== 'N/A'"
            :src="result.poster_url" 
            :alt="result.title"
            class="result-poster">
          <div v-else class="result-placeholder">📽️</div>
          <div class="result-info">
            <p class="result-title">{{ result.title }}</p>
            <p class="result-year">{{ result.year }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="form-divider">OR</div>

    <form @submit.prevent="handleAddMovie" class="form">
      <div class="form-group">
        <label for="title">Movie Title *</label>
        <input 
          id="title"
          v-model="title" 
          type="text"
          placeholder="Enter movie title"
          required>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="year">Year</label>
          <input 
            id="year"
            v-model.number="year" 
            type="number"
            placeholder="2024"
            min="1900"
            max="2099">
        </div>
        
        <div class="form-group">
          <label for="rating">Rating (1-10)</label>
          <div class="rating-input-wrapper">
            <input 
              id="rating"
              v-model.number="rating" 
              type="number"
              placeholder="e.g., 8.5"
              min="1"
              max="10"
              step="0.01"
              @blur="validateRating">
            <span v-if="rating !== null && rating !== undefined" class="rating-display">{{ rating }}/10</span>
          </div>
          <div v-if="ratingError" class="input-error">{{ ratingError }}</div>
        </div>
      </div>
      
      <div class="form-group">
        <label for="notes">Notes</label>
        <textarea 
          id="notes"
          v-model="notes" 
          placeholder="Add your notes..."
          rows="3"></textarea>
      </div>

      <div class="form-group checkbox">
        <input 
          id="watched"
          v-model="watched" 
          type="checkbox">
        <label for="watched">Mark as watched</label>
      </div>

      <button type="submit" :disabled="loading" class="btn-submit">
        {{ loading ? '⏳ Adding...' : '➕ Add to Watchlist' }}
      </button>
      
      <div v-if="error" class="form-error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'
import { searchMoviesTMDB } from '../services/tmdb.js'
import api from '../services/api.js'

export default {
  emits: ['movie-added'],
  setup(props, { emit }) {
    const title = ref('')
    const year = ref(new Date().getFullYear())
    const rating = ref(null)
    const notes = ref('')
    const watched = ref(false)
    const loading = ref(false)
    const error = ref('')
    const ratingError = ref('')
    const searchQuery = ref('')
    const searching = ref(false)
    const searchResults = ref([])
    const selectedPosterUrl = ref(null)

    const validateRating = () => {
      if (rating.value !== null && rating.value !== undefined) {
        // Round to 2 decimal places
        rating.value = Math.round(rating.value * 100) / 100
        
        if (rating.value > 10) {
          rating.value = 10
          ratingError.value = 'Rating cannot exceed 10'
          setTimeout(() => ratingError.value = '', 3000)
        } else if (rating.value < 1 && rating.value > 0) {
          rating.value = 1
          ratingError.value = 'Rating must be at least 1'
          setTimeout(() => ratingError.value = '', 3000)
        } else if (rating.value <= 0) {
          rating.value = null
          ratingError.value = ''
        } else {
          ratingError.value = ''
        }
      }
    }

    const searchTMDB = async () => {
      if (!searchQuery.value.trim()) return
      searching.value = true
      searchResults.value = []
      try {
        const results = await searchMoviesTMDB(searchQuery.value)
        searchResults.value = results
      } catch (err) {
        error.value = 'Failed to search movies'
      } finally {
        searching.value = false
      }
    }

    const selectFromSearch = (result) => {
      title.value = result.title
      year.value = result.year
      // Store poster_url in a ref so we can send it when adding
      selectedPosterUrl.value = result.poster_url || null
      searchResults.value = []
      searchQuery.value = ''
    }

    const handleAddMovie = async () => {
      error.value = ''
      loading.value = true
      
      try {
        // If no poster selected, try to find one automatically
        if (!selectedPosterUrl.value && title.value) {
          try {
            const results = await searchMoviesTMDB(title.value)
            if (results && results.length > 0) {
              // Use the first result's poster
              selectedPosterUrl.value = results[0].poster_url
            }
          } catch (err) {
            console.warn('Auto-fetch poster failed:', err)
          }
        }

        await api.post('/movies', {
          title: title.value,
          year: year.value || null,
          rating: rating.value || null,
          notes: notes.value || null,
          watched: watched.value,
          poster_url: selectedPosterUrl.value || null
        })
        
        title.value = ''
        year.value = new Date().getFullYear()
        rating.value = null
        notes.value = ''
        watched.value = false
        selectedPosterUrl.value = null
        
        emit('movie-added')
      } catch (err) {
        error.value = err.response?.data?.msg || 'Failed to add movie'
      } finally {
        loading.value = false
      }
    }

    return {
      title,
      year,
      rating,
      notes,
      watched,
      loading,
      error,
      ratingError,
      searchQuery,
      searching,
      searchResults,
      selectedPosterUrl,
      searchTMDB,
      selectFromSearch,
      validateRating,
      handleAddMovie
    }
  }
}
</script>

<style scoped>
.add-movie-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 100%;
}

.card-title {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3em;
  font-weight: 700;
}

.search-section {
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95em;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-btn {
  padding: 12px 20px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s;
  font-weight: 600;
}

.search-btn:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.search-results {
  background: #f8f9fa;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
}

.result-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: all 0.2s;
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background: white;
}

.result-poster {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 12px;
}

.result-placeholder {
  width: 40px;
  height: 60px;
  background: #ddd;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5em;
  margin-right: 12px;
}

.result-info {
  flex: 1;
}

.result-title {
  font-weight: 600;
  color: #333;
  margin: 0 0 4px 0;
  font-size: 0.95em;
}

.result-year {
  color: #999;
  margin: 0;
  font-size: 0.85em;
}

.form-divider {
  text-align: center;
  color: #999;
  margin: 25px 0;
  font-weight: 600;
  position: relative;
  display: flex;
  align-items: center;
  gap: 15px;
}

.form-divider::before,
.form-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e0e0e0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 8px;
}

.form-group.checkbox input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.form-group.checkbox label {
  margin: 0;
  cursor: pointer;
  font-weight: 500;
}

label {
  font-weight: 600;
  color: #333;
  font-size: 0.9em;
}

.rating-input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.rating-display {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9em;
  min-width: 40px;
}

.input-error {
  color: #f44336;
  font-size: 0.8em;
  margin-top: 4px;
}

input[type="text"],
input[type="number"],
textarea {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95em;
  font-family: inherit;
  transition: all 0.3s;
  width: 100%;
}

input[type="text"]:focus,
input[type="number"]:focus,
textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

textarea {
  resize: vertical;
  min-height: 70px;
}

.btn-submit {
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95em;
  cursor: pointer;
  transition: all 0.3s;
  align-self: flex-start;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-error {
  color: #f44336;
  font-size: 0.9em;
  background: #ffebee;
  padding: 12px;
  border-radius: 6px;
  border-left: 3px solid #f44336;
}
</style>
