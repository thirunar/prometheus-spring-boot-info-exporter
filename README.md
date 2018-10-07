# prometheus-spring-boot-version-exporter

Scans the spring boot services to fetch the version and converts to prometheus metrics 


### Config

```yml
exporter_port: 9158 # Port on which prometheus can call this exporter to get metrics
log_level: info
json_data_urls:
- url: http://userservice.dev:8080/admin/info
  label: userservice-dev
- url: http://userservice.qa:8080/admin/info
  label: userservice-qa
- url: http://userservice.prod:8080/admin/info
  label: userservice-prod

metric_name: spring_boot_info # All metric names will be prefixed with this value
tags:
- name: version
  description: Version of service
  path: $.app.version
- name: stage
  description: Deployed Stage 
  path: $.app.stage
- name: service_name
  description: Name of the service
  path: $.app.name
```


### Run

#### Using code (local)

```
# Ensure python 2.x and pip installed
pip install -r app/requirements.txt
python app/exporter.py example/config.yml
```

#### Using docker

```
docker run -p 9158:9158 -v $(pwd)/example/config.yml:/etc/prometheus-spring-boot-info-exporter/config.yml rthirucs/prometheus-spring-boot-info-exporter /etc/prometheus-spring-boot-info-exporter/config.yml
```
Metrics will available in http://localhost:9158


