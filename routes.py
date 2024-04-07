from app import app
from flask import redirect, render_template, request, url_for
from sqlalchemy.sql import text
import users
import folium
import parks
import reviews

@app.route("/", methods=["GET", "POST"])
def index():
    park_coordinates = parks.get_coordinates()
    search_results = None
    if request.method == "POST":
        has_separate_areas = 'has_separate_areas' in request.form
        has_entrance_area = 'has_entrance_area' in request.form
        has_beach = 'has_beach' in request.form
        search_results = parks.search(has_separate_areas, has_entrance_area, has_beach)

    m = folium.Map(location=[60.1799, 24.9384],  width='100%', height=600, zoom_start=13)
    for park in park_coordinates:
        popup_content = f"<a href='/park/{park['id']}'>{park['name']}</a>"
        folium.Marker(
            [park['latitude'], park['longitude']],
            popup=popup_content
        ).add_to(m)
    
    m.save("templates/map.html")
    return render_template("index.html", park_coordinates=park_coordinates, search_results=search_results)
 
 
@app.route('/park/<int:park_id>')
def park_details(park_id):
    park_info = parks.get_park_details(park_id)

    if park_info:
        review = reviews.get_reviews_for_park(park_id)
        return render_template('park_details.html', park_id=park_id, park_info=park_info, review=review)
    else:
        return "Puistoa ei löytynyt"


@app.route('/park/<int:park_id>/review', methods=['POST'])
def submit_review_route(park_id):
    user_id = reviews.session.get('user_id')
    if not user_id:
        return redirect(url_for('/')) 
    stars = request.form['rating']
    comment = request.form['comment']
    
    success, message = reviews.submit_review(user_id, park_id, stars, comment)
    if not success:
        return message  
    return redirect(url_for('park_details', park_id=park_id)) 
 

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")
    

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")
        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")
        if not users.register(username, password1, role):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
    
        return redirect("/")
    

