import json

from app import app, db
from app.modules.plastic import ReadHostServices, ReadServicesDict, AssignCategory
from app.modules.beauty import ReadHostServicesBeauty, ReadServicesDictBeauty, AssignCategoryBeauty
from app.models import User, ScraperCategory, PlasticServices, BeautyServices
from app.forms import LoginForm, EditCategoryForm, EditService
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
    form = EditCategoryForm()
    cat_name = form.data["cat_name"]
    cat_link = form.data["cat_link"]
    print(form.data)

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


@app.route("/_autocomplete_plastic", methods=["GET"])
def autocomplete_plastic():
    services_names = []
    services = ReadHostServices().services
    for s in services:
        services_names.append(f'{s["service"]} ({s["type"]})')

    return Response(
        json.dumps(services_names, ensure_ascii=False), mimetype="application/json"
    )


@app.route("/_autocomplete_beauty", methods=["GET"])
def autocomplete_beauty():
    services_names = []
    services = ReadHostServicesBeauty().services
    for s in services:
        services_names.append(f'{s["service"]}')

    return Response(
        json.dumps(services_names, ensure_ascii=False), mimetype="application/json"
    )


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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/v1/images/<shop_id>/<image_name>")
def send_picture_r(shop_id, image_name):
    return send_file(f"./files/pics/{shop_id}/{image_name}")


@app.route("/plastic_surgery_categories", methods=["GET", "POST"])
@login_required
def plastic_surgery_categories():
    page = request.args.get("page", 1, type=int)

    services = PlasticServices.query.paginate(page, 25, False)
    next_url = url_for('plastic_surgery_categories', page=services.next_num) \
        if services.has_next else None
    prev_url = url_for('plastic_surgery_categories', page=services.prev_num) \
        if services.has_prev else None

    form = EditService()

    print(form.data)

    if request.method == "POST":
        AssignCategory(
            old_value=form.data["cat_to_change"], new_value=form.data["cat_name"]
        )

    return render_template(
        "plastic.html",
        form=form,
        services=services,
        page=page,
        next_url=next_url,
        prev_url=prev_url
    )


@app.route("/beauty_categories", methods=["GET", "POST"])
@login_required
def beauty_categories():
    page = request.args.get("page", 1, type=int)

    services = BeautyServices.query.paginate(page, 25, False)
    next_url = url_for('beauty_categories', page=services.next_num) \
        if services.has_next else None
    prev_url = url_for('beauty_categories', page=services.prev_num) \
        if services.has_prev else None

    form = EditService()

    print(form.data)

    if request.method == "POST":
        AssignCategoryBeauty(
            old_value=form.data["cat_to_change"], new_value=form.data["cat_name"]
        )

    return render_template(
        "beauty.html",
        form=form,
        services=services,
        page=page,
        next_url=next_url,
        prev_url=prev_url
    )