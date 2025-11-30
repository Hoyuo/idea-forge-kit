# Error Handling Patterns

> Universal error handling patterns.

---

## Error Structure

```
Error:
  code        : string (UPPER_SNAKE_CASE)
  message     : string (human readable)
  details     : object (optional, additional info)
  statusCode  : integer (HTTP status)
```

---

## Standard Error Types

| Error Type | Code | HTTP Status | Description |
|------------|------|-------------|-------------|
| ValidationError | VALIDATION_FAILED | 400 | Invalid input data |
| AuthenticationError | UNAUTHORIZED | 401 | Auth required/failed |
| AuthorizationError | FORBIDDEN | 403 | Permission denied |
| NotFoundError | NOT_FOUND | 404 | Resource not found |
| ConflictError | CONFLICT | 409 | Resource conflict |
| RateLimitError | RATE_LIMITED | 429 | Too many requests |
| InternalError | INTERNAL_ERROR | 500 | Server error |

---

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  }
}
```

---

## Error Hierarchy Pattern

```
BaseError
├── ClientError (4xx)
│   ├── ValidationError (400)
│   ├── AuthenticationError (401)
│   ├── AuthorizationError (403)
│   ├── NotFoundError (404)
│   ├── ConflictError (409)
│   └── RateLimitError (429)
└── ServerError (5xx)
    ├── InternalError (500)
    ├── NotImplementedError (501)
    └── ServiceUnavailableError (503)
```

---

## Validation Error Details

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Request validation failed",
    "details": {
      "errors": [
        {
          "field": "email",
          "code": "INVALID_FORMAT",
          "message": "Invalid email format"
        },
        {
          "field": "password",
          "code": "TOO_SHORT",
          "message": "Password must be at least 8 characters"
        }
      ]
    }
  }
}
```

---

## Error Handling Guidelines

### DO

- ✅ Use specific error types
- ✅ Include helpful error messages
- ✅ Log errors with context
- ✅ Return consistent error format
- ✅ Include request ID for tracing

### DON'T

- ❌ Expose stack traces in production
- ❌ Leak sensitive information
- ❌ Use generic error messages
- ❌ Catch and ignore errors
- ❌ Return different formats for different errors

---

## Error Logging Pattern

```
LogEntry:
  timestamp   : ISO 8601 datetime
  level       : ERROR | WARN | INFO
  request_id  : unique request identifier
  error_code  : error code from response
  message     : error message
  stack_trace : (only in non-production)
  context:
    user_id   : if authenticated
    endpoint  : request path
    method    : HTTP method
    payload   : sanitized request body
```

---

## Retry Patterns

### Retryable Errors

| Code | Retry | Wait Strategy |
|------|-------|---------------|
| 429 | Yes | Exponential backoff |
| 500 | Maybe | Limited retries (3) |
| 502 | Yes | Exponential backoff |
| 503 | Yes | Exponential backoff |
| 504 | Yes | Exponential backoff |

### Non-Retryable Errors

| Code | Action |
|------|--------|
| 400 | Fix request |
| 401 | Re-authenticate |
| 403 | Check permissions |
| 404 | Resource doesn't exist |
| 409 | Resolve conflict |

---

## Circuit Breaker Pattern

```
CircuitBreaker:
  states: CLOSED | OPEN | HALF_OPEN

  CLOSED:
    - Normal operation
    - Track failures
    - Open if threshold exceeded

  OPEN:
    - Fail fast (don't call service)
    - Wait for timeout
    - Move to HALF_OPEN

  HALF_OPEN:
    - Allow one request
    - Success → CLOSED
    - Failure → OPEN
```

**Thresholds:**
- Failure threshold: 5 failures in 60 seconds
- Recovery timeout: 30 seconds
- Half-open success threshold: 3 consecutive successes
