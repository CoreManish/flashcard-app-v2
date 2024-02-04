# run.py

from app import app

# In your run.py or main application file
from app import db
from app.models import *

# Create tables
with app.app_context():
    # Create tables
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)