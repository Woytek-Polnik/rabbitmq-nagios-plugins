#!/usr/bin/env python
from argparse import ArgumentParser
from pycinga import Response, CRITICAL, OK
from base_rabbit_check import BaseRabbitCheck


class RabbitAlivenessCheck(BaseRabbitCheck):
    """
    performs a single rabbitmq build in aliveness-test
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument("--vhost", help="RabbitMQ vhost", type=str, default="%2F")

    def makeUrl(self):
        """
        forms self.url, a correct url to polling a rabbit aliveness
        """
        try:
            if self.options.use_ssl is True:
                self.url = "https://%s:%s/api/aliveness-test/%s" % (
                    self.options.hostname,
                    self.options.port,
                    self.options.vhost,
                )
            else:
                self.url = "http://%s:%s/api/aliveness-test/%s" % (
                    self.options.hostname,
                    self.options.port,
                    self.options.vhost,
                )
            return True
        except Exception as e:
            self.rabbit_error = 3
            self.rabbit_note = "problem forming api url:", e
        return False

    def testOptions(self):
        """
        returns false if necessary options aren't present
        """
        if not self.options.vhost:
            return False
        return True

    def setPerformanceData(self, data, result):
        result.set_perf_data("rabbit_error", self.rabbit_error)
        return result

    def parseResult(self, data):
        if data["status"] == "ok":
            return Response(OK, "Response status was ok")
        return Response(CRITICAL, data["status"])


if __name__ == "__main__":
    obj = RabbitAlivenessCheck()
    obj.check().exit()
