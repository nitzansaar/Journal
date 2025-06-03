# 📝 Daily Journal Web App

A full-stack journaling application built with Next.js, FastAPI, and Supabase.

## 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python
- **Database**: Supabase (PostgreSQL with authentication)
- **Containerization**: Docker and Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Supabase account and project

### 1. Database Setup

1. Go to your Supabase project dashboard
2. Navigate to the SQL Editor
3. Run the SQL script from `database_setup.sql` to create the tables and policies

### 2. Environment Variables

Add the following to your `.env` file (you already have most of these):

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

**Important**: Add your `SUPABASE_SERVICE_ROLE_KEY` from Supabase Dashboard → Settings → API → service_role key

### 3. Run the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📱 Features

- **Authentication**: Sign up and login with email/password
- **Journal Entries**: Create, view, and manage personal journal entries
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Automatic refresh of entries
- **Secure**: Row-level security ensures users only see their own entries

## 🔧 Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Backend Development

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📊 API Endpoints

### Authentication
All endpoints require an `Authorization: Bearer <token>` header.

### POST `/entries`
Create a new journal entry.

**Request Body:**
```json
{
  "content": "Today I learned about Docker."
}
```

**Response:**
```json
{
  "id": "uuid",
  "created_at": "2024-01-01T12:00:00Z",
  "user_id": "user_id", 
  "content": "Today I learned about Docker."
}
```

### GET `/entries`
Get all entries for the authenticated user.

**Response:**
```json
[
  {
    "id": "uuid",
    "created_at": "2024-01-01T12:00:00Z",
    "content": "Today I learned about Docker."
  }
]
```

## 🗄️ Database Schema

### `journal_entries` Table

| Column       | Type      | Description               |
|-------------|-----------|---------------------------|
| `id`        | UUID      | Primary key               |
| `user_id`   | TEXT      | User ID from Supabase     |
| `content`   | TEXT      | Journal entry content     |
| `created_at`| TIMESTAMP | Entry creation timestamp  |

## 🔒 Security

- Row Level Security (RLS) policies ensure data isolation
- JWT token validation on all API endpoints
- Environment variables for sensitive configuration
- CORS configuration for frontend-backend communication

## 🐳 Docker Services

- **frontend**: Next.js application (port 3000)
- **backend**: FastAPI application (port 8000)

## 📝 Usage

1. **Sign Up**: Create a new account with email and password
2. **Sign In**: Login with your credentials
3. **Write Entry**: Use the form to write a new journal entry
4. **View Entries**: See all your previous entries sorted by date
5. **Sign Out**: Logout securely

## 🛠️ Troubleshooting

### Common Issues

1. **Backend fails to start**: Make sure `SUPABASE_SERVICE_ROLE_KEY` is set in `.env`
2. **Frontend can't connect**: Verify `NEXT_PUBLIC_API_URL` points to `http://localhost:8000`
3. **Authentication errors**: Check that the Supabase URL and anon key are correct
4. **Database errors**: Ensure the `journal_entries` table exists and RLS policies are set

### Logs

```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs frontend
docker-compose logs backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 