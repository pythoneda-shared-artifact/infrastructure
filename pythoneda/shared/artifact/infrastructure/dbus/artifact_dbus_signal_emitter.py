# vim: set fileencoding=utf-8
"""
pythoneda/shared/artifact/infrastructure/dbus/artifact_dbus_signal_emitter.py

This file defines the ArtifactDbusSignalEmitter class.

Copyright (C) 2023-today rydnr's pythoneda-shared-artifact/infrastructure

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from dbus_next import BusType
from pythoneda.shared.artifact.events import (
    CommittedChangesPushed,
    CommittedChangesTagged,
    DockerImageAvailable,
    DockerImagePushed,
    DockerImageRequested,
    StagedChangesCommitted,
    TagPushed,
)
from pythoneda.shared.artifact.events.infrastructure.dbus import (
    DbusCommittedChangesPushed,
    DbusCommittedChangesTagged,
    DbusDockerImageAvailable,
    DbusDockerImagePushed,
    DbusDockerImageRequested,
    DbusStagedChangesCommitted,
    DbusTagPushed,
)
from pythoneda.shared.infrastructure.dbus import DbusSignalEmitter
from typing import Dict


class ArtifactDbusSignalEmitter(DbusSignalEmitter):
    """
    A Port that emits events generated by Domain-Artifact as d-bus signals.

    Class name: ArtifactDbusSignalEmitter

    Responsibilities:
        - Connect to d-bus.
        - Emit domain events as d-bus signals.

    Collaborators:
        - pythoneda.shared.application.PythonEDA: Requests emitting events.
        - pythoneda.shared.artifact.events.infrastructure.dbus.DbusCommittedChangesPushed
        - pythoneda.shared.artifact.events.infrastructure.dbus.DbusCommittedChangesTagged
        - pythoneda.shared.artifact.events.infrastructure.dbus.DbusDockerImageAvailable
        - pythoneda.shared.artifact.events.infrastructure.dbus.DbusDockerImagePushed
        - pythoneda.shared.artifact.events.infrastructure.dbus.DbusDockerImageRequested
        - pythoneda.shared.artifact.events.infrastructure.dbus.StagedChangesCommitted
        - pythoneda.shared.artifact.events.infrastructure.dbus.TagPushed
    """

    def __init__(self):
        """
        Creates a new ArtifactDbusSignalEmitter instance.
        """
        super().__init__("pythoneda.shared.artifact.events.infrastructure.dbus")

    def signal_emitters(self) -> Dict:
        """
        Retrieves the configured event emitters.
        :return: For each event, a list with the event interface and the bus type.
        :rtype: Dict
        """
        result = {}

        key = self.__class__.full_class_name(CommittedChangesPushed)
        result[key] = [DbusCommittedChangesPushed, BusType.SYSTEM]
        key = self.__class__.full_class_name(CommittedChangesTagged)
        result[key] = [DbusCommittedChangesTagged, BusType.SYSTEM]
        key = self.__class__.full_class_name(DockerImageAvailable)
        result[key] = [DbusDockerImageAvailable, BusType.SYSTEM]
        key = self.__class__.full_class_name(DockerImagePushed)
        result[key] = [DbusDockerImagePushed, BusType.SYSTEM]
        key = self.__class__.full_class_name(DockerImageRequested)
        result[key] = [DbusDockerImageRequested, BusType.SYSTEM]
        key = self.__class__.full_class_name(StagedChangesCommitted)
        result[key] = [DbusStagedChangesCommitted, BusType.SYSTEM]
        key = self.__class__.full_class_name(TagPushed)
        result[key] = [DbusTagPushed, BusType.SYSTEM]

        return result


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
