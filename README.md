# LearnHub - منصة تعليمية تفاعلية

### Overview
LearnHub is a web-based educational platform built with Flask, designed to allow students to enroll in and manage courses. It supports light and dark themes, multilingual interfaces (English and Arabic with RTL support), and AJAX-based course enrollment/unenrollment. The platform uses SQLite for data storage and Bootstrap 5 for a responsive, modern UI.

### Features
- **User Authentication**: Secure login and registration.
- **Course Management**: Browse, enroll, and unenroll from courses via AJAX.
- **Multilingual Support**: English and Arabic with RTL layout for Arabic.
- **Theme Switcher**: Light and dark modes with persistent theme selection.
- **Responsive Design**: Optimized for mobile and desktop using Bootstrap 5.
- **API Endpoints**: RESTful API for course management.

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Redis (optional, for session storage)
- Git (for cloning the repository)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mohammadzaza93/Student-Course-Portal-Python-Flask.git
   cd learnhub
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**:
   ```bash
   python -c "from app import db; db.create_all()"
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your browser.

### Configuration
- **Environment Variables**:
  Create a `.env` file in the root directory:
  ```env
  FLASK_ENV=development
  SECRET_KEY=your-secret-key
  DATABASE_URL=sqlite:///learnhub.db
  REDIS_URL=redis://localhost:6379/0
  ```
- **Translations**:
  To update translations, run:
  ```bash
  pybabel extract -F babel.cfg -o messages.pot .
  pybabel update -i messages.pot -d translations
  pybabel compile -d translations -f
  ```

### Project Structure
```
learnhub/
├── app.py                  # Main application file
├── api.py                  # API endpoints
├── models.py               # Database models
├── forms.py                # Forms for registration/login
├── static/
│   ├── style.css          # Custom styles
│   ├── script.js          # Frontend JavaScript
│   ├── images/            # Logos and course images
├── templates/
│   ├── layout.html        # Base template
│   ├── dashboard.html     # User dashboard
│   ├── courses.html       # Course listing
│   ├── course_detail.html # Course details (optional)
├── translations/          # Language files (en, ar)
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```

### Usage
- **Register/Login**: Create an account or log in to access the dashboard.
- **Browse Courses**: View available courses and enroll via the courses page.
- **Manage Enrollment**: Enroll or unenroll from courses in the dashboard.
- **Switch Language**: Use the language dropdown to switch between English and Arabic.
- **Toggle Theme**: Use the theme switcher to toggle between light and dark modes.

### API Endpoints
- `GET /api/courses`: List all courses with enrollment status.
- `POST /ajax/enroll`: Enroll in a course.
- `POST /ajax/unenroll`: Unenroll from a course.

### Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.


