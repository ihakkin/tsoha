import os
from flask import session
from sqlalchemy.sql import text
from db import db

def submit_review(user_id, park_id, stars, comment):
    if 'user_id' not in session or session['user_id'] != user_id:
        return False, "Vain kirjautuneet käyttäjät voivat jättää arvosteluja."
    try:
        sql = "INSERT INTO reviews (user_id, park_id, stars, comment) VALUES (:user_id, :park_id, :stars, :comment)"
        db.session.execute(text(sql), {"user_id": user_id, "park_id": park_id, "stars": stars, "comment": comment})
        db.session.commit()
        return True, "Kiitos arviosta."
    except Exception as e:
        return False, str(e)

def get_reviews_for_park(park_id):
    sql = "SELECT r.stars, r.comment, u.username FROM reviews r JOIN users u ON r.user_id = u.id WHERE r.park_id = :park_id"
    review = db.session.execute(text(sql), {"park_id": park_id}).fetchall()
    return review