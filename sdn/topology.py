from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


def create_topology():

    net = Mininet(switch=OVSSwitch)

    # Connect to SDN controller
    controller = net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6633
    )

    # Add hosts
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    h3 = net.addHost('h3', ip='10.0.0.3')
    h4 = net.addHost('h4', ip='10.0.0.4')

    # Add switch
    s1 = net.addSwitch('s1')

    # Connect hosts to switch
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    # Start network
    net.start()

    print("\nDistributed Log Aggregation SDN Topology")
    print("----------------------------------------")
    print("h1 -> 10.0.0.1  (Log Client)")
    print("h2 -> 10.0.0.2  (Log Client)")
    print("h3 -> 10.0.0.3  (Log Client)")
    print("h4 -> 10.0.0.4  (Log Server)")
    print("s1 -> Open vSwitch")
    print("c0 -> SDN Controller")
    print("----------------------------------------\n")

    CLI(net)

    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
