#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List

@dataclass
class Ability():
    """
    API Class for unit abilities.
    """
    id: str
    name: str
    description: str
    tooltip: str
    iconPath: str
    aoe: int
    bounces: int
    cooldown: int
    damage: int
    duration: int

    def __repr__(self):
        return f"Ability<{self.name}>"

    def __hash__(self):
        return hash(self.id)


@dataclass
class Unit():
    """
    API Class for units.
    """
    id: str
    name: str
    legion: str
    description: str
    tooltip: str
    iconPath: str
    armorType: str
    attackType: str
    attackSpeed: str
    range: int
    attackMode: str
    moveSpeed: int
    moveSpeedDescription: str
    moveType: str
    upgradesTo: List[str]
    goldCost: int
    mythiumCost: int
    totalValue: int
    dps: float
    hp: int
    mana: int
    income: int
    bounty: int
    abilities: List[Ability]

    def __repr__(self):
        return f"Unit<{self.name}>"

    def __hash__(self):
        return hash(self.id)


class LocationBox():
    """
    These boxes will usually be 24x24 - the size of the icons in LTD2.
    They represent the location and size of an object found in an image.

    X = Width = Left/Right.
    Y = Height = Up/Down.
    """
    def __init__(self, x_offset, y_offset, x_size, y_size):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.x_size = x_size
        self.y_size = y_size

    def __repr__(self):
        return f"Box<({self.x_offset},{self.y_offset})>"
