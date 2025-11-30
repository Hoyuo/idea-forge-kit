# /forge:design - Architecture Design & Diagrams

## Usage

```
/forge:design AUTH-001
/forge:design AUTH-001 --type class
/forge:design AUTH-001 --type sequence --flow login
```

## Input

`$ARGUMENTS` - PRD ID (optionally specify diagram type and scope)

## Language Configuration

Read from `.forge/config.json`:
- Use `language.conversation` for design explanations
- Use `language.output_documents` for diagram documentation

## Workflow

### 1. Design Preparation

```
IdeaForge Design: {PRD_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

1. Load PRD: `.forge/prds/{PRD_ID}.md`
2. Load tasks: `.forge/tasks/{PRD_ID}/tasks.json`
3. Analyze requirements for design elements

### 2. Diagram Types

#### System Architecture Diagram
High-level system overview showing all components and their relationships.

```plantuml
@startuml system-architecture
!theme plain
skinparam componentStyle rectangle

title System Architecture: {PRD_ID}

package "Client Layer" {
  [Web App]
  [Mobile App]
}

package "API Gateway" {
  [Load Balancer]
  [Rate Limiter]
}

package "Service Layer" {
  [Auth Service]
  [Core Service]
  [Notification Service]
}

package "Data Layer" {
  database "Primary DB"
  database "Cache"
  database "Message Queue"
}

[Web App] --> [Load Balancer]
[Mobile App] --> [Load Balancer]
[Load Balancer] --> [Auth Service]
[Load Balancer] --> [Core Service]
[Auth Service] --> [Primary DB]
[Core Service] --> [Cache]
[Core Service] --> [Message Queue]

@enduml
```

#### Class Diagram
Entity and model structure with relationships.

```plantuml
@startuml class-diagram
!theme plain
skinparam classAttributeIconSize 0

title Domain Model: {PRD_ID}

class User {
  +id: UUID
  +email: String
  +username: String
  +passwordHash: String
  +status: UserStatus
  +createdAt: DateTime
  +updatedAt: DateTime
  --
  +validatePassword(password): Boolean
  +generateToken(): String
}

enum UserStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
}

class Session {
  +id: UUID
  +userId: UUID
  +token: String
  +expiresAt: DateTime
  +createdAt: DateTime
  --
  +isValid(): Boolean
  +refresh(): Session
}

class AuditLog {
  +id: UUID
  +userId: UUID
  +action: String
  +details: JSON
  +createdAt: DateTime
}

User "1" -- "*" Session : has
User "1" -- "*" AuditLog : generates
User -- UserStatus

@enduml
```

#### Sequence Diagram
API flow and service communication.

```plantuml
@startuml sequence-login
!theme plain

title Login Flow: {PRD_ID}

actor User as user
participant "Client" as client
participant "API Gateway" as gateway
participant "Auth Service" as auth
database "Database" as db
participant "Token Service" as token

user -> client: Enter credentials
client -> gateway: POST /auth/login
gateway -> auth: Validate request

auth -> db: Find user by email
db --> auth: User data

alt User found
  auth -> auth: Verify password hash

  alt Password valid
    auth -> token: Generate JWT
    token --> auth: Access + Refresh tokens
    auth -> db: Create session
    auth --> gateway: 200 OK + tokens
    gateway --> client: Login success
    client --> user: Redirect to dashboard
  else Password invalid
    auth --> gateway: 401 Unauthorized
    gateway --> client: Invalid credentials
    client --> user: Show error
  end
else User not found
  auth --> gateway: 401 Unauthorized
  gateway --> client: Invalid credentials
  client --> user: Show error
end

@enduml
```

#### Package/Component Diagram
Module structure and dependencies.

```plantuml
@startuml package-diagram
!theme plain

title Package Structure: {PRD_ID}

package "API Layer" as api {
  [Controllers]
  [Middleware]
  [Routes]
}

package "Service Layer" as service {
  [AuthService]
  [UserService]
  [NotificationService]
}

package "Domain Layer" as domain {
  [Entities]
  [ValueObjects]
  [DomainEvents]
}

package "Infrastructure Layer" as infra {
  [Repositories]
  [ExternalAPIs]
  [Messaging]
}

package "Shared" as shared {
  [Utils]
  [Constants]
  [Types]
}

api ..> service : uses
service ..> domain : uses
service ..> infra : uses
infra ..> domain : implements
api ..> shared : uses
service ..> shared : uses

@enduml
```

#### ER Diagram (Entity Relationship)
Database schema visualization.

```plantuml
@startuml er-diagram
!theme plain
skinparam linetype ortho

title Database Schema: {PRD_ID}

entity "users" as users {
  *id : uuid <<PK>>
  --
  *email : varchar(255) <<unique>>
  username : varchar(50)
  *password_hash : varchar(255)
  status : enum
  *created_at : timestamp
  updated_at : timestamp
}

entity "sessions" as sessions {
  *id : uuid <<PK>>
  --
  *user_id : uuid <<FK>>
  *token : varchar(500)
  *expires_at : timestamp
  *created_at : timestamp
}

entity "audit_logs" as audit {
  *id : uuid <<PK>>
  --
  user_id : uuid <<FK>>
  *action : varchar(100)
  details : jsonb
  *created_at : timestamp
}

users ||--o{ sessions : "has"
users ||--o{ audit : "generates"

@enduml
```

#### State Diagram
State transitions for entities.

```plantuml
@startuml state-diagram
!theme plain

title User State: {PRD_ID}

[*] --> Pending : Register

Pending --> Active : Verify email
Pending --> [*] : Timeout (24h)

Active --> Suspended : Admin action
Active --> Inactive : User request
Active --> Active : Login/Logout

Suspended --> Active : Admin restore
Suspended --> [*] : Delete

Inactive --> Active : Reactivate
Inactive --> [*] : Delete (30 days)

@enduml
```

#### Activity Diagram
Workflow and business process.

```plantuml
@startuml activity-diagram
!theme plain

title Registration Flow: {PRD_ID}

start

:User enters registration form;

:Validate input data;

if (Valid input?) then (yes)
  :Check email availability;

  if (Email available?) then (yes)
    :Hash password;
    :Create user record;
    :Generate verification token;
    :Send verification email;
    :Show success message;
  else (no)
    :Show "email exists" error;
  endif
else (no)
  :Show validation errors;
endif

stop

@enduml
```

### 3. Design Output Structure

`.forge/design/{PRD_ID}/`:
```
design/
├── diagrams/
│   ├── system-architecture.puml
│   ├── class-diagram.puml
│   ├── sequence-login.puml
│   ├── sequence-register.puml
│   ├── package-diagram.puml
│   ├── er-diagram.puml
│   ├── state-user.puml
│   └── activity-register.puml
├── images/                      # Generated PNG/SVG (optional)
│   ├── system-architecture.png
│   └── ...
└── DESIGN.md                    # Design documentation
```

### 4. Design Documentation

`.forge/design/{PRD_ID}/DESIGN.md`:

```markdown
# {PRD_ID} Design Document

## Overview
{Brief description of the design}

## System Architecture
![System Architecture](diagrams/system-architecture.puml)

{Architecture explanation}

## Domain Model
![Class Diagram](diagrams/class-diagram.puml)

### Entities
- **User**: Core user entity with authentication
- **Session**: User session management
- **AuditLog**: Activity tracking

## API Flows

### Login Flow
![Login Sequence](diagrams/sequence-login.puml)

{Flow explanation}

### Registration Flow
![Registration Activity](diagrams/activity-register.puml)

{Flow explanation}

## Database Schema
![ER Diagram](diagrams/er-diagram.puml)

{Schema explanation}

## Module Structure
![Package Diagram](diagrams/package-diagram.puml)

{Module explanation}
```

### 5. Completion Message

```
Design Complete: {PRD_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated Diagrams:
   ├── System Architecture ✓
   ├── Class Diagram ✓
   ├── Sequence Diagrams (3) ✓
   ├── Package Diagram ✓
   ├── ER Diagram ✓
   ├── State Diagrams (2) ✓
   └── Activity Diagrams (2) ✓

Output:
   .forge/design/{PRD_ID}/

View Options:
   • PlantUML Server: https://www.plantuml.com/plantuml
   • VS Code Extension: PlantUML
   • IntelliJ Plugin: PlantUML Integration

Next Steps:
   /forge:build {PRD_ID}  - Start implementation
   /forge:design {PRD_ID} --type sequence --flow {name}  - Add more diagrams
```

## Options

- `--type {type}`: Generate specific diagram type only
  - `system`: System architecture
  - `class`: Class/domain model
  - `sequence`: Sequence diagram
  - `package`: Package/component
  - `er`: Entity relationship
  - `state`: State diagram
  - `activity`: Activity diagram
- `--flow {name}`: For sequence/activity, specify the flow name
- `--format {format}`: Output format (puml, png, svg)
- `--update`: Update existing diagrams based on changes
