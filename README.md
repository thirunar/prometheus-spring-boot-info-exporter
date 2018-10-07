# prometheus-spring-boot-version-exporter

Scans the spring boot services to fetch the version and converts to prometheus metrics 


### Config

```yml
exporter_port: 9158 # Port on which prometheus can call this exporter to get metrics
log_level: info
json_data_urls:
- url: http://transaction-service.dev:8080/admin/info # Url to get json data used for fetching metric values 
  label: transaction-service-dev
- url: http://transaction-service.qa:8080/admin/info 
  label: transaction-service-qa
- url: http://user-service.dev:8080/admin/info 
  label: user-service-dev
- url: http://user-service.qa:8080/admin/info 
  label: user-service-qa
metric_name_prefix:  wallet # All metric names will be prefixed with this value
metrics:
- name: version 
  description: Version of service
  path: $.app.version
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


