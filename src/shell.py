# import logging
import os
import typer
# from src.constants.config import LOGGING_CONFIG
from src.commands.ls_cmd import ls_command
from src.commands.cat_cmd import cat_command
# from src.commands.cd_cmd import cd_command
from pathlib import Path
from src.constants.file_mode import FileReadMode
from typing import Literal
from click_shell import make_click_shell
# from click.core import Context


app = typer.Typer()

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    # logging.config.dictConfig(LOGGING_CONFIG)
    # logger = logging.getLogger(__name__)

    if ctx.invoked_subcommand is None:
        shell = make_click_shell(ctx, prompt=os.getcwd() + "> ")
        shell.cmdloop()


@app.command()
def ls(
    path: Path = typer.Argument('.', help="List of files and directories"),
    long: bool = typer.Option(False, "--long", "-l", help="Long format"),
    advanced: bool = typer.Option(False, "--advanced", "-a", help="Hidden files")
):
    if path is None or not path.exists():
        path = Path.cwd()

    content = ls_command(path, long_format=long, advanced=advanced)
    typer.echo(content)

@app.command()
def cat(
    filename: Path = typer.Argument(Path.cwd(), help="Path to file"),
    mode: Literal[FileReadMode.string, FileReadMode.bytes] = typer.Option(FileReadMode.string, "--mode", "-m", help="Read mode"),
):
    data = cat_command(filename, mode=mode)
    typer.echo(data)

@app.command()
def cd(
    path: Path = typer.Argument(..., help="Path to directory"),
):
    path = Path(path)

    # Проверка существования пути
    if not path.exists():
        typer.echo(f"cd: no such file or directory: {path}", err=True)
        raise typer.Exit(1)

    # Проверка, что это директория
    if not path.is_dir():
        typer.echo(f"cd: not a directory: {path}", err=True)
        raise typer.Exit(1)

    # Выполняем смену директории
    try:
        os.chdir(path)
        typer.echo(Path.cwd())
    except OSError as e:
        typer.echo(f"cd: {e}", err=True)
        raise typer.Exit(1)
