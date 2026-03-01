from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os
from dotenv import load_dotenv

# Environment variables load karo .env file se
load_dotenv()

app = Flask(__name__)
# Secret key aur admin pin ko env se fetch karo, ya default fallback use karo
app.secret_key = os.environ.get('SECRET_KEY', 'nrega_vibe_secret_key') 

# --- SET YOUR ADMIN PIN IN A .env FILE ---
ADMIN_PIN = os.environ.get('ADMIN_PIN', '12345')

# --- FIX: Absolute Path for Database ---
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'nrega_bookmarks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nrega_code = db.Column(db.String(20), nullable=False)
    state_name = db.Column(db.String(50), default="JHARKHAND")
    state_code = db.Column(db.String(10), default="34")
    blocks = db.relationship('Block', backref='district', lazy=True)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nrega_code = db.Column(db.String(20), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_application = db.Column(db.Boolean, default=False) 
    sort_order = db.Column(db.Integer, default=0)
    links = db.relationship('Link', backref='category', lazy=True)

class BookmarkRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(800), nullable=False)
    suggested_category = db.Column(db.String(100), nullable=False)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(800), nullable=False) 
    icon_class = db.Column(db.String(100), nullable=True)
    is_dynamic = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(500), nullable=True)

with app.app_context():
    db.create_all()

# --- ADMIN DECORATOR ---
# Ye function check karega ki user logged in hai ya nahi
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- PUBLIC ROUTES ---
@app.route('/ads.txt')
def ads_txt():
    ad_code = "google.com, pub-7555042175718049, DIRECT, f08c47fec0942fa0"
    return ad_code, 200, {'Content-Type': 'text/plain'}

@app.route('/')
def index():
    categories = Category.query.order_by(Category.sort_order).all()
    apps = [c for c in categories if c.is_application]
    bookmarks = [c for c in categories if not c.is_application]
    districts = District.query.order_by(District.name).all()
    
    greeting_setting = Setting.query.filter_by(key='greeting_message').first()
    custom_greeting = greeting_setting.value if greeting_setting and greeting_setting.value else ""
    
    return render_template('index.html', apps=apps, bookmarks=bookmarks, districts=districts, custom_greeting=custom_greeting)

@app.route('/get_blocks/<int:district_id>')
def get_blocks(district_id):
    blocks = Block.query.filter_by(district_id=district_id).order_by(Block.name).all()
    block_list = [{'id': b.id, 'name': b.name, 'nrega_code': b.nrega_code} for b in blocks]
    return jsonify(block_list)

@app.route('/submit_request', methods=['POST'])
def submit_request():
    title = request.form.get('title')
    url = request.form.get('url')
    category = request.form.get('category')
    
    if title and url:
        new_req = BookmarkRequest(title=title, url=url, suggested_category=category)
        db.session.add(new_req)
        db.session.commit()
    return jsonify({"status": "success"})

# --- LOGIN / LOGOUT ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('pin') == ADMIN_PIN:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = "Incorrect PIN. Please try again."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# --- PROTECTED ADMIN ROUTES ---
@app.route('/admin')
@admin_required
def admin():
    categories = Category.query.order_by(Category.sort_order).all()
    links = Link.query.all()
    bookmark_requests = BookmarkRequest.query.all() 
    
    greeting_setting = Setting.query.filter_by(key='greeting_message').first()
    custom_greeting = greeting_setting.value if greeting_setting else ""
    
    return render_template('admin.html', categories=categories, links=links, requests=bookmark_requests, custom_greeting=custom_greeting)

@app.route('/admin/update_greeting', methods=['POST'])
@admin_required
def update_greeting():
    message = request.form.get('greeting_message')
    setting = Setting.query.filter_by(key='greeting_message').first()
    if not setting:
        setting = Setting(key='greeting_message', value=message)
        db.session.add(setting)
    else:
        setting.value = message
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/add_category', methods=['POST'])
@admin_required
def add_category():
    name = request.form.get('name')
    is_app = request.form.get('is_application') == 'on'
    sort_order = request.form.get('sort_order', 0, type=int)
    
    if name:
        new_cat = Category(name=name, is_application=is_app, sort_order=sort_order)
        db.session.add(new_cat)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete_category/<int:id>')
@admin_required
def delete_category(id):
    cat = Category.query.get(id)
    if cat:
        Link.query.filter_by(category_id=id).delete()
        db.session.delete(cat)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/add_link', methods=['POST'])
@admin_required
def add_link():
    title = request.form.get('title')
    url = request.form.get('url')
    icon = request.form.get('icon_class')
    category_id = request.form.get('category_id')
    is_dynamic = request.form.get('is_dynamic') == 'on'
    
    if title and url and category_id:
        new_link = Link(title=title, url=url, icon_class=icon, category_id=category_id, is_dynamic=is_dynamic)
        db.session.add(new_link)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/edit_link/<int:id>')
@admin_required
def edit_link(id):
    link = Link.query.get_or_404(id)
    categories = Category.query.order_by(Category.sort_order).all()
    return render_template('edit_link.html', link=link, categories=categories)

@app.route('/admin/update_link/<int:id>', methods=['POST'])
@admin_required
def update_link(id):
    link = Link.query.get_or_404(id)
    link.title = request.form.get('title')
    link.url = request.form.get('url')
    link.icon_class = request.form.get('icon_class')
    link.category_id = request.form.get('category_id')
    link.is_dynamic = request.form.get('is_dynamic') == 'on'
    
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete_link/<int:id>')
@admin_required
def delete_link(id):
    link = Link.query.get(id)
    if link:
        db.session.delete(link)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/approve_request/<int:req_id>', methods=['POST'])
@admin_required
def approve_request(req_id):
    req = BookmarkRequest.query.get(req_id)
    if req:
        cat_id = request.form.get('category_id')
        new_link = Link(title=req.title, url=req.url, icon_class='mdi mdi-link-variant', is_dynamic=False, category_id=cat_id)
        db.session.add(new_link)
        db.session.delete(req) 
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/delete_request/<int:req_id>')
@admin_required
def delete_request(req_id):
    req = BookmarkRequest.query.get(req_id)
    if req:
        db.session.delete(req)
        db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)