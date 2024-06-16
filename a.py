import cv2
import pytesseract
import numpy as np
import uuid
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def replace_text_in_image(image_path, template_str: str = '', replacement_str: str = ''):
    if template_str == '' or replacement_str == '':
        raise Exception('template_str or replacement_str is empty')
    
    replacements = replacement_str.split(';')
    templates = template_str.split(';')

    # Загружаем изображение с помощью OpenCV
    img = cv2.imread(image_path)

    # Преобразуем изображение в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))

    dilation = cv2.dilate(thresh1, rect_kernel, iterations=8)

    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Проверяем, не слишком ли мала область, чтобы быть текстом
        if w < 10 or h < 10:
            continue

        # Обрезаем область по координатам для OCR
        cropped = img[y:y + h, x:x + w]

        # Распознаем текст в текущей области
        text = pytesseract.image_to_string(cropped).strip()

        print(f"Detected text: {text} at coordinates ({x}, {y}, {w}, {h})")

        for template, replacement in zip(templates, replacements):
            if template in text:
                print(f"Replacing '{template}' with '{replacement}'")

                # Закрашиваем старый текст белым цветом в OpenCV
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)
                # Рисуем новый текст
                font_scale = 1.5
                font_thickness = 2
                font = cv2.FONT_HERSHEY_SIMPLEX

                text_size = cv2.getTextSize(replacement, font, font_scale, font_thickness)[0]
                text_x = x + int(text_size[0] / 2)
                text_y = y + text_size[1] 
                print

                cv2.putText(img, replacement, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)
                break  # Прекращаем дальнейшую проверку, если замена произошла

    unique_filename = str(uuid.uuid4()) + '_modified.jpg'
    cv2.imwrite(unique_filename, img)
    return unique_filename

# Пример использования
input_image_path = "templates/FF0417-01-free-certificate-template-16x9-1.jpg"
output_image_path = replace_text_in_image(
    input_image_path,
    template_str="Enter Name Here;SIGNATURE",
    replacement_str="John Doe;aaaaa"
)
print(f"Изображение сохранено по пути: {output_image_path}")
