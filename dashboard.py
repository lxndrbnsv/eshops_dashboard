from app import app, db
from app.models import User, ScraperCategory, RefCode


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "ScraperCategory": ScraperCategory,
        "RefCode": RefCode
    }
