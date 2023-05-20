FROM python:3.9
WORKDIR ./parcs_master/parcs_master
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . ./parcs_master/parcs_master
CMD ["python", "./parcs_master/parcs_master/api/app.py"]