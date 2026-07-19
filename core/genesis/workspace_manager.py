import time
import uuid


class GenesisWorkspaceManager:

    def __init__(self):

        self.system = "GENESIS WORKSPACE MANAGER v1"

        self.workspaces = []



    def create_workspace(
        self,
        name,
        project_type,
        owner_agent
    ):

        workspace = {

            "id":
            "workspace_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "type":
            project_type,

            "owner":
            owner_agent,

            "files":
            [],

            "version":
            "v1.0",

            "status":
            "CREATED",

            "created":
            time.time()

        }


        self.workspaces.append(workspace)


        print(
            f"📦 Workspace created: {name}"
        )


        return workspace



    def add_file(
        self,
        workspace_id,
        filename,
        agent
    ):

        for workspace in self.workspaces:

            if workspace["id"] == workspace_id:

                workspace["files"].append(
                    {
                        "file":
                        filename,

                        "created_by":
                        agent,

                        "timestamp":
                        time.time()
                    }
                )


                return {

                    "status":
                    "FILE_ADDED",

                    "file":
                    filename

                }



        return {

            "status":
            "WORKSPACE_NOT_FOUND"

        }



    def list_workspaces(self):

        return self.workspaces



    def report(self):

        return {

            "system":
            self.system,

            "workspaces":
            len(self.workspaces),

            "timestamp":
            time.time()

        }



workspace_manager = GenesisWorkspaceManager()
