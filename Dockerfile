FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements.txt
ENV PYHTONUNBUFFERED=1
RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6 


RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install urllib3
RUN pip3 install redis
RUN pip3 install opencv-python-headless
# RUN pip install vedis --use-pep517
RUN pip3 install -r requirements.txt

RUN chmod 775 .
COPY . . 

CMD ["python3","-u", "certification.bot.py"]