"""
pythoneda/shared/artifact/infrastructure/cli/staged_changes_committed_cli_handler.py

This file defines the StagedChangesCommittedCliHandler class.

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
from pythoneda import BaseObject
from pythoneda.application import PythonEDA
from pythoneda.shared.artifact.events import Change, StagedChangesCommitted
from pythoneda.shared.git import GitCommit, GitDiff, GitRepo
import sys


class StagedChangesCommittedCliHandler(BaseObject):

    """
    A CLI handler in charge of handling StagedChangesCommitted events.

    Class name: StagedChangesCommittedCliHandler

    Responsibilities:
        - Build and emit a StagedChangesCommitted event from the information provided by the CLI.

    Collaborators:
        - pythoneda.artifact.application.ArtifactApp: Gets notified back to process the StagedChangesCommitted event.
        - pythoneda.shared.artifact.events.StagedChangesCommitted
    """

    def __init__(self):
        """
        Creates a new StagedChangesCommittedCliHandler.
        """
        super().__init__()

    async def handle(self, app: PythonEDA, args):
        """
        Processes the command specified from the command line.
        :param app: The PythonEDA application.
        :type app: pythoneda.application.PythonEDA
        :param args: The CLI args.
        :type args: argparse.args
        """
        if not args.repository_folder:
            print(f"-r|--repository-folder is mandatory")
            sys.exit(1)
        else:
            git_repo = GitRepo.from_folder(args.repository_folder)
            change = Change.from_unidiff_text(
                GitDiff(args.repository_folder).committed_diff(),
                git_repo.url,
                git_repo.rev,
                args.repository_folder,
            )
            hash_value, diff, message = GitCommit(args.repository_folder).latest_commit()
            event = StagedChangesCommitted(message, change, hash_value)
            StagedChangesCommittedCliHandler.logger().debug(event)
            await app.accept(event)
