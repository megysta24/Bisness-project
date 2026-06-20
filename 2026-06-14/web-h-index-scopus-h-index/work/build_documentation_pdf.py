from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = r"C:\Users\stoia\Documents\Codex\2026-06-14\web-h-index-scopus-h-index\outputs\publication_activity_system\documentation.pdf"
ARIAL = r"C:\Windows\Fonts\arial.ttf"
ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

pdfmetrics.registerFont(TTFont("Arial", ARIAL))
pdfmetrics.registerFont(TTFont("Arial-Bold", ARIAL_BOLD))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BgTitle", fontName="Arial-Bold", fontSize=22, leading=28, alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle(name="BgSub", fontName="Arial", fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#4b5563")))
styles.add(ParagraphStyle(name="BgH1", fontName="Arial-Bold", fontSize=16, leading=20, textColor=colors.HexColor("#2454a6"), spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="BgH2", fontName="Arial-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#172033"), spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name="BgBody", fontName="Arial", fontSize=10.5, leading=14, alignment=TA_LEFT, spaceAfter=6))
styles.add(ParagraphStyle(name="BgSmall", fontName="Arial", fontSize=9, leading=12, textColor=colors.HexColor("#4b5563"), spaceAfter=4))


def p(text, style="BgBody"):
    return Paragraph(text, styles[style])


def table(data, widths=None, font_size=8.5):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Arial"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf3ff")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172033")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cfd7e6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def screenshot(title, items):
    data = [[Paragraph(f"<b>{title}</b>", styles["BgBody"])]]
    for item in items:
        data.append([Paragraph(item, styles["BgSmall"])])
    t = Table(data, colWidths=[16.5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2454a6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#9aa8bd")),
        ("INNERGRID", (0, 1), (-1, -1), 0.3, colors.HexColor("#d9deea")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(1.6 * cm, 1.1 * cm, "Web система за публикационна активност")
    canvas.drawRightString(A4[0] - 1.6 * cm, 1.1 * cm, f"стр. {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=1.6 * cm,
    rightMargin=1.6 * cm,
    topMargin=1.6 * cm,
    bottomMargin=1.8 * cm,
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=footer)])

story = []
story += [
    Spacer(1, 3.2 * cm),
    p("Курсова работа", "BgTitle"),
    p("Web базирана информационна система за отчитане на публикационната активност на департамент", "BgTitle"),
    Spacer(1, 0.8 * cm),
    p("Тема: Департамент „Информатика“", "BgSub"),
    p("Backend: Python Flask | Frontend: HTML, CSS, JavaScript | База данни: MySQL", "BgSub"),
    Spacer(1, 2.0 * cm),
    p("Студент: ........................................................", "BgBody"),
    p("Факултетен номер: ..............................................", "BgBody"),
    p("Преподавател: ..................................................", "BgBody"),
    Spacer(1, 3.0 * cm),
    p("Година: 2026", "BgSub"),
    PageBreak(),
]

story += [
    p("1. Обща характеристика", "BgH1"),
    p("Разработката представлява web базирана информационна система за съхраняване, редактиране, търсене и отчитане на публикационната активност на преподавателите от департамент. Системата поддържа преподаватели, научни публикации, индексиране, цитиращи публикации и потребители с различни права."),
    p("Избраната реализация е Python Flask за backend, HTML/CSS/JavaScript за потребителски интерфейс и MySQL като релационна база данни. MySQL Workbench се използва за създаване и преглед на базата."),
    p("2. Структура на базата данни", "BgH1"),
    p("Базата е нормализирана чрез отделяне на справочни таблици и междинни таблици за връзките много-към-много. Това избягва повторение на списъци от автори, типове публикации и индексиращи източници в една колона."),
]

schema_rows = [
    ["Таблица", "Основни полета", "Ключове и предназначение"],
    ["teachers", "id, first_name, middle_name, last_name, academic_position, scientific_degree, h_index_scopus, h_index_wos", "PK: id. Данни за преподавателите."],
    ["users", "id, email, password_hash, role, teacher_id, is_active_flag", "PK: id, UK: email, FK: teacher_id. Потребители и роли."],
    ["publication_types", "id, name", "PK: id, UK: name. Типове: списание, сборник, книга, глава, монография."],
    ["indexing_sources", "id, name", "PK: id, UK: name. Scopus, WoS, НРФС, други."],
    ["publications", "id, title, venue, publication_year, publication_type_id, isbn_issn, doi", "PK: id, FK: publication_type_id, UK: doi. Публикации на департамента."],
    ["publication_authors", "publication_id, teacher_id, author_order", "Съставен PK. M:N между публикации и преподаватели."],
    ["publication_indexing", "publication_id, indexing_source_id", "Съставен PK. M:N между публикации и индексиращи източници."],
    ["citing_publications", "id, title, authors_text, venue, publication_year, publication_type_id, isbn_issn, doi", "PK: id, FK: publication_type_id. Публикации, които цитират."],
    ["citation_links", "publication_id, citing_publication_id", "Съставен PK. M:N между цитирани и цитиращи публикации."],
]
story.append(table([[p(c, "BgSmall") for c in row] for row in schema_rows], widths=[3.2 * cm, 7.3 * cm, 6.0 * cm], font_size=7.5))

story += [
    p("3. Диаграма на връзките", "BgH1"),
    Preformatted(
        """TEACHERS 1--0..1 USERS
TEACHERS M--N PUBLICATIONS чрез PUBLICATION_AUTHORS
PUBLICATIONS M--N INDEXING_SOURCES чрез PUBLICATION_INDEXING
PUBLICATIONS M--N CITING_PUBLICATIONS чрез CITATION_LINKS
PUBLICATION_TYPES 1--N PUBLICATIONS
PUBLICATION_TYPES 1--N CITING_PUBLICATIONS""",
        ParagraphStyle("code", fontName="Arial", fontSize=9, leading=12, backColor=colors.HexColor("#f3f4f6"), borderPadding=8),
    ),
    p("4. Нормализация", "BgH1"),
    p("Първа нормална форма: всички полета са атомарни; списъците от автори, индексирания и цитирания са изнесени в отделни таблици."),
    p("Втора нормална форма: таблиците с прост първичен ключ нямат частични зависимости; междинните таблици използват съставни ключове само за връзките."),
    p("Трета нормална форма / BCNF: справочните данни за тип публикация и индексиращ източник са отделени. Няма транзитивни зависимости като име на тип публикация, записано директно в publications."),
    PageBreak(),
    p("5. Основни функции", "BgH1"),
]

features = [
    ["Функция", "Реализация"],
    ["Главно меню", "Начална страница с навигация към преподаватели, публикации, цитирания, отчети и потребители."],
    ["CRUD преподаватели", "Списък, търсене, добавяне, редакция и изтриване."],
    ["CRUD публикации", "Въвеждане на заглавие, автори, място на публикуване, година, тип, ISBN/ISSN, DOI и индексиране."],
    ["Цитирания", "Въвеждане на публикации, в които се цитират една или повече публикации на департамента."],
    ["Отчети", "Брой публикации и цитирания по преподавател, общи стойности за департамента, бутон за печат."],
    ["Потребители и роли", "Администратор, редактор общо съдържание, редактор лично съдържание."],
]
story.append(table([[p(c, "BgSmall") for c in row] for row in features], widths=[4.4 * cm, 12.1 * cm], font_size=8.5))

story += [
    p("6. Потребителски роли", "BgH1"),
    p("<b>Администратор</b> управлява потребителите и има достъп до всички данни."),
    p("<b>Редактор на общото съдържание</b> може да добавя и редактира общата информация за преподаватели, публикации и цитирания."),
    p("<b>Редактор на личното съдържание</b> вижда всички въведени данни, но може да редактира само публикации, в които участва като автор, и собствените си преподавателски данни."),
    p("7. Екранни илюстрации", "BgH1"),
    screenshot("Главно меню", ["Статистики: преподаватели, публикации, цитирания", "Навигация: Преподаватели | Публикации | Цитирания | Отчети | Потребители", "Последни публикации"]),
    Spacer(1, 0.3 * cm),
    screenshot("Форма за публикация", ["Заглавие, издание, година, тип, ISBN/ISSN, DOI", "Checkbox списък с автори от департамента", "Checkbox списък с индексиране: Scopus, WoS, НРФС, други"]),
    Spacer(1, 0.3 * cm),
    screenshot("Отчет", ["Общо за департамента", "Таблица: преподавател, h-index Scopus, h-index WoS, публикации, цитирания", "Бутон за печат чрез window.print()"]),
    PageBreak(),
    p("8. Демонстрационни данни", "BgH1"),
    p("В базата са включени шест преподаватели, шест публикации, пет цитиращи публикации, четири индексиращи източника и четири потребителски профила. Паролата за демонстрация е password123."),
]

demo_rows = [
    ["Потребител", "Роля", "Предназначение"],
    ["admin@department.local", "admin", "Управление на потребители."],
    ["head@department.local", "department_editor", "Редакция на общото съдържание."],
    ["tuparova@department.local", "personal_editor", "Лична редакция за конкретен преподавател."],
    ["ivanov@department.local", "personal_editor", "Втори пример за личен редактор."],
]
story.append(table([[p(c, "BgSmall") for c in row] for row in demo_rows], widths=[5.2 * cm, 4.0 * cm, 7.3 * cm], font_size=8.5))

story += [
    p("9. Стартиране", "BgH1"),
    Preformatted(
        """1. В MySQL Workbench се изпълняват database/schema.sql и database/seed.sql.
2. В папката на проекта:
   python -m venv .venv
   .venv\\Scripts\\Activate.ps1
   pip install -r requirements.txt
3. Копира се .env като .env и се въвежда MySQL паролата.
4. Стартиране:
   python run.py
5. Отваря се http://127.0.0.1:5000""",
        ParagraphStyle("code2", fontName="Arial", fontSize=9, leading=12, backColor=colors.HexColor("#f3f4f6"), borderPadding=8),
    ),
    p("10. Заключение", "BgH1"),
    p("Проектът покрива изискванията за релационна MySQL база, нормализация, стандартни операции за въвеждане/корекция/изтриване/търсене, отчети на екран и печат, както и три нива потребители с различни права."),
]

doc.build(story)
print(OUTPUT)

