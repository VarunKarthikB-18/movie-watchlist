// TMDB API utility for popular/search movies
const TMDB_API_KEY = '885ef92a497cb93aeec3b89cdda09697'; // Actual TMDB API key from user
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500';

export const getPopularMoviesTMDB = async () => {
  try {
    const response = await fetch(
      `${TMDB_BASE_URL}/movie/popular?api_key=${TMDB_API_KEY}&language=en-US&page=1`
    );
    const data = await response.json();
    if (data.results && Array.isArray(data.results)) {
      return data.results.map(movie => ({
        title: movie.title,
        year: movie.release_date ? parseInt(movie.release_date.slice(0, 4)) : null,
        poster_url: movie.poster_path ? `${TMDB_IMAGE_BASE}${movie.poster_path}` : null,
        plot: movie.overview,
        tmdb_id: movie.id,
        rating: movie.vote_average
      }));
    }
    return [];
  } catch (error) {
    console.error('TMDB popular movies error:', error);
    return [];
  }
};

export const searchMoviesTMDB = async (query) => {
  if (!query || query.trim().length === 0) return [];
  try {
    // Fetch first page
    const response = await fetch(
      `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&language=en-US&query=${encodeURIComponent(query)}&page=1&include_adult=false`
    );
    const data = await response.json();
    
    // Check for API errors
    if (data.status_code) {
      console.error('TMDB API error:', data.status_message);
      return [];
    }
    
    if (!data.results || !Array.isArray(data.results)) {
      return [];
    }

    let allResults = [...data.results];
    
    // If there are more pages and we have less than 40 results, fetch page 2
    if (data.total_pages > 1 && allResults.length < 40) {
      try {
        const response2 = await fetch(
          `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&language=en-US&query=${encodeURIComponent(query)}&page=2&include_adult=false`
        );
        const data2 = await response2.json();
        if (data2.results && Array.isArray(data2.results)) {
          allResults = [...allResults, ...data2.results];
        }
      } catch (err) {
        console.warn('Failed to fetch page 2:', err);
      }
    }
    
    // Map and return results (up to 40)
    return allResults.slice(0, 40).map(movie => ({
      title: movie.title,
      year: movie.release_date ? parseInt(movie.release_date.slice(0, 4)) : null,
      poster_url: movie.poster_path ? `${TMDB_IMAGE_BASE}${movie.poster_path}` : null,
      plot: movie.overview,
      tmdb_id: movie.id,
      rating: movie.vote_average
    }));
  } catch (error) {
    console.error('TMDB search error:', error);
    return [];
  }
};

export const getTrendingMoviesTMDB = async () => {
  try {
    const response = await fetch(
      `${TMDB_BASE_URL}/trending/movie/week?api_key=${TMDB_API_KEY}&language=en-US`
    );
    const data = await response.json();
    if (data.results && Array.isArray(data.results)) {
      return data.results.slice(0, 10).map(movie => ({
        title: movie.title,
        year: movie.release_date ? parseInt(movie.release_date.slice(0, 4)) : null,
        poster_url: movie.poster_path ? `${TMDB_IMAGE_BASE}${movie.poster_path}` : null,
        plot: movie.overview,
        tmdb_id: movie.id,
        rating: movie.vote_average
      }));
    }
    return [];
  } catch (error) {
    console.error('TMDB trending movies error:', error);
    return [];
  }
};
