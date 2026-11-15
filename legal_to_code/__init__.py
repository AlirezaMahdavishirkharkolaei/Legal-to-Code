"""Legal-to-Code: rules of international (economic) law as tested, traceable code."""

from .core import REGISTRY, RUBRIC, Codifiability, Provision, Result, rule  # noqa: F401
from .modules import linked, oecd_mtc, wto_dsu  # noqa: F401

__version__ = "0.1.0"
