import os
import pathlib

from boogie.configurations import PathsConf as Base, env


class PathsConf(Base):
    BASE_DIR = REPO_DIR = pathlib.Path(__file__).parent.parent.parent.parent
    ROOT_DIR = SRC_DIR = APPS_DIR = REPO_DIR / 'src'
    PROJECT_DIR = ROOT_DIR / 'ej'

    # Local paths
    LOCAL_DIR = REPO_DIR / 'local'
    DB_DIR = LOCAL_DIR / 'db'
    MEDIA_ROOT = env(LOCAL_DIR / 'media')
    STATIC_ROOT = env(LOCAL_DIR / 'static')
    FRAGMENTS_DIR = LOCAL_DIR / 'fragments'
    PAGES_DIR = LOCAL_DIR / 'pages'
    LOG_DIR = LOCAL_DIR / 'logs'
    LOG_FILE_PATH = LOG_DIR / 'logfile.log'
    ROOT_TEMPLATE_DIR = PROJECT_DIR / 'templates'

    # Frontend paths
    LIB_DIR = REPO_DIR / 'lib'
    LIB_BUILD = LIB_DIR / 'build'
    THEMES_DIR = LIB_DIR / 'themes'

    def finalize(self, settings):
        """
        Create missing paths.
        """
        for path in [self.LOCAL_DIR, self.DB_DIR, self.MEDIA_ROOT,
                     self.STATIC_ROOT, self.LOG_DIR, self.LIB_DIR,
                     self.LIB_BUILD]:
            if not os.path.exists(path):
                mkdir_recursive(path)

        return super().finalize(settings)

    def get_staticfiles_dirs(self, repo_dir):
        return [repo_dir / 'lib/build', repo_dir / 'lib/assets']

    def get_django_templates_dirs(self):
        return [self.ROOT_TEMPLATE_DIR / 'django']

    def get_jinja_templates_dirs(self):
        return [self.ROOT_TEMPLATE_DIR / 'jinja2']


def mkdir_recursive(path):
    # TODO: implement recursive dir creation.
    print(f'making required directory: {path}')
    os.mkdir(path)
