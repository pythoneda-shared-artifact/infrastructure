"""
pythoneda/shared/artifact/infrastructure/cli/artifact_cli.py

This file defines the ArtifactCli.

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
import abc
import argparse
from importlib import import_module
from pythoneda import BaseObject, PrimaryPort


class ArtifactCli(BaseObject, PrimaryPort, abc.ABC):

    """
    A PrimaryPort to be used as post-commit-hook in git to send StagedChangesCommitted events.

    Class name: ArtifactCli

    Responsibilities:
        - Parse the command-line to retrieve the information about the commit.

    Collaborators:
        - pythoneda.application.PythonEDA subclasses: They are notified back with the information retrieved from the command line.
        - pythoneda.shared.artifact.infrastructure.cli.*: CLI handlers.
    """

    @classmethod
    @property
    def is_one_shot_compatible(cls) -> bool:
        """
        Retrieves whether this primary port should be instantiated when
        "one-shot" behavior is active.
        It should return False unless the port listens to future messages
        from outside.
        :return: True in such case.
        :rtype: bool
        """
        return True

    async def accept(self, app):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA instance.
        :type app: PythonEDA
        """
        parser = argparse.ArgumentParser(description="Sends a artifact-related events")

        parser.add_argument(
            "-e",
            "--event",
            required=False,
            choices=[
                "StagedChangesCommitted",
                "CommittedChangesPushed",
                "CommittedChangesTagged",
                "TagPushed",
            ],
            help="The type of event to send.",
        )
        parser.add_argument(
            "-r", "--repository-folder", required=False, help="The repository folder"
        )
        parser.add_argument("-t", "--tag", required=False, help="The tag")

        args, unknown_args = parser.parse_known_args()

        if args.event is not None:
            event_in_snake_case = self.__class__.camel_to_snake(args.event)

            module = import_module(
                f"pythoneda.shared.artifact.infrastructure.cli.{event_in_snake_case}_cli_handler"
            )
            handler_class = getattr(module, f"{args.event}CliHandler")
            await handler_class(app).handle(args)
