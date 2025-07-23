from flask import Blueprint, render_template, request, redirect, abort, flash, url_for
from .models import db, URL, generate_short_id

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        custom_alias = request.form.get('custom_alias') or None

        # If a custom alias is provided, ensure it's unique and valid
        if custom_alias:
            existing_alias = URL.query.filter_by(short_id=custom_alias).first()
            if existing_alias:
                flash(f"Alias '{custom_alias}' is already taken. Please choose another.", 'danger')
                return render_template('index.html')
            short_id = custom_alias
        else:
            # generate a random one
            short_id = generate_short_id()
            while URL.query.filter_by(short_id=short_id).first() is not None:
                short_id = generate_short_id()

        # Save (or re‑use) the mapping
        existing = URL.query.filter_by(original_url=original_url).first()
        if existing and not custom_alias:
            short_id = existing.short_id
        else:
            new_url = URL(original_url=original_url, short_id=short_id)
            db.session.add(new_url)
            db.session.commit()

        short_url = url_for('main.redirect_short_url', short_id=short_id, _external=True)
        return render_template('result.html', short_url=short_url)

    return render_template('index.html')


@main.route('/<short_id>')
def redirect_short_url(short_id):
    url = URL.query.filter_by(short_id=short_id).first()
    if url:
        return redirect(url.original_url)
    return abort(404)
