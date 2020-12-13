#!/usr/bin/env python3

import csv

class CsvUnit():
    """
    Represents a player unit.
    """

    def __init__(self, row):
        """
        Initialise the unit using a row from a tsv, csv, table, etc.
        Derived from: https://beta.legiontd2.com/guide/units/
        """
        self.legion = row[0]
        self.tier = row[1]
        self.fighter = row[2]
        self.cost = row[3]
        self.value = row[4]
        self.range = row[5]
        self.dps = row[6]
        self.hp = row[7]
        self.dmg_type = row[8]
        self.def_type = row[9]
        if len(row) > 10:
            self.ability_1 = row[10]
        if len(row) > 11:
            self.ability_2 = row[11]

    def __repr__(self):
        return f"CsvUnit<{self.fighter}>"


def get_all_units():
    units = []
    with open("details.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            units.append(CsvUnit(row))
    return units
