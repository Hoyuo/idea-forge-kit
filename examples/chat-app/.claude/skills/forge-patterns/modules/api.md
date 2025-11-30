# API Design Patterns

> OpenAPI 3.0 specification with RESTful 2.0 conventions.

---

## RESTful 2.0 Design Principles

### 1. Resource-Centric URLs (Use Nouns, Plural)

```
✅ Correct:
  GET    /users              # List users
  GET    /users/{id}         # Get single user
  POST   /users              # Create user
  PUT    /users/{id}         # Update user (full)
  PATCH  /users/{id}         # Update user (partial)
  DELETE /users/{id}         # Delete user

❌ Wrong:
  GET    /getUsers           # Verb in URL
  POST   /createUser         # Verb in URL
  GET    /user/{id}          # Singular form
  POST   /users/create       # Action in path
```

### 2. Nested Resources (Relationships)

```
# User's posts (belongs_to relationship)
GET    /users/{userId}/posts          # List user's posts
POST   /users/{userId}/posts          # Create post for user
GET    /users/{userId}/posts/{postId} # Get specific post

# Maximum 2 levels of nesting recommended
❌ /users/{id}/posts/{id}/comments/{id}/replies  # Too deep
✅ /comments/{id}/replies                         # Flatten instead
```

### 3. HTTP Methods and Semantics

| Method | Action | Idempotent | Safe | Request Body |
|--------|--------|------------|------|--------------|
| GET | Read | Yes | Yes | No |
| POST | Create | No | No | Yes |
| PUT | Replace | Yes | No | Yes |
| PATCH | Update | Yes | No | Yes |
| DELETE | Remove | Yes | No | No |

### 4. HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable | Semantic error |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Error | Server error |

### 5. Query Parameters (Filtering, Sorting, Pagination)

```
# Filtering
GET /users?status=active&role=admin

# Sorting (field:direction)
GET /users?sort=createdAt:desc
GET /users?sort=name:asc,createdAt:desc    # Multiple

# Pagination
GET /users?page=1&limit=20                 # Offset-based
GET /users?cursor=abc123&limit=20          # Cursor-based

# Field Selection (sparse fieldsets)
GET /users?fields=id,name,email

# Search
GET /users?q=john                          # Full-text search
GET /users?search[name]=john               # Field-specific
```

### 6. Versioning

```
# URL Path (Recommended)
/api/v1/users
/api/v2/users

# Header-based
Accept: application/vnd.api+json;version=1

# Query Parameter
/api/users?version=1
```

### 7. HATEOAS (Hypermedia Links)

```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "links": {
    "self": "/api/v1/users/123",
    "posts": "/api/v1/users/123/posts",
    "profile": "/api/v1/users/123/profile"
  }
}
```

### 8. Standard Response Envelope

```json
// Success (single resource)
{
  "data": { ... },
  "links": { "self": "..." }
}

// Success (collection)
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  },
  "links": {
    "self": "/users?page=1",
    "first": "/users?page=1",
    "prev": null,
    "next": "/users?page=2",
    "last": "/users?page=5"
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invalid input",
    "details": [ ... ]
  }
}
```

---

## OpenAPI 3.0 Specification

### Base Template

```yaml
openapi: 3.0.3
info:
  title: ${PROJECT_NAME} API
  description: Auto-generated from IdeaForge PRD
  version: 1.0.0

servers:
  - url: http://localhost:8000/api/v1
    description: Development
  - url: https://api.example.com/v1
    description: Production

tags:
  - name: auth
    description: Authentication endpoints
  - name: resources
    description: Resource operations

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Standard Schemas

```yaml
components:
  schemas:
    # Error Response
    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
          example: "NOT_FOUND"
        message:
          type: string
          example: "Resource not found"
        details:
          type: object

    # Pagination
    PaginationMeta:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    # Timestamps (reusable)
    Timestamps:
      type: object
      properties:
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time
```

### Authentication Endpoints

```yaml
paths:
  /auth/register:
    post:
      tags: [auth]
      summary: Register new user
      operationId: registerUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  format: password
                  minLength: 8
      responses:
        '201':
          description: User created
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          description: Email already exists

  /auth/login:
    post:
      tags: [auth]
      summary: User login
      operationId: loginUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  format: password
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  accessToken:
                    type: string
                  refreshToken:
                    type: string
                  expiresIn:
                    type: integer
        '401':
          description: Invalid credentials
```

### CRUD Resource Pattern

```yaml
paths:
  /resources:
    get:
      summary: List resources with pagination
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: search
          in: query
          schema:
            type: string
        - name: sort
          in: query
          schema:
            type: string
            enum: [createdAt, updatedAt, name]
        - name: order
          in: query
          schema:
            type: string
            enum: [asc, desc]
      responses:
        '200':
          description: List of resources

    post:
      summary: Create new resource
      security:
        - bearerAuth: []
      responses:
        '201':
          description: Resource created

  /resources/{id}:
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      summary: Get resource by ID
      responses:
        '200':
          description: Resource details
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: Update resource
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Resource updated

    delete:
      summary: Delete resource
      security:
        - bearerAuth: []
      responses:
        '204':
          description: Resource deleted
```

### WebSocket Events (AsyncAPI)

```yaml
asyncapi: 2.6.0
info:
  title: WebSocket Events
  version: 1.0.0

channels:
  /ws/{roomId}:
    parameters:
      roomId:
        schema:
          type: string
    subscribe:
      summary: Receive events
      message:
        payload:
          type: object
          properties:
            type:
              type: string
              enum: [message, typing, join, leave]
            data:
              type: object
    publish:
      summary: Send events
      message:
        payload:
          type: object
          required: [type]
          properties:
            type:
              type: string
            content:
              type: string
```
