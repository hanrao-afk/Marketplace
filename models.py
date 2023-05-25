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
    ### TODO: define here any fields you need.
    ### To help you, here's how to declare the user_email field.
    Field('Name'),
    Field('Condition'),
    Field('Category'),
    Field('Price', 'integer', requires=IS_INT_IN_RANGE(1,1000000), default=0)
)

db.commit()
