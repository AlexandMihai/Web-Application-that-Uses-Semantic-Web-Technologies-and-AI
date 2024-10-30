from flask import Blueprint, render_template, session
from .chat.routes import get_current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    user_id = get_current_user()
    is_logged_in = bool(user_id)
    if not is_logged_in:
        session.pop('chat_history', None)
    return render_template('main.html', is_logged_in=is_logged_in)