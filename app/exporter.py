#!/usr/bin/python

import json
import time
import urllib2
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import argparse
import yaml
from objectpath import Tree
import logging

DEFAULT_PORT = 9158
DEFAULT_LOG_LEVEL = 'info'


class JsonPathCollector(object):
    def __init__(self, config):
        self._config = config

    def collect(self):
        config = self._config
        endpoints = config['json_data_urls']
        for endpoint in endpoints:
            try: 
                result = json.loads(urllib2.urlopen(endpoint['url'], timeout=10).read())
                result_tree = Tree(result)
                labels = ['instance_id']
                values = [endpoint['label']]
                for tag in config['tags']:
                    tag_name = tag['name']
                    tag_path = tag['path']
                    value = result_tree.execute(tag_path)
                    logging.info("tag_name: {}, value for '{}' : {}".format(tag_name, tag_path, value))
                    labels.append(tag_name)
                    values.append(value)
                metric = GaugeMetricFamily(config['metric_name'], "spring boot info", labels=labels)
                metric.add_metric(values, 1)
                yield metric
            except:
                logging.info("Could not fetch details for %s", endpoint['label'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Expose metrics bu jsonpath for configured url')
    parser.add_argument('config_file_path', help='Path of the config file')
    args = parser.parse_args()
    with open(args.config_file_path) as config_file:
        config = yaml.load(config_file)
        log_level = config.get('log_level', DEFAULT_LOG_LEVEL)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.getLevelName(log_level.upper()))
        exporter_port = config.get('exporter_port', DEFAULT_PORT)
        logging.debug("Config %s", config)
        logging.info('Starting server on port %s', exporter_port)
        start_http_server(exporter_port)
        REGISTRY.register(JsonPathCollector(config))
    while True: time.sleep(60)

