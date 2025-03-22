from app import app, db, create_dummy_jobs

with app.app_context():
    db.create_all()
    create_dummy_jobs()
    print("Database initialized successfully!") 