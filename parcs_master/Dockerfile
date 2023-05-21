FROM python:3.11
COPY . ./parcs_master
RUN pip install -r ./parcs_node/requirements.txt
EXPOSE 8080
CMD ["python", "./parcs_master/app.py"]