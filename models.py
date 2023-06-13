"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'listing',
    Field('Name'),
    Field('Condition', requires=IS_IN_SET(['New', 'Used - Like New', 'Used - Good', 'Used - Fair'])),
    Field('Category', requires=IS_IN_SET(['Clothing', 'Electronics', 'Dorm Gear', 'School Supplies' ,'Free Stuff', 'Other'])),
    Field('Price', 'integer', requires=IS_INT_IN_RANGE(1,1000000), default=0),
    Field('Image', 'text'),
    Field('Description', 'text')
)

db.define_table(
    'account_info',
    Field('Email', default=get_user_email),
    Field('Phone', 'string'),
    Field('Payment',requires=IS_IN_SET(['Venmo', 'CashApp', 'Zelle', 'Apple Pay' ,'Cash', 'Other'])),
    Field('College',  requires=IS_IN_SET(['Cowell', 'Stevenson', 'Crown', 'Merill' ,'Porter', 'Kresge', 'Oakes', 'Rachel Carson', 'College Nine', 'College Ten', 'Graduate Student', 'Other' ]))
)

db.commit()
