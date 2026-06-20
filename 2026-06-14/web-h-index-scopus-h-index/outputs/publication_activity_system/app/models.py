from flask_login import UserMixin
from werkzeug.security import check_password_hash

from app import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("admin", "department_editor", "personal_editor"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    is_active_flag = db.Column(db.Boolean, nullable=False, default=True)

    teacher = db.relationship("Teacher", back_populates="user", uselist=False)

    @property
    def is_active(self):
        return self.is_active_flag

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can_manage_users(self):
        return self.role == "admin"

    def can_edit_all_content(self):
        return self.role in ("admin", "department_editor")


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    academic_position = db.Column(
        db.Enum("асистент", "главен асистент", "доцент", "професор"), nullable=False
    )
    scientific_degree = db.Column(db.Enum("доктор", "доктор на науките"), nullable=False)
    h_index_scopus = db.Column(db.Integer, nullable=False, default=0)
    h_index_wos = db.Column(db.Integer, nullable=False, default=0)

    publications = db.relationship(
        "Publication", secondary="publication_authors", back_populates="authors"
    )
    user = db.relationship("User", back_populates="teacher", uselist=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    @property
    def display_title(self):
        title = "проф." if self.academic_position == "професор" else self.academic_position
        degree = "д.н." if self.scientific_degree == "доктор на науките" else "д-р"
        return f"{title} {degree} {self.full_name}"


class PublicationType(db.Model):
    __tablename__ = "publication_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)


class IndexingSource(db.Model):
    __tablename__ = "indexing_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False, unique=True)


publication_authors = db.Table(
    "publication_authors",
    db.Column("publication_id", db.Integer, db.ForeignKey("publications.id"), primary_key=True),
    db.Column("teacher_id", db.Integer, db.ForeignKey("teachers.id"), primary_key=True),
    db.Column("author_order", db.Integer, nullable=False, default=1),
)


publication_indexing = db.Table(
    "publication_indexing",
    db.Column("publication_id", db.Integer, db.ForeignKey("publications.id"), primary_key=True),
    db.Column("indexing_source_id", db.Integer, db.ForeignKey("indexing_sources.id"), primary_key=True),
)


citation_links = db.Table(
    "citation_links",
    db.Column("publication_id", db.Integer, db.ForeignKey("publications.id"), primary_key=True),
    db.Column("citing_publication_id", db.Integer, db.ForeignKey("citing_publications.id"), primary_key=True),
)


class Publication(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    venue = db.Column(db.String(300), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    publication_type_id = db.Column(db.Integer, db.ForeignKey("publication_types.id"), nullable=False)
    isbn_issn = db.Column(db.String(80), nullable=True)
    doi = db.Column(db.String(160), nullable=True, unique=True)

    publication_type = db.relationship("PublicationType")
    authors = db.relationship("Teacher", secondary=publication_authors, back_populates="publications")
    indexing_sources = db.relationship("IndexingSource", secondary=publication_indexing)
    citing_publications = db.relationship("CitingPublication", secondary=citation_links, back_populates="cited_publications")


class CitingPublication(db.Model):
    __tablename__ = "citing_publications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    authors_text = db.Column(db.String(500), nullable=False)
    venue = db.Column(db.String(300), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    publication_type_id = db.Column(db.Integer, db.ForeignKey("publication_types.id"), nullable=False)
    isbn_issn = db.Column(db.String(80), nullable=True)
    doi = db.Column(db.String(160), nullable=True, unique=True)

    publication_type = db.relationship("PublicationType")
    cited_publications = db.relationship("Publication", secondary=citation_links, back_populates="citing_publications")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

