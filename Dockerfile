FROM python:3.8

COPY . .

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["./start.sh"]
