from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os
import csv
import io
from dotenv import load_dotenv

# Environment variables load karo .env file se
load_dotenv()

app = Flask(__name__)
# Secret key aur admin pin ko env se fetch karo, ya default fallback use karo
app.secret_key = os.environ.get('SECRET_KEY', 'nrega_vibe_secret_key')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload size

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

@app.route('/admin/download_backup')
@admin_required
def download_backup():
    db_path = os.path.join(instance_path, 'nrega_bookmarks.db')
    if os.path.exists(db_path):
        return send_file(db_path, as_attachment=True, download_name="nrega_bookmarks_backup.db")
    return "Database file not found!", 404


@app.route('/admin/export_bookmarks')
@admin_required
def export_bookmarks():
    """Saare categories aur links ek CSV file mein export karo."""
    categories = Category.query.order_by(Category.sort_order).all()

    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow([
        'category_name',
        'is_application',
        'sort_order',
        'title',
        'url',
        'icon_class',
        'is_dynamic'
    ])

    for cat in categories:
        for link in cat.links:
            writer.writerow([
                cat.name,
                '1' if cat.is_application else '0',
                cat.sort_order,
                link.title,
                link.url,
                link.icon_class or '',
                '1' if link.is_dynamic else '0'
            ])

    # Empty category bhi export karo (bina links ke)
    for cat in categories:
        if not cat.links:
            writer.writerow([
                cat.name,
                '1' if cat.is_application else '0',
                cat.sort_order,
                '',  # no link
                '',
                '',
                ''
            ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),  # utf-8-sig for Excel compatibility
        mimetype='text/csv',
        as_attachment=True,
        download_name='bookmarks_export.csv'
    )


@app.route('/admin/import_bookmarks', methods=['POST'])
@admin_required
def import_bookmarks():
    """CSV file se bookmarks import karo. Existing data replace nahi hogi — sirf naye add honge ya existing update honge."""
    if 'csv_file' not in request.files:
        flash('Koi file select nahi ki!', 'error')
        return redirect(url_for('admin'))

    file = request.files['csv_file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        flash('Sirf .csv file allowed hai!', 'error')
        return redirect(url_for('admin'))

    replace_all = request.form.get('replace_all') == 'on'

    try:
        stream = io.StringIO(file.stream.read().decode('utf-8-sig'))
        reader = csv.DictReader(stream)

        required_cols = {'category_name', 'title', 'url'}
        if not required_cols.issubset(set(reader.fieldnames or [])):
            flash(f'CSV mein ye columns hone chahiye: {", ".join(required_cols)}', 'error')
            return redirect(url_for('admin'))

        if replace_all:
            Link.query.delete()
            Category.query.delete()
            db.session.commit()

        added_cats = 0
        added_links = 0
        updated_links = 0

        # category cache taaki baar baar DB query na ho
        cat_cache = {}

        for row in reader:
            cat_name = row.get('category_name', '').strip()
            title = row.get('title', '').strip()
            url = row.get('url', '').strip()

            if not cat_name:
                continue  # category name mandatory hai

            # Category lookup / create
            if cat_name not in cat_cache:
                cat = Category.query.filter_by(name=cat_name).first()
                if not cat:
                    try:
                        sort_order = int(row.get('sort_order', 0))
                    except (ValueError, TypeError):
                        sort_order = 0
                    is_app = str(row.get('is_application', '0')).strip() in ('1', 'true', 'True', 'yes')
                    cat = Category(name=cat_name, is_application=is_app, sort_order=sort_order)
                    db.session.add(cat)
                    db.session.flush()  # id generate karo
                    added_cats += 1
                cat_cache[cat_name] = cat
            else:
                cat = cat_cache[cat_name]

            if not title or not url:
                continue  # link fields nahi hain, skip

            icon_class = row.get('icon_class', '').strip() or None
            try:
                is_dynamic = str(row.get('is_dynamic', '0')).strip() in ('1', 'true', 'True', 'yes')
            except Exception:
                is_dynamic = False

            # Existing link dhundo (same title + category)
            existing = Link.query.filter_by(title=title, category_id=cat.id).first()
            if existing:
                existing.url = url
                existing.icon_class = icon_class
                existing.is_dynamic = is_dynamic
                updated_links += 1
            else:
                new_link = Link(
                    title=title,
                    url=url,
                    icon_class=icon_class,
                    is_dynamic=is_dynamic,
                    category_id=cat.id
                )
                db.session.add(new_link)
                added_links += 1

        db.session.commit()
        flash(
            f'Import successful! {added_cats} new categories, {added_links} links added, {updated_links} links updated.',
            'success'
        )

    except Exception as e:
        db.session.rollback()
        flash(f'Import mein error aaya: {str(e)}', 'error')

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)