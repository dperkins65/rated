from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.schema import UniqueConstraint


db = SQLAlchemy()


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, str) and id.isdigit(),
                isinstance(id, (int, float))),):
            return cls.query.get(int(id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class Base(CRUDMixin, db.Model):
    __abstract__  = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class User(UserMixin, Base):
    __tablename__ = 'users'

    ROLE_USER = 0
    ROLE_ADMIN = 1

    name = db.Column(db.String(255), unique=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __init__(
            self,
            name=None,
            role=None):
        self.name = name
        self.role = role

    @property
    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def __repr__(self):
        if self.is_admin:
            role = 'admin'
        else:
            role = 'user'
        return '<User %r:%r>' % (role, self.name)


class Brand(Base):
    __tablename__ = 'brands'

    name = db.Column(db.String(255), unique=True)

    def __init__(
            self,
            name=None):
        self.name = name

    def __repr__(self):
        return '<Brand %r>' % (self.name)


class Model(Base):
    __tablename__ = 'models'

    name = db.Column(db.String(255), unique=True)
    brand = db.relationship('Brand', backref='models')
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    notes = db.Column(db.Text)

    __table_args__ = (UniqueConstraint(brand_id, name),)

    def __init__(
            self,
            name=None,
            brand=None,
            notes=None):
        self.name = name
        self.brand = brand
        self.notes = notes

    def __repr__(self):
        return '<Model %r:%r>' % (self.brand.name, self.name)


class Survey(Base):
    __tablename__ = 'surveys'

    rating = db.Column(db.Integer)
    user = db.relationship('User', uselist=False, backref='surveys')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model = db.relationship('Model', backref='surveys')
    model_id = db.Column(db.Integer, db.ForeignKey('models.id'))

    def __init__(
            self,
            rating=None,
            user=None,
            model=None):
        self.rating = rating
        self.user = user
        self.model = model

    def __repr__(self):
        return '<Survey %r:%r:%r>' % (self.user.name,
                                      self.model.brand.name,
                                      self.model.name)
