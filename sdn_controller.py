from os_ken.base import app_manager
from os_ken.controller import ofp_event
from os_ken.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from os_ken.ofproto import ofproto_v1_3
from os_ken.lib.packet import packet, ethernet, ether_types

class SDNLogController(app_manager.OSKenApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def add_flow(self, dp, priority, match, actions):
        parser = dp.ofproto_parser
        ofp = dp.ofproto
        instructions = [
            parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)
        ]
        mod = parser.OFPFlowMod(
            datapath=dp,
            priority=priority,
            match=match,
            instructions=instructions
        )
        dp.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features(self, ev):
        dp = ev.msg.datapath
        parser = dp.ofproto_parser
        ofp = dp.ofproto

        self.add_flow(
            dp, 100,
            parser.OFPMatch(
                eth_type=0x0800,
                ip_proto=17,
                udp_dst=10001
            ),
            [
                parser.OFPActionSetQueue(1),
                parser.OFPActionOutput(4)
            ]
        )

        self.add_flow(
            dp, 50,
            parser.OFPMatch(
                eth_type=0x0800,
                ip_proto=17,
                udp_dst=10000
            ),
            [
                parser.OFPActionSetQueue(0),
                parser.OFPActionOutput(4)
            ]
        )

        self.add_flow(
            dp, 0,
            parser.OFPMatch(),
            [parser.OFPActionOutput(ofp.OFPP_CONTROLLER,
                                    ofp.OFPCML_NO_BUFFER)]
        )

        self.logger.info("QoS flow rules installed on switch %s", dp.id)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in(self, ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth is None or eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        actions = [parser.OFPActionOutput(ofp.OFPP_FLOOD)]

        out = parser.OFPPacketOut(
            datapath=dp,
            buffer_id=msg.buffer_id,
            in_port=msg.match['in_port'],
            actions=actions,
            data=msg.data if msg.buffer_id == ofp.OFP_NO_BUFFER else None
        )
        dp.send_msg(out)
