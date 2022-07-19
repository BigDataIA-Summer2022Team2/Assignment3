FROM python:3.9

LABEL coder1="Cheng"
LABEL coder2="Meihu"
LABEL description="DAMG 7245 Big Data Summer 2022 Assignment 3"
LABEL version="beta-0.1"

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#RUN python3 ./src/readInput.py 
CMD python3 ./src/main.py ${username} ${password} ${full_name} ${email}


EXPOSE 3000
EXPOSE 4000


