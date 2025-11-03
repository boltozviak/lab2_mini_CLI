# import zipfile
# import tarfile
# import logging
# from os import PathLike
# from pathlib import Path

# logger = logging.getLogger(__name__)

# def zip_command(
#     src: PathLike[str] | str,
#     archive_name: PathLike[str] | str,
# ) -> None:
#     src = Path(src)
#     archive_name = Path(archive_name)

#     if not src.exists():
#         logger.error(f"Entered path is not exists: {src}")
#         raise FileNotFoundError(f"Entered path is not exists: {src}")

#     if not src.is_dir():
#         logger.error(f"Entered path is not a dir: {src}")
#         raise IsADirectoryError(f"Entered path is not a dir: {src}")

#     if archive_name.exists():
#         logger.error(f"Entered archive file already exists: {archive_name}")
#         raise FileExistsError(f"Entered archive file already exists: {archive_name}")

#     try:
#         with zipfile.ZipFile(archive_name, 'w') as zipf:
#             zipf.write(src, src.name)
#             logger.info(f"Successfully created archive: {archive_name}")
#     except OSError as e:
#         logger.error(f"Error creating archive: {e}: {src} to {archive_name}")
#         raise

# # def unzip_command(
# #     archive_name: PathLike[str] | str,
# #     destination: PathLike[str] | str,
# # ) -> None:
# #     archive_name = Path(archive_name)
# #     destination = Path(destination)

# #     if not archive_name.exists():
# #         logger.error(f"Archive file is not exists: {archive_name}")
# #         raise FileNotFoundError(f"Archive file is not exists: {archive_name}")

# # def tar_command(
# #     src: PathLike[str] | str,
# #     archive_name: PathLike[str] | str,
# # ) -> None:
# #     src = Path(src)
# #     archive_name = Path(archive_name)

# #     if not src.exists():
# #         logger.error(f"Source file is not exists: {src}")
# #         raise FileNotFoundError(f"Source file is not exists: {src}")
