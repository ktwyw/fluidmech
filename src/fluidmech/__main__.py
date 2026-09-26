"""Allow ``python -m fluidmech``."""

import sys

from .cli import main

sys.exit(main())
