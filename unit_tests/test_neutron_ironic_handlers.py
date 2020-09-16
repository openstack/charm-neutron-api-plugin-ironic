import mock

import reactive.neutron_ironic_handlers as handlers

import charms_openstack.test_utils as test_utils


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        hook_set = {
            'when': {
                'configure_principle': (
                    'neutron-plugin-api-subordinate.connected', ),
                'install_ironic': (
                    'neutron-plugin-api-subordinate.available', ),
                'render_stuff': (
                    'identity-credentials.available', ),
                'setup_endpoint': (
                    'identity-credentials.connected', ),
            }
        }
        self.registered_hooks_test_helper(handlers, hook_set, [])


class TestHandlers(test_utils.PatchHelper):

    def test_configure_principal(self):
        mocked_reactive = mock.MagicMock()
        self.patch_object(handlers, 'reactive',
                          name='reactive',
                          new=mocked_reactive)
        principal_charm = mock.MagicMock()
        mocked_reactive.endpoint_from_flag.return_value = principal_charm
        principal_charm.neutron_config_data = {
            'mechanism_drivers': 'driver1,driver2'
        }

        mocked_config = mock.MagicMock()
        self.patch_object(handlers, 'config',
                          name='config',
                          new=mocked_config)
        mocked_config.return_value = 'my_config_value'

        handlers.configure_principal()
        principal_charm.configure_plugin.assert_called_once_with(
            neutron_plugin='ironic',
            mechanism_drivers='driver1,driver2,baremetal')
