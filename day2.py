import re
import numpy as np
from functools import reduce
from collections import namedtuple
from helpers import get_input_lines

GameHistory = namedtuple("GameHistory", ("ndx", "records"))
Record = namedtuple("Record", ("blue", "green", "red"))

def parse_input_line(line: str) -> GameHistory:
    """Parse complete line of input"""
    game_str, record_str = line.split(":")
    return GameHistory(
        ndx=int(re.search(r"\d+", game_str).group()),
        records=[parse_record_game_history(r) for r in record_str.split(";")],
    )


def parse_record_game_history(record_str: str) -> Record:
    """Parse the record history associated with a game"""
    d = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }

    for c in record_str.split(","):
        num_str, color = c.split()
        d[color.strip()] = int(num_str)
    return Record(**d)


def is_valid_solution(max_balls: Record, potential_solution: Record) -> bool:
    """Return whether a potential_solution can be satisfied by the set
    of balls described by max_balls"""
    return (
        max_balls.green >= potential_solution.green
        and max_balls.red >= potential_solution.red
        and max_balls.blue >= potential_solution.blue
    )

def calculate_max_balls_lower_bound(records: Record) -> Record:
    """Calculate the minimal red/blue/green ballset such that all the
    records will be valid solutions"""

    return Record(*np.array(records).max(axis=0))


def main():
    lines = get_input_lines("day2")

    game_records = [parse_input_line(l) for l in lines]

    # Problem 1:
    # Sum of the indexes for all games in which every trial record in that
    # game's history constitutes a valid solution

    max_balls = Record(red=12, green=13, blue=14)
    p1 = sum(
        [
            game.ndx
            for game in game_records
            if np.all([is_valid_solution(max_balls, r) for r in game.records])
        ]
    )

    # Problem 2
    # For each game record calculate the smallest ball group (x, y, z) satisfying
    # the games, calculate x * y * z.  Take the sum over all games.
    p2 = sum(
        [
            reduce(lambda x, y: x * y, calculate_max_balls_lower_bound(game.records))
            for game in game_records
        ]
    )

    print(p1)
    print(p2)

    return



if __name__ == '__main__':
    main()
