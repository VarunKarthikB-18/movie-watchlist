<template>
  <div class="movie-list">
    <div v-if="movies.length === 0" class="empty-state">
      <p>📭 No movies found</p>
    </div>
    
    <div v-else class="movies-grid">
      <MovieCard 
        v-for="movie in movies" 
        :key="movie.id"
        :movie="movie"
        @updated="$emit('movie-updated')"
        @deleted="$emit('movie-deleted')" />
    </div>
  </div>
</template>

<script>
import MovieCard from './MovieCard.vue'

export default {
  components: {
    MovieCard
  },
  props: {
    movies: {
      type: Array,
      required: true
    }
  },
  emits: ['movie-updated', 'movie-deleted']
}
</script>

<style scoped>
.movie-list {
  width: 100%;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 1.2em;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 25px;
  padding: 20px 0;
}

@media (max-width: 1200px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .movies-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 10px;
  }
}
</style>
