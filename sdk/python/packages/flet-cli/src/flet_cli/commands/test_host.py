"""
Provisioning entry point for the Flet integration-test host.

`provision_test_host` is defined in `flet_cli.commands.test` (alongside the
`flet test` command) and re-exported here so the flet pytest plugin can import
it from a stable, command-agnostic module without pulling in argparse wiring.
"""

from flet_cli.commands.test import provision_test_host

__all__ = ["provision_test_host"]
