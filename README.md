# Rabbitmq Nagios Plugins

Set of python based rabbitmq plugins.

## Install

```bash
pip install pycinga
```

Copy these scripts into /usr/lib(64)/nagios/plugins

## Usage

Note, these scripts require a HOSTNAME not HOSTADDRESS in order to differentiate some of the information rabbit returns. Here's a sample:

```bash
  check_rabbit_aliveness.py -H $HOSTNAME$ --username $ARG1$ --password $ARG2$ --vhost $ARG3$
  check_rabbit_queue.py -H $HOSTNAME$ --username $ARG1$ --password $ARG2$ --vhost $ARG3$ --queue $ARG4$ -w $ARG5$ -c $ARG6$
```

## Closing remarks

Definite kudo's to some of the other developers around the web. In particularly, a lot of the base idea for this came from https://github.com/kmcminn/rabbit-nagios
