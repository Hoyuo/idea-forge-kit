# Database Schema Patterns

> Language-agnostic database design patterns.

---

## Entity Definition Pattern

```
Entity: {EntityName}
─────────────────────────────────────
Fields:
  id          : primary_key, auto_generated
  created_at  : timestamp, auto_set_on_create
  updated_at  : timestamp, auto_update
  {field}     : {type}, {constraints}

Relationships:
  belongs_to  : {Parent} via {foreign_key}
  has_many    : {Children}
  has_one     : {Related}
  many_to_many: {Others} via {junction_table}

Indexes:
  unique      : [{fields}]
  composite   : [{fields}]

Constraints:
  not_null    : [{fields}]
  check       : {condition}
```

---

## Example Entity

```
Entity: User
─────────────────────────────────────
Fields:
  id          : uuid, primary_key
  email       : string(255), unique, not_null
  username    : string(50), unique
  password    : string(255), not_null
  status      : enum(active, inactive, suspended)
  created_at  : timestamp
  updated_at  : timestamp

Relationships:
  has_many    : Posts
  has_many    : Comments
  has_one     : Profile

Indexes:
  unique      : [email]
  unique      : [username]
```

---

## Migration Pattern

```
Migration: {timestamp}_{action}_{entity}
─────────────────────────────────────
Up:
  - CREATE TABLE {name}
  - ADD COLUMN {column}
  - ADD INDEX {index}

Down:
  - DROP TABLE {name}
  - DROP COLUMN {column}
  - DROP INDEX {index}
```

---

## Common Field Types

| Type | Description | Examples |
|------|-------------|----------|
| uuid | Unique identifier | id, external_id |
| string(n) | Variable length text | name, email |
| text | Long text | description, content |
| integer | Whole numbers | count, age |
| decimal(p,s) | Precise decimals | price, amount |
| boolean | True/false | is_active, verified |
| timestamp | Date and time | created_at |
| date | Date only | birth_date |
| enum | Fixed set of values | status, type |
| json/jsonb | Structured data | metadata, settings |

---

## Relationship Patterns

### One-to-Many

```
Entity: Post
─────────────────────────────────────
Fields:
  id          : uuid, primary_key
  user_id     : uuid, foreign_key(users.id)
  title       : string(255), not_null
  content     : text

Relationships:
  belongs_to  : User via user_id
```

### Many-to-Many

```
Entity: PostTag (junction table)
─────────────────────────────────────
Fields:
  post_id     : uuid, foreign_key(posts.id)
  tag_id      : uuid, foreign_key(tags.id)

Indexes:
  primary     : [post_id, tag_id]
  index       : [tag_id]
```

### Self-Referential

```
Entity: Comment
─────────────────────────────────────
Fields:
  id          : uuid, primary_key
  parent_id   : uuid, foreign_key(comments.id), nullable
  content     : text, not_null

Relationships:
  belongs_to  : Comment via parent_id (self)
  has_many    : Comment as replies
```

---

## Index Guidelines

| Type | When to Use |
|------|-------------|
| Primary Key | Always on id field |
| Unique | Email, username, natural keys |
| Foreign Key | All relationship fields |
| Composite | Multi-column queries |
| Partial | Conditional queries (WHERE status = 'active') |
| Full-text | Search fields |

---

## Soft Delete Pattern

```
Entity: {EntityName}
─────────────────────────────────────
Fields:
  ...
  deleted_at  : timestamp, nullable

Query Patterns:
  Active:     WHERE deleted_at IS NULL
  Deleted:    WHERE deleted_at IS NOT NULL
  All:        (no filter)
```

---

## Audit Log Pattern

```
Entity: AuditLog
─────────────────────────────────────
Fields:
  id          : uuid, primary_key
  entity_type : string(100), not_null
  entity_id   : uuid, not_null
  action      : enum(create, update, delete)
  changes     : jsonb
  actor_id    : uuid, foreign_key(users.id)
  created_at  : timestamp

Indexes:
  composite   : [entity_type, entity_id]
  index       : [actor_id]
  index       : [created_at]
```
