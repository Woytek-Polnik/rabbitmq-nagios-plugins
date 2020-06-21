#!/usr/bin/env python
from argparse import ArgumentParser
from base_rabbit_check import BaseRabbitCheck


class RabbitQueueCheck(BaseRabbitCheck):
    """
    performs a nagios compliant check on a single exchange and
    attempts to catch all errors. expected usage is with a critical threshold of 0
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument("--vhost", help="RabbitMQ vhost", type=str, default="%2F")
    parser.add_argument("--exchange", help="Name of the exchange in inspect", type=str)

    def makeUrl(self):
        """
        forms self.url, a correct url to polling a rabbit exchange
        """
        try:
            if self.options.use_ssl is True:
                self.url = "https://%s:%s/api/exchanges/%s/%s" % (
                    self.options.hostname,
                    self.options.port,
                    self.options.vhost,
                    self.options.exchange,
                )
            else:
                self.url = "http://%s:%s/api/exchanges/%s/%s" % (
                    self.options.hostname,
                    self.options.port,
                    self.options.vhost,
                    self.options.exchange,
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
        if (
            not self.options.hostname
            or not self.options.port
            or not self.options.vhost
            or not self.options.exchange
        ):
            return False
        return True

    def setPerformanceData(self, data, result):
        if data.get("message_stats"):
            result.set_perf_data(
                self.exchange + ".publish_out_rate",
                data["message_stats"]["publish_out_details"]["rate"],
            )
            result.set_perf_data(
                self.exchange + ".publish_in_rate",
                data["message_stats"]["publish_in_details"]["rate"],
            )
        else:
            result.set_perf_data(self.exchange + ".publish_out_rate", 0)
            result.set_perf_data(self.exchange + ".publish_in_rate", 0)
        return result

    def parseResult(self, data):
        self.exchange = self.options.exchange
        result = self.response_for_value(0)
        result.message = "Exchange found"
        self.rabbit_note = result.message
        return result


if __name__ == "__main__":
    obj = RabbitQueueCheck()
    obj.check().exit()
