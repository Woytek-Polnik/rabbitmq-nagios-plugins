rabbitmq-nagios-plugins
=======================

Set of python based rabbitmq plugins.  To install:

#### python
pip install pycinga

copy these scripts into $NAGIOS_HOME/libexec/

Configure your nagios system.  Note, these scripts require a HOSTNAME not HOSTADDRESS in order to differentiate some of the information rabbit returns.  Here's a sample:

```
define command {
   command_name check_rabbitmq_aliveness
   command_line    $USER1$/nagios_rabbitmq_checks/check_rabbit_aliveness.py -H $HOSTNAME$ --username $ARG1$ --password $ARG2$ --vhost $ARG3$
}

define command {
   command_name check_rabbitmq_queue
   command_line    $USER1$/nagios_rabbitmq_checks/check_rabbit_queue.py -H $HOSTNAME$ --username $ARG1$ --password $ARG2$ --vhost $ARG3$ --queue $ARG4$ -w $ARG5$ -c $ARG6$
}
```

Definite kudo's to some of the other developers around the web.  In particularly, a lot of the base idea for this came from https://github.com/kmcminn/rabbit-nagios
