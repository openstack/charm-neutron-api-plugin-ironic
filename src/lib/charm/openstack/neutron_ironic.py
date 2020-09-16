from charmhelpers.core.hookenv import (
    config,
    log
)
import charms_openstack.charm as charm

IRONIC_AGENT_CONF = "/etc/neutron/plugins/ml2/ironic_neutron_agent.ini"


def request_endpoint_information(keystone):
    charm = NeutronIronicAgentCharm.singleton
    keystone.request_credentials(
        charm.name, region=charm.region)


class NeutronIronicAgentCharm(charm.OpenStackCharm):
    abstract_class = False

    release = 'train'
    name = 'ironic'
    group = 'neutron'
    
    python_version = 3
    packages = ['ironic-neutron-agent', 'python3-ironic-neutron-agent']
    default_service = 'ironic-neutron-agent'
    services = [default_service,]

    restart_map = {
        IRONIC_AGENT_CONF: [default_service, ],
    }

    release_pkg = version_package = 'neutron-common'

    def install(self):
        self.configure_source()
        super().install()
