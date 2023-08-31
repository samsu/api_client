# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

import six
import sys

from oslo_config import cfg
from oslo_log import log as logging

from api_client._i18n import _, _LE


LOG = logging.getLogger(__name__)

exc_log_opts = [
    cfg.BoolOpt('fatal_exception_format_errors',
                default=False,
                help='Make exception message format errors fatal'),
]

CONF = cfg.CONF
CONF.register_opts(exc_log_opts)


class FortinetException(Exception):
    """Base Fortinet Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    msg_fmt = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs

            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception(_LE('Exception in string format operation'))
                for name, value in six.iteritems(kwargs):
                    LOG.error("%s: %s" % (name, value))

                if CONF.fatal_exception_format_errors:
                    six.reraise(*exc_info)
                else:
                    # at least get the core message out if something happened
                    message = self.msg_fmt

        self.message = message
        super(FortinetException, self).__init__(message)

    def format_message(self):
        return self.args[0]


class Invalid(FortinetException):
    msg_fmt = _("Unacceptable parameters.")
    code = 400


class NotFound(FortinetException):
    msg_fmt = _("Resource could not be found.")
    code = 404


class VirtualInterfaceMacAddressException(FortinetException):
    msg_fmt = _("Creation of virtual interface with "
                "unique mac address failed")


class HypervisorUnavailable(FortinetException):
    msg_fmt = _("Connection to the hypervisor is broken on host: %(host)s")


class DeviceDetachFailed(FortinetException):
    msg_fmt = _("Device detach failed for %(device)s: %(reason)s)")


class InstanceNotFound(NotFound):
    ec2_code = 'InvalidInstanceID.NotFound'
    msg_fmt = _("Instance %(instance_id)s could not be found.")


class DeviceNotFound(NotFound):
    msg_fmt = _("Device '%(device)s' not found.")


class InvalidParameterValue(Invalid):
    ec2_code = 'InvalidParameterValue'
    msg_fmt = _("%(err)s")


class InvalidAggregateAction(Invalid):
    msg_fmt = _("Unacceptable parameters.")
    code = 400


class InvalidAggregateActionAdd(InvalidAggregateAction):
    msg_fmt = _("Cannot add host to aggregate "
                "%(aggregate_id)s. Reason: %(reason)s.")


class InvalidAggregateActionDelete(InvalidAggregateAction):
    msg_fmt = _("Cannot remove host from aggregate "
                "%(aggregate_id)s. Reason: %(reason)s.")


class InvalidAggregateActionUpdate(InvalidAggregateAction):
    msg_fmt = _("Cannot update aggregate "
                "%(aggregate_id)s. Reason: %(reason)s.")


class InvalidAggregateActionUpdateMeta(InvalidAggregateAction):
    msg_fmt = _("Cannot update metadata of aggregate "
                "%(aggregate_id)s. Reason: %(reason)s.")


class InvalidGroup(Invalid):
    msg_fmt = _("Group not valid. Reason: %(reason)s")


class InvalidSortKey(Invalid):
    msg_fmt = _("Sort key supplied was not valid.")


class InvalidStrTime(Invalid):
    msg_fmt = _("Invalid datetime string: %(reason)s")


class InstanceInvalidState(Invalid):
    msg_fmt = _("Instance %(instance_uuid)s in %(attr)s %(state)s. Cannot "
                "%(method)s while the instance is in this state.")


class InstanceNotRunning(Invalid):
    msg_fmt = _("Instance %(instance_id)s is not running.")


class InstanceNotInRescueMode(Invalid):
    msg_fmt = _("Instance %(instance_id)s is not in rescue mode")


class InstanceNotRescuable(Invalid):
    msg_fmt = _("Instance %(instance_id)s cannot be rescued: %(reason)s")


class InstanceNotReady(Invalid):
    msg_fmt = _("Instance %(instance_id)s is not ready")


class InstanceSuspendFailure(Invalid):
    msg_fmt = _("Failed to suspend instance: %(reason)s")


class InstanceResumeFailure(Invalid):
    msg_fmt = _("Failed to resume instance: %(reason)s")


class InstancePowerOnFailure(Invalid):
    msg_fmt = _("Failed to power on instance: %(reason)s")


class InstancePowerOffFailure(Invalid):
    msg_fmt = _("Failed to power off instance: %(reason)s")


class InstanceRebootFailure(Invalid):
    msg_fmt = _("Failed to reboot instance: %(reason)s")


class InstanceTerminationFailure(Invalid):
    msg_fmt = _("Failed to terminate instance: %(reason)s")


class InstanceDeployFailure(Invalid):
    msg_fmt = _("Failed to deploy instance: %(reason)s")


class MultiplePortsNotApplicable(Invalid):
    msg_fmt = _("Failed to launch instances: %(reason)s")


class InvalidFixedIpAndMaxCountRequest(Invalid):
    msg_fmt = _("Failed to launch instances: %(reason)s")


class ServiceUnavailable(Invalid):
    msg_fmt = _("Service is unavailable at this time.")


