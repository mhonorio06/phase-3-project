#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.waterfall import Waterfall
from models.country import Country

def reset_database():
    Waterfall.drop_table()
    Country.drop_table()
    Country.create_table()
    Waterfall.create_table()
    

breakpoint()