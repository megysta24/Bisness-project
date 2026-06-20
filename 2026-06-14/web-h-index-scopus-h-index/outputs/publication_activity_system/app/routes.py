from sqlalchemy import func, or_
from werkzeug.security import generate_password_hash

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import (
    CitingPublication,
    IndexingSource,
    Publication,
    PublicationType,
    Teacher,
    User,
    citation_links,
    publication_authors,
)

main_bp = Blueprint("main", __name__)


def require_admin():
    if not current_user.can_manage_users():
        abort(403)


def can_edit_teacher(teacher_id):
    return current_user.can_edit_all_content() or current_user.teacher_id == teacher_id


def can_edit_publication(publication):
    if current_user.can_edit_all_content():
        return True
    return any(author.id == current_user.teacher_id for author in publication.authors)


@main_bp.route("/")
@login_required
def dashboard():
    teacher_count = Teacher.query.count()
    publication_count = Publication.query.count()
    citation_count = db.session.query(citation_links).count()
    latest_publications = Publication.query.order_by(Publication.publication_year.desc()).limit(5).all()
    return render_template(
        "dashboard.html",
        teacher_count=teacher_count,
        publication_count=publication_count,
        citation_count=citation_count,
        latest_publications=latest_publications,
    )


@main_bp.route("/teachers")
@login_required
def teachers():
    q = request.args.get("q", "").strip()
    query = Teacher.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Teacher.first_name.like(like),
                Teacher.middle_name.like(like),
                Teacher.last_name.like(like),
                Teacher.academic_position.like(like),
            )
        )
    return render_template("teachers.html", teachers=query.order_by(Teacher.last_name).all(), q=q)


@main_bp.route("/teachers/new", methods=["GET", "POST"])
@login_required
def teacher_new():
    if not current_user.can_edit_all_content():
        abort(403)
    if request.method == "POST":
        teacher = Teacher(
            first_name=request.form["first_name"],
            middle_name=request.form["middle_name"],
            last_name=request.form["last_name"],
            academic_position=request.form["academic_position"],
            scientific_degree=request.form["scientific_degree"],
            h_index_scopus=int(request.form.get("h_index_scopus") or 0),
            h_index_wos=int(request.form.get("h_index_wos") or 0),
        )
        db.session.add(teacher)
        db.session.commit()
        flash("Преподавателят е добавен.", "success")
        return redirect(url_for("main.teachers"))
    return render_template("teacher_form.html", teacher=None)


@main_bp.route("/teachers/<int:teacher_id>/edit", methods=["GET", "POST"])
@login_required
def teacher_edit(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    if not can_edit_teacher(teacher.id):
        abort(403)
    if request.method == "POST":
        teacher.first_name = request.form["first_name"]
        teacher.middle_name = request.form["middle_name"]
        teacher.last_name = request.form["last_name"]
        teacher.academic_position = request.form["academic_position"]
        teacher.scientific_degree = request.form["scientific_degree"]
        teacher.h_index_scopus = int(request.form.get("h_index_scopus") or 0)
        teacher.h_index_wos = int(request.form.get("h_index_wos") or 0)
        db.session.commit()
        flash("Данните са обновени.", "success")
        return redirect(url_for("main.teachers"))
    return render_template("teacher_form.html", teacher=teacher)


@main_bp.route("/teachers/<int:teacher_id>/delete", methods=["POST"])
@login_required
def teacher_delete(teacher_id):
    if not current_user.can_edit_all_content():
        abort(403)
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    flash("Преподавателят е изтрит.", "success")
    return redirect(url_for("main.teachers"))


@main_bp.route("/publications")
@login_required
def publications():
    q = request.args.get("q", "").strip()
    query = Publication.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Publication.title.like(like), Publication.venue.like(like), Publication.doi.like(like)))
    return render_template("publications.html", publications=query.order_by(Publication.publication_year.desc()).all(), q=q)


def fill_publication_from_form(publication):
    publication.title = request.form["title"]
    publication.venue = request.form["venue"]
    publication.publication_year = int(request.form["publication_year"])
    publication.publication_type_id = int(request.form["publication_type_id"])
    publication.isbn_issn = request.form.get("isbn_issn") or None
    publication.doi = request.form.get("doi") or None
    author_ids = [int(x) for x in request.form.getlist("author_ids")]
    indexing_ids = [int(x) for x in request.form.getlist("indexing_ids")]
    publication.authors = Teacher.query.filter(Teacher.id.in_(author_ids)).all() if author_ids else []
    publication.indexing_sources = IndexingSource.query.filter(IndexingSource.id.in_(indexing_ids)).all() if indexing_ids else []


@main_bp.route("/publications/new", methods=["GET", "POST"])
@login_required
def publication_new():
    if request.method == "POST":
        publication = Publication(title="", venue="", publication_year=2026, publication_type_id=1)
        fill_publication_from_form(publication)
        if not publication.authors:
            flash("Изберете поне един автор от департамента.", "error")
        elif not current_user.can_edit_all_content() and current_user.teacher_id not in [a.id for a in publication.authors]:
            abort(403)
        else:
            db.session.add(publication)
            db.session.commit()
            flash("Публикацията е добавена.", "success")
            return redirect(url_for("main.publications"))
    return render_template("publication_form.html", publication=None, teachers=Teacher.query.all(), types=PublicationType.query.all(), indexes=IndexingSource.query.all())


@main_bp.route("/publications/<int:publication_id>/edit", methods=["GET", "POST"])
@login_required
def publication_edit(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    if not can_edit_publication(publication):
        abort(403)
    if request.method == "POST":
        fill_publication_from_form(publication)
        if not current_user.can_edit_all_content() and current_user.teacher_id not in [a.id for a in publication.authors]:
            abort(403)
        db.session.commit()
        flash("Публикацията е обновена.", "success")
        return redirect(url_for("main.publications"))
    return render_template("publication_form.html", publication=publication, teachers=Teacher.query.all(), types=PublicationType.query.all(), indexes=IndexingSource.query.all())


@main_bp.route("/publications/<int:publication_id>/delete", methods=["POST"])
@login_required
def publication_delete(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    if not can_edit_publication(publication):
        abort(403)
    db.session.delete(publication)
    db.session.commit()
    flash("Публикацията е изтрита.", "success")
    return redirect(url_for("main.publications"))


@main_bp.route("/citations")
@login_required
def citations():
    items = CitingPublication.query.order_by(CitingPublication.publication_year.desc()).all()
    return render_template("citations.html", citations=items)


@main_bp.route("/citations/new", methods=["GET", "POST"])
@login_required
def citation_new():
    if not current_user.can_edit_all_content():
        abort(403)
    if request.method == "POST":
        citation = CitingPublication(
            title=request.form["title"],
            authors_text=request.form["authors_text"],
            venue=request.form["venue"],
            publication_year=int(request.form["publication_year"]),
            publication_type_id=int(request.form["publication_type_id"]),
            isbn_issn=request.form.get("isbn_issn") or None,
            doi=request.form.get("doi") or None,
        )
        publication_ids = [int(x) for x in request.form.getlist("publication_ids")]
        citation.cited_publications = Publication.query.filter(Publication.id.in_(publication_ids)).all()
        db.session.add(citation)
        db.session.commit()
        flash("Цитиращата публикация е добавена.", "success")
        return redirect(url_for("main.citations"))
    return render_template("citation_form.html", citation=None, types=PublicationType.query.all(), publications=Publication.query.all())


@main_bp.route("/citations/<int:citation_id>/edit", methods=["GET", "POST"])
@login_required
def citation_edit(citation_id):
    if not current_user.can_edit_all_content():
        abort(403)
    citation = CitingPublication.query.get_or_404(citation_id)
    if request.method == "POST":
        citation.title = request.form["title"]
        citation.authors_text = request.form["authors_text"]
        citation.venue = request.form["venue"]
        citation.publication_year = int(request.form["publication_year"])
        citation.publication_type_id = int(request.form["publication_type_id"])
        citation.isbn_issn = request.form.get("isbn_issn") or None
        citation.doi = request.form.get("doi") or None
        publication_ids = [int(x) for x in request.form.getlist("publication_ids")]
        citation.cited_publications = Publication.query.filter(Publication.id.in_(publication_ids)).all()
        db.session.commit()
        flash("Цитиращата публикация е обновена.", "success")
        return redirect(url_for("main.citations"))
    return render_template("citation_form.html", citation=citation, types=PublicationType.query.all(), publications=Publication.query.all())


@main_bp.route("/citations/<int:citation_id>/delete", methods=["POST"])
@login_required
def citation_delete(citation_id):
    if not current_user.can_edit_all_content():
        abort(403)
    citation = CitingPublication.query.get_or_404(citation_id)
    db.session.delete(citation)
    db.session.commit()
    flash("Цитиращата публикация е изтрита.", "success")
    return redirect(url_for("main.citations"))


@main_bp.route("/reports")
@login_required
def reports():
    rows = (
        db.session.query(
            Teacher,
            func.count(func.distinct(Publication.id)).label("publications_count"),
            func.count(citation_links.c.citing_publication_id).label("citations_count"),
        )
        .outerjoin(publication_authors, Teacher.id == publication_authors.c.teacher_id)
        .outerjoin(Publication, Publication.id == publication_authors.c.publication_id)
        .outerjoin(citation_links, Publication.id == citation_links.c.publication_id)
        .group_by(Teacher.id)
        .order_by(Teacher.last_name)
        .all()
    )
    totals = {
        "teachers": Teacher.query.count(),
        "publications": Publication.query.count(),
        "citations": db.session.query(citation_links).count(),
    }
    return render_template("reports.html", rows=rows, totals=totals)


@main_bp.route("/users")
@login_required
def users():
    require_admin()
    return render_template("users.html", users=User.query.order_by(User.email).all())


@main_bp.route("/users/new", methods=["GET", "POST"])
@login_required
def user_new():
    require_admin()
    if request.method == "POST":
        user = User(
            email=request.form["email"].strip().lower(),
            password_hash=generate_password_hash(request.form["password"]),
            role=request.form["role"],
            teacher_id=int(request.form["teacher_id"]) if request.form.get("teacher_id") else None,
            is_active_flag=bool(request.form.get("is_active_flag")),
        )
        db.session.add(user)
        db.session.commit()
        flash("Потребителят е добавен.", "success")
        return redirect(url_for("main.users"))
    return render_template("user_form.html", user=None, teachers=Teacher.query.all())


@main_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def user_edit(user_id):
    require_admin()
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.email = request.form["email"].strip().lower()
        if request.form.get("password"):
            user.password_hash = generate_password_hash(request.form["password"])
        user.role = request.form["role"]
        user.teacher_id = int(request.form["teacher_id"]) if request.form.get("teacher_id") else None
        user.is_active_flag = bool(request.form.get("is_active_flag"))
        db.session.commit()
        flash("Потребителят е обновен.", "success")
        return redirect(url_for("main.users"))
    return render_template("user_form.html", user=user, teachers=Teacher.query.all())


@main_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def user_delete(user_id):
    require_admin()
    if user_id == current_user.id:
        flash("Не можете да изтриете текущия потребител.", "error")
        return redirect(url_for("main.users"))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Потребителят е изтрит.", "success")
    return redirect(url_for("main.users"))
