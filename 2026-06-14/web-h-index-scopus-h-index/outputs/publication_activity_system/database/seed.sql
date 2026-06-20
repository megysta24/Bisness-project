USE publication_activity;

INSERT INTO publication_types (name) VALUES
('списание'),
('сборник от конференция'),
('книга'),
('глава от книга'),
('монография');

INSERT INTO indexing_sources (name) VALUES
('Scopus'),
('WoS'),
('НРФС'),
('други');

INSERT INTO teachers
(first_name, middle_name, last_name, academic_position, scientific_degree, h_index_scopus, h_index_wos)
VALUES
('Даниела', 'Иванова', 'Тупарова', 'професор', 'доктор', 8, 6),
('Георги', 'Петров', 'Тупаров', 'професор', 'доктор', 10, 7),
('Елена', 'Георгиева', 'Тупарова', 'доцент', 'доктор', 5, 4),
('Иван', 'Николаев', 'Иванов', 'главен асистент', 'доктор', 3, 2),
('Мария', 'Петрова', 'Стоянова', 'доцент', 'доктор', 6, 5),
('Петър', 'Димитров', 'Петров', 'асистент', 'доктор', 1, 0);

INSERT INTO publications
(title, venue, publication_year, publication_type_id, isbn_issn, doi)
VALUES
('Exploring the Role of Large Language Models in Advancing Student Assessment in Database Courses',
 'MIPRO 2025 - Proceedings, pp. 1448-1453', 2025, 2, '979-833153597-1', '10.1109/MIPRO65660.2025.11131984'),
('Digital Learning Environments for Programming Education',
 'International Journal of Emerging Technologies in Learning', 2024, 1, '1863-0383', '10.3991/ijet.v19i01.40101'),
('Modeling Student Progress in Web-Based Courses',
 'Education and Information Technologies', 2023, 1, '1360-2357', '10.1007/s10639-023-11111-1'),
('Methods for Database Course Assessment',
 'Proceedings of CompSysTech', 2022, 2, '978-1-4503-9999-1', '10.1145/3565719.3565721'),
('Software Systems for Academic Reporting',
 'University Publishing House', 2021, 3, '978-954-00-0001-1', NULL),
('Learning Analytics in Computer Science Education',
 'Advances in Intelligent Systems', 2020, 4, '978-3-030-00000-1', '10.1007/978-3-030-00000-1_12');

INSERT INTO publication_authors (publication_id, teacher_id, author_order) VALUES
(1, 3, 1), (1, 2, 2), (1, 1, 3),
(2, 1, 1), (2, 5, 2),
(3, 4, 1), (3, 2, 2),
(4, 1, 1), (4, 3, 2),
(5, 5, 1), (5, 6, 2),
(6, 2, 1), (6, 4, 2);

INSERT INTO publication_indexing (publication_id, indexing_source_id) VALUES
(1, 1), (2, 1), (2, 2), (3, 2), (4, 3), (5, 4), (6, 1), (6, 3);

INSERT INTO citing_publications
(title, authors_text, venue, publication_year, publication_type_id, isbn_issn, doi)
VALUES
('AI-Supported Assessment Practices in Higher Education',
 'Petrova, A., Dimitrov, N.', 'Journal of Educational Computing', 2026, 1, '2042-7530', '10.1000/jec.2026.001'),
('Database Education after Generative AI',
 'Mihaylov, S., Angelova, R.', 'EDULEARN Proceedings', 2025, 2, '978-84-09-63010-3', '10.21125/edulearn.2025.1001'),
('Learning Analytics Dashboards for Universities',
 'Kolev, I.', 'Information Systems Education Conference', 2024, 2, '978-1-7138-0000-0', '10.18260/1-2--44444'),
('Quality Indicators for Academic Publishing',
 'Nikolova, M., Kanev, K.', 'Science Metrics Review', 2023, 1, '2815-1120', NULL),
('Digital Transformation in Computer Science Departments',
 'Ruseva, V.', 'Higher Education Studies', 2022, 1, '1925-4741', '10.5539/hes.v12n4p10');

INSERT INTO citation_links (publication_id, citing_publication_id) VALUES
(1, 1), (1, 2), (2, 1), (3, 3), (4, 4), (5, 5), (6, 3), (6, 4);

INSERT INTO users (email, password_hash, role, teacher_id, is_active_flag) VALUES
('admin@department.local', 'pbkdf2:sha256:1000000$coursework$ad5526401c5c6da9b679ce52c75e4df8a92f78aa63753f358855d8078fc90351', 'admin', NULL, TRUE),
('head@department.local', 'pbkdf2:sha256:1000000$coursework$ad5526401c5c6da9b679ce52c75e4df8a92f78aa63753f358855d8078fc90351', 'department_editor', 1, TRUE),
('tuparova@department.local', 'pbkdf2:sha256:1000000$coursework$ad5526401c5c6da9b679ce52c75e4df8a92f78aa63753f358855d8078fc90351', 'personal_editor', 3, TRUE),
('ivanov@department.local', 'pbkdf2:sha256:1000000$coursework$ad5526401c5c6da9b679ce52c75e4df8a92f78aa63753f358855d8078fc90351', 'personal_editor', 4, TRUE);
