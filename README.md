# Groq AI Chat Platform

A production-grade AI chat backend built with Django REST Framework, Groq LLaMA 3, JWT auth, Redis rate limiting & caching, Celery async tasks, and raw SQL analytics. Deployed on Railway.

---

## Quick Start

```bash
git clone https://github.com/areeb-ajmal/Groq-Ai-chatBot-Backend-using-Django-Django-REST-Framework.git
cd Groq-Ai-chatBot-Backend-using-Django-Django-REST-Framework

pip install -r requirements.txt
```

Create a `.env` file in the root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/ai_chat_db
GROQ_API_KEY=your-groq-api-key
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

Start Celery (in separate terminals):

```bash
celery -A core worker --loglevel=info
celery -A core beat --loglevel=info
```

---

## Stack

| | |
|---|---|
| **Framework** | Django + Django REST Framework |
| **AI** | Groq API (LLaMA 3) |
| **Auth** | JWT via `simplejwt`, custom user model |
| **Cache / Rate Limit** | Redis |
| **Async Tasks** | Celery + Celery Beat |
| **Database** | PostgreSQL (SQLite for dev) |
| **Deployment** | Railway + Redis Cloud |

---

## Project Structure

```
ai_chat_platform/
├── accounts/           # CustomUser model, JWT signup/login
├── chat/               # Conversation & Message models, Groq client
├── analytics/          # Raw SQL usage stats endpoints
├── notifications/      # Celery tasks — welcome email, daily report
└── core/               # settings.py, celery.py, urls.py
```

---

## API Endpoints

**Auth**
```
POST  /api/auth/register/       Create account
POST  /api/auth/login/          Get JWT tokens
POST  /api/auth/refresh/        Refresh access token
```

**Chat**
```
POST  /api/chat/send/                           Send message → get AI reply
GET   /api/chat/conversations/                  List conversations
GET   /api/chat/conversations/{id}/messages/    Full chat history
```

**Analytics** *(Raw SQL)*
```
GET   /api/analytics/summary/      Total messages, active users
GET   /api/analytics/top-users/    Most active users
```

---

## Deployment (Railway)

**Procfile:**
```
web:    gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A core worker --loglevel=info
beat:   celery -A core beat --loglevel=info
```

Set these as Railway environment variables:
`SECRET_KEY` `DATABASE_URL` `REDIS_URL` `GROQ_API_KEY` `EMAIL_HOST_USER` `EMAIL_HOST_PASSWORD` `DEBUG=False` `ALLOWED_HOSTS`

---

## License

MIT
