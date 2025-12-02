"""CLI shim to expose the CLI entrypoint at `cli.dub_to_irish`.

This lets users run `python -m cli.dub_to_irish` and keeps the
implementation located in `irishautodub/dub_to_irish.py`.
"""

from irishautodub.dub_to_irish import *
