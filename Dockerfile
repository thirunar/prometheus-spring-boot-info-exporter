FROM python:2.7.13-alpine

COPY app /opt/prometheus-spring-boot-info-exporter

RUN pip install -r /opt/prometheus-spring-boot-info-exporter/requirements.txt

EXPOSE 9158

ENTRYPOINT ["python", "/opt/prometheus-spring-boot-info-exporter/exporter.py"]
