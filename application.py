from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

from requests.models import Response

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, SportItem, User

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
	

app = Flask(__name__)

tempuser = User(name='Temp User', email='user@temp.com', picture='') 

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


categories = session.query(Category).order_by(asc(Category.name)).all()
latest_items = session.query(SportItem).order_by(desc(SportItem.id)).limit(9)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
	return render_template('showCatalog.html', categories=categories, latest_items=latest_items)

@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
    	user_id = createUser(login_session)

    login_session['user_id'] = 	user_id 

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user.
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response 

	# Revoke current user token
	access_token = credentials.access_token
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	print 'result is '
	print result
	if result['status'] == '200':
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfully disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

def createUser(login_session):

    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):

    user = session.query(User).filter_by(id=user_id).first()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).first()
        return user.id
    except:
        return None


@app.route('/catalog/<string:category_name>/items/')
def showCategoryItems(category_name):

	category = session.query(Category).filter_by(name=category_name).one()
	category_items = session.query(SportItem).filter_by(category_id=category.id).all()

	return render_template('showCategoryItems.html', categories=categories, category_items=category_items, selected_category=category.name)

@app.route('/catalog/<string:category_name>/items/new/', methods=['POST', 'GET'])
def createCategoryItem(category_name):
	if 'username' not in login_session:
		return redirect('/login')

	category = session.query(Category).filter_by(name=category_name).one()
	if request.method == 'GET':
		return render_template('createCategoryItem.html', category=category)
	else:
		category_items = session.query(SportItem).filter_by(category_id=category.id).all()
		newitem = SportItem(name=request.form['name'], description=request.form['description'],category=category, user_id=login_session['user_id'])
		session.add(newitem)
		session.commit()

		return redirect(url_for('showCategoryItems', category_name=category_name))	


@app.route('/catalog/new', methods=['POST', 'GET'])
def addItem():
	if 'username' not in login_session:
		return redirect('/login')

	if request.method == 'GET':
		return render_template('addItem.html', categories=categories)
	else:

		category = session.query(Category).filter_by(name=str(request.form.get('selectedcategory'))).one()
		user = session.query(User).filter_by(email=login_session['email']).one()		
		newitem = SportItem(name=request.form['name'], description=request.form['description'],category=category, user=user)
		session.add(newitem)
		session.commit()

		return redirect(url_for('showCategoryItems', category_name=category.name))	

@app.route('/catalog/json')
def showJsonCategoryItems():
	all_items = session.query(SportItem).all()
	all_categories = session.query(Category).all()

	return jsonify(Items=[i.serialize for i in all_items])
		# return jsonify(Category=[i.serialize for i in [session.query(SportItem).filter_by(category=c).all() for c in all_categories]])

@app.route('/catalog/<int:category_id>/item/<int:item_id>/json/')
def showJsonItem(category_id, item_id):
	item = session.query(SportItem).filter_by(category_id=category_id).filter_by(id=item_id).one()

	return jsonify(Item=item.serialize)

@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
	category = session.query(Category).filter_by(name=category_name).one()
	item = session.query(SportItem).filter_by(category=category).filter_by(name=item_name).first()
	creator = getUserInfo(item.user_id)
	
	if ( 'username' not in login_session ) or ( ('email' in login_session ) and (login_session['email'] != creator.email ) ):
		''' if user is not logged in or the logged in user is not same as the creator of the item, show public version '''
		return render_template('publicshowItem.html', item=item)
	else:
		print(login_session, creator.id)
		return render_template('showItem.html', item=item, creator=creator)


@app.route('/catalog/<string:category_name>/<string:item_name>/edit/', methods=['POST','GET'])
def editItem(category_name, item_name):
	if 'username' not in login_session:
		return redirect('/login')


	item = session.query(SportItem).filter_by(name=item_name).one()
	if request.method == 'GET':
		return render_template('editItem.html', item=item, categories=categories, category_name=category_name, item_name=item_name)
	else:
		item.name = request.form['name']
		item.description = request.form['description']
		category = session.query(Category).filter_by(name=str(request.form.get('categoryname'))).one()
		item.category = category
		session.add(item)
		session.commit()
		return redirect(url_for('showCategoryItems', category_name=category_name))	


@app.route('/catalog/<string:category_name>/<string:item_name>/delete/', methods=['POST','GET'])
def deleteItem(category_name, item_name):
	if 'username' not in login_session:
		return redirect('/login')
		
	item = session.query(SportItem).filter_by(name=item_name).first()	
	if request.method == 'GET':
		return render_template('deleteItem.html', item_name=item.name, category_name=category_name)
	else:
		session.delete(item)
		session.commit()
		return redirect(url_for('showCategoryItems', category_name=category_name))

if __name__ == '__main__':

    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)