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
    1)сохраняет команду в историю;
    2)создаёт файл истории, если он не существует

    3)сохраняет команду в словарь history, где ключом является номер команды,
    а значением - сама команда(сохраняет как корректные команды, так и неверные)
    4)добавляет в файл .history
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
    _original_onecmd - записывает в себя введённую команду
    shell.onecmd - сохраняет команду в историю и затем выполняет её,
    т.к. save_to_history возвращает None, то _original_onecmd выполнится после save_to_history
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

    shell = make_click_shell(ctx, prompt=lambda: os.getcwd() + "> ")
    _original_onecmd = shell.onecmd

    def error_handler(line: str):
        try:
            save_to_history(line)
            return _original_onecmd(line)
        except OSError as e:
            typer.echo(f"Ошибка работы с файлом/директорией: {e}")
        except ValueError as e:
            typer.echo(f"Ошибка значения: {e}")
        except KeyboardInterrupt:
            typer.echo("\nИспользуйте 'exit' для выхода")
        except Exception as e:
            typer.echo(f"Неожиданная ошибка: {e}")

    shell.onecmd = error_handler
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
    content = ls_command(path, long_format=long, advanced=advanced)
    typer.echo(content)

@app.command()
def cat(
    filename: Path = typer.Argument(..., help="Какой файл читаем"),
    mode: Literal[FileReadMode.string, FileReadMode.bytes] = typer.Option(FileReadMode.string, "--mode", "-m", help="Как читаем"),
):
    data = cat_command(filename, mode=mode)
    typer.echo(data)

@app.command()
def cd(
    path: Path = typer.Argument(..., help="В какую директорию подорваться"),
):
    cd_command(path)

@app.command()
def mv(
    filename_source: Path = typer.Argument(..., help="Чё перекидываем/переименовываем"),
    filename_destination: Path = typer.Argument(..., help="Во что перекидываем/переименовываем"),
):
    mv_command(filename_source, filename_destination)

@app.command()
def rm(
    filename: Path = typer.Argument(..., help="Чё удаляем"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Удаляем каталог"),
):
    if recursive:
        confirm = typer.confirm("Ты точно хочешь удалить этот каталог?")
        if not confirm:
            typer.echo("Отмена")
            return
    rm_command(filename, recursive=recursive)

@app.command()
def cp(
    filename_source: Path = typer.Argument(..., help="Чё копируем"),
    filename_destination: Path = typer.Argument(..., help="Куда копируем"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Копируем каталог"),
):
    if recursive:
        confirm = typer.confirm("Ты точно хочешь копировать этот каталог?")
        if not confirm:
            typer.echo("Отмена")
            return
    cp_command(filename_source, filename_destination, recursive=recursive)

@app.command()
def zip(
    src: Path = typer.Argument(..., help="Чё запаковываем"),
    archive_name: Path = typer.Argument(..., help="Как назовём архив"),
):
    zip_command(src, archive_name)

@app.command()
def unzip(
    archive_name: Path = typer.Argument(..., help="Какой zip распаковываем"),
):
    unzip_command(archive_name)

@app.command()
def tar(
    src: Path = typer.Argument(..., help="Чё запаковываем"),
    archive_name: Path = typer.Argument(..., help="Как назовём архив"),
):
    tar_command(src, archive_name)

@app.command()
def untar(
    archive_name: Path = typer.Argument(..., help="Какой tar распаковываем"),
):
    untar_command(archive_name)

@app.command()
def history() -> None:
    typer.echo(history_command())
