"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .models import get_user_email
from . common import db, session, T, cache, auth, signed_url
import base64
from pydal.validators import *


url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    products = db(db.listing).select().as_list()

    return dict(
        get_products_url = URL('get_products'),
        products=products,
        )


# @action('add', method = ["GET", "POST"])
# @action.uses(db, auth.user, 'add.html')
# def add():
#     form = Form(db.listing, csrf_session = session, formstyle = FormStyleBulma)
#     if form.accepted:
#         redirect(URL('index'))
#     return dict(form = form)

@action('account', method = ["GET", "POST"])
@action.uses(db, auth.user, 'account.html')
def account():
    account_info = str(get_user_email())
    # getting email based on user current logged in 

    query = (db.account_info.Email == account_info)
    rows = db(query).select().as_list()

    if not rows:
        db.account_info.insert(Email=account_info, Phone='N/A', Payment='Other', College='Other')
        query = (db.account_info.Email == account_info)
        rows = db(query).select().as_list()


    query2 = (db.listing.creator == get_user_email())
    products = db(query2).select()

    return dict(account_info=account_info, rows=rows, products=products)
    


@action('add', method = ["GET", "POST"])
@action.uses(db, auth.user, 'add.html')
def add():
    form = Form([Field('Name'),
    Field('Condition', requires=IS_IN_SET(['New', 'Used - Like New', 'Used - Good', 'Used - Fair'])),
    Field('Category', requires=IS_IN_SET(['Clothing', 'Electronics', 'Dorm Gear', 'School Supplies' ,'Free Stuff', 'Other'])),
    Field('Price', 'integer', requires=IS_INT_IN_RANGE(1,1000000), default=0),
    Field('Image', 'upload'),
    Field('Description', 'text') 
    ], csrf_session = session, formstyle = FormStyleBulma)
    if form.accepted:
        # We manually process the fields, this is to get image upload button and create the form
        # database stores the image as text, allowing us to store the data_url for each listing
       
        fileObject = form.vars['Image']
        # this is the image object that is passed in
       
        contents = fileObject.file.read()
        # this is the contents of the image, essentially what encode

        encodedVal = base64.b64encode(contents).decode('utf-8')
        data_url = f'data:{fileObject.content_type};base64,{encodedVal}'

        # first line encodes the file to base 64 then decodes to make it part of data URL
        # second line creates the URL which we can call in index.html
    
        db.listing.insert(
            Name=form.vars["Name"],
            Condition=form.vars["Condition"],
            Category=form.vars["Category"],
            Price=form.vars["Price"],
            Image=data_url,
            Description=form.vars['Description']
        )
        # this actually stores it in the DB
        redirect(URL('index'))
    return dict(form = form)

@action('save_account_info', method=['GET', 'POST'])
@action.uses(db, auth.user, 'account.html')
def save_account_info():
    form = Form([
    Field('Address', 'string'),
    Field('Phone', 'string'),
    Field('College',  requires=IS_IN_SET(['Cowell', 'Stevenson', 'Crown', 'Merill' ,'Porter', 'Kresge', 'Oakes', 'Rachel Carson', 'College Nine', 'College Ten', 'Graduate Student', 'Other' ]))
    ], csrf_session = session, formstyle = FormStyleBulma)
    if form.accepted:    
        db.listing.insert(
            Address=form.vars["Address"],
            Phone=form.vars["Phone"],
            College=form.vars["College"],
        )
    return dict(form = form)
    
@action('edit/<account_id:int>', method = ["GET", "POST"])
@action.uses(db, auth.user, 'edit.html')
def edit(account_id = None):
    assert account_id is not None
    p = db.account_info[account_id]
    if p is None:
        redirect(URL('index'))
    form = Form(db.account_info, record = p, deletable = False, csrf_session = session, formstyle = FormStyleBulma)
    if form.accepted:
        redirect(URL('account'))
    return dict(form=form)




@action('home', method=["GET", "POST"])
@action.uses(db, auth.user, 'index.html')
def home():
    redirect(URL('default', 'index'))


@action('description/<listing_id:int>', method = ["GET", "POST"])
@action.uses(db, auth.user, 'description.html')
def description(listing_id = None):
    assert listing_id is not None

    item = db(db.listing.id == listing_id).select().as_list()
    print(item[0]['Price'])

    creator = db(db.account_info.Email == item[0]['creator']).select()


    return dict(item=item, creator = creator)

@action('get_products')
@action.uses(db, auth.user)
def get_products():

    t = request.params.get('q')
    if t:
        tt = t.strip()
        q = ((db.listing.Name.contains(tt)) |
             (db.listing.Description.contains(tt)))
        

    results = db(q).select(db.listing.ALL).as_list()

    print(results)
    return dict(results=results)

@action('filter/<listing_category>', method = ["GET", "POST"])
@action.uses(db, auth.user, 'category.html')
def filter(listing_category):

    assert listing_category is not None
    if(listing_category.isdigit()):
        max_price = int(listing_category)
        display = db(db.listing.Price < max_price).select().as_list()
    else:
        display = db(db.listing.Category == listing_category).select().as_list()
    
    return dict(listing_category=listing_category, display=display)

@action('edit_listing/<listing_id:int>', method = ["GET", "POST"])
@action.uses(db, auth.user, 'edit_listing.html')
def edit_listing(listing_id = None):
    assert listing_id is not None
    p = db.listing[listing_id]
    # print(p)
    if p is None:
        redirect(URL('account'))

    form = Form([Field('Name'),
    Field('Condition', requires=IS_IN_SET(['New', 'Used - Like New', 'Used - Good', 'Used - Fair'])),
    Field('Category', requires=IS_IN_SET(['Clothing', 'Electronics', 'Dorm Gear', 'School Supplies' ,'Free Stuff', 'Other'])),
    Field('Price', 'integer', requires=IS_INT_IN_RANGE(1,1000000), default=0),
    Field('Image', 'upload'),
    Field('Description', 'text') 
    ], record = p, deletable = False, csrf_session = session, formstyle = FormStyleBulma)

    # form = Form(db.listing, record = p, deletable = False, csrf_session = session, formstyle = FormStyleBulma)
    
    if form.accepted:
        # We manually process the fields, this is to get image upload button and create the form
        # database stores the image as text, allowing us to store the data_url for each listing
       
        fileObject = form.vars['Image']
        # this is the image object that is passed in
       
        contents = fileObject.file.read()
        # this is the contents of the image, essentially what encode

        encodedVal = base64.b64encode(contents).decode('utf-8')
        data_url = f'data:{fileObject.content_type};base64,{encodedVal}'

        # first line encodes the file to base 64 then decodes to make it part of data URL
        # second line creates the URL which we can call in index.html
    
        p.update_record(
            Name=form.vars["Name"],
            Condition=form.vars["Condition"],
            Category=form.vars["Category"],
            Price=form.vars["Price"],
            Image=data_url,
            Description=form.vars["Description"]
        )
        # this actually stores it in the DB
        redirect(URL('account'))

    return dict(form = form)

@action('delete_listing/<listing_id:int>', method = ["GET", "POST"])
@action.uses(db, auth.user)
def delete_listing(listing_id=None):
    assert listing_id is not None
    p = db.listing[listing_id]

    if p is None:
        # If there is no such listing, then redirect to account.
        redirect(URL('account'))
    else:
        # Delete the listing and redirect to account.
        p.delete_record()
        # Commit changes to the database
        db.commit()
        redirect(URL('account'))
