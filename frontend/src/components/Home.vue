<template>
  <div class="home-container" style="min-height: 100vh;">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1>Welcome to CINEWATCH 🎬</h1>
        <p>Track, rate, and discover your favorite movies</p>
      </div>
    </section>

    <!-- Main Content: Stats & Charts on Left, Trending on Right -->
    <div class="home-layout">
      <!-- LEFT COLUMN: Stats & Pie Chart -->
      <div class="left-column">
        <!-- Quick Stats -->
        <section class="quick-stats">
          <div class="stat-card">
            <span class="stat-icon">🎬</span>
            <div class="stat-info">
              <span class="stat-number">{{ totalMovies }}</span>
              <span class="stat-label">Total Movies</span>
            </div>
          </div>
          <div class="stat-card">
            <span class="stat-icon">✓</span>
            <div class="stat-info">
              <span class="stat-number">{{ watchedCount }}</span>
              <span class="stat-label">Watched</span>
            </div>
          </div>
          <div class="stat-card">
            <span class="stat-icon">📽️</span>
            <div class="stat-info">
              <span class="stat-number">{{ unwatchedCount }}</span>
              <span class="stat-label">To Watch</span>
            </div>
          </div>
        </section>

        <!-- Pie Chart -->
        <section class="chart-section">
          <h2 class="section-title">📊 Your Watchlist Overview</h2>
          <div class="chart-wrapper">
            <div v-if="totalMovies === 0" class="chart-empty">
              <p>📭 Add movies to see your watchlist overview</p>
            </div>
            <div v-else class="chart-display">
              <svg class="pie-chart-svg" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="80" :style="{ strokeDasharray: `${circumference * watchPercentage} ${circumference}`, strokeDashoffset: 0 }" class="pie-watched" />
                <circle cx="100" cy="100" r="80" :style="{ strokeDasharray: `${circumference * unwatchedPercentage} ${circumference}`, strokeDashoffset: -circumference * watchPercentage }" class="pie-unwatched" />
              </svg>
              <div class="chart-legend">
                <div class="legend-item">
                  <span class="legend-color watched"></span>
                  <span>Watched: {{ watchedCount }}</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color unwatched"></span>
                  <span>To Watch: {{ unwatchedCount }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- RIGHT COLUMN: Trending Movies -->
      <div class="right-column">
        <section class="trending-section">
          <h2 class="section-title">🔥 Trending This Week</h2>
          
          <div v-if="loadingTrending" class="loading-indicator">
            <p>Loading trending movies...</p>
          </div>
          
          <div v-else-if="trendingMovies.length === 0" class="empty-state">
            <p>Unable to load trending movies</p>
          </div>
          
          <div v-else class="trending-grid">
            <div 
              v-for="(movie, index) in trendingMovies" 
              :key="movie.tmdb_id"
              class="trending-card"
              @click="handleMovieClick(movie)"
            >
              <div class="card-number">{{ index + 1 }}</div>
              <img 
                v-if="movie.poster_url"
                :src="movie.poster_url" 
                :alt="movie.title"
                class="trending-poster"
              />
              <div v-else class="trending-poster-placeholder">
                <span class="placeholder-text">No Image</span>
              </div>
              <div class="trending-info">
                <h3>{{ movie.title }}</h3>
                <div class="trending-meta">
                  <span class="year">{{ movie.year || 'N/A' }}</span>
                  <span class="rating">⭐ {{ movie.rating ? movie.rating.toFixed(1) : 'N/A' }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { getTrendingMoviesTMDB } from '../services/tmdb.js'

export default {
  props: {
    movies: {
      type: Array,
      required: true
    }
  },
  emits: ['movie-clicked'],
  setup(props, { emit }) {
    const trendingMovies = ref([])
    const loadingTrending = ref(true)
    const circumference = 2 * Math.PI * 80 // radius = 80

    const totalMovies = computed(() => props.movies.length)
    
    const watchedCount = computed(() => 
      props.movies.filter(m => m.watched).length
    )
    
    const unwatchedCount = computed(() => 
      props.movies.filter(m => !m.watched).length
    )

    const watchPercentage = computed(() => {
      if (totalMovies.value === 0) return 0
      return watchedCount.value / totalMovies.value
    })

    const unwatchedPercentage = computed(() => {
      if (totalMovies.value === 0) return 0
      return unwatchedCount.value / totalMovies.value
    })

    const fetchTrendingMovies = async () => {
      try {
        loadingTrending.value = true
        const movies = await getTrendingMoviesTMDB()
        trendingMovies.value = movies
      } catch (error) {
        console.error('Error fetching trending movies:', error)
        trendingMovies.value = []
      } finally {
        loadingTrending.value = false
      }
    }

    const handleMovieClick = (movie) => {
      emit('movie-clicked', movie)
    }

    onMounted(() => {
      fetchTrendingMovies()
    })

    return {
      trendingMovies,
      loadingTrending,
      totalMovies,
      watchedCount,
      unwatchedCount,
      watchPercentage,
      unwatchedPercentage,
      circumference,
      handleMovieClick
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.home-container {
  width: 100%;
  min-height: 100vh;
  background: #0f0f0f;
  color: #fff;
}

/* ===== HERO SECTION ===== */
.hero-section {
  position: relative;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  margin-bottom: 40px;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.15), rgba(29, 185, 84, 0.1));
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  animation: slideDown 0.8s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-content h1 {
  font-size: 2.5em;
  font-weight: 900;
  margin-bottom: 10px;
  background: linear-gradient(135deg, #e50914, #1db954);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-content p {
  font-size: 1.2em;
  color: #ccc;
  font-weight: 300;
}

/* ===== LAYOUT ===== */
.home-layout {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 60px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.right-column {
  display: flex;
  flex-direction: column;
}

/* ===== QUICK STATS ===== */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.stat-card {
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.1), rgba(100, 100, 100, 0.1));
  border: 1px solid rgba(229, 9, 20, 0.3);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  transition: all 0.3s;
}

.stat-card:hover {
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.2), rgba(100, 100, 100, 0.2));
  transform: translateY(-5px);
  border-color: #e50914;
}

.stat-icon {
  font-size: 2em;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-number {
  font-size: 1.8em;
  font-weight: 700;
  color: #e50914;
}

.stat-label {
  color: #999;
  font-size: 0.9em;
}

/* ===== CHART SECTION ===== */
.chart-section {
  background: rgba(20, 20, 20, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(229, 9, 20, 0.3);
  border-radius: 10px;
  padding: 30px;
  flex: 1;
}

.section-title {
  font-size: 1.5em;
  font-weight: 700;
  margin-bottom: 25px;
  color: #fff;
}

.chart-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
}

.pie-chart-svg {
  width: 250px;
  height: 250px;
  max-width: 100%;
}

.pie-watched {
  fill: none;
  stroke: #e50914;
  stroke-width: 30;
  transform-origin: 100px 100px;
  transform: rotate(-90deg);
  transition: all 0.3s ease;
}

.pie-unwatched {
  fill: none;
  stroke: #1db954;
  stroke-width: 30;
  transform-origin: 100px 100px;
  transform: rotate(-90deg);
  transition: all 0.3s ease;
}

.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-left: 30px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1em;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
}

.legend-color.watched {
  background: #e50914;
}

.legend-color.unwatched {
  background: #1db954;
}

.chart-empty {
  text-align: center;
  color: #666;
  padding: 40px 20px;
  font-size: 1.1em;
}

.chart-loading {
  text-align: center;
  color: #999;
  padding: 40px 20px;
  font-size: 1em;
}

/* ===== TRENDING SECTION ===== */
.trending-section {
  background: rgba(20, 20, 20, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(229, 9, 20, 0.3);
  border-radius: 10px;
  padding: 30px;
  height: fit-content;
  max-height: 800px;
  overflow-y: auto;
}

.loading-indicator {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 1em;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
  font-size: 1em;
}

.trending-grid {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.trending-card {
  display: grid;
  grid-template-columns: 30px 70px 1fr;
  gap: 15px;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.trending-card:hover {
  background: rgba(229, 9, 20, 0.15);
  border-color: #e50914;
  transform: translateX(5px);
}

.card-number {
  font-size: 1.2em;
  font-weight: 700;
  color: #e50914;
  text-align: center;
}

.trending-poster {
  width: 70px;
  height: 100px;
  object-fit: cover;
  border-radius: 5px;
  border: 1px solid rgba(229, 9, 20, 0.3);
}

.trending-poster-placeholder {
  width: 70px;
  height: 100px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  border: 1px dashed rgba(229, 9, 20, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  color: #666;
  font-size: 0.75em;
  text-align: center;
  padding: 10px;
}

.trending-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.trending-info h3 {
  font-size: 0.95em;
  font-weight: 600;
  color: #fff;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.trending-meta {
  display: flex;
  gap: 10px;
  font-size: 0.85em;
  color: #999;
}

.year {
  color: #ccc;
}

.rating {
  color: #1db954;
  font-weight: 600;
}

/* ===== SCROLLBAR STYLING ===== */
.trending-section::-webkit-scrollbar {
  width: 8px;
}

.trending-section::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.trending-section::-webkit-scrollbar-thumb {
  background: rgba(229, 9, 20, 0.5);
  border-radius: 10px;
}

.trending-section::-webkit-scrollbar-thumb:hover {
  background: rgba(229, 9, 20, 0.7);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1200px) {
  .home-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .quick-stats {
    grid-template-columns: repeat(3, 1fr);
  }

  .chart-wrapper {
    flex-direction: column;
  }

  .chart-legend {
    margin-left: 0;
    margin-top: 20px;
  }
}

@media (max-width: 768px) {
  .home-layout {
    padding: 0 20px;
  }

  .quick-stats {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .stat-card {
    padding: 15px;
    flex-direction: row;
    text-align: left;
  }

  .stat-icon {
    font-size: 1.5em;
  }

  .stat-number {
    font-size: 1.5em;
  }

  .chart-section,
  .trending-section {
    padding: 20px;
  }

  .section-title {
    font-size: 1.2em;
  }

  .chart-wrapper {
    min-height: 250px;
  }

  .trending-card {
    grid-template-columns: 25px 50px 1fr;
    gap: 10px;
  }

  .trending-poster {
    width: 50px;
    height: 75px;
  }

  .trending-poster-placeholder {
    width: 50px;
    height: 75px;
  }

  .hero-content h1 {
    font-size: 1.8em;
  }

  .hero-content p {
    font-size: 1em;
  }
}

@media (max-width: 480px) {
  .hero-section {
    height: 150px;
    margin-bottom: 30px;
  }

  .hero-content h1 {
    font-size: 1.5em;
  }

  .hero-content p {
    font-size: 0.9em;
  }

  .quick-stats {
    gap: 8px;
  }

  .stat-card {
    padding: 12px;
    gap: 8px;
  }

  .stat-icon {
    font-size: 1.2em;
  }

  .stat-label {
    font-size: 0.8em;
  }

  .trending-card {
    grid-template-columns: 20px 45px 1fr;
    gap: 8px;
    padding: 10px;
  }

  .trending-poster {
    width: 45px;
    height: 67px;
  }

  .trending-poster-placeholder {
    width: 45px;
    height: 67px;
  }

  .card-number {
    font-size: 1em;
  }

  .trending-info h3 {
    font-size: 0.85em;
  }
}
</style>
