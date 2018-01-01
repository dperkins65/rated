from app.config import APPLICATION_ROOT
from app.database import db, User


def create_db():
    """Creates the database."""
    db.create_all()


def drop_db():
    """Drops the database."""
    db.drop_all()


def recreate_db():
    """Same as running drop_db() and create_db()."""
    drop_db()
    create_db()
    populate_db()


def populate_db():
    """Populates the database with seed data."""
    try:
        users = [
            User(name=u'admin', role=1),
        ]
        db.session.add_all(users)
        db.session.commit()
    except:
        db.session.rollback()
        raise Exception("Failed to populate the database")
    finally:
        db.session.close()
