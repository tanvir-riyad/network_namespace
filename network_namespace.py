import subprocess
import platform
import socket


if platform.system() == 'Linux':
    print('Its a linux OS!')
else:
    print('network namespace are supported on Linux only')


def create_network_namespace(name):
    subprocess.run(['ip', 'netns', 'add', name])


def create_veth_pair(veth1, veth2):
    subprocess.run(['sudo', 'ip', 'link', 'add', veth1, 'type', 'veth', 'peer', 'name', veth2])


def assign_cable_to_namespace(veth, namespace):
    subprocess.run(['sudo', 'ip', 'link', 'set', veth, 'netns', namespace], check=True)


def configure_interface_ip(namespace, veth, ip):
    subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace, 'ip', 'addr', 'add', ip, 'dev', veth])
    subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace, 'ip', 'link', 'set', 'dev', veth, 'up'])


if __name__ == "__main__":
    namespace1 = 'ns1'
    namespace2 = 'ns2'
    vethernet1 = 'veth_cable_1'
    vethernet2 = 'veth_cable_2'
    ip1 = '192.168.1.10/24'
    ip2 = '192.168.1.20/24'
    port = 49152

    subprocess.run(['sudo', 'ip', 'netns', 'delete', namespace1], check=False)
    subprocess.run(['sudo', 'ip', 'netns', 'delete', namespace2], check=False)

    create_network_namespace(namespace1)
    create_network_namespace(namespace2)

    create_veth_pair(vethernet1, vethernet2)

    assign_cable_to_namespace(vethernet1, namespace1)
    assign_cable_to_namespace(vethernet2, namespace2)

    configure_interface_ip(namespace1, vethernet1, ip1)
    configure_interface_ip(namespace2, vethernet2, ip2)


    # subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace1, 'ping', '192.168.1.20'], check=True)

    subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace1, 'ping', '192.168.1.20', '-c', '5'], check=True)
    subprocess.run(['sudo', 'ip', 'netns', 'exec', namespace2, 'ping', '192.168.1.10', '-c', '5'], check=True)