FROM python:3.7

RUN mkdir /usr/src/app/

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt

EXPOSE 8050
COPY . /usr/src/app/
CMD ["python", "extract.py"]
CMD ["python", "preprocess.py"]
CMD ["python", "app.py"]
