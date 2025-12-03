<template>
  <div class="movie-card" :class="{ watched: movie.watched }">
    <!-- Poster Container -->
    <div class="poster-container">
      <img 
        v-if="movie.poster_url && movie.poster_url !== 'N/A'"
        :src="movie.poster_url" 
        :alt="movie.title"
        class="poster-image"
        @error="posterError = true">
      <div v-else-if="posterError || !movie.poster_url" class="poster-placeholder">
        📽️
      </div>

      <!-- Hover Overlay -->
      <div class="overlay">
        <button 
          class="btn-toggle-watched"
          :class="{ watched: movie.watched }"
          @click="handleToggleWatched"
          :disabled="updating"
          :title="movie.watched ? 'Mark as unwatched' : 'Mark as watched'">
          {{ movie.watched ? '✓ Watched' : '+ Watchlist' }}
        </button>
        <button 
          class="btn-delete"
          @click="handleDelete"
          :disabled="deleting"
          title="Delete">
          🗑️
        </button>
      </div>

      <!-- Watched Badge -->
      <div v-if="movie.watched" class="watched-badge">✓</div>
      
      <!-- Rating Badge -->
      <div v-if="movie.rating" class="rating-badge">⭐ {{ movie.rating }}</div>
    </div>

    <!-- Info Section -->
    <div class="info-section">
      <h3 class="movie-title" :title="movie.title">{{ movie.title }}</h3>
      <div v-if="movie.year" class="movie-year">{{ movie.year }}</div>
      <div v-if="movie.notes" class="movie-notes">{{ movie.notes }}</div>
      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import api from '../services/api.js'

export default {
  props: {
    movie: {
      type: Object,
      required: true
    }
  },
  emits: ['updated', 'deleted'],
  setup(props, { emit }) {
    const updating = ref(false)
    const deleting = ref(false)
    const error = ref('')
    const posterError = ref(false)

    const handleToggleWatched = async () => {
      updating.value = true
      error.value = ''
      
      try {
        await api.put(`/movies/${props.movie.id}`, {
          watched: !props.movie.watched
        })
        emit('updated')
      } catch (err) {
        error.value = 'Failed to update'
      } finally {
        updating.value = false
      }
    }

    const handleDelete = async () => {
      if (!confirm('Delete this movie?')) {
        return
      }
      
      deleting.value = true
      error.value = ''
      
      try {
        await api.delete(`/movies/${props.movie.id}`)
        emit('deleted')
      } catch (err) {
        error.value = 'Failed to delete'
        deleting.value = false
      }
    }

    return {
      updating,
      deleting,
      error,
      posterError,
      handleToggleWatched,
      handleDelete
    }
  }
}
</script>

<style scoped>
.movie-card {
  background: rgba(30, 30, 30, 0.6);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.movie-card:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 0 12px 25px rgba(229, 9, 20, 0.3);
}

.movie-card.watched {
  opacity: 0.85;
}

.poster-container {
  position: relative;
  width: 100%;
  aspect-ratio: 2 / 3;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
  flex-shrink: 0;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.movie-card:hover .poster-image {
  transform: scale(1.1);
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3em;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Overlay */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
  padding: 10px;
}

.movie-card:hover .overlay {
  opacity: 1;
}

.btn-toggle-watched,
.btn-delete {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.3s;
}

.btn-toggle-watched {
  background: #e50914;
  color: white;
  width: 100%;
}

.btn-toggle-watched:hover:not(:disabled) {
  background: #c40812;
  transform: scale(1.05);
}

.btn-toggle-watched.watched {
  background: #1db954;
}

.btn-toggle-watched:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-delete {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1.2em;
  width: 40px;
  height: 40px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-delete:hover:not(:disabled) {
  background: rgba(255, 107, 107, 0.8);
}

.btn-delete:disabled {
  opacity: 0.5;
}

/* Badges */
.watched-badge,
.rating-badge {
  position: absolute;
  background: rgba(0, 0, 0, 0.8);
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: 600;
  backdrop-filter: blur(5px);
}

.watched-badge {
  top: 8px;
  left: 8px;
  background: #1db954;
  color: white;
}

.rating-badge {
  top: 8px;
  right: 8px;
  color: #ffc107;
  background: rgba(0, 0, 0, 0.9);
}

/* Info Section */
.info-section {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.movie-title {
  margin: 0;
  font-size: 0.95em;
  color: #fff;
  font-weight: 700;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.movie-year {
  color: #999;
  font-size: 0.8em;
}

.movie-notes {
  color: #ccc;
  font-size: 0.8em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.error-msg {
  color: #ff6b6b;
  font-size: 0.75em;
  margin-top: auto;
}

@media (max-width: 768px) {
  .movie-card:hover {
    transform: translateY(-4px) scale(1.02);
  }

  .overlay {
    opacity: 1;
    background: rgba(0, 0, 0, 0.9);
  }
}
</style>
