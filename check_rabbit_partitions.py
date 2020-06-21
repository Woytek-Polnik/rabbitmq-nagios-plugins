#!/usr/bin/env python
from argparse import ArgumentParser
from pycinga import Response, CRITICAL, OK
from base_rabbit_check import BaseRabbitCheck


class RabbitPartionsCheck(BaseRabbitCheck):
    """
    performs a nagios compliant check on partition status
    attempts to catch all errors. expected usage is with a critical threshold of 0
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument("--nodes", help="RabbitMQ nodes", type=int, default=1)

    def makeUrl(self):
        """
        forms self.url, a correct url to polling a rabbit queue
        """
        try:
            if self.options.use_ssl is True:
                self.url = "https://%s:%s/api/nodes" % (self.options.hostname, self.options.port)
            else:
                self.url = "http://%s:%s/api/nodes" % (self.options.hostname, self.options.port)
            return True
        except Exception as e:
            self.rabbit_error = 3
            self.rabbit_note = "problem forming api url:", e
        return False

    def testOptions(self):
        if not self.options.nodes:
            return False
        return True

    def setPerformanceData(self, data, result):
        result.set_perf_data("rabbit_error", self.rabbit_error)
        return result

    def parseResult(self, data):
        for node in data:
            if len(node['partitions']) != 0:
                return Response(CRITICAL, 'Partition found %s' % node['name'])
        return Response(OK, "No partitions found")


if __name__ == "__main__":
    obj = RabbitPartionsCheck()
    obj.check().exit()
