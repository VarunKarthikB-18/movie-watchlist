<template>
  <div class="app-wrapper">
    <!-- Login/Register Page -->
    <div v-if="!isAuthenticated" class="auth-page">
      <div class="auth-overlay"></div>
      <div class="auth-content">
        <div class="logo-section">
          <h1 class="logo">🎬 CINEWATCH</h1>
          <p class="tagline">Your Personal Movie Kingdom</p>
        </div>

        <div class="auth-card">
          <div class="auth-tabs">
            <button 
              class="tab-btn"
              :class="{ active: authMode === 'login' }"
              @click="authMode = 'login'">
              Sign In
            </button>
            <button 
              class="tab-btn"
              :class="{ active: authMode === 'register' }"
              @click="authMode = 'register'">
              Create Account
            </button>
            <div class="tab-underline" :style="{ left: authMode === 'login' ? '0' : '50%' }"></div>
          </div>

          <div class="tab-content">
            <Login v-if="authMode === 'login'" @login="handleLogin" />
            <Register v-if="authMode === 'register'" @register="handleRegister" />
          </div>
        </div>
      </div>
    </div>

    <!-- Main App Page -->
    <div v-else class="app-page">
      <!-- Netflix-style Header with Navigation -->
      <header class="netflix-header">
        <div class="header-content">
          <h1 class="logo">🎬 CINEWATCH</h1>
          <nav class="nav-menu">
            <button 
              class="nav-btn"
              :class="{ active: currentPage === 'home' }"
              @click="currentPage = 'home'">
              🏠 Home
            </button>
            <button 
              class="nav-btn"
              :class="{ active: currentPage === 'watchlist' }"
              @click="currentPage = 'watchlist'">
              📽️ My Watchlist
            </button>
          </nav>
          <div class="header-controls">
            <button class="btn-filter" @click="showFilters = !showFilters" v-show="currentPage === 'watchlist'">⚙️ Filters</button>
            <button class="logout-btn" @click="handleLogout">Sign Out</button>
          </div>
        </div>
      </header>

      <!-- Filter Panel (only show in watchlist) -->
      <div v-if="showFilters && currentPage === 'watchlist'" class="filter-panel">
        <div class="filter-group">
          <label>Search</label>
          <input 
            v-model="filters.search"
            type="text"
            placeholder="Search movies..."
            class="filter-input">
        </div>
        <div class="filter-group">
          <label>Status</label>
          <select v-model="filters.status" class="filter-select">
            <option value="">All</option>
            <option value="watched">Watched</option>
            <option value="unwatched">Not Watched</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Rating</label>
          <select v-model.number="filters.minRating" class="filter-select">
            <option value="">All Ratings</option>
            <option value="7">7+</option>
            <option value="8">8+</option>
            <option value="9">9+</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Sort By</label>
          <select v-model="filters.sortBy" class="filter-select">
            <option value="recent">Recently Added</option>
            <option value="rating">Rating (High to Low)</option>
            <option value="title">Title (A-Z)</option>
            <option value="year">Year (Newest)</option>
          </select>
        </div>
      </div>

      <!-- HOME PAGE -->
      <div v-if="currentPage === 'home'" class="page-content">
        <Home 
          :movies="movies"
          @movie-clicked="openMovieDetail" />
      </div>

      <!-- WATCHLIST PAGE -->
      <div v-if="currentPage === 'watchlist'" class="page-content">
        <main class="main-content">
          <!-- Search Results Section (only when searching) -->
          <section v-if="filters.search && filters.search.trim().length > 0" class="search-results-section">
            <h2 class="section-title">🔍 Search Results</h2>
            <div v-if="searching" class="searching-indicator">Searching...</div>
            <div v-else-if="searchResults.length === 0" class="empty-state">
              <p>No movies found for "{{ filters.search }}"</p>
            </div>
            <div v-else>
              <MovieList 
                :movies="searchResults" 
                @movie-clicked="openMovieDetail" />
            </div>
          </section>

          <!-- Hero Section with Quick Add -->
          <section class="hero-section">
            <div class="hero-overlay"></div>
            <div class="hero-content">
              <h2>Add Your Next Movie</h2>
              <AddMovie @movie-added="fetchMovies" />
            </div>
          </section>

          <!-- Stats Section -->
          <section class="stats-section">
            <div class="stat-card">
              <span class="stat-icon">🎬</span>
              <div class="stat-info">
                <span class="stat-number">{{ movies.length }}</span>
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
              <span class="stat-icon">⭐</span>
              <div class="stat-info">
                <span class="stat-number">{{ avgRating }}</span>
                <span class="stat-label">Avg Rating</span>
              </div>
            </div>
          </section>

          <!-- Movies Section (only show when not searching) -->
          <section v-if="!filters.search || filters.search.trim().length === 0" class="movies-section">
            <div v-if="filteredMovies.length === 0" class="empty-state">
              <p v-if="movies.length === 0">📭 No movies yet. Add one to get started!</p>
              <p v-else>🔍 No movies match your filters</p>
            </div>
            
            <div v-else>
              <div v-if="isShowingDemoMovies" class="demo-notice">
                <p>🎬 These are popular movies from TMDB. Click "Add to Watchlist" on any movie to add it to your personal watchlist!</p>
              </div>
              <MovieList 
                :movies="filteredMovies" 
                @movie-updated="fetchMovies" 
                @movie-deleted="fetchMovies"
                @movie-clicked="openMovieDetail" />
            </div>
          </section>
        </main>
      </div>
    </div>

    <!-- Notifications -->
    <div v-if="successMsg" class="notification success">
      <span>✓ {{ successMsg }}</span>
      <button @click="successMsg = ''" class="close-btn">×</button>
    </div>
    <div v-if="errorMsg" class="notification error">
      <span>✗ {{ errorMsg }}</span>
      <button @click="errorMsg = ''" class="close-btn">×</button>
    </div>

    <!-- Movie Detail Modal -->
    <MovieDetailModal 
      :isOpen="showMovieModal"
      :movie="selectedMovie"
      @close="closeMovieDetail"
      @updated="fetchMovies"
      @deleted="fetchMovies"
      @added="fetchMovies" />
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import MovieList from './components/MovieList.vue'
import AddMovie from './components/AddMovie.vue'
import MovieDetailModal from './components/MovieDetailModal.vue'
import Home from './components/Home.vue'
import { getToken, logout } from './services/auth.js'
import api from './services/api.js'
import { getPopularMoviesTMDB, searchMoviesTMDB } from './services/tmdb.js'

export default {
  components: {
    Login,
    Register,
    MovieList,
    AddMovie,
    MovieDetailModal,
    Home
  },
  setup() {
    const isAuthenticated = ref(!!getToken())
    const authMode = ref('login')
    const movies = ref([])
    const successMsg = ref('')
    const errorMsg = ref('')
    const showFilters = ref(false)
    const selectedMovie = ref(null)
    const showMovieModal = ref(false)
    const searchResults = ref([])
    const searching = ref(false)
    const currentPage = ref('home') // home, watchlist
    
    const filters = ref({
      search: '',
      status: '',
      minRating: '',
      sortBy: 'recent'
    })

    const watchedCount = computed(() => 
      movies.value.filter(m => m.watched).length
    )

    const avgRating = computed(() => {
      const ratedMovies = movies.value.filter(m => m.rating)
      if (ratedMovies.length === 0) return '—'
      const avg = (ratedMovies.reduce((sum, m) => sum + parseFloat(m.rating || 0), 0) / ratedMovies.length)
      // Format to 2 decimal places, removing trailing zeros
      return parseFloat(avg.toFixed(2))
    })

    const filteredMovies = computed(() => {
      let result = [...movies.value]

      // Search filter
      if (filters.value.search) {
        result = result.filter(m => 
          m.title.toLowerCase().includes(filters.value.search.toLowerCase())
        )
      }

      // Status filter
      if (filters.value.status === 'watched') {
        result = result.filter(m => m.watched)
      } else if (filters.value.status === 'unwatched') {
        result = result.filter(m => !m.watched)
      }

      // Rating filter
      if (filters.value.minRating) {
        result = result.filter(m => m.rating && m.rating >= filters.value.minRating)
      }

      // Sorting
      if (filters.value.sortBy === 'rating') {
        result.sort((a, b) => (b.rating || 0) - (a.rating || 0))
      } else if (filters.value.sortBy === 'title') {
        result.sort((a, b) => a.title.localeCompare(b.title))
      } else if (filters.value.sortBy === 'year') {
        result.sort((a, b) => (b.year || 0) - (a.year || 0))
      } else {
        result.reverse()
      }

      return result
    })

    const handleLogin = async () => {
      isAuthenticated.value = true
      successMsg.value = 'Welcome back! 🎬'
      setTimeout(() => { successMsg.value = '' }, 3000)
      await fetchMovies()
    }

    const handleRegister = async () => {
      authMode.value = 'login'
      successMsg.value = 'Account created! Please sign in.'
      setTimeout(() => { successMsg.value = '' }, 3000)
    }

    const handleLogout = () => {
      logout()
      isAuthenticated.value = false
      movies.value = []
      currentPage.value = 'home'
      successMsg.value = 'Signed out successfully'
      setTimeout(() => { successMsg.value = '' }, 2000)
    }

    const isShowingDemoMovies = computed(() => {
      // Check if movies are from TMDB (have tmdb_id but no id)
      return movies.value.length > 0 && movies.value.some(m => m.tmdb_id && !m.id)
    })

    const fetchMovies = async () => {
      try {
        const response = await api.get('/movies')
        movies.value = response.data || []
        errorMsg.value = ''
      } catch (error) {
        console.error(error);
        errorMsg.value = 'Unable to load your watchlist.'
        movies.value = []
      }
    }

    const openMovieDetail = (movie) => {
      selectedMovie.value = movie
      showMovieModal.value = true
    }

    const closeMovieDetail = () => {
      showMovieModal.value = false
      selectedMovie.value = null
    }

    // Watch for search input changes and fetch TMDB results
    let searchTimeout = null
    watch(() => filters.value.search, (newSearch) => {
      // Clear previous timeout
      if (searchTimeout) {
        clearTimeout(searchTimeout)
      }
      
      // Debounce search by 300ms
      searchTimeout = setTimeout(async () => {
        if (newSearch && newSearch.trim().length > 0) {
          searching.value = true
          try {
            const results = await searchMoviesTMDB(newSearch.trim())
            searchResults.value = results
          } catch (err) {
            console.error('Search error:', err)
            searchResults.value = []
          } finally {
            searching.value = false
          }
        } else {
          searchResults.value = []
        }
      }, 300)
    })

    onMounted(() => {
      if (isAuthenticated.value) {
        fetchMovies()
      }
    })

    return {
      isAuthenticated,
      authMode,
      movies,
      successMsg,
      errorMsg,
      showFilters,
      filters,
      filteredMovies,
      watchedCount,
      avgRating,
      isShowingDemoMovies,
      selectedMovie,
      showMovieModal,
      searchResults,
      searching,
      currentPage,
      openMovieDetail,
      closeMovieDetail,
      handleLogin,
      handleRegister,
      handleLogout,
      fetchMovies
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

.app-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #0f0f0f;
  color: #fff;
  overflow-y: auto;
  overflow-x: hidden;
}

/* ===== AUTH PAGE ===== */
.auth-page {
  width: 100%;
  height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.auth-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  z-index: 1;
}

.auth-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 450px;
  width: 100%;
  padding: 20px;
}

.logo-section {
  margin-bottom: 40px;
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

.logo {
  font-size: 3em;
  font-weight: 900;
  letter-spacing: 2px;
  color: #e50914;
  text-shadow: 0 4px 20px rgba(229, 9, 20, 0.5);
  margin-bottom: 10px;
}

.tagline {
  color: #ccc;
  font-size: 1.1em;
  font-weight: 300;
}

.auth-card {
  background: rgba(20, 20, 20, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 40px 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.auth-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 30px;
  position: relative;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  color: #999;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.3s;
}

.tab-btn.active {
  color: #e50914;
}

.tab-underline {
  position: absolute;
  bottom: -1px;
  width: 50%;
  height: 2px;
  background: #e50914;
  transition: left 0.3s ease;
}

.tab-content {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* ===== APP PAGE ===== */
.app-page {
  width: 100%;
  display: flex;
  flex-direction: column;
  min-height: auto;
}

.netflix-header {
  background: linear-gradient(180deg, rgba(15, 15, 15, 0.9) 0%, rgba(15, 15, 15, 0) 100%);
  padding: 20px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

.header-content .logo {
  font-size: 1.8em;
  font-weight: 900;
  color: #e50914;
  letter-spacing: 1px;
  margin-right: 40px;
}

.nav-menu {
  display: flex;
  gap: 0;
  flex: 1;
}

.nav-btn {
  padding: 12px 20px;
  background: none;
  border: none;
  color: #999;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 2px solid transparent;
}

.nav-btn:hover {
  color: #e50914;
}

.nav-btn.active {
  color: #e50914;
  border-bottom-color: #e50914;
}

.header-controls {
  display: flex;
  gap: 15px;
  margin-left: auto;
}

.btn-filter,
.logout-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.95em;
}

.btn-filter {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.btn-filter:hover {
  background: rgba(255, 255, 255, 0.2);
}

.logout-btn {
  background: #e50914;
  color: #fff;
}

.logout-btn:hover {
  background: #c40812;
  transform: scale(1.05);
}

/* Filter Panel */
.filter-panel {
  background: rgba(30, 30, 30, 0.95);
  padding: 20px 40px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  animation: slideDown 0.3s ease;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group label {
  color: #999;
  font-size: 0.9em;
  font-weight: 600;
}

.filter-input,
.filter-select {
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 5px;
  color: #fff;
  font-size: 0.95em;
  transition: all 0.3s;
}

.filter-input:focus,
.filter-select:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
  border-color: #e50914;
}

/* Main Content */
.main-content {
  flex: 1;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 40px;
}

.page-content {
  width: 100%;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Hero Section */
.hero-section {
  margin: 40px 0;
  position: relative;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.1), rgba(100, 100, 100, 0.1));
  border-radius: 10px;
  z-index: 0;
}

.hero-content {
  position: relative;
  z-index: 1;
  background: rgba(20, 20, 20, 0.6);
  backdrop-filter: blur(10px);
  padding: 40px;
  border-radius: 10px;
  border: 1px solid rgba(229, 9, 20, 0.3);
}

.hero-content h2 {
  font-size: 2em;
  margin-bottom: 30px;
  color: #e50914;
}

/* Stats Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 40px 0;
}

.stat-card {
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.1), rgba(100, 100, 100, 0.1));
  border: 1px solid rgba(229, 9, 20, 0.3);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s;
}

.stat-card:hover {
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.2), rgba(100, 100, 100, 0.2));
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 2.5em;
}

.stat-info {
  display: flex;
  flex-direction: column;
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

/* Search Results Section */
.search-results-section {
  margin: 40px 0 30px 0;
}

.section-title {
  font-size: 1.8em;
  color: #fff;
  margin-bottom: 20px;
  font-weight: 700;
}

.searching-indicator {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 1.1em;
}

/* Movies Section */
.movies-section {
  margin: 40px 0 60px 0;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  font-size: 1.2em;
}

.demo-notice {
  background: linear-gradient(135deg, rgba(229, 9, 20, 0.2), rgba(100, 100, 100, 0.2));
  border: 1px solid rgba(229, 9, 20, 0.5);
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  text-align: center;
}

.demo-notice p {
  color: #fff;
  margin: 0;
  font-size: 0.95em;
  font-weight: 500;
}

/* Notifications */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 25px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 15px;
  z-index: 1000;
  animation: slideInRight 0.3s ease;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.notification.success {
  background: #1db954;
  color: white;
}

.notification.error {
  background: #e50914;
  color: white;
}

.close-btn {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2em;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s;
}

.close-btn:hover {
  opacity: 1;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    padding: 0 20px;
    flex-wrap: wrap;
  }

  .header-content .logo {
    margin-right: 20px;
    font-size: 1.4em;
  }

  .nav-menu {
    order: 3;
    width: 100%;
    margin-top: 10px;
  }

  .nav-btn {
    flex: 1;
    text-align: center;
  }

  .header-controls {
    margin-left: 0;
  }

  .main-content {
    padding: 0 20px;
  }

  .hero-content {
    padding: 25px;
  }

  .hero-content h2 {
    font-size: 1.5em;
  }

  .logo {
    font-size: 2em;
  }

  .filter-panel {
    padding: 15px 20px;
    grid-template-columns: 1fr;
  }
}
</style>
