import time
import json
from threading import Thread

from ..Telegraf import Plugin as ReportPlugin
from ..Aggregator import AggregatorPlugin
from ...core.interfaces import AbstractPlugin

from .server import ReportServer

import logging

logger = logging.getLogger(__name__)


def uts(dt):
    return int(time.mktime(dt.timetuple()))


class Plugin(AbstractPlugin, Thread):
    '''Interactive report plugin '''
    SECTION = "report"

    @staticmethod
    def get_key():
        return __file__

    def __init__(self, core):
        AbstractPlugin.__init__(self, core)
        Thread.__init__(self)
        self.daemon = True  # Thread auto-shutdown
        self.port = 8080
        self.last_sec = None
        self.server = None
        self.data = []
        self.stats = []
        self.monitoring = []

    def get_all_data(self):
        return {"data": self.data,
                "stats": self.stats,
                "monitoring": self.monitoring, }

    def get_available_options(self):
        return ["port"]

    def configure(self):
        self.port = int(self.get_option("port", self.port))
        try:
            aggregator = self.core.get_plugin_of_type(AggregatorPlugin)
            aggregator.add_result_listener(self)
        except KeyError:
            logger.warning(
                "No aggregator module, no valid report will be available")

        try:
            mon = self.core.get_plugin_of_type(ReportPlugin)
            if mon.monitoring:
                mon.monitoring.add_listener(self)
        except KeyError:
            logger.warning("No monitoring module, monitroing report disabled")

    def prepare_test(self):
        try:
            self.server = ReportServer(self)
            self.server.owner = self
        except Exception, ex:
            logger.warning("Failed to start web results server: %s", ex)

    def start_test(self):
        self.start()

    def end_test(self, retcode):
        logger.info("Ended test. Sending command to reload pages.")
        self.server.reload()
        return retcode

    def run(self):
        if (self.server):
            self.server.serve()
            logger.info("Server started.")

    def on_aggregated_data(self, data, stats):
        """
        @data: aggregated data
        @stats: stats about gun
        """
        if data:
            self.data.append(data)
        if stats:
            self.stats.append(stats)
        if self.server is not None and (data or stats):
            message = {'data': data, 'stats': stats}
            self.server.send({k: v for k, v in message.iteritems() if v})

    def monitoring_data(self, data):
        if data:
            self.monitoring.append(data)
            message = {'monitoring': data, }
            if self.server is not None:
                self.server.send(message)

    def post_process(self, retcode):
        report_json = self.core.mkstemp(".json", "report_")
        logger.info("Saving JSON report to %s", report_json)
        self.core.add_artifact_file(report_json)
        with open(report_json, 'w') as report_json_file:
            json.dump(self.get_all_data(), report_json_file, indent=2)
        report_html = self.core.mkstemp(".html", "report_")
        logger.info("Saving HTML report to %s", report_html)
        self.core.add_artifact_file(report_html)
        with open(report_html, 'w') as report_html_file:
            report_html_file.write(self.server.render_offline())
        # raw_input('Press Enter to stop report server.')
        self.server.stop()
        del self.server
        self.server = None
        return retcode
