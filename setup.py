import pycyphal
from contextlib import suppress
from pathlib import Path
from setuptools import Command, setup
from setuptools.command.build import build
import pathlib


class CustomCommand(Command):
    def initialize_options(self) -> None:
        self.bdist_dir = None
        self.proto_msgs_path = None
        self.pkg_name = None

    def finalize_options(self) -> None:
        self.pkg_name = self.distribution.get_name().replace("-", "_")
        self.proto_msgs_path = Path(self.pkg_name)
        with suppress(Exception):
            self.bdist_dir = Path(self.get_finalized_command("bdist_wheel").bdist_dir)

    def run(self) -> None:
        if self.bdist_dir:
            # Create package structure
            output_dir = self.bdist_dir
            cur_path = pathlib.Path(__file__).parent
            uavcan_path = cur_path / "uavcan"
            pycyphal.dsdl.compile_all(
                root_namespace_directories=[
                    cur_path / "uavcan",
                    cur_path / "reg",
                ],
                output_directory=output_dir,
            )


class CustomBuild(build):
    sub_commands = [("build_custom", None)] + build.sub_commands


setup(cmdclass={"build": CustomBuild, "build_custom": CustomCommand})
