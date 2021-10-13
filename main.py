from flask_login import login_required, current_user
from flask import Blueprint, render_template
from .models import ArtistID

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    id_count = ArtistID.query.filter_by(user_id=current_user.id).count()
    return render_template("profile.html", name=current_user.name, count=id_count)
