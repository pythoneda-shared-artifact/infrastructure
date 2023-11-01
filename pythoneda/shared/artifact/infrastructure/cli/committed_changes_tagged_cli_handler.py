"""
pythoneda/shared/artifact/infrastructure/cli/committed_changes_tagged_cli_handler.py

This file defines the CommittedChangesTaggedCliHandler class.

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
from pythoneda.infrastructure.cli import CliHandler
from pythoneda.shared.artifact_changes.events import CommittedChangesTagged
from pythoneda.shared.git import GitRepo
import sys


class CommittedChangesTaggedCliHandler(CliHandler):

    """
    A CLI handler in charge of handling CommittedChangesTagged events.

    Class name: CommittedChangesTaggedCliHandler

    Responsibilities:
        - Build and emit a CommittedChangesTagged event from the information provided by the CLI.

    Collaborators:
        - pythoneda.artifact.application.ArtifactApp: Gets notified back to process the CommittedChangesTagged event.
        - pythoneda.shared.artifact_changes.events.CommittedChangesTagged
    """

    def __init__(self, app):
        """
        Creates a new CommittedChangesTaggedCliHandler.
        :param app: The ArtifactApp application.
        :type app: pythoneda.artifact.application.ArtifactApp
        """
        super().__init__(app)

    async def handle(self, args):
        """
        Processes the command specified from the command line.
        :param args: The CLI args.
        :type args: argparse.args
        """
        if not args.repository_folder:
            print(f"-r|--repository-folder is mandatory")
            sys.exit(1)
        else:
            git_repo = GitRepo.from_folder(args.repository_folder)
            event = CommittedChangesTagged(
                args.tag, git_repo.url, git_repo.rev, git_repo.folder
            )
            CommittedChangesTaggedCliHandler.logger().debug(event)
            await self.app.accept(event)
