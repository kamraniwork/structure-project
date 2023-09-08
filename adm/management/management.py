# pip install click==8.1.3
import click
from adm.config.runtime_config import settings
from adm.utils.config.configuration import Configuration


@click.group()
def cli():
    pass


@cli.command("start_scheduler")
def run_app_scheduler():
    # TODO: write something
    pass


if __name__ == "__main__":
    config = settings['default']
    Configuration.configure(config, alternative_env_search_dir=__file__)
    cli()
