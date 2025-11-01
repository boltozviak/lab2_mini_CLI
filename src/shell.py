import os
from logging.config import dictConfig
import typer
from src.constants.config import LOGGING_CONFIG
from src.commands.ls_cmd import ls_command
from src.commands.cat_cmd import cat_command
from src.commands.pwd_cmd import pwd_command
from src.commands.cd_cmd import cd_command
from src.commands.mv_cmd import mv_command
from src.commands.rm_cmd import rm_command
from src.commands.cp_cmd import cp_command
from pathlib import Path
from src.constants.file_mode import FileReadMode
from typing import Literal
from click_shell import make_click_shell


app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    dictConfig(LOGGING_CONFIG)
    typer.echo("---- Mini CLI ----")
    typer.echo("Wrtie 'exit' to exit")

    if ctx.invoked_subcommand is None:
        shell = make_click_shell(ctx, prompt=lambda: os.getcwd() + "> ")
        shell.cmdloop()

@app.command()
def pwd() -> None:
    typer.echo(pwd_command())


@app.command()
def ls(
    path: Path = typer.Argument(None, help="List of files and directories"),
    long: bool = typer.Option(False, "--long", "-l", help="Long format"),
    advanced: bool = typer.Option(False, "--advanced", "-a", help="Hidden files")
):
    if path is None:
        path = Path.cwd()

    try:
        content = ls_command(path, long_format=long, advanced=advanced)
        typer.echo(content)
    except OSError as e:
        typer.echo(e)

@app.command()
def cat(
    filename: Path = typer.Argument(..., help="Path to file"),
    mode: Literal[FileReadMode.string, FileReadMode.bytes] = typer.Option(FileReadMode.string, "--mode", "-m", help="Read mode"),
):
    try:
        data = cat_command(filename, mode=mode)
        typer.echo(data)
    except OSError as e:
        typer.echo(e)

@app.command()
def cd(
    path: Path = typer.Argument(..., help="Path to directory"),
):
    try:
        cd_command(path)
    except OSError as e:
        typer.echo(e)

@app.command()
def mv(
    filename_source: Path = typer.Argument(..., help="Path to source file"),
    filename_destination: Path = typer.Argument(..., help="Path to destination file"),
):
    try:
        mv_command(filename_source, filename_destination)
    except OSError as e:
        typer.echo(e)

@app.command()
def rm(
    filename: Path = typer.Argument(..., help="Path to file"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursive remove"),
):
    try:
        rm_command(filename, recursive=recursive)
    except OSError as e:
        typer.echo(e)

@app.command()
def cp(
    filename_source: Path = typer.Argument(..., help="Path to source file"),
    filename_destination: Path = typer.Argument(..., help="Path to destination file"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursive copy"),
):
    try:
        cp_command(filename_source, filename_destination, recursive=recursive)
    except OSError as e:
        typer.echo(e)
