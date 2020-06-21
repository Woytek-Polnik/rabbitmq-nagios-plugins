#!/usr/bin/env python
from pycinga import Response, CRITICAL, OK
from base_rabbit_check import BaseRabbitCheck


class RabbitConnectionsCheck(BaseRabbitCheck):
    """
    performs a nagios compliant check on connections and
    attempts to catch blocked connection - not running ones.
    Expected usage is with a critical threshold of 0
    """

    def makeUrl(self):
        """
        forms self.url, a correct url to polling a rabbit vhost
        """
        try:
            if self.options.use_ssl is True:
                self.url = "https://%s:%s/api/connections" % (
                    self.options.hostname,
                    self.options.port,
                )
            else:
                self.url = "http://%s:%s/api/connections" % (
                    self.options.hostname,
                    self.options.port,
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
        if not self.options.hostname or not self.options.port:
            return False
        return True

    def setPerformanceData(self, data, result):

        result.set_perf_data("connections", self.connections_count)
        result.set_perf_data("connections.running", self.ok_connections_count)
        result.set_perf_data("connections.running_rate", self.ok_connections_rate)
        result.set_perf_data("connections.not_running", self.not_running_connections_count)
        result.set_perf_data("connections.not_running_rate", self.not_running_connections_rate)
        result.set_perf_data("receive_rate", self.receive_rate)
        result.set_perf_data("send_rate", self.send_rate)
        return result

    def parseResult(self, data):
        connections_count = len(data)
        ok_connections_count = 0
        not_running_connections_count = 0
        receive_rate = 0
        send_rate = 0

        # Process state
        for d in data:
            if d.get("state") == "running":
                ok_connections_count += 1
            else:
                not_running_connections_count += 1
            receive_rate += d.get("recv_oct_details", {}).get("rate", 0)
            send_rate += d.get("send_oct_details", {}).get("rate", 0)

        try:
            not_running_connections_rate = not_running_connections_count / (connections_count / 100.0)
        except ZeroDivisionError:
            not_running_connections_rate = 0
        try:
            ok_connections_rate = ok_connections_count / (connections_count / 100.0)
        except ZeroDivisionError:
            ok_connections_rate = 0
        self.connections_count = connections_count
        self.ok_connections_count = ok_connections_count
        self.not_running_connections_count = not_running_connections_count
        self.receive_rate = receive_rate
        self.send_rate = send_rate
        self.not_running_connections_rate = not_running_connections_rate
        self.ok_connections_rate = ok_connections_rate

        message = "CHECK completed - connections_running ({0}, {1}%), connections_not_running ({2}, {3}%)".format(
            ok_connections_count, ok_connections_rate, not_running_connections_count, not_running_connections_rate
        )

        return self.response_for_value(not_running_connections_rate, message)


if __name__ == "__main__":
    obj = RabbitConnectionsCheck()
    obj.check().exit()
