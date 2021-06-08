import os
import json
import datetime
import subprocess

from app import app, db
from app.models import User, ScraperCategory
from app.forms import LoginForm, EditCategoryForm
from app.modules.categories import LoadCategories, CompareCategories
from app.modules.external_categories import GetExternalCategories, WriteExternalCategories, LoadExternalCategories
from flask import send_file, render_template, redirect, url_for, jsonify, Response, request
from flask_login import current_user, login_user, logout_user, login_required


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("User: ", user, flush=True)
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)


@app.route("/view_available_categories")
@login_required
def view_available_categories():
    return None


@app.route("/refresh_external_categories")
@login_required
def refresh_external_categories():
    WriteExternalCategories(
        categories=GetExternalCategories().categories
    )
    return jsonify(status="success")


@app.route("/view_categories/<shop>")
@login_required
def view_categories(shop):
    categories = LoadCategories(shop).categories
    return render_template(
        "view_categories.html", shop_name=shop, categories=categories
    )


@app.route("/edit_categories/<shop>", methods=["GET", "POST"])
@login_required
def edit_categories(shop):
    print(request, flush=True)
    form = EditCategoryForm()
    cat_name = form.data["cat_name"]
    cat_link = form.data["cat_link"]
    print(form.data, flush=True)

    categories = LoadCategories(shop).categories

    if request.method == "POST":
        category_to_change = ScraperCategory.query.filter_by(cat_link=cat_link).first()
        category_to_change.cat_name = cat_name
        category_to_change.cat_id = CompareCategories(
            keyword=cat_name.split(" (", 1)[0].strip()
        ).cat_id

        db.session.commit()

    return render_template(
        "edit_categories.html",
        shop_name=shop,
        categories=categories,
        form=form,
    )


@app.route("/_autocomplete", methods=["GET"])
def autocomplete():
    category_names = []
    categories = LoadExternalCategories().categories
    for c in categories:
        category_names.append(
            f'{c["name"]} ({c["name_ru"]}) Parent: {c["parent_name"]} ({c["parent_name_ru"]})'
        )

    return Response(json.dumps(category_names, ensure_ascii=False), mimetype="application/json")


@app.route("/raeder")
@login_required
def raeder_page():
    return render_template("raeder.html", shop_name="raeder")


@app.route("/bonami")
@login_required
def bonami_page():
    return render_template("bonami.html", shop_name="bonami")


@app.route("/tescoma")
@login_required
def tescoma_page():
    return render_template("tescoma.html", shop_name="tescoma")


@app.route("/zara_home")
@login_required
def zara_home_page():
    return render_template("zara_home.html", shop_name="zara_home")


@app.route("/zara")
@login_required
def zara_page():
    return render_template("zara.html", shop_name="zara")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/v1/images/<shop_id>/<image_name>")
def send_picture_r(shop_id, image_name):
    return send_file(f"./files/pics/{shop_id}/{image_name}")


@app.route("/start_scraper", methods=["GET"])
@login_required
def start_scraper():
    print(datetime.datetime.now(), flush=True)
    print(request, flush=True)

    shop = request.args.get("shop")
    update = int(request.args.get("update"))

    if shop is None:
        return jsonify(status="error", msg="shop argument is None")
    if update is None:
        return jsonify(status="error", msg="update argument is None")

    subprocess.Popen(f"python3 ./scrapers/{shop}/{shop}.py")

    return jsonify(status="success", msg=f"{shop} has been launched")


@app.route("/stop_scraper", methods=["GET"])
@login_required
def stop_scraper():
    print(datetime.datetime.now(), flush=True)
    print(request)

    shop = request.args.get("shop")

    if shop is None:
        return jsonify(status="error", msg="shop argument is None")

    os.system(f"killall {shop}")

    return jsonify(status="success", msg=f"{shop} has been stopped")
