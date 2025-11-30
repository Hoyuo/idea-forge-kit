# Architecture Design (PlantUML)

> Text-based architecture visualization with PlantUML.
> Preview: https://www.plantuml.com/plantuml

---

## Diagram Types Overview

| Type | Purpose | Use When |
|------|---------|----------|
| System Architecture | High-level component overview | Project kickoff, stakeholder communication |
| Class Diagram | Entity/model relationships | Domain modeling, database design |
| Sequence Diagram | API flow, service interaction | API design, integration planning |
| Package Diagram | Module structure, dependencies | Code organization, layering |
| ER Diagram | Database schema | Data modeling |
| State Diagram | Entity state transitions | Workflow design |
| Activity Diagram | Business process flow | User journey, workflow |

---

## System Architecture Diagram

```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle

title System Architecture: {PROJECT}

package "Presentation Layer" {
  [Web Client]
  [Mobile Client]
  [Admin Dashboard]
}

package "API Layer" {
  [API Gateway]
  [Load Balancer]
}

package "Service Layer" {
  [Service A]
  [Service B]
  [Service C]
}

package "Data Layer" {
  database "Primary DB"
  database "Cache"
  queue "Message Queue"
}

package "External" {
  cloud "Third-party APIs"
}

[Web Client] --> [API Gateway]
[Mobile Client] --> [API Gateway]
[API Gateway] --> [Service A]
[Service A] --> [Primary DB]
[Service A] --> [Cache]
[Service B] --> [Message Queue]
[Service C] --> [Third-party APIs]

@enduml
```

---

## Class Diagram (Domain Model)

```plantuml
@startuml
!theme plain
skinparam classAttributeIconSize 0

title Domain Model: {PROJECT}

' Abstract base
abstract class BaseEntity {
  +id: UUID
  +createdAt: DateTime
  +updatedAt: DateTime
}

' Main entities
class User extends BaseEntity {
  +email: String
  +username: String
  +passwordHash: String
  +status: Status
  --
  +authenticate(password): Boolean
  +generateToken(): Token
}

class Resource extends BaseEntity {
  +name: String
  +ownerId: UUID
  +data: JSON
  --
  +validate(): Boolean
}

' Enums
enum Status {
  ACTIVE
  INACTIVE
  SUSPENDED
}

' Relationships
User "1" -- "*" Resource : owns
User -- Status

@enduml
```

---

## Sequence Diagram (API Flow)

```plantuml
@startuml
!theme plain

title API Flow: {OPERATION}

actor Client as client
participant "API Gateway" as gateway
participant "Auth Service" as auth
participant "Core Service" as core
database "Database" as db

client -> gateway: Request
gateway -> auth: Validate token

alt Token valid
  auth --> gateway: OK
  gateway -> core: Process request
  core -> db: Query data
  db --> core: Result
  core --> gateway: Response
  gateway --> client: 200 OK
else Token invalid
  auth --> gateway: 401 Unauthorized
  gateway --> client: 401 Error
end

@enduml
```

---

## Package/Component Diagram

```plantuml
@startuml
!theme plain

title Package Structure: {PROJECT}

package "api" as api {
  [routes]
  [middleware]
  [handlers]
}

package "service" as svc {
  [business logic]
  [validators]
}

package "domain" as domain {
  [entities]
  [value objects]
  [interfaces]
}

package "infrastructure" as infra {
  [repositories]
  [external clients]
  [config]
}

api ..> svc : uses
svc ..> domain : uses
infra ..> domain : implements
svc ..> infra : uses

@enduml
```

---

## ER Diagram (Database Schema)

```plantuml
@startuml
!theme plain
skinparam linetype ortho

title Database Schema: {PROJECT}

entity "users" {
  *id : uuid <<PK>>
  --
  *email : varchar(255) <<unique>>
  username : varchar(50)
  *password_hash : varchar(255)
  status : varchar(20)
  *created_at : timestamp
  updated_at : timestamp
}

entity "resources" {
  *id : uuid <<PK>>
  --
  *owner_id : uuid <<FK>>
  *name : varchar(255)
  data : jsonb
  *created_at : timestamp
  updated_at : timestamp
}

entity "audit_logs" {
  *id : uuid <<PK>>
  --
  user_id : uuid <<FK>>
  *action : varchar(100)
  details : jsonb
  *created_at : timestamp
}

users ||--o{ resources : "owns"
users ||--o{ audit_logs : "generates"

@enduml
```

---

## State Diagram

```plantuml
@startuml
!theme plain

title Entity State: {ENTITY}

[*] --> Created : initialize

Created --> Active : activate
Created --> [*] : delete

Active --> Suspended : suspend
Active --> Inactive : deactivate
Active --> Active : update

Suspended --> Active : restore
Suspended --> [*] : delete

Inactive --> Active : reactivate
Inactive --> [*] : delete (after retention)

@enduml
```

---

## Activity Diagram (Workflow)

```plantuml
@startuml
!theme plain

title Workflow: {PROCESS}

start

:Receive input;

:Validate input;

if (Valid?) then (yes)
  :Process data;

  fork
    :Update database;
  fork again
    :Send notification;
  end fork

  :Return success;
else (no)
  :Return validation error;
endif

stop

@enduml
```

---

## Design Output Structure

```
.forge/design/{PRD_ID}/
├── diagrams/
│   ├── system-architecture.puml
│   ├── class-diagram.puml
│   ├── sequence-{flow}.puml
│   ├── package-diagram.puml
│   ├── er-diagram.puml
│   ├── state-{entity}.puml
│   └── activity-{process}.puml
├── images/                      # Generated images (optional)
└── DESIGN.md                    # Design documentation
```

---

## PlantUML Best Practices

1. **Use themes**: `!theme plain` for clean output
2. **Title every diagram**: `title {Diagram Name}`
3. **Group related elements**: Use `package`, `rectangle`, `folder`
4. **Use stereotypes**: `<<interface>>`, `<<abstract>>`, `<<PK>>`, `<<FK>>`
5. **Keep diagrams focused**: One concept per diagram
6. **Use consistent naming**: Match code naming conventions
7. **Add notes when needed**: `note right of X : explanation`

---

## Rendering Options

| Tool | Description |
|------|-------------|
| PlantUML Server | https://www.plantuml.com/plantuml |
| VS Code Extension | PlantUML extension |
| IntelliJ Plugin | PlantUML Integration |
| CLI | `java -jar plantuml.jar diagram.puml` |
| GitHub Action | `plantuml/plantuml-action` |
