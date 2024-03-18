FROM python:3

ADD requirements.txt /

RUN pip3 install -r requirements.txt

ADD api.py /

# Run app when the container launches
CMD [ "python", "./api.py" ]