from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///jobportal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'jobseeker' or 'employer'
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary = db.Column(db.String(50))
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_dummy_jobs():
    # Create a dummy employer if it doesn't exist
    employer = User.query.filter_by(email='employer@example.com').first()
    if not employer:
        employer = User(
            email='employer@example.com',
            name='TechCorp Inc.',
            user_type='employer'
        )
        employer.set_password('password123')
        db.session.add(employer)
        db.session.commit()

    # Check if we already have jobs
    if Job.query.count() == 0:
        dummy_jobs = [
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp Inc.',
                'location': 'San Francisco, CA',
                'description': 'We are looking for an experienced software engineer to join our team. The ideal candidate will have strong experience with Python, JavaScript, and modern web frameworks.',
                'requirements': '- 5+ years of experience\n- Strong Python and JavaScript skills\n- Experience with React and Node.js\n- Bachelor\'s degree in Computer Science or related field',
                'salary': '$120,000 - $150,000',
                'employer_id': employer.id
            },
            {
                'title': 'Digital Marketing Manager',
                'company': 'MarketingPro',
                'location': 'New York, NY',
                'description': 'Seeking a creative and data-driven marketing manager to lead our digital marketing efforts. You will be responsible for developing and executing marketing strategies across various channels.',
                'requirements': '- 3+ years of digital marketing experience\n- Strong analytical skills\n- Experience with SEO and social media marketing\n- Bachelor\'s degree in Marketing or related field',
                'salary': '$80,000 - $100,000',
                'employer_id': employer.id
            },
            {
                'title': 'UI/UX Designer',
                'company': 'DesignHub',
                'location': 'Remote',
                'description': 'Join our design team to create beautiful and intuitive user interfaces. We need someone who can translate complex requirements into elegant solutions.',
                'requirements': '- 3+ years of UI/UX design experience\n- Proficiency in Figma and Adobe Creative Suite\n- Strong portfolio\n- Bachelor\'s degree in Design or related field',
                'salary': '$90,000 - $120,000',
                'employer_id': employer.id
            },
            {
                'title': 'Sales Manager',
                'company': 'SalesForce',
                'location': 'Chicago, IL',
                'description': 'Looking for a dynamic sales manager to lead our sales team and drive revenue growth. The ideal candidate will have a proven track record in B2B sales.',
                'requirements': '- 5+ years of sales experience\n- Strong leadership skills\n- Experience with CRM systems\n- Bachelor\'s degree in Business or related field',
                'salary': '$100,000 - $130,000',
                'employer_id': employer.id
            }
        ]

        for job_data in dummy_jobs:
            job = Job(**job_data)
            db.session.add(job)
        
        db.session.commit()

# Routes
@app.route('/')
def index():
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('index.html', jobs=jobs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        user_type = request.form.get('user_type')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(email=email, name=name, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post-job', methods=['GET', 'POST'])
@login_required
def post_job():
    if current_user.user_type != 'employer':
        flash('Only employers can post jobs')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        job = Job(
            title=request.form.get('title'),
            company=request.form.get('company'),
            location=request.form.get('location'),
            description=request.form.get('description'),
            requirements=request.form.get('requirements'),
            salary=request.form.get('salary'),
            employer_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully')
        return redirect(url_for('index'))
    return render_template('post_job.html')

@app.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    if current_user.user_type != 'jobseeker':
        flash('Only job seekers can apply for jobs')
        return redirect(url_for('index'))
    
    job = Job.query.get_or_404(job_id)
    if Application.query.filter_by(job_id=job_id, user_id=current_user.id).first():
        flash('You have already applied for this job')
        return redirect(url_for('index'))
    
    application = Application(job_id=job_id, user_id=current_user.id)
    db.session.add(application)
    db.session.commit()
    flash('Application submitted successfully')
    return redirect(url_for('index'))

@app.route('/jobs/<category>')
def jobs_by_category(category):
    jobs = Job.query.filter(Job.title.ilike(f'%{category}%')).order_by(Job.created_at.desc()).all()
    return render_template('jobs.html', jobs=jobs, category=category)

@app.route('/companies')
def companies():
    # Get unique companies from jobs
    companies = db.session.query(Job.company, db.func.count(Job.id).label('job_count')).group_by(Job.company).all()
    return render_template('companies.html', companies=companies)

@app.route('/career-advice')
def career_advice():
    return render_template('career_advice.html')

@app.route('/profile')
@login_required
def profile():
    if current_user.user_type == 'jobseeker':
        applications = Application.query.filter_by(user_id=current_user.id).all()
    else:
        applications = Application.query.join(Job).filter(Job.employer_id == current_user.id).all()
    return render_template('profile.html', applications=applications)

@app.route('/applications')
@login_required
def applications():
    if current_user.user_type == 'jobseeker':
        applications = Application.query.filter_by(user_id=current_user.id).all()
    else:
        applications = Application.query.join(Job).filter(Job.employer_id == current_user.id).all()
    return render_template('applications.html', applications=applications)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here you would typically handle the contact form submission
        # For now, we'll just flash a message
        flash('Thank you for your message. We will get back to you soon!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', now=datetime.utcnow())

@app.route('/terms')
def terms():
    return render_template('terms.html', now=datetime.utcnow())

@app.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', job=job)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_dummy_jobs()
    app.run(debug=True) 