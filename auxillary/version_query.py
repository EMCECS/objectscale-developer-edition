import importlib


class version_manager:
    repo_index = 'EMCECS/charts'
    default_version = 'v0.33.0'
    supported_versions = ['v0.33.0', 'v0.30.0', 'v0.31.0', 'v0.31.1', 'v0.31.2', 'v0.32.0', 'v0.32.1']
    selected_version = default_version
    pygithub = None
    token = None
    tags = None
    tag_names = None

    def __init__(self, token):
        self.pygithub = importlib.import_module('github')
        self.token = token

    def fetch_versions(self):

        try:
            github_user = self.pygithub.Github(self.token)
            chart_repo = github_user.get_repo(self.repo_index)
        except Exception as e:
            if self.token == 'NO TOKEN' or self.token is None:
                print(e)
                print('No token provided. Please provide a valid token with access to the chart repo.')
                return
            else:
                print('Error pulling repo information. Consult the stacktrace for more info')
                return

        self.tag_names = []
        self.tags = chart_repo.get_tags()

        for tag in self.tags:
            self.tag_names.append(tag.name)

    def list_versions(self):
        for list_item in self.tags:
            print(list_item.name)

    def select_version(self, version: str):
        if self.tags is None:
            self.fetch_versions()

        if version in self.supported_versions:
            self.selected_version = version
        else:
            if version in self.tag_names:
                print('Unsupported version selected. Errors may occur')
                self.selected_version = version
            else:
                print('Version \'' + version + '\' not found in available versions.')
                exit(-1)

        print('Version set to '+self.selected_version)