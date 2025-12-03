# Movie Watchlist API Testing Guide

Complete curl examples for testing all API endpoints.

## Prerequisites

Make sure both servers are running:
- Backend: `http://127.0.0.1:5000`
- Frontend: `http://localhost:5173`

## 1. Health Check

```bash
# Test if backend is running
curl http://127.0.0.1:5000/

# Expected Response:
# {"message": "Movie Watchlist backend is running!"}
```

---

## 2. Authentication Endpoints

### Register a New User

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepassword123"
  }'

# Expected Response (201):
# {"msg": "user created", "user_id": 2}
```

**Error Cases:**

```bash
# Missing email or password
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
# Response (400): {"msg": "email and password required"}

# Email already registered
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "test"}'
# Response (400): {"msg": "email already registered"}
```

### Login to Get JWT Token

```bash
# Login with demo user
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "password": "demo123"
  }'

# Expected Response (200):
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "user_id": 1
# }
```

**Save token for next requests:**

```bash
# Using bash
TOKEN="your_token_from_login_response"

# Or dynamically extract it:
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"demo123"}' \
  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

echo $TOKEN
```

**Error Cases:**

```bash
# Missing credentials
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com"}'
# Response (400): {"msg": "email and password required"}

# Wrong password
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "wrongpassword"}'
# Response (401): {"msg": "bad credentials"}

# Non-existent user
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "nonexistent@example.com", "password": "test"}'
# Response (401): {"msg": "bad credentials"}
```

---

## 3. Movie Endpoints (All Protected - Require JWT)

### List All Movies

```bash
# Get all movies for authenticated user
curl -X GET http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer $TOKEN"

# Expected Response (200):
# [
#   {
#     "id": 1,
#     "title": "Inception",
#     "year": 2010,
#     "watched": true,
#     "rating": 9,
#     "notes": "Mind-bending sci-fi masterpiece",
#     "poster_url": null,
#     "user_id": 1
#   },
#   {
#     "id": 2,
#     "title": "The Matrix",
#     "year": 1999,
#     "watched": false,
#     "rating": null,
#     "notes": null,
#     "poster_url": null,
#     "user_id": 1
#   }
# ]
```

### Create a New Movie

```bash
# Basic movie with only title (required field)
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "The Dark Knight"
  }'

# Expected Response (201):
# {
#   "id": 3,
#   "title": "The Dark Knight",
#   "year": null,
#   "watched": false,
#   "rating": null,
#   "notes": null,
#   "poster_url": null,
#   "user_id": 1
# }
```

**With all optional fields:**

```bash
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Interstellar",
    "year": 2014,
    "watched": true,
    "rating": 10,
    "notes": "Epic space exploration - must watch!",
    "poster_url": "https://example.com/interstellar.jpg"
  }'

# Expected Response (201): Complete movie object
```

**Error Cases:**

```bash
# Missing title (required)
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"year": 2020}'
# Response (400): {"msg": "title required"}

# Without authorization header
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Movie"}'
# Response (401): {"msg": "Missing Authorization Header"}
```

### Update a Movie

```bash
# Update single field
curl -X PUT http://127.0.0.1:5000/movies/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "watched": true
  }'

# Expected Response (200): Updated movie object
# {
#   "id": 1,
#   "title": "Inception",
#   "year": 2010,
#   "watched": true,
#   "rating": 9,
#   "notes": "Mind-bending sci-fi masterpiece",
#   "poster_url": null,
#   "user_id": 1
# }
```

**Update multiple fields:**

```bash
curl -X PUT http://127.0.0.1:5000/movies/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "watched": true,
    "rating": 10,
    "notes": "Best movie ever!"
  }'
```

**Error Cases:**

```bash
# Movie not found (or belongs to different user)
curl -X PUT http://127.0.0.1:5000/movies/9999 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"watched": true}'
# Response (404): {"msg": "movie not found"}

# Invalid movie ID
curl -X PUT http://127.0.0.1:5000/movies/invalid \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"watched": true}'
# Response (404): Not Found
```

### Delete a Movie

```bash
curl -X DELETE http://127.0.0.1:5000/movies/1 \
  -H "Authorization: Bearer $TOKEN"

# Expected Response (200):
# {"msg": "deleted"}
```

**Verify deletion:**

```bash
# List movies - movie 1 should be gone
curl -X GET http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer $TOKEN"
```

**Error Cases:**

```bash
# Movie not found (or belongs to different user)
curl -X DELETE http://127.0.0.1:5000/movies/9999 \
  -H "Authorization: Bearer $TOKEN"
# Response (404): {"msg": "movie not found"}
```

---

## Complete Workflow Example

Here's a complete workflow from registration to movie management:

```bash
#!/bin/bash

echo "🎬 Movie Watchlist API Testing"
echo "================================"

# 1. Register a new user
echo ""
echo "1️⃣  Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"testpass123"
  }')
echo $REGISTER_RESPONSE | jq .
USER_ID=$(echo $REGISTER_RESPONSE | jq .user_id)

# 2. Login to get JWT token
echo ""
echo "2️⃣  Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"testuser@example.com",
    "password":"testpass123"
  }')
echo $LOGIN_RESPONSE | jq .
TOKEN=$(echo $LOGIN_RESPONSE | jq -r .access_token)

# 3. Create a movie
echo ""
echo "3️⃣  Creating a movie..."
CREATE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title":"Interstellar",
    "year":2014,
    "watched":true,
    "rating":10
  }')
echo $CREATE_RESPONSE | jq .
MOVIE_ID=$(echo $CREATE_RESPONSE | jq .id)

# 4. List all movies
echo ""
echo "4️⃣  Listing all movies..."
curl -s -X GET http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer $TOKEN" | jq .

# 5. Update a movie
echo ""
echo "5️⃣  Updating movie (toggle watched)..."
curl -s -X PUT http://127.0.0.1:5000/movies/$MOVIE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "watched": false,
    "rating": 9
  }' | jq .

# 6. Delete a movie
echo ""
echo "6️⃣  Deleting movie..."
curl -s -X DELETE http://127.0.0.1:5000/movies/$MOVIE_ID \
  -H "Authorization: Bearer $TOKEN" | jq .

echo ""
echo "✅ Workflow complete!"
```

Save as `test_workflow.sh`, then run:

```bash
chmod +x test_workflow.sh
./test_workflow.sh
```

---

## Using jq for Pretty Output

If you don't have `jq` installed, install it:

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Or use Python alternative:
curl ... | python -m json.tool
```

---

## API Response Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successfully updated movie |
| 201 | Created | New user/movie created |
| 400 | Bad Request | Missing required fields |
| 401 | Unauthorized | Invalid/missing token or credentials |
| 404 | Not Found | Movie doesn't exist |
| 422 | Unprocessable Entity | Invalid data format |
| 500 | Server Error | Unexpected error |

---

## Useful curl Options

```bash
# Pretty print JSON
curl ... | jq .

# Save response to file
curl ... -o response.json

# Verbose (show headers)
curl ... -v

# Show only response headers
curl ... -i

# Silent mode (no progress bar)
curl ... -s

# Follow redirects
curl ... -L

# Custom timeout (seconds)
curl ... --max-time 10
```

---

## Debugging Tips

1. **Check token format**: Should be `Authorization: Bearer <token>`
2. **Check token expiration**: Tokens expire after 24 hours
3. **Check CORS**: Ensure backend CORS is enabled
4. **Check database**: Verify data persisted with `flask db`
5. **Check logs**: Watch terminal output for backend errors
6. **Use -v flag**: See full request/response for debugging

---

## Example: Testing with Postman

Instead of curl, you can use Postman:

1. Create new POST request to `http://127.0.0.1:5000/auth/login`
2. Body → raw → JSON → paste credentials
3. Send → copy `access_token` from response
4. New request to `http://127.0.0.1:5000/movies`
5. Headers → Add `Authorization: Bearer <token>`
6. Send

---

Happy Testing! 🎬
