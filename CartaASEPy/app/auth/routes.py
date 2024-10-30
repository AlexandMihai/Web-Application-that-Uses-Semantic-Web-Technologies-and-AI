from flask import Blueprint, request, jsonify, render_template, session
from flask_jwt_extended import create_access_token, unset_jwt_cookies
import bcrypt
from ..database import get_db

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    return render_template('login.html')

@bp.route('/loginprocess', methods=['POST'])
def login_process():
    data = request.json
    credential = data['username']
    password = data['password']
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, username, email, password FROM users WHERE username=%s OR email=%s", (credential, credential))
    result = cur.fetchone()

    if result and bcrypt.checkpw(password.encode('utf-8'), result[3].encode('utf-8')):
        user_id = result[0]
        access_token = create_access_token(identity=user_id)
        session['chat_history'] = []
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"status": "error", "message": "Invalid username/email or password!"}), 401


@bp.route('/logout')
def logout():
    response = jsonify({"msg": "You have been logged out."})
    session.pop('chat_history', None)
    unset_jwt_cookies(response)
    return response

@bp.route('/signup')
def signup():
    return render_template('signup.html')

@bp.route('/signupprocess', methods=['POST'])
def signup_process():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        db.commit()
        return jsonify({"status": "success", "message": "Account created successfully!"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@bp.route('/password_reset')
def password_reset():
    return render_template('password_reset.html')

@bp.route('/password_change')
def password_change():
    return render_template('password_change.html')

@bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    from ..mail import send_reset_email
    from datetime import datetime, timedelta
    import random
    import string

    data = request.json
    user_email = data['email']
    reset_code = ''.join(random.choices(string.digits, k=6))
    token_expiration = datetime.utcnow() + timedelta(minutes=15)
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE users SET reset_token=%s, token_expiration=%s WHERE email=%s", (reset_code, token_expiration, user_email))
    db.commit()
    send_reset_email(user_email, reset_code)
    return jsonify({"status": "success", "message": "Email sent"})

@bp.route('/reset_and_change_password', methods=['POST'])
def reset_and_change_password():
    from datetime import datetime
    data = request.json
    user_code = data['code']
    new_password = data['password']
    current_time = datetime.utcnow()
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT email, token_expiration FROM users WHERE reset_token=%s", (user_code,))
    user = cur.fetchone()
    if user and user[1] > current_time:
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_password, user[0]))
        db.commit()
        return jsonify({"status": "success", "message": "Password updated successfully."}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid or expired code."}), 400
