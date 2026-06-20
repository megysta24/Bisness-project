DROP DATABASE IF EXISTS publication_activity;
CREATE DATABASE publication_activity CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE publication_activity;

CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    middle_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    academic_position ENUM('асистент', 'главен асистент', 'доцент', 'професор') NOT NULL,
    scientific_degree ENUM('доктор', 'доктор на науките') NOT NULL,
    h_index_scopus INT NOT NULL DEFAULT 0,
    h_index_wos INT NOT NULL DEFAULT 0,
    CONSTRAINT chk_teacher_h_scopus CHECK (h_index_scopus >= 0),
    CONSTRAINT chk_teacher_h_wos CHECK (h_index_wos >= 0)
);

CREATE TABLE publication_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE indexing_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE publications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    venue VARCHAR(300) NOT NULL,
    publication_year INT NOT NULL,
    publication_type_id INT NOT NULL,
    isbn_issn VARCHAR(80),
    doi VARCHAR(160) UNIQUE,
    CONSTRAINT fk_publication_type FOREIGN KEY (publication_type_id)
        REFERENCES publication_types(id),
    CONSTRAINT chk_publication_year CHECK (publication_year BETWEEN 1900 AND 2100)
);

CREATE TABLE publication_authors (
    publication_id INT NOT NULL,
    teacher_id INT NOT NULL,
    author_order INT NOT NULL DEFAULT 1,
    PRIMARY KEY (publication_id, teacher_id),
    CONSTRAINT fk_pub_author_publication FOREIGN KEY (publication_id)
        REFERENCES publications(id) ON DELETE CASCADE,
    CONSTRAINT fk_pub_author_teacher FOREIGN KEY (teacher_id)
        REFERENCES teachers(id) ON DELETE CASCADE
);

CREATE TABLE publication_indexing (
    publication_id INT NOT NULL,
    indexing_source_id INT NOT NULL,
    PRIMARY KEY (publication_id, indexing_source_id),
    CONSTRAINT fk_pub_index_publication FOREIGN KEY (publication_id)
        REFERENCES publications(id) ON DELETE CASCADE,
    CONSTRAINT fk_pub_index_source FOREIGN KEY (indexing_source_id)
        REFERENCES indexing_sources(id)
);

CREATE TABLE citing_publications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    authors_text VARCHAR(500) NOT NULL,
    venue VARCHAR(300) NOT NULL,
    publication_year INT NOT NULL,
    publication_type_id INT NOT NULL,
    isbn_issn VARCHAR(80),
    doi VARCHAR(160) UNIQUE,
    CONSTRAINT fk_citing_type FOREIGN KEY (publication_type_id)
        REFERENCES publication_types(id),
    CONSTRAINT chk_citing_year CHECK (publication_year BETWEEN 1900 AND 2100)
);

CREATE TABLE citation_links (
    publication_id INT NOT NULL,
    citing_publication_id INT NOT NULL,
    PRIMARY KEY (publication_id, citing_publication_id),
    CONSTRAINT fk_citation_publication FOREIGN KEY (publication_id)
        REFERENCES publications(id) ON DELETE CASCADE,
    CONSTRAINT fk_citation_citing FOREIGN KEY (citing_publication_id)
        REFERENCES citing_publications(id) ON DELETE CASCADE
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'department_editor', 'personal_editor') NOT NULL,
    teacher_id INT NULL UNIQUE,
    is_active_flag BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_user_teacher FOREIGN KEY (teacher_id)
        REFERENCES teachers(id) ON DELETE SET NULL
);

CREATE INDEX idx_teachers_name ON teachers(last_name, first_name);
CREATE INDEX idx_publications_year ON publications(publication_year);
CREATE INDEX idx_publications_title ON publications(title);
CREATE INDEX idx_citing_year ON citing_publications(publication_year);

