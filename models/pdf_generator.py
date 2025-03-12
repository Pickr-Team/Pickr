import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from reportlab.lib.colors import Color, white
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer


def generate_topic_poster(supervisor, topics):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4, bottomup=0)
    c.setFillColorRGB(51 / 255, 51 / 255, 51 / 255)
    c.rect(0, 0, 595, 842, fill=1)

    max_lines = 4
    line_length = 500
    start_y = 280
    line_spacing = 20
    seed = 220

    # Fonts
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    font_path = os.path.join(parent_dir, 'static', 'font', 'Dank-Mono-Italic.ttf') # C:\Users\20854\Desktop\Pickr\models\static\font\Dank-Mono-Italic.ttf
    pdfmetrics.registerFont(TTFont('DankMono_Italic', font_path))
    font_path = os.path.join(parent_dir, 'static', 'font', 'Dank-Mono-Regular.ttf')
    pdfmetrics.registerFont(TTFont('DankMono', font_path))

    c.setFont("DankMono_Italic", 40)
    c.setFillColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
    c.drawString(50, 100, supervisor.first_name + '\'s Topics')

    c.setLineWidth(1)
    c.setStrokeColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
    c.line(50, 150, 545, 150)

    for i in range(len(topics)):
        if i < 3:
            c.setFont("DankMono", 15)
            c.setFillColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
            c.drawString(50, 190 + i * seed, topics[i].name)

            c.setFont("DankMono", 15)
            c.setFillColor(white)
            c.drawString(50, 220 + i * seed, topics[i].get_type_name())
            c.drawString(50, 250 + i * seed, str(topics[i].quota) + ' Positions')

            c.setFont("DankMono_Italic", 15)
            c.setFillColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
            c.drawString(200, 250 + i * seed, 'PK' + str(format(topics[i].id, '04d')))

            c.setFillColor(white)
            c.setFont("DankMono", 12)
            for i in range(len(topics)):
                description = topics[i].description
                words = description.split()
                current_line = ""
                line_count = 0

                for word in words:

                    test_line = (current_line + " " + word if current_line else word)
                    if line_count == max_lines - 1:
                        test_line += "..."

                    if c.stringWidth(test_line, "DankMono", 12) <= line_length:
                        current_line = test_line
                        if line_count == max_lines - 1:
                            break
                    else:
                        if line_count < max_lines:
                            c.drawString(50, start_y + i * seed + line_count * line_spacing, current_line)
                            line_count += 1
                            current_line = word
                        else:
                            current_line += "..."
                            c.drawString(50, start_y + i * seed + line_count * line_spacing, current_line)
                            break

                if line_count < max_lines:
                    c.drawString(50, start_y + i * seed + line_count * line_spacing, current_line)

                c.setLineWidth(1)
                c.setStrokeColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
                c.line(50, 370 + i * seed, 545, 370 + i * seed)

        else:
            if (i - 3) % 3 == 0:
                c.showPage()
                c.setFillColorRGB(51 / 255, 51 / 255, 51 / 255)
                c.rect(0, 0, 595, 842, fill=1)
                c.drawImage('static/image/logo_footer.png', 440, 780, 104, 30)

            page_index = (i - 3) % 3
            c.setFont("DankMono", 15)
            c.setFillColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
            c.drawString(50, 100 + page_index * seed, topics[i].name)

            c.setFont("DankMono", 15)
            c.setFillColor(white)
            c.drawString(50, 130 + page_index * seed, topics[i].get_type_name())
            c.drawString(50, 160 + page_index * seed, str(topics[i].quota) + ' Positions')

            c.setFont("DankMono_Italic", 15)
            c.setFillColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
            c.drawString(200, 160 + page_index * seed, 'PK' + str(format(topics[i].id, '04d')))

            c.setFillColor(white)
            c.setFont("DankMono", 12)

            description = topics[i].description
            words = description.split()
            current_line = ""
            line_count = 0

            for word in words:
                test_line = (current_line + " " + word if current_line else word)
                if line_count == max_lines - 1:
                    test_line += "..."

                if c.stringWidth(test_line, "DankMono", 12) <= line_length:
                    current_line = test_line
                    if line_count == max_lines - 1:
                        break
                else:
                    if line_count < max_lines:
                        c.drawString(50, 190 + page_index * seed + line_count * line_spacing, current_line)
                        line_count += 1
                        current_line = word
                    else:
                        current_line += "..."
                        c.drawString(50, 190 + page_index * seed + line_count * line_spacing, current_line)
                        break

                if line_count < max_lines:
                    c.drawString(50, 190 + page_index * seed + line_count * line_spacing, current_line)

                c.setLineWidth(1)
                c.setStrokeColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
                c.line(50, 280 + page_index * seed, 545, 280 + page_index * seed)

    c.save()
    return pdf_buffer


# todo: bug: Chinese text cannot be printed (but English works)
def generate_report_pdf(report, graduation_year):
    supervisor_name = report.student.get_supervisor_name()

    primary_color = Color(225 / 255, 108 / 255, 99 / 255)
    dark_bg = Color(51 / 255, 51 / 255, 51 / 255)

    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(current_dir)
    font_path = os.path.join(parent_dir, 'static', 'font', 'Dank-Mono-Regular.ttf')
    registerFont(TTFont('DankMono', font_path))
    font_path = os.path.join(parent_dir, 'static', 'font', 'Dank-Mono-Italic.ttf')
    registerFont(TTFont('DankMono_Bold', font_path))

    styles = {
        'title': ParagraphStyle(
            name='Title',
            fontName='DankMono_Bold',
            fontSize=24,
            textColor=primary_color,
            alignment=1,
            leading=36,
            spaceAfter=25
        ),
        'header': ParagraphStyle(
            name='Header',
            fontName='DankMono_Bold',
            fontSize=18,
            textColor=white,
            spaceAfter=12
        ),
        'body': ParagraphStyle(
            name='Body',
            fontName='DankMono',
            fontSize=12,
            textColor=white,
            leading=14,
            spaceAfter=14,
            alignment=TA_JUSTIFY
        ),
        'label': ParagraphStyle(
            name='Label',
            fontName='DankMono_Bold',
            fontSize=12,
            textColor=primary_color,
            spaceAfter=6
        )
    }

    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=A4,
                          rightMargin=50, leftMargin=50,
                          topMargin=50, bottomMargin=50)

    def add_decor(canvas, doc):
        canvas.setFillColor(dark_bg)
        canvas.rect(0, 0, A4[0], A4[1], fill=1)

        line_y = doc.bottomMargin + 20
        canvas.setStrokeColor(primary_color)
        canvas.setLineWidth(1)
        canvas.line(50, line_y, A4[0] - 50, line_y)

        footer_y = line_y + 15
        canvas.saveState()
        canvas.setFont('DankMono', 10)
        canvas.setFillColor(primary_color)
        canvas.drawString(50, footer_y, f"Generated by CDUT-OBU Project Management System - 'Pickr' | Page {doc.page}")
        canvas.restoreState()

    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id='normal')
    doc.addPageTemplates([PageTemplate(id='All', frames=frame, onPage=add_decor)])

    content = []

    content.append(Paragraph(
        "Chengdu University of Technology<br/>"
        "Oxford Brookes College<br/>"
        "<font size='18' color='#E16C63'>Project Module (CHC6096)</font>",
        styles['title']
    ))
    content.append(Spacer(1, 25))

    content.append(Paragraph(
        f"Weekly Report Sheet - {graduation_year - 1}/{graduation_year} Academic Year",
        styles['header']
    ))
    content.append(Spacer(1, 30))

    info_content = [
        ["STUDENT NAME:", report.student.english_name],
        ["SUPERVISOR:", supervisor_name],
        ["PROJECT:", report.student.get_final_topic_name()],
        [f"SEMESTER {report.semester} | WEEK {report.week}", report.submit_time]
    ]

    for label, value in info_content:
        content.append(Paragraph(f"<font color='#E16C63'>{label}</font> {value}", styles['body']))

    content.append(Spacer(1, 30))

    sections = [
        ('CURRENT WEEK PLAN', report.current_plan),
        ('CHALLENGES ENCOUNTERED', report.issues),
        ('NEXT WEEK PLAN', report.next_plan),
        ('SUPERVISOR FEEDBACK', report.feedback)
    ]

    for title, text in sections:
        content.append(Paragraph(title, styles['label']))
        content.append(Spacer(1, 6))

        formatted_text = "<br/>".join(text.split('\n')) if text else ""
        content.append(Paragraph(formatted_text, styles['body']))
        content.append(Spacer(1, 24))

    doc.build(content)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
