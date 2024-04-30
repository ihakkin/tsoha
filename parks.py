from sqlalchemy.sql import text
from db import db


def get_coordinates():
    sql = """SELECT p.id, p.name, a.latitude, a.longitude FROM parks p
               JOIN address a ON p.id = a.park_id"""
    result = db.session.execute(text(sql))
    parks_list = result.fetchall()
    park_coordinates = [
        {
            'id': park[0],
            'name': park[1],
            'latitude': park[2],
            'longitude': park[3]
        }
        for park in parks_list
    ]
    return park_coordinates


def search(has_separate_areas, has_entrance_area, has_beach):
    base_query = """
    SELECT p.id, p.name, a.latitude, a.longitude
    FROM parks p
    JOIN address a ON p.id = a.park_id
    """
    conditions = []
    if has_separate_areas:
        conditions.append("p.has_separate_areas = true")
    if has_entrance_area:
        conditions.append("p.has_entrance_area = true")
    if has_beach:
        conditions.append("p.has_beach = true")
    condition_str = " AND ".join(conditions) if conditions else "1=1"
    final_query = f"{base_query} WHERE {condition_str}"
    result = db.session.execute(text(final_query))
    return [
        {
            'id': park.id,
            'name': park.name,
            'latitude': park.latitude,
            'longitude': park.longitude
        }
        for park in result.fetchall()
    ]


def get_park_details(park_id):
    sql = """SELECT p.id, p.name, a.street, a.postal_code, a.city,
               p.has_separate_areas, p.has_entrance_area, p.has_beach FROM parks p
               JOIN address a ON p.id = a.park_id WHERE p.id = :park_id"""
    result = db.session.execute(text(sql), {'park_id': park_id})
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
    return None
    