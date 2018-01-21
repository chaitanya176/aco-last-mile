#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:28:44 2017

@author: Chaitanya
"""
import time
import math
import argparse
import sys
from datetime import timedelta

from pants import World, Edge
from pants import Solver

# Real-world latitude longitude coordinates.
TEST_COORDS_38 = [
                 [40.489806,-78.403319],
                 [40.808499,-77.895752],
                 [40.803390,-77.883049],
                 [40.792134,-77.867813],
                 [40.800097,-77.867198],
                 [40.831305,-77.843047],
                 [40.823346,-77.874715],
                 [40.814783,-77.854642],
                 [40.808623,-77.855536],
                 [40.807439,-77.856156],
                 [40.803221,-77.861796],
                 [40.803845,-77.865218],
                 [40.797601,-77.866382],
                 [40.793705,-77.868122],
                 [40.792065,-77.863437],
                 [40.793436,-77.860714],
                 [40.793360,-77.859769],
                 [40.798125,-77.855862],
                 [40.798464,-77.855829],
                 [40.794870,-77.860170],
                 [40.794759,-77.860740],
                 [40.793323,-77.862671],
                 [40.779583,-77.879468],
                 [40.773129,-77.856234],
                 [40.778888,-77.853733],
                 [40.780296,-77.850761],
                 [40.783378,-77.837776],
                 [40.783824,-77.827286],
                 [40.785654,-77.834790],
                 [40.798522,-77.860419],
                 [40.804293,-77.854620],
                 [40.801510,-77.861751],
                 [40.799695,-77.869574],
                 [40.798525,-77.870421],
                 [40.797015,-77.870886],
                 [40.797324,-77.868361],
                 [40.813198,-77.906811],
                 [40.832941,-77.800758]
]

# 45-45-90 triangle with unit length legs.
TEST_COORDS_3 = [
    (0, 0), (1, 0), (0, 1)
]

# Unit square with diagonals.
TEST_COORDS_4 = [
    (0, 0), (1, 0), (0, 1), (1, 1)
]

# Same as above except with additional node in center of left edge.
TEST_COORDS_5 = [
    (0, 0), (1, 0), (0, 1), (1, 1), (0, 0.5)
]


def dist(a, b):
    """Return the distance between two points represeted as a 2-tuple."""
    return math.sqrt((a[1] - b[1]) ** 2 + (a[0] - b[0]) ** 2)

def run_demo(nodes, *args, **kwargs):
    world = World(nodes, dist)
    solver = Solver(**kwargs)

    solver_setting_report_format = "\n".join([
        "Solver settings:",
        "limit={w.limit}",
        "rho={w.rho}, Q={w.q}",
        "alpha={w.alpha}, beta={w.beta}",
        "elite={w.elite}"
        ])

    print(solver_setting_report_format.format(w=solver))

    columns = "{!s:<25}\t{:<25}"
    divider = "-" * (25 + 25)
    header = columns.format("Time Elapsed", "Distance")
    columns = columns.replace('<', '>', 1)

    print()
    print(header)
    print(divider)

    fastest = None
    start_time = time.time()
    for i, ant in enumerate(solver.solutions(world)):
        fastest = ant
        fastest_time = timedelta(seconds=(time.time() - start_time))
        print(columns.format(fastest_time, ant.distance))
    total_time = timedelta(seconds=(time.time() - start_time))

    print(divider)
    print("Best solution:")
    for i, n in zip(fastest.visited, fastest.tour):
        print("  {:>8} = {}".format(i, n))

    print("Solution length: {}".format(fastest.distance))
    print("Found at {} out of {} seconds.".format(fastest_time, total_time))


if __name__ == '__main__':
    epilog = "\n".join([
        'For best results:',
        '  * 0.5 <= A <= 1',
        '  * 1.0 <= B <= 5',
        '  * A < B',
        '  * L >= 2000',
        '  * N > 1',
        '',
        ('For more information, please visit '
            'https://github.com/rhgrant10/Pants.')
        ])

    parser = argparse.ArgumentParser(
        description='Script that demos the ACO-Pants package.',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version='%(prog)s 0.5.1',
        )
    parser.add_argument(
        '-a', '--alpha',
        type=float, default=1,
        help='relative importance placed on pheromones; default=%(default)s',
        metavar='A'
        )
    parser.add_argument(
        '-b', '--beta',
        type=float, default=3,
        help='relative importance placed on distances; default=%(default)s',
        metavar='B'
        )
    parser.add_argument(
        '-l', '--limit',
        type=int, default=100,
        help='number of iterations to perform; default=%(default)s',
        metavar='L'
        )
    parser.add_argument(
        '-p', '--rho',
        type=float, default=0.4,
        help=('ratio of evaporated pheromone (0 <= P <= 1); '
            'default=%(default)s'),
        metavar='P'
        )
    parser.add_argument(
        '-e', '--elite',
        type=float, default=0.5,
        help='ratio of elite ant\'s pheromone; default=%(default)s',
        metavar='E'
        )
    parser.add_argument(
        '-q', '--Q',
        type=float, default=1,
        help=('total pheromone capacity of each ant (Q > 0); '
            'default=%(default)s'),
        metavar='Q'
        )
    parser.add_argument(
        '-t', '--t0',
        type=float, default=0.01,
        help=('initial amount of pheromone on every edge (T > 0); '
            'default=%(default)s'),
        metavar='T'
        )
    parser.add_argument(
        '-c', '--count', dest='ant_count',
        type=int, default=10,
        help=('number of ants used in each iteration (N > 0); '
            'default=%(default)s'),
        metavar='N'
        )
    parser.add_argument(
        '-d', '--dataset',
        type=int, default=38, choices=[3, 4, 5, 38],
        help='specify a particular set of demo data; default=%(default)s',
        metavar='D'
        )

    args = parser.parse_args()

    nodes = {
        3: TEST_COORDS_3,
        4: TEST_COORDS_4,
        5: TEST_COORDS_5,
        38: TEST_COORDS_38
    }[args.dataset]

    run_demo(nodes, **args.__dict__)
