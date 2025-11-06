import os
import platform
import typer
import json

from logging.config import dictConfig
from typing import Literal
from pathlib import Path
from click_shell import make_click_shell

from src.constants.config import LOGGING_CONFIG
from src.commands.ls_cmd import ls_command
from src.commands.cat_cmd import cat_command
from src.commands.pwd_cmd import pwd_command
from src.commands.cd_cmd import cd_command
from src.commands.mv_cmd import mv_command
from src.commands.rm_cmd import rm_command
from src.commands.cp_cmd import cp_command
from src.commands.history_cmd import history_command
from src.commands.arch_cmd import zip_command, unzip_command, tar_command, untar_command
from src.constants.file_mode import FileReadMode


app = typer.Typer()
HISTORY_FILE = Path(__file__).parent.parent / ".history"

def save_to_history(command: str):
    '''
    сохраняет команду в историю
    создаёт файл истории, если он не существует

    сохраняет команду в словарь history, где ключом является номер команды,
    а значением - сама команда(сохраняет как корректные команды, так и неверные)
    добавляет в .history
    '''

    if not command or not command.strip():
        return

    if not HISTORY_FILE.exists():
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w") as f:
            json.dump({}, f)

    history = {}
    with open(HISTORY_FILE, "r") as f:
        content = f.read().strip()
        if content:
            history = json.loads(content)
            history = {int(k): v for k, v in history.items()}

    next_num = max(history.keys(), default=0) + 1
    history[next_num] = command.strip()

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    '''
    callback - запускается при вызове скрипта без аргументов
    invoke_without_command=True - callback выполняется без указания команды, т.е.
    проверяет ОС, инициализирует логирование, запускает интерактивную оболочку

    shell - интерактивная оболочка ClickShell
    _original_onecmd - оригинальный команду
    shell.onecmd - сохраняет команду в историю и затем выполняет её,
    т.к. save_to_history возвращает None
    '''

    system = platform.system()
    root_dir = Path.home()

    if system == "Windows":
        typer.echo("Не поддерживаем Венду")
        typer.exit(1)
    else:
        os.chdir(root_dir)

    dictConfig(LOGGING_CONFIG)
    typer.echo("\t\t  " + "-" * 10 + " МИНИ CLI " + "-" * 10)
    typer.echo("\t\tНапишите 'exit' чтобы покинуть нас")

    if ctx.invoked_subcommand is None:
        shell = make_click_shell(ctx, prompt=lambda: os.getcwd() + "> ")
        _original_onecmd = shell.onecmd
        shell.onecmd = lambda line: save_to_history(line) or _original_onecmd(line)
        shell.cmdloop()

@app.command()
def pwd() -> None:
    typer.echo(pwd_command())

@app.command()
def ls(
    path: Path = typer.Argument(None, help="Какой каталог вывести"),
    long: bool = typer.Option(False, "--long", "-l", help="Побольше инфы про файлы/каталоги"),
    advanced: bool = typer.Option(False, "--advanced", "-a", help="Заныканные файлы")
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
    filename: Path = typer.Argument(..., help="Какой файл читаем"),
    mode: Literal[FileReadMode.string, FileReadMode.bytes] = typer.Option(FileReadMode.string, "--mode", "-m", help="Как читаем"),
):
    try:
        data = cat_command(filename, mode=mode)
        typer.echo(data)
    except OSError as e:
        typer.echo(e)
    except ValueError as e:
        typer.echo(e)

@app.command()
def cd(
    path: Path = typer.Argument(..., help="В какую директорию подорваться"),
):
    try:
        cd_command(path)
    except OSError as e:
        typer.echo(e)

@app.command()
def mv(
    filename_source: Path = typer.Argument(..., help="Чё перекидываем/переименовываем"),
    filename_destination: Path = typer.Argument(..., help="Во что перекидываем/переименовываем"),
):
    try:
        mv_command(filename_source, filename_destination)
    except OSError as e:
        typer.echo(e)

@app.command()
def rm(
    filename: Path = typer.Argument(..., help="Чё удаляем"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Удаляем каталог"),
):
    try:
        if recursive:
            confirm = typer.confirm("Ты точно хочешь удалить этот каталог?")
            if not confirm:
                typer.echo("Отмена")
        rm_command(filename, recursive=recursive)
    except OSError as e:
        typer.echo(e)

@app.command()
def cp(
    filename_source: Path = typer.Argument(..., help="Чё копируем"),
    filename_destination: Path = typer.Argument(..., help="Куда копируем"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Копируем каталог"),
):
    try:
        if recursive:
            confirm = typer.confirm("Ты точно хочешь копировать этот каталог?")
            if not confirm:
                typer.echo("Отмена")
        cp_command(filename_source, filename_destination, recursive=recursive)
    except OSError as e:
        typer.echo(e)

@app.command()
def zip(
    src: Path = typer.Argument(..., help="Чё запаковываем"),
    archive_name: Path = typer.Argument(..., help="Как назовём архив"),
):
    try:
        zip_command(src, archive_name)
    except OSError as e:
        typer.echo(e)
    except ValueError as e:
        typer.echo(e)

@app.command()
def unzip(
    archive_name: Path = typer.Argument(..., help="Какой zip распаковываем"),
):
    try:
        unzip_command(archive_name)
    except OSError as e:
        typer.echo(e)
    except ValueError as e:
        typer.echo(e)

@app.command()
def tar(
    src: Path = typer.Argument(..., help="Чё запаковываем"),
    archive_name: Path = typer.Argument(..., help="Как назовём архив"),
):
    try:
        tar_command(src, archive_name)
    except OSError as e:
        typer.echo(e)
    except ValueError as e:
        typer.echo(e)

@app.command()
def untar(
    archive_name: Path = typer.Argument(..., help="Какой tar распаковываем"),
):
    try:
        untar_command(archive_name)
    except OSError as e:
        typer.echo(e)
    except ValueError as e:
        typer.echo(e)

@app.command()
def history() -> None:
    typer.echo(history_command())
