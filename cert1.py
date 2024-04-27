# import PyPDF2
import os
# from fpdf import FPDF
import fitz  
import datetime
from fitz import *
def create_certificate(name, template_path, output_path):
    # Открываем шаблонный PDF
    doc = fitz.open(template_path)
   
    
    search_text = "{{name}}"
    for page in doc:
        found_item: list[Shape]= page.search_for(search_text)
        found_date: list[Shape] = page.search_for('{{date}}')
        found_title : list[Shape] = page.search_for('{{title}}')

        if(not found_item):
            return False
        # print(found_item)

        # page.add_redact_annot(found_item[0], '')  # create redaction for text
        # page.apply_redactions()  # apply the redaction now
        # page.insert_text(found_item[0].bl , name, fontsize=20, fontname="Helvetica", encoding="UTF-8")
        
        # page.add_redact_annot(found_date[0], '')  # create redaction for text
        # page.apply_redactions()  # apply the redaction now
        # page.insert_text(found_date[0].bl , datetime.date.today().strftime("%d.%m.%Y"), fontsize=12, fontname="Helvetica", encoding="UTF-8")
        
        page.add_redact_annot(found_item[0], '')  
        page.apply_redactions()  
        page.insert_textbox(found_item[0] , name, fontsize=20, fontname="Helvetica", encoding=TEXT_ENCODING_LATIN, lineheight=0.8, align=TEXT_ALIGN_CENTER)
        
        # page.add_redact_annot(found_title[0], '')  
        # page.apply_redactions()  
        # page.insert_textbox(found_title[0] , "G", fontsize=20, fontname="Helvetica", encoding=TEXT_ENCODING_LATIN, lineheight=0.8, align=TEXT_ALIGN_CENTER, expandtabs=8)

        # page.add_redact_annot(found_date[0], '')  
        # page.apply_redactions()  
        # page.insert_textbox(found_date[0] , datetime.date.today().strftime("%d.%m.%Y"), fontsize=20, fontname="Helvetica", encoding=TEXT_ENCODING_LATIN, lineheight=0.8, align=TEXT_ALIGN_CENTER,expandtabs=8)

    doc.save(output_path)
        #     writer.write(output_pdf)

if __name__ == "__main__":
    names = ["Alina"]  # Список имен
    template_pdf = "template.pdf"  # Путь к шаблонному файлу PDF
    output_dir = "certificates"  # Папка для сохранения сертификатов
    
    # Создаем папку, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Генерируем сертификаты
    for name in names:
        output_pdf_path = os.path.join(output_dir, f"{name}_certificate.pdf")
        create_certificate(name, template_pdf, output_pdf_path)
