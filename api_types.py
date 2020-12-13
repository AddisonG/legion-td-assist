#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List

@dataclass
class Ability():
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


@dataclass
class Unit():
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
