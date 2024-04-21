from db import db
from sqlalchemy.sql import text


def get_groups():
    sql = "SELECT id, name, description FROM groups ORDER BY name"
    return db.session.execute(text(sql)).fetchall()

def get_parks_by_group(group_id):
    sql = "SELECT p.id, p.name FROM parks p JOIN park_groups pg ON p.id = pg.park_id WHERE pg.group_id = :group_id"
    return db.session.execute(text(sql), {'group_id': group_id}).fetchall()
