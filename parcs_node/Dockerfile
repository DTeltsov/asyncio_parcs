FROM python:3.11
COPY . ./parcs_node
RUN pip install -r ./parcs_node/requirements.txt
EXPOSE 8080
CMD ["python", "./parcs_node/app.py"]