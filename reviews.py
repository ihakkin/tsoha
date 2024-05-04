from flask import session
from sqlalchemy.sql import text
from sqlalchemy import exc
from db import db

def submit_review(user_id, park_id, stars, comment):
    if 'user_id' not in session or session['user_id'] != user_id:
        return False, 'Vain kirjautuneet käyttäjät voivat jättää arvosteluja.'
    try:
        sql = """INSERT INTO reviews (user_id, park_id, stars, comment)
        VALUES (:user_id, :park_id, :stars, :comment)"""
        db.session.execute(text(sql), {
            "user_id": user_id,
            "park_id": park_id,
            "stars": stars,
            "comment": comment
            })
        db.session.commit()
    except exc.SQLAlchemyError:
        return False
    return True

def get_reviews_for_park(park_id):
    sql = """SELECT r.id, r.stars, r.comment, u.username FROM reviews r
    JOIN users u ON r.user_id = u.id WHERE r.park_id = :park_id"""
    return db.session.execute(text(sql), {'park_id': park_id}).fetchall()

def get_review(user_id, park_id):
    sql = """SELECT stars, comment FROM reviews WHERE user_id=:user_id AND course_id=:course_id"""
    return db.session.execute(text(sql), {'user_id': user_id, 'course_id': park_id}).fetchone()

def get_ranking():
    sql =  """SELECT p.id, p.name, AVG(r.stars) AS average_rating FROM reviews r
    JOIN parks p ON p.id = r.park_id GROUP BY p.id, p.name ORDER BY average_rating DESC LIMIT 5"""
    return db.session.execute(text(sql)).fetchall()

def delete_review(review_id):
    try:
        sql = """DELETE FROM reviews WHERE id = :review_id"""
        db.session.execute(text(sql), {'review_id': review_id})
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        return False
