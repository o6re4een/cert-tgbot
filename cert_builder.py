# import PyPDF2
import os
from fpdf import FPDF
import fitz  
import datetime
from fitz import *

from a import replace_text_in_image


def image_to_pdf(image_path:str) -> str:
    output_path = os.path.splitext(image_path)[0] + ".pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, x=0, y=0, w=210, h=297)
    path = pdf.output(output_path)
    return output_path

def create_custom_cert(custom_template_path:str="", custom_search_text:str="", custom_data_text:str=""):
    output_path = replace_text_in_image(
        custom_template_path,
        custom_search_text,
        custom_data_text
        )
    return output_path


def create_certificate(name:str = "",title:str = "",date:str = "", template_path:str = "", output_path:str = ""):
    # Открываем шаблонный PDF
   
    
    
   
    doc = fitz.open(template_path)
    for page in doc:
        search_text = "{{name}}"
        found_name: list[Shape]= page.search_for(search_text)
        found_date: list[Shape] = page.search_for('{{date}}')
        found_title : list[Shape] = page.search_for('{{title}}')

        if(not found_name):
            return False
            # print(found_item)

            # page.add_redact_annot(found_item[0], '')  # create redaction for text
            # page.apply_redactions()  # apply the redaction now
            # page.insert_text(found_item[0].bl , name, fontsize=20, fontname="Helvetica", encoding="UTF-8")
            
            # page.add_redact_annot(found_date[0], '')  # create redaction for text
            # page.apply_redactions()  # apply the redaction now
            # page.insert_text(found_date[0].bl , datetime.date.today().strftime("%d.%m.%Y"), fontsize=12, fontname="Helvetica", encoding="UTF-8")
            
        page.add_redact_annot(found_name[0], '')  
        page.apply_redactions()  
        page.insert_textbox(found_name[0] , name, fontsize=20, fontname="Helvetica", encoding=TEXT_ENCODING_LATIN, lineheight=0.8, align=TEXT_ALIGN_CENTER)
            
        page.add_redact_annot(found_title[0], '')  
        page.apply_redactions()  
        page.insert_textbox(found_title[0] , title, fontsize=20, fontname="Helvetica", encoding=TEXT_ENCODING_LATIN, lineheight=0.8, align=TEXT_ALIGN_CENTER, expandtabs=8)

        page.add_redact_annot(found_date[0], '')  
        page.apply_redactions()  
        page.insert_textbox(found_date[0] , date, fontsize=20, fontname="Helvetica", encoding=TEXT_ENCODING_LATIN, lineheight=0.8, align=TEXT_ALIGN_CENTER,expandtabs=8)

    doc.save(output_path)
    return True
        #     writer.write(output_pdf)


def process_create_certificate(participants_data: list[dict[str,str]]) -> list[str]:

    
    template_pdf = "template.pdf"  # Путь к шаблонному файлу PDF
    output_dir = "certificates"  # Папка для сохранения сертификатов
    
    # Создаем папку, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    generated_certs = []
    # Генерируем сертификаты
    for participant in participants_data:
        output_pdf_path = os.path.join(output_dir, f"{participant['name']}_certificate.pdf")
        is_generated = create_certificate(participant['name'], participant['title'], participant['date'], template_pdf, output_pdf_path)
        if(is_generated):
            generated_certs.append(output_pdf_path)
    print(generated_certs)
    return generated_certs

# process_create_certificate(["Name Name"])

   
