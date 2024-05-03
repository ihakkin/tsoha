from flask import session, flash, redirect, render_template, request, url_for, jsonify
import folium
from app import app
import users
import parks
import reviews
import groups



@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = None
    markers = parks.get_coordinates()
    if request.method == 'POST' and request.form:
        has_separate_areas = 'has_separate_areas' in request.form
        has_entrance_area = 'has_entrance_area' in request.form
        has_beach = 'has_beach' in request.form
        search_results = parks.search(has_separate_areas, has_entrance_area, has_beach)
        if search_results:
            markers = search_results
        else:
            flash('Haku ei tuottanut yhtään tulosta', 'error')
    map = build_map(markers)
    ranking = reviews.get_ranking()
    return render_template('index.html', markers=markers, search_results=search_results, ranking=ranking)

def build_map(markers):
    map = folium.Map(location=[60.1799, 24.9684], width='100%', height=600, zoom_start=13)
    for park in markers:
        popup_content = f"<a href='/park/{park['id']}'>{park['name']}</a>"
        folium.Marker([park['latitude'], park['longitude']], popup=popup_content).add_to(map)
    map.save('templates/map.html')
    return map


@app.route('/park/<int:park_id>')
def park_details(park_id):
    park_info = parks.get_park_details(park_id)
    if park_info:
        review = reviews.get_reviews_for_park(park_id)
        return render_template('park_details.html', park_id=park_id, park_info=park_info, review=review)
    return 'Puistoa ei löytynyt'


@app.route('/park/<int:park_id>', methods=['POST'])
def submit_review_route(park_id):
    users.check_csrf()
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    park_info = parks.get_park_details(park_id)
    review= reviews.get_reviews_for_park(park_id)
    stars = request.form['rating']
    comment = request.form['comment']
    if len(comment) > 1000:
        flash('Kommentti on liian pitkä', 'error')
        return render_template('park_details.html', park_id=park_id, park_info=park_info, review=review, rating=stars, comment=comment)
    if reviews.submit_review(user_id, park_id, stars, comment):
        flash('Kiitos arviostasi!', 'success')
    return redirect(url_for('park_details', park_id=park_id))


@app.route('/delete-review/<int:review_id>/<int:park_id>', methods=['POST'])
def delete_review_route(review_id, park_id):
    users.check_csrf()
    if session.get('user_role') != 2:
        flash('Sinulla ei ole oikeuksia suorittaa tätä toimintoa.', 'error')
        return redirect(url_for('index'))
    if reviews.delete_review(review_id):
        flash('Arvio on poistettu onnistuneesti.', 'success')
    else:
        flash('Arvion poistaminen epäonnistui.', 'error')
    return redirect(url_for('park_details', park_id=park_id))


@app.route('/groups')
def show_groups():
    group_data = groups.get_groups()
    parks_data = groups.get_all_parks()
    return render_template('groups.html', groups=group_data, parks=parks_data)
   

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
        return render_template('groups.html', name=name, description=description)
    if groups.add_group_to_db(name, description):
        flash('Ryhmä lisätty onnistuneesti.', 'success')
    else:
        flash('Ryhmän lisääminen epäonnistui.', 'error')
        return render_template('groups.html', name=name, description=description)
    return redirect(url_for('show_groups'))


@app.route('/add-park-to-group', methods=['POST'])
def add_park_to_group():
    if session.get('user_role') != 2:
        flash('Sinulla ei ole oikeuksia suorittaa tätä toimintoa.', 'error')
        return redirect(url_for('show_groups'))
    if request.method == 'POST':
        users.check_csrf()
        park_id = request.form.get('park_id')
        group_id = request.form.get('group_id')
        if groups.add_park_to_group(park_id, group_id):
            flash('Puisto lisätty ryhmään onnistuneesti!', 'success')
        else:
            flash('Puiston lisääminen ryhmään epäonnistui.', 'error')
        return redirect(url_for('show_groups'))
   

@app.route('/add_park', methods=['GET', 'POST'])
def add_park_route():
    if request.method == 'POST':
        users.check_csrf()
        if session.get('user_role') != 2:
            flash('Sinulla ei ole oikeuksia suorittaa tätä toimintoa.', 'error')
            return redirect(url_for('index'))
        name = request.form['name']
        street = request.form['street']
        postal_code = request.form['postal_code']
        city = request.form['city']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        has_separate_areas = 'has_separate_areas' in request.form
        has_entrance_area = 'has_entrance_area' in request.form
        has_beach = 'has_beach' in request.form
        if len(name) > 50 or len(street) > 50 or len(city) > 50:
            flash ('Syöte on liian pitkä', 'error')
        elif not postal_code.isdigit() or len(postal_code) != 5:
            flash ('Postinumeron on oltava viisinumeroinen.', 'error')
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                flash('Tarkista koordinaattien arvot.', 'error')
        except ValueError:
            flash('Leveys- ja pituusasteen on oltava numeerisia arvoja. Käytä pistettä desimaalipilkun sijaan', 'error')
            return render_template('add_park.html', 
                                   name=name, street=street, postal_code=postal_code,
                                   city=city, latitude=latitude, longitude=longitude,
                                   has_separate_areas=has_separate_areas,
                                   has_entrance_area=has_entrance_area,
                                   has_beach=has_beach)
        success, message = parks.add_park(name, has_separate_areas, has_entrance_area, has_beach,
                                          street, postal_code, city, latitude, longitude)
        if not success:
            flash(message or 'Koirapuiston lisääminen epäonnistui. Tarkista tiedot ja yritä uudelleen.', 'error')
            return render_template('add_park.html', 
                                   name=name, street=street, postal_code=postal_code,
                                   city=city, latitude=latitude, longitude=longitude,
                                   has_separate_areas=has_separate_areas,
                                   has_entrance_area=has_entrance_area,
                                   has_beach=has_beach)
        flash('Koirapuisto lisätty onnistuneesti!', 'success')
        return redirect(url_for('index'))
    return render_template('add_park.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Kirjautuminen ei onnistunut. Tarkista käyttäjätunnus ja salasana.', 'error')
            return render_template('login.html', username=username)
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
    else:
        flash("Rekisteröinti onnistui!", 'success')
        return redirect(url_for('index'))
    flash(error_message, 'error')
    return render_template('register.html', username=username, role=role, password1=password1, password2=password2)
