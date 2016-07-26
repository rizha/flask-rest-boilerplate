import os

from app import create_app
from extensions import celery


app = create_app(os.getenv('FLASK_CONFIG') or 'local')
app.app_context().push
