# -*- coding: utf-8 -*-
import click
from helper.launcher import startServer, startScheduler
from setting import BANNER, VERSION

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
def cli():
    """GatherProxy cli tool"""


@cli.command(name="schedule")
def schedule():
    """start scheduler"""
    click.echo(BANNER)
    startScheduler()


@cli.command(name="server")
def server():
    """Start api service"""
    click.echo(BANNER)
    startServer()


if __name__ == "__main__":
    cli()
