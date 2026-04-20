from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.recoco import Timer

log = core.getLogger()

class SimpleMonitor(object):
    def __init__(self):
        core.openflow.addListeners(self)
        Timer(5, self.get_stats, recurring=True)

    def get_stats(self):
        for con in core.openflow._connections.values():
            con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

    def _handle_FlowStatsReceived(self, event):
        if not event.stats:
            return

        top_flow = max(event.stats, key=lambda x: x.byte_count)

        if top_flow.byte_count > 0:
            bandwidth = top_flow.byte_count / 5.0

            print("\n====== Network Utilization ======")
            print("Top Flow Traffic")
            print("Packets    :", top_flow.packet_count)
            print("Bytes      :", top_flow.byte_count)
            print("Bandwidth  :", round(bandwidth, 2), "B/s")
            print("================================")

def launch():
    SimpleMonitor()
