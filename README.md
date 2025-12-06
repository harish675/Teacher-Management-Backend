# Teacher Management Backend API

A FastAPI-based backend service for managing teachers, students, courses, and enrollments. This application provides a RESTful API for educational management with MongoDB as the database.

## 🚀 Features

- **Student Management** - CRUD operations for student records
- **Teacher Management** - Manage teacher profiles and information
- **Course Management** - Create and manage courses
- **Teacher Assignment** - Assign teachers to courses
- **Student Enrollment** - Enroll students in courses
- **Health Check** - API health monitoring endpoint
- **Auto Seeding** - Automatic database seeding on startup
- **JSON Logging** - Structured logging for better observability
- **CORS Support** - Cross-Origin Resource Sharing enabled

## 📋 Prerequisites

- Python 3.10 or higher
- MongoDB (local or cloud instance like MongoDB Atlas)
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Teacher-BE
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=kevin_assignment_db

# Server Configuration
PORT=8000
API_PREFIX=/rent-easy/api

# Environment
ENVIRONMENT=development
```

## 🏃 Running the Application

### Development Mode

```bash
fastapi dev main.py --port 8000
```

The API will be available at: `http://localhost:8000/rent-easy/api`

### Production Mode

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/rent-easy/api/docs`
- **ReDoc**: `http://localhost:8000/rent-easy/api/redoc`

### Available Endpoints

#### Health Check
- `GET /rent-easy/api/health` - Check API health status

#### Students
- `GET /rent-easy/api/students` - Get all students
- `POST /rent-easy/api/students` - Create a new student
- `GET /rent-easy/api/students/{id}` - Get student by ID
- `PUT /rent-easy/api/students/{id}` - Update student
- `DELETE /rent-easy/api/students/{id}` - Delete student

#### Teachers
- `GET /rent-easy/api/teachers` - Get all teachers
- `POST /rent-easy/api/teachers` - Create a new teacher
- `GET /rent-easy/api/teachers/{id}` - Get teacher by ID
- `PUT /rent-easy/api/teachers/{id}` - Update teacher
- `DELETE /rent-easy/api/teachers/{id}` - Delete teacher

#### Courses
- `GET /rent-easy/api/courses` - Get all courses
- `POST /rent-easy/api/courses` - Create a new course
- `GET /rent-easy/api/courses/{id}` - Get course by ID
- `PUT /rent-easy/api/courses/{id}` - Update course
- `DELETE /rent-easy/api/courses/{id}` - Delete course

#### Teacher Assignments
- `POST /rent-easy/api/assign-teacher` - Assign teacher to course
- `GET /rent-easy/api/assign-teacher/{course_id}` - Get assigned teachers

#### Student Enrollments
- `POST /rent-easy/api/enroll-student` - Enroll student in course
- `GET /rent-easy/api/enroll-student/{course_id}` - Get enrolled students

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t teacher-backend .
```

### Run Docker Container

```bash
docker run -p 8000:8000 \
  -e MONGO_URL=your_mongo_url \
  -e DB_NAME=kevin_assignment_db \
  -e ENVIRONMENT=production \
  teacher-backend
```

## ☁️ Cloud Deployment (Render)

For detailed deployment instructions to Render, see [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md).

### Quick Steps:

1. Push code to GitHub/GitLab
2. Create a MongoDB Atlas cluster
3. Create a new Web Service on Render
4. Select **Docker** as runtime
5. Set environment variables
6. Deploy!

## 🗂️ Project Structure

```
Teacher-BE/
├── src/
│   ├── app.py                 # FastAPI application setup
│   ├── router.py              # Main router configuration
│   ├── config/                # Configuration files
│   ├── lib/                   # Shared libraries (database, etc.)
│   └── modules/               # Feature modules
│       ├── student/           # Student management
│       ├── teacher/           # Teacher management
│       ├── course/            # Course management
│       ├── assign_teacher/    # Teacher assignment
│       ├── enrolled_studets/  # Student enrollment
│       └── seed_data/         # Database seeding
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .dockerignore             # Docker ignore rules
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Development

### Code Quality

This project uses Ruff for linting and formatting:

```bash
# Run linter
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

### Pre-commit Hooks

Install pre-commit hooks:

```bash
pre-commit install
```

## 🧪 Testing

```bash
# Run tests (when test suite is added)
pytest
```

## 📝 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGO_URL` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `DB_NAME` | Database name | `kevin_assignment_db` | Yes |
| `PORT` | Server port | `8000` | No |
| `API_PREFIX` | API route prefix | `/rent-easy/api` | No |
| `ENVIRONMENT` | Environment mode | `development` | No |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### MongoDB Connection Issues

- Ensure MongoDB is running: `sudo systemctl status mongod`
- Check connection string in `.env`
- Verify network access if using MongoDB Atlas

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

For issues and questions, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and MongoDB**
