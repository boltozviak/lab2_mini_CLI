import os
import platform
from logging.config import dictConfig
import typer
import logging
import json
from src.constants.config import LOGGING_CONFIG
from src.commands.ls_cmd import ls_command
from src.commands.cat_cmd import cat_command
from src.commands.pwd_cmd import pwd_command
from src.commands.cd_cmd import cd_command
from src.commands.mv_cmd import mv_command
from src.commands.rm_cmd import rm_command
from src.commands.cp_cmd import cp_command
# from src.commands.arch_commands import zip_command
from pathlib import Path
from src.constants.file_mode import FileReadMode
from typing import Literal
from click_shell import make_click_shell


app = typer.Typer()
logger = logging.getLogger(__name__)
HISTORY_FILE = Path(".history")

def save_to_history(command: str):
    history = {}
    if HISTORY_FILE.exists():
         with open(HISTORY_FILE, "r") as f:
            content = f.read().strip()
            if content:
                history = json.loads(content)
                history = {int(k): v for k, v in history.items()}

    next_num = max(history.keys(), default=0) + 1
    history[next_num] = command

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    dictConfig(LOGGING_CONFIG)
    typer.echo("\t\t\t---- Mini CLI ----")
    typer.echo("\t\t\tWrite 'exit' to exit")

    system = platform.system()
    root_dir = Path.home()

    if system == "Windows":
        typer.echo("Don't support Windows")
        typer.exit(1)
    else:
        os.chdir(root_dir)

    if ctx.invoked_subcommand is None:
        shell = make_click_shell(ctx, prompt=lambda: os.getcwd() + "> ")
        _original_default = shell.default
        shell.default = lambda command: (save_to_history(command), _original_default(command))
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
    logger.debug(f"ls command: {path}, {long}, {advanced}")
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
    logger.debug(f"cat command: {filename}, {mode}")
    try:
        data = cat_command(filename, mode=mode)
        typer.echo(data)
    except OSError as e:
        typer.echo(e)
    except ValueError as e:
        typer.echo(e)

@app.command()
def cd(
    path: Path = typer.Argument(..., help="Path to directory"),
):
    logger.debug(f"cd command: {path}")
    try:
        cd_command(path)
    except OSError as e:
        typer.echo(e)

@app.command()
def mv(
    filename_source: Path = typer.Argument(..., help="Path to source file"),
    filename_destination: Path = typer.Argument(..., help="Path to destination file"),
):
    logger.debug(f"mv command: {filename_source}, {filename_destination}")
    try:
        mv_command(filename_source, filename_destination)
    except OSError as e:
        typer.echo(e)

@app.command()
def rm(
    filename: Path = typer.Argument(..., help="Path to file"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursive remove"),
):
    logger.debug(f"rm command: {filename}, {recursive}")
    try:
        if recursive:
            confirm = typer.confirm("Are you sure you want to remove this catalog?")
            if not confirm:
                typer.echo("Operation cancelled")
        rm_command(filename, recursive=recursive)
    except OSError as e:
        typer.echo(e)

@app.command()
def cp(
    filename_source: Path = typer.Argument(..., help="Path to source file"),
    filename_destination: Path = typer.Argument(..., help="Path to destination file"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursive copy"),
):
    logger.debug(f"cp command: {filename_source}, {filename_destination}, {recursive}")
    try:
        if recursive:
            confirm = typer.confirm("Are you sure you want to copy this catalog?")
            if not confirm:
                typer.echo("Operation cancelled")
        cp_command(filename_source, filename_destination, recursive=recursive)
    except OSError as e:
        typer.echo(e)

# @app.command()
# def zip(
#     src: Path = typer.Argument(..., help="Path to source file"),
#     archive_name: Path = typer.Argument(..., help="Path to archive file"),
#     recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursive zip"),
# ):
#     try:
#         zip_command(src, archive_name, recursive=recursive)
#     except OSError as e:
#         typer.echo(e)

# @app.command()
# def unzip(
#     archive_name: Path = typer.Argument(..., help="Path to archive file"),
#     destination: Path = typer.Argument(..., help="Path to destination file"),
# ):
#     try:
#         unzip_command(archive_name, destination)
#     except OSError as e:
#         typer.echo(e)

# @app.command()
# def tar(
#     src: Path = typer.Argument(..., help="Path to source file"),
#     archive_name: Path = typer.Argument(..., help="Path to archive file"),
#     recursive: bool = typer.Option(False, "--recursive", "-r", help="Recursive tar"),
# ):
#     try:
#         tar_command(src, archive_name, recursive=recursive)
#     except OSError as e:
#         typer.echo(e)

# @app.command()
# def untar(
#     archive_name: Path = typer.Argument(..., help="Path to archive file"),
#     destination: Path = typer.Argument(..., help="Path to destination file"),
# ):
#     try:
#         untar_command(archive_name, destination)
#     except OSError as e:
#         typer.echo(e)

# @app.command()
# def history() -> None:
#     typer.echo(history_command())
