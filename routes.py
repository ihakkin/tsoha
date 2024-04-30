from flask import session, flash, redirect, render_template, request, url_for, jsonify
from sqlalchemy.sql import text
import folium
from app import app
import users
import parks
import reviews
import groups


@app.route('/', methods=['GET', 'POST'])
def index():
    park_coordinates = parks.get_coordinates()
    search_results = None
    search_attempted = False
    if request.method == 'POST' and request.form:
        search_attempted = True
        has_separate_areas = 'has_separate_areas' in request.form
        has_entrance_area = 'has_entrance_area' in request.form
        has_beach = 'has_beach' in request.form
        search_results = parks.search(has_separate_areas, has_entrance_area, has_beach)
    if search_results:
        markers = search_results
    else:
        markers = park_coordinates
        if search_attempted:
            flash('Haku ei tuottanut yhtään tulosta', 'error')
    map = folium.Map(location=[60.1799, 24.9684], width='100%', height=600, zoom_start=13)
    for park in markers:
        popup_content = f"<a href='/park/{park['id']}'>{park['name']}</a>"
        folium.Marker(
            [park['latitude'], park['longitude']],
            popup=popup_content
        ).add_to(map)
    map.save('templates/map.html')
    ranking = reviews.get_ranking()
    return render_template('index.html', park_coordinates=park_coordinates, search_results=search_results, ranking=ranking)


@app.route('/park/<int:park_id>')
def park_details(park_id):
    park_info = parks.get_park_details(park_id)
    if park_info:
        review = reviews.get_reviews_for_park(park_id)
        return render_template('park_details.html', park_id=park_id, park_info=park_info, review=review)
    return 'Puistoa ei löytynyt'


@app.route('/park/<int:park_id>', methods=['POST'])
def submit_review_route(park_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    stars = request.form['rating']
    comment = request.form['comment']
    if len(comment) > 1000:
        flash('Kommentti on liian pitkä', 'error')
        return redirect(url_for('park_details', park_id=park_id))
    users.check_csrf()
    success, message = reviews.submit_review(user_id, park_id, stars, comment)
    if not success:
        flash(message, 'error')
        return redirect(url_for('park_details', park_id=park_id))
    flash('Kiitos arviostasi!', 'success')
    return redirect(url_for('park_details', park_id=park_id))


@app.route('/delete-review/<int:review_id>/<int:park_id>', methods=['POST'])
def delete_review_route(review_id, park_id):
    users.check_csrf()
    if session.get('user_role') != 2:
        flash('Sinulla ei ole oikeuksia suorittaa tätä toimintoa.', 'error')
        return redirect(url_for('index'))
    try:
        reviews.delete_review(review_id)
        flash('Arvio on poistettu onnistuneesti.', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('park_details', park_id=park_id))


@app.route('/groups')
def show_groups():
    group_data = groups.get_groups()
    return render_template('groups.html', groups=group_data)


@app.route('/get-parks/<int:group_id>')
def get_park_groups(group_id):
    parks_by_groups = groups.get_parks_by_group(group_id)
    park_groups = [row._asdict() for row in parks_by_groups]
    return jsonify({'park_groups': park_groups})


@app.route('/add-group', methods=['POST'])
def add_group():
    users.check_csrf()
    if session.get('user_role') != 2:
        flash('Sinulla ei ole oikeuksia suorittaa tätä toimintoa.', 'error')
        return redirect(url_for('groups'))
    name = request.form.get('name')
    description = request.form.get('description')
    if not name or not description:
        flash('Nimi ja kuvaus ovat pakollisia.', 'error')
        return redirect(url_for('groups'))
    success, message = groups.add_group_to_db(name, description)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('show_groups'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not users.login(username, password):
            flash('Kirjautuminen ei onnistunut. Tarkista käyttäjätunnus ja salasana.', 'error')
            return redirect(url_for('login'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    role = request.form['role']
    error_message = None
    if len(username) < 1 or len(username) > 20:
        error_message = 'Käyttäjänimessä tulee olla 1-20 merkkiä'
    elif password1 != password2:
        error_message = 'Salasanat eroavat toisistaan, tarkista salasanan oikeinkirjoitus'
    elif password1 == '':
        error_message = 'Salasanakenttä on tyhjä'
    elif not users.register(username, password1, role):
        error_message = 'Rekisteröinti ei onnistunut. Käyttäjänimi on varattu.'
    if error_message:
        flash(error_message, 'error')
        return redirect(url_for('register'))
    flash("Rekisteröinti onnistui!", 'success')
    return redirect(url_for('index'))
    