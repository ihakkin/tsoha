from sqlalchemy.sql import text
from sqlalchemy import exc
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
    except exc.SQLAlchemyError:
        return False
    return True

def get_all_parks():
    sql = "SELECT id, name FROM parks ORDER BY name"
    return db.session.execute(text(sql)).fetchall()
    
    
def add_park_to_group(park_id, group_id):
    try:
        sql = """INSERT INTO park_groups (park_id, group_id) VALUES (:park_id, :group_id)"""
        db.session.execute(text(sql), {'park_id': park_id, 'group_id': group_id})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False