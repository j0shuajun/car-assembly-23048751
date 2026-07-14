import assembly
from car_assembly import cli


def test_assembly_entrypoint_delegates_to_cli_main():
    assert assembly.main is cli.main
