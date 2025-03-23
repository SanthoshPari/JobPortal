# Job Portal

A modern job portal built with Flask that connects job seekers with employers. Features include user authentication, job posting, job search, and application management.

## Features

- User Authentication (Job Seekers & Employers)
- Job Posting & Management
- Job Search & Filtering
- Job Applications
- Company Profiles
- Responsive Design
- Modern UI/UX

## Tech Stack

- Python/Flask
- SQLAlchemy
- HTML5/CSS3
- JavaScript
- SQLite Database

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job-portal.git
cd job-portal
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python app.py
```

6. Visit `http://localhost:5000` in your browser

## Default Test Account (Employer)
- Email: admin@example.com
- Password: admin123

## Project Structure

```
job-portal/
├── app.py              # Main application file
├── init_db.py          # Database initialization
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── instance/          # Database and instance-specific files
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 