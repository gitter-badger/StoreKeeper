from datetime import datetime

from app import validators
from app.server import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True, info={'validators': validators.username})
    password_hash = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False, info={'validators': validators.email})
    admin = db.Column(db.Boolean, nullable=False, default=False)
    disabled = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self)-> str:
        return '%s [admin=%r disabled=%r]' % (self.username, self.admin, self.disabled)

    @classmethod
    def get(cls, username: str) -> "User":
        return cls.query.filter_by(username=username).first()

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    # flask-loginmanager
    def is_authenticated(self) -> bool:
        return True

    # flask-loginmanager
    def is_active(self) -> bool:
        return not self.disabled

    # flask-loginmanager
    def is_anonymous(self) -> bool:
        return False

    # flask-loginmanager
    def get_id(self) -> str:
        return str(self.id)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    article_number = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)

    vendor = db.relationship('Vendor')
    unit = db.relationship('Unit')
    barcodes = db.relationship('Barcode', lazy='dynamic')

    def __repr__(self)-> str:
        return "%s" % self.name

    @classmethod
    def get(cls, id: int) -> "Item":
        return cls.query.filter_by(id=id).first()


class Barcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(15), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    main = db.Column(db.Boolean, default=False)

    item = db.relationship('Item')

    def __repr__(self)-> str:
        return "%s [quantity=%r]" % (self.barcode, self.quantity)

    @classmethod
    def get(cls, id: int) -> "Barcode":
        return cls.query.filter_by(id=id).first()


class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    items = db.relationship('Item', lazy='dynamic')

    def __repr__(self)-> str:
        return "%s" % self.name

    @classmethod
    def get(cls, id: int) -> "Vendor":
        return cls.query.filter_by(id=id).first()


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self)-> str:
        return "%s" % self.unit

    @classmethod
    def get(cls, id: int) -> "Unit":
        return cls.query.filter_by(id=id).first()


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    comment = db.Column(db.Text)
    outbound_close_timestamp = db.Column(db.DateTime)
    outbound_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    return_close_timestamp = db.Column(db.DateTime)
    return_close_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('Customer')
    outbound_close_user = db.relationship('User', foreign_keys=[outbound_close_user_id])
    return_close_user = db.relationship('User', foreign_keys=[return_close_user_id])
    work_items = db.relationship('WorkItem', lazy='dynamic')

    def __repr__(self)-> str:
        return "%s [%r]" % (self.id, self.customer)

    @classmethod
    def get(cls, id: int) -> "Work":
        return cls.query.filter_by(id=id).first()


class WorkItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    outbound_quantity = db.Column(db.Integer, nullable=False)
    return_quantity = db.Column(db.Integer)

    work = db.relationship('Work')
    item = db.relationship('Item')

    def __repr__(self)-> str:
        return "%s [-%s, +%s]" % (self.item, self.outbound_quantity, self.return_quantity)

    @classmethod
    def get(cls, id: int) -> "WorkItem":
        return cls.query.filter_by(id=id).first()


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self)-> str:
        return "%s" % self.name

    @classmethod
    def get(cls, id: int) -> "Customer":
        return cls.query.filter_by(id=id).first()


class Acquisition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text)

    items = db.relationship('AcquisitionItem', lazy='dynamic')

    def __repr__(self)-> str:
        return "%s [%s]" % (self.id, self.timestamp)

    @classmethod
    def get(cls, id: int) -> "Acquisition":
        return cls.query.filter_by(id=id).first()


class AcquisitionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acquisition_id = db.Column(db.Integer, db.ForeignKey('acquisition.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    acquisition = db.relationship('Acquisition')
    item = db.relationship('Item')

    def __repr__(self)-> str:
        return "%s [%r]" % (self.id, self.item)

    @classmethod
    def get(cls, id: int) -> "AcquisitionItem":
        return cls.query.filter_by(id=id).first()


class Stocktaking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text)

    items = db.relationship('StocktakingItem', lazy='dynamic')

    def __repr__(self)-> str:
        return "%s [%s]" % (self.id, self.timestamp)

    @classmethod
    def get(cls, id: int) -> "Stocktaking":
        return cls.query.filter_by(id=id).first()


class StocktakingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stocktaking_id = db.Column(db.Integer, db.ForeignKey('stocktaking.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    stocktaking = db.relationship('Stocktaking')
    item = db.relationship('Item')

    def __repr__(self)-> str:
        return "%s [%r]" % (self.id, self.item)

    @classmethod
    def get(cls, id: int) -> "StocktakingItem":
        return cls.query.filter_by(id=id).first()
