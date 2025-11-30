# IdeaForge Patterns Skill

> TDD 워크플로우 및 코딩 패턴 가이드

---

## TDD Patterns

### 1. RED Phase - 테스트 먼저

```python
# tests/test_{feature}.py

import pytest
from src.{module} import {function}


class Test{Feature}:
    """Test cases for {feature}."""

    def test_{scenario}_success(self):
        """성공 케이스 테스트."""
        # Arrange
        input_data = ...

        # Act
        result = {function}(input_data)

        # Assert
        assert result == expected

    def test_{scenario}_failure(self):
        """실패 케이스 테스트."""
        with pytest.raises(ExpectedException):
            {function}(invalid_data)

    def test_{scenario}_edge_case(self):
        """엣지 케이스 테스트."""
        # Edge case handling
        pass
```

### 2. GREEN Phase - 최소 구현

```python
# src/{module}.py

def {function}(data):
    """
    {Function description}.

    Args:
        data: Input data

    Returns:
        Result

    Raises:
        ValueError: If data is invalid
    """
    # Minimal implementation to pass tests
    if not data:
        raise ValueError("Data is required")

    return result
```

### 3. REFACTOR Phase - 개선

체크리스트:
- [ ] 중복 코드 제거
- [ ] 의미있는 변수명
- [ ] 함수 분리 (단일 책임)
- [ ] 타입 힌트 추가
- [ ] docstring 작성
- [ ] 테스트 재실행으로 통과 확인

---

## API Design Patterns

### FastAPI Endpoint

```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["feature"])


class RequestModel(BaseModel):
    """Request schema."""
    field: str


class ResponseModel(BaseModel):
    """Response schema."""
    id: str
    result: str


@router.post("/endpoint", response_model=ResponseModel)
async def create_something(
    request: RequestModel,
    db: Session = Depends(get_db),
) -> ResponseModel:
    """
    Create something.

    Args:
        request: Request data

    Returns:
        Created resource

    Raises:
        HTTPException: If creation fails
    """
    try:
        result = await service.create(request)
        return ResponseModel(id=result.id, result=result.data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## Database Patterns

### SQLAlchemy Model

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

---

## Frontend Patterns

### React Component (TypeScript)

```typescript
import React, { useState, useCallback } from 'react';

interface Props {
  initialValue: string;
  onSubmit: (value: string) => void;
}

export const Component: React.FC<Props> = ({ initialValue, onSubmit }) => {
  const [value, setValue] = useState(initialValue);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim()) {
      setError('Value is required');
      return;
    }
    onSubmit(value);
  }, [value, onSubmit]);

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        aria-label="Input field"
      />
      {error && <span role="alert">{error}</span>}
      <button type="submit">Submit</button>
    </form>
  );
};
```

---

## Error Handling

```python
class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, code: str = "UNKNOWN"):
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(AppError):
    """Validation error."""

    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class NotFoundError(AppError):
    """Resource not found error."""

    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} with id {id} not found", "NOT_FOUND")
```

---

## Testing Best Practices

1. **Arrange-Act-Assert** 패턴 사용
2. **한 테스트당 하나의 검증**
3. **테스트 이름은 동작을 설명**
4. **Fixture로 반복 코드 제거**
5. **Mocking은 외부 의존성에만**
6. **Coverage 80% 이상 목표**
