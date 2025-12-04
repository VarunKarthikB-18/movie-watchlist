<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-btn" @click="closeModal">×</button>
      
      <div class="modal-body">
        <!-- Left: Movie Poster -->
        <div class="poster-section">
          <img 
            v-if="movie.poster_url && movie.poster_url !== 'N/A'"
            :src="movie.poster_url" 
            :alt="movie.title"
            class="detail-poster">
          <div v-else class="poster-placeholder-large">📽️</div>
        </div>

        <!-- Right: Movie Details & Controls -->
        <div class="details-section">
          <h2 class="detail-title">{{ movie.title }}</h2>
          <div v-if="movie.year" class="detail-year">{{ movie.year }}</div>
          
          <div v-if="movie.plot || movie.notes" class="detail-plot">
            {{ movie.plot || movie.notes }}
          </div>

          <!-- Watched Status Toggle -->
          <div class="control-group">
            <label class="control-label">Watched Status</label>
            <button 
              class="btn-watched-toggle"
              :class="{ watched: localMovie.watched }"
              @click="toggleWatched"
              :disabled="updating || !movie.id">
              {{ localMovie.watched ? '✓ Watched' : '○ Not Watched' }}
            </button>
          </div>

          <!-- Rating Input -->
          <div class="control-group">
            <label class="control-label">Your Rating (1-10)</label>
            <div class="rating-control">
              <input 
                type="number"
                v-model.number="localMovie.rating"
                min="1"
                max="10"
                step="0.01"
                class="rating-input"
                :disabled="updating || !movie.id"
                @blur="updateRating"
                placeholder="e.g., 8.5">
              <span v-if="localMovie.rating" class="rating-display">/10</span>
            </div>
          </div>

          <!-- Notes Editor -->
          <div class="control-group">
            <label class="control-label">Notes</label>
            <textarea 
              v-model="localMovie.notes"
              class="notes-input"
              :disabled="updating || !movie.id"
              placeholder="Add your thoughts about this movie..."
              rows="4"
              @blur="updateNotes"></textarea>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons" v-if="movie.id">
            <button 
              class="btn-save"
              @click="saveChanges"
              :disabled="updating">
              {{ updating ? 'Saving...' : '💾 Save Changes' }}
            </button>
            <button 
              class="btn-delete"
              @click="handleDelete"
              :disabled="deleting">
              {{ deleting ? 'Deleting...' : '🗑️ Delete Movie' }}
            </button>
          </div>

          <!-- For demo movies -->
          <div v-else class="action-buttons">
            <button 
              class="btn-add"
              @click="handleAddToWatchlist"
              :disabled="adding">
              {{ adding ? 'Adding...' : '+ Add to Watchlist' }}
            </button>
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import api from '../services/api.js'

export default {
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    movie: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['close', 'updated', 'deleted', 'added'],
  setup(props, { emit }) {
    const updating = ref(false)
    const deleting = ref(false)
    const adding = ref(false)
    const error = ref('')
    const localMovie = ref({
      watched: false,
      rating: null,
      notes: ''
    })

    // Sync local state with movie prop
    watch(() => props.movie, (newMovie) => {
      if (newMovie) {
        localMovie.value = {
          watched: newMovie.watched || false,
          rating: newMovie.rating || null,
          notes: newMovie.notes || ''
        }
      }
    }, { immediate: true })

    const closeModal = () => {
      emit('close')
    }

    const toggleWatched = async () => {
      if (!props.movie.id) return
      updating.value = true
      error.value = ''
      
      try {
        localMovie.value.watched = !localMovie.value.watched
        await api.put(`/movies/${props.movie.id}`, {
          watched: localMovie.value.watched
        })
        emit('updated')
      } catch (err) {
        error.value = 'Failed to update watched status'
        localMovie.value.watched = !localMovie.value.watched // Revert
      } finally {
        updating.value = false
      }
    }

    const updateRating = async () => {
      if (!props.movie.id) return
      
      // Round to 2 decimal places
      if (localMovie.value.rating !== null && localMovie.value.rating !== undefined) {
        localMovie.value.rating = Math.round(localMovie.value.rating * 100) / 100
      }
      
      if (localMovie.value.rating === props.movie.rating) return
      
      updating.value = true
      error.value = ''
      
      try {
        // Clamp rating between 1-10
        if (localMovie.value.rating > 10) localMovie.value.rating = 10
        if (localMovie.value.rating < 1 && localMovie.value.rating > 0) localMovie.value.rating = 1
        if (localMovie.value.rating <= 0) localMovie.value.rating = null
        
        await api.put(`/movies/${props.movie.id}`, {
          rating: localMovie.value.rating || null
        })
        emit('updated')
      } catch (err) {
        error.value = 'Failed to update rating'
      } finally {
        updating.value = false
      }
    }

    const updateNotes = async () => {
      if (!props.movie.id) return
      if (localMovie.value.notes === props.movie.notes) return
      
      updating.value = true
      error.value = ''
      
      try {
        await api.put(`/movies/${props.movie.id}`, {
          notes: localMovie.value.notes || null
        })
        emit('updated')
      } catch (err) {
        error.value = 'Failed to update notes'
      } finally {
        updating.value = false
      }
    }

    const saveChanges = async () => {
      if (!props.movie.id) return
      updating.value = true
      error.value = ''
      
      try {
        await api.put(`/movies/${props.movie.id}`, {
          watched: localMovie.value.watched,
          rating: localMovie.value.rating || null,
          notes: localMovie.value.notes || null
        })
        emit('updated')
        closeModal()
      } catch (err) {
        error.value = 'Failed to save changes'
      } finally {
        updating.value = false
      }
    }

    const handleDelete = async () => {
      if (!props.movie.id) return
      if (!confirm('Are you sure you want to delete this movie?')) return
      
      deleting.value = true
      error.value = ''
      
      try {
        await api.delete(`/movies/${props.movie.id}`)
        emit('deleted')
        closeModal()
      } catch (err) {
        error.value = 'Failed to delete movie'
        deleting.value = false
      }
    }

    const handleAddToWatchlist = async () => {
      adding.value = true
      error.value = ''
      
      try {
        await api.post('/movies', {
          title: props.movie.title,
          year: props.movie.year || null,
          rating: props.movie.rating || null,
          notes: props.movie.plot || null,
          watched: false,
          poster_url: props.movie.poster_url || null
        })
        emit('added')
        closeModal()
      } catch (err) {
        error.value = err.response?.data?.msg || 'Failed to add movie'
      } finally {
        adding.value = false
      }
    }

    return {
      localMovie,
      updating,
      deleting,
      adding,
      error,
      closeModal,
      toggleWatched,
      updateRating,
      updateNotes,
      saveChanges,
      handleDelete,
      handleAddToWatchlist
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: linear-gradient(135deg, rgba(20, 20, 20, 0.98), rgba(30, 30, 30, 0.98));
  border-radius: 15px;
  width: 90%;
  max-width: 900px;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(229, 9, 20, 0.3);
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #fff;
  font-size: 2em;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  z-index: 10;
}

.close-btn:hover {
  background: rgba(255, 107, 107, 0.8);
  transform: rotate(90deg);
}

.modal-body {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 30px;
  padding: 40px;
}

.poster-section {
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.detail-poster {
  width: 100%;
  max-width: 300px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.poster-placeholder-large {
  width: 100%;
  max-width: 300px;
  aspect-ratio: 2/3;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 5em;
}

.details-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: #fff;
}

.detail-title {
  font-size: 2.2em;
  font-weight: 900;
  color: #fff;
  margin: 0;
  line-height: 1.2;
}

.detail-year {
  font-size: 1.2em;
  color: #999;
  font-weight: 500;
}

.detail-plot {
  color: #ccc;
  line-height: 1.6;
  font-size: 1em;
  margin: 10px 0;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.control-label {
  font-weight: 600;
  color: #fff;
  font-size: 0.95em;
}

.btn-watched-toggle {
  padding: 12px 20px;
  border: 2px solid #e50914;
  background: transparent;
  color: #e50914;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1em;
}

.btn-watched-toggle.watched {
  background: #1db954;
  border-color: #1db954;
  color: #fff;
}

.btn-watched-toggle:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
}

.btn-watched-toggle:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.rating-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-input {
  padding: 12px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: 8px;
  font-size: 1.2em;
  width: 80px;
  font-weight: 600;
}

.rating-input:focus {
  outline: none;
  border-color: #e50914;
  background: rgba(255, 255, 255, 0.15);
}

.rating-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.rating-display {
  color: #ffc107;
  font-size: 1.2em;
  font-weight: 600;
}

.notes-input {
  padding: 12px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: 8px;
  font-size: 0.95em;
  font-family: inherit;
  resize: vertical;
  width: 100%;
}

.notes-input:focus {
  outline: none;
  border-color: #e50914;
  background: rgba(255, 255, 255, 0.15);
}

.notes-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 10px;
}

.btn-save,
.btn-add {
  flex: 1;
  padding: 14px;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-save:hover:not(:disabled),
.btn-add:hover:not(:disabled) {
  background: #c40812;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
}

.btn-delete {
  flex: 1;
  padding: 14px;
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
  border: 2px solid #ff6b6b;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete:hover:not(:disabled) {
  background: rgba(255, 107, 107, 0.3);
  transform: translateY(-2px);
}

.btn-save:disabled,
.btn-add:disabled,
.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
  padding: 12px;
  border-radius: 8px;
  border-left: 3px solid #ff6b6b;
  font-size: 0.9em;
}

@media (max-width: 768px) {
  .modal-body {
    grid-template-columns: 1fr;
    padding: 30px 20px;
  }

  .poster-section {
    justify-content: center;
  }

  .detail-title {
    font-size: 1.6em;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>

