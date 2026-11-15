"""OECD Model Tax Convention on Income and on Capital (2017 text, with 2025 Commentary update where relevant).

Source: OECD (2017), Model Tax Convention on Income and on Capital: Condensed Version 2017, OECD Publishing, Paris;
2025 Update approved by the OECD Council on 18 November 2025 (mainly Commentary changes).

Bilateral treaties depart from the Model, often substantially. Pass a ``TreatyProfile`` with the actual
treaty's figures; the default reproduces the Model.
"""

from . import provisions, rules  # noqa: F401  (registers provisions and rules)
from .rules import TreatyProfile  # noqa: F401
