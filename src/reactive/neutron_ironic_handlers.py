import charms.reactive as reactive
import charm.openstack.neutron_ironic as ironic

from charmhelpers.core.hookenv import (
    log,
)

from charms_openstack.charm import (
    provide_charm_instance,
    use_defaults,
    optional_interfaces,
)


use_defaults(
    'charm.default-select-release',
    'update-status',
)


@reactive.when('identity-credentials.available')
def render_stuff(*args):
    with provide_charm_instance() as ironic_charm:
        ironic_charm.render_with_interfaces(
            optional_interfaces(args))
        ironic_charm.assess_status()
    reactive.set_state('config.complete')


@reactive.when('identity-credentials.connected')
def setup_endpoint(keystone):
    with provide_charm_instance() as charm_class:
        ironic.request_endpoint_information(keystone)
        charm_class.assess_status()


@reactive.when_not('ironic-agent-package.installed')
@reactive.when('neutron-plugin-api-subordinate.available')
def install_ironic():
    with provide_charm_instance() as charm_class:
        charm_class.install()
    reactive.set_state('ironic-agent-package.installed')


@reactive.when_any('neutron-plugin-api-subordinate.connected')
def configure_principal():
    try:
        api_principal = reactive.endpoint_from_flag(
            'neutron-plugin-api-subordinate.connected')

        mech_drivers = []
        existing_mech_drivers = api_principal.neutron_config_data.get(
            'mechanism_drivers', None)
        if existing_mech_drivers:
            mech_drivers.extend(existing_mech_drivers.split(','))

        mech_drivers.append("baremetal")
        mechanism_drivers = ','.join(mech_drivers)
    except AttributeError:
        log("The principal charm isn't ready yet. "
            "Postponing its configuration...")
        return

    api_principal.configure_plugin(
        neutron_plugin='ironic',
        mechanism_drivers=mechanism_drivers)
