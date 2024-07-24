import mongoengine
from datetime import datetime
from mongoengine import DateTimeField, DecimalField, Document, EmailField, EmbeddedDocument, EmbeddedDocumentListField, \
    EnumField, IntField, ReferenceField, StringField, ValidationError
from app.enums import Exchanges, Instruments


class BaseDocument(Document):
    meta = {
        'abstract': True
    }
    creation_date = DateTimeField(default=datetime.utcnow())
    last_modification_date = DateTimeField(default=datetime.utcnow())


class Users(BaseDocument):
    meta = {
        'indexes': [
            'email', ('email', 'password', )
        ]
    }
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    last_logged_in = DateTimeField(default=datetime.utcnow())


class Investment(EmbeddedDocument):
    symbol = StringField()


class Watchlist(BaseDocument):
    meta = {
        'auto_create_index_on_save': True,
        'indexes': [
            'author', 'name', ('author', 'name', ),
        ]
    }
    name = StringField(required=True, unique=True)
    author = ReferenceField(Users, reverse_delete_rule=mongoengine.CASCADE, required=True)
    investments = EmbeddedDocumentListField(Investment)


    def validate(self, clean=True):
        super().validate(clean=clean)
        symbol_set = set()
        for investment in self.investments:
            if investment.symbol in symbol_set:
                raise ValidationError("Duplicate symbols are not allowed within a watchlist.")
            symbol_set.add(investment.symbol)


    def save(self, *args, **kwargs):
        self.validate()
        return super().save(*args, **kwargs)


class Symbols(BaseDocument):
    exchange = EnumField(Exchanges, required=True)
    token = IntField(required=True, unique=True)
    lot_size = IntField(required=True)
    symbol = StringField(required=True)
    trading_symbol = StringField(required=True, unique=True)
    instrument = EnumField(Instruments, required=True)
    tick_size = DecimalField(required=True)
    prev_closing_price = DecimalField()
    prev_closing = DateTimeField()
