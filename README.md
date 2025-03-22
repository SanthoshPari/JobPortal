# Job Portal

A modern job portal built with Flask, allowing job seekers to find and apply for jobs, and employers to post job listings.

## Features

- **User Authentication**
  - Job seeker and employer registration
  - Secure login/logout functionality
  - Role-based access control

- **Job Seeker Features**
  - Browse job listings
  - Search jobs by category
  - Apply for jobs
  - Track application status
  - View company profiles

- **Employer Features**
  - Post job listings
  - Manage job postings
  - View applicants
  - Company profile management

- **General Features**
  - Modern, responsive design
  - Category-based job browsing
  - Company listings
  - Career advice section
  - Contact form

## Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- SQLite
- Bootstrap 5
- HTML/CSS
- JavaScript

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/job-portal.git
   cd job-portal
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
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

6. Visit http://localhost:5000 in your web browser

## Default Test Account

- **Employer Account**
  - Email: employer@example.com
  - Password: password123

## Project Structure

```
job-portal/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   │   ├── hero/
│   │   ├── icons/
│   │   └── logos/
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── ...
├── app.py
├── init_db.py
└── requirements.txt
```

## Contributing

Feel free to fork this project and submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 