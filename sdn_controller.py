from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ether_types


class SDNLogController(app_manager.OSKenApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def add_flow(self, datapath, priority, match, actions):
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(
            datapath.ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=priority,
            match=match,
            instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features(self, ev):
        dp = ev.msg.datapath
        p = dp.ofproto_parser
        o = dp.ofproto

        actions = [p.OFPActionOutput(o.OFPP_CONTROLLER,
                                      o.OFPCML_NO_BUFFER)]
        self.add_flow(dp, 0, p.OFPMatch(), actions)

        critical = p.OFPMatch(
            eth_type=ether_types.ETH_TYPE_IP,
            ip_proto=17,
            udp_dst=10001
        )
        self.add_flow(
            dp, 100,
            critical,
            [p.OFPActionOutput(o.OFPP_FLOOD)]
        )

        normal = p.OFPMatch(
            eth_type=ether_types.ETH_TYPE_IP,
            ip_proto=17,
            udp_dst=10000
        )
        self.add_flow(
            dp, 50,
            normal,
            [p.OFPActionOutput(o.OFPP_FLOOD)]
        )

        self.logger.info("Switch connected: %s", dp.id)
        self.logger.info("Critical UDP priority: 100")
        self.logger.info("Normal UDP priority: 50")

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in(self, ev):
        msg = ev.msg
        dp = msg.datapath
        p = dp.ofproto_parser
        o = dp.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth and eth.ethertype != ether_types.ETH_TYPE_LLDP:
            self.logger.info(
                "Packet received: %s -> %s",
                eth.src,
                eth.dst
            )

        actions = [p.OFPActionOutput(o.OFPP_FLOOD)]

        out = p.OFPPacketOut(
            datapath=dp,
            buffer_id=msg.buffer_id,
            in_port=msg.match['in_port'],
            actions=actions,
            data=msg.data if msg.buffer_id == o.OFP_NO_BUFFER else None
        )

        dp.send_msg(out)
