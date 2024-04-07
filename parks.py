from db import db 
from sqlalchemy.sql import text


def get_coordinates():
    sql = text("SELECT p.id, p.name, a.latitude, a.longitude FROM parks p JOIN address a ON p.id = a.park_id")
    result = db.session.execute(sql)
    parks_list = result.fetchall()
    
    park_coordinates = [{"id": park[0], "name": park[1], "latitude": park[2], "longitude": park[3]} for park in parks_list]
    return park_coordinates


def search(has_separate_areas, has_entrance_area, has_beach):
    base_query = "SELECT p.id, p.name, a.latitude, a.longitude FROM parks p JOIN address a ON p.id = a.park_id WHERE "
    conditions = []
    
    if has_separate_areas:
        conditions.append("p.has_separate_areas = true")
    if has_entrance_area:
        conditions.append("p.has_entrance_area = true")
    if has_beach:
        conditions.append("p.has_beach = true")
    if conditions:
        condition_str = " AND ".join(conditions)
        final_query = base_query + condition_str
    else:
        final_query = base_query + "1=1"  
    result = db.session.execute(text(final_query))
    search_list = result.fetchall()
    search_results = [{"id": park[0], "name": park[1], "latitude":park[2], "longitude": park[3]} for park in search_list]
    return search_results   


def get_park_details(park_id):
    sql = text("SELECT p.id, p.name, a.street, a.postal_code, a.city, p.has_separate_areas, p.has_entrance_area, p.has_beach " \
          "FROM parks p JOIN address a ON p.id = a.park_id WHERE p.id = :park_id")
    result = db.session.execute(sql, {'park_id': park_id})
    park_info = result.fetchone()

    if park_info:
        has_separate_areas = 'Kyllä' if park_info[5] else 'Ei'
        has_entrance_area = 'Kyllä' if park_info[6] else 'Ei'
        has_beach = 'Kyllä' if park_info[7] else 'Ei'

        return {
            'id': park_info[0],
            'name': park_info[1],
            'address': f"{park_info[2]}, {park_info[3]} {park_info[4]}",
            'features': {
                'Separate areas for small and big dogs': has_separate_areas,
                'Entrance area': has_entrance_area,
                'Dog beach': has_beach
            }
        }
    else:
        return None