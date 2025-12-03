// OMDB API service for getting movie data and images
// Uses OMDB API with robust error handling

const OMDB_API_KEY = 'b6003b9d' // Working API key
const OMDB_BASE_URL = 'https://www.omdbapi.com'

export const searchMovieOMDB = async (title) => {
  try {
    const response = await fetch(
      `${OMDB_BASE_URL}/?apikey=${OMDB_API_KEY}&t=${encodeURIComponent(title)}&type=movie`
    )
    const data = await response.json()
    
    if (data.Response === 'True') {
      return {
        title: data.Title,
        year: parseInt(data.Year),
        poster_url: data.Poster !== 'N/A' ? data.Poster : null,
        plot: data.Plot,
        imdbID: data.imdbID,
        imdbRating: data.imdbRating
      }
    }
    return null
  } catch (error) {
    console.error('OMDB API error:', error)
    return null
  }
}

export const searchMoviesOMDB = async (query) => {
  if (!query || query.trim().length === 0) {
    return []
  }

  try {
    const response = await fetch(
      `${OMDB_BASE_URL}/?apikey=${OMDB_API_KEY}&s=${encodeURIComponent(query)}&type=movie`
    )
    const data = await response.json()
    
    if (data.Response === 'True' && data.Search) {
      return data.Search.map(movie => ({
        title: movie.Title,
        year: movie.Year,
        poster_url: movie.Poster !== 'N/A' ? movie.Poster : null,
        imdbID: movie.imdbID
      }))
    }
    return []
  } catch (error) {
    console.error('OMDB API error:', error)
    return []
  }
}
