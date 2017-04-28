#!/bin/bash

# Available RabbitMQ environment Variables
# RABBITMQ_USERNAME - Default: user
# RABBITMQ_PASSWORD - Default: bitnami
# RABBITMQ_VHOST    - RabbitMQ application vhost. Default: /
# RABBITMQ_ERLANG_COOKIE - Erlang Cookie to determine whether different nodes are allowed to communicate with each other.
# RABBITMQ_NODE_TYPE - Node Type. Valid Values: stats, queue-ram, queue_disc. Default: stats
# RABBITMQ_NODE_NAME - Node name and host. E.g.: node@hostname or node(localhost won't work in cluster topology). Default rabbit@localhost
# RABBITMQ_NODE_PORT - Node port. Default: 5672
# RABBITMQ_CLUSTER_NODE_NAME - Node name for cluster with E.g.: clusternode@hostname
# RABBITMQ_MANAGER_PORT - Manager port. Default: 15672

# Pass these environment variables into the docker run command like so.
# docker run -e "variable_name=variable_value"

# Start docker container for RabbitMQ service. 
sudo docker run --name rabbitmq bitnami/rabbitmq:latest
