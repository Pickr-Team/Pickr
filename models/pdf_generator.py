from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO


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
    pdfmetrics.registerFont(TTFont('DankMono_Italic', 'static/font/Dank-Mono-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('DankMono', 'static/font/Dank-Mono-Regular.ttf'))

    c.setFont("DankMono_Italic", 40)
    c.setFillColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
    c.drawString(50, 100, supervisor.first_name + '\'s Topics')

    c.setLineWidth(1)
    c.setStrokeColorRGB(225 / 255.0, 108 / 255.0, 99 / 255.0)
    c.line(50, 150, 545, 150)

    for i in range(len(topics)):
        if i < 3:
            c.setFont("DankMono", 20)
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
                # 放图片
                c.drawImage('static/image/logo_footer.png', 440, 780, 104, 30)

            page_index = (i - 3) % 3
            c.setFont("DankMono", 20)
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
