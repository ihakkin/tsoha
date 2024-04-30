from sqlalchemy.sql import text
from db import db



def get_groups():
    sql = """SELECT id, name, description FROM groups ORDER BY name"""
    return db.session.execute(text(sql)).fetchall()

def get_parks_by_group(group_id):
    sql = """SELECT p.id, p.name FROM parks p JOIN park_groups pg ON p.id = pg.park_id
    WHERE pg.group_id = :group_id"""
    return db.session.execute(text(sql), {'group_id': group_id}).fetchall()

def add_group_to_db(name, description):
    try:
        sql = """INSERT INTO groups (name, description) VALUES (:name, :description)"""
        db.session.execute(text(sql), {'name': name, 'description': description})
        db.session.commit()
        return True, 'Ryhmä lisätty onnistuneesti.'
    except Exception as e:
        db.session.rollback()
        return False, f'Ryhmän lisääminen epäonnistui: {str(e)}'
    