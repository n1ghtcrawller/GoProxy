# Instruction

### 1.
```bash
  git clone git@github.com:n1ghtcrawller/GoProxy.git
```
### 2. add .env with:
```
POSTGRES_USER,
POSTGRES_PASSWORD,
POSTGRES_DB,
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB},
BOT_TOKEN,
HOST
```
3. 
```bash
  docker-compose up --build
```
### DOCS: localhost:8000/docs

