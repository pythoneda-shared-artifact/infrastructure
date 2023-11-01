"""
pythoneda/shared/artifact/infrastructure/cli/artifact_commit_pushed_cli_handler.py

This file defines the ArtifactCommitPushedCliHandler class.

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
from pythoneda.shared.artifact_changes.events import ArtifactCommitPushed
from pythoneda.shared.git import GitRepo
import sys


class ArtifactCommitPushedCliHandler(CliHandler):

    """
    A CLI handler in charge of handling ArtifactCommitPushed events.

    Class name: ArtifactCommitPushedCliHandler

    Responsibilities:
        - Build and emit a ArtifactCommitPushed event from the information provided by the CLI.

    Collaborators:
        - pythoneda.artifact.application.ArtifactApp: Gets notified back to process the ArtifactCommitPushed event.
        - pythoneda.shared.artifact_changes.events.ArtifactCommitPushed
    """

    def __init__(self, app):
        """
        Creates a new ArtifactCommitPushedCliHandler.
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
            event = ArtifactCommitPushed(
                args.tag, git_repo.url, git_repo.rev, git_repo.folder
            )
            ArtifactCommitPushedCliHandler.logger().debug(event)
            await self.app.accept(event)
