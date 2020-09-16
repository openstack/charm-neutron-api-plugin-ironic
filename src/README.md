# Overview

This subordinate charm provides the
[Bare metal ML2 Plugin][python-networking-baremetal] support to the
[OpenStack Neutron API service][charm-neutron-api].

When this charm is related to the neutron-api charm it will install the
```ironic-neutron-agent``` and the ```baremetal``` mechanism driver on
each neutron-api unit in the region. The required mechanism driver will
be communicated back to the neutron-api service and will be added to
the appropriate configuration file.

The ironic agent requires keystone credentials, obtained via a relation
with keystone.

# Usage

## Configuration

This charm requires no special configuration outside of the standard
OpenStack configuration options (openstack-origin, region, etc.)

## Deployment

This is a subordinate charm that needs to attach itself to an existing
neutron-api deployment.

To deploy (partial deployment only):

    juju deploy neutron-api
    juju deploy neutron-openvswitch
    juju deploy neutron-api-plugin-ironic
    juju deploy keystone

    juju add-relation neutron-api neutron-api-plugin-ironic
    juju add-relation neutron-api neutron-openvswitch
    juju add-relation neutron-api-plugin-ironic keystone


[charm-neutron-api]: https://jaas.ai/neutron-api
[python-networking-baremetal]: https://opendev.org/x/networking-baremetal