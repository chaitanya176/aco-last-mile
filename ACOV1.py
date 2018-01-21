#!/usr/bin/env python
import time
import math
import argparse
from datetime import timedelta
from pants import World, Edge
from pants import Solver

ADD_COORDS_38 = [
[40.808499,-77.895752],
[40.803390,-77.883049],
[40.792134,-77.867813],
[40.800097,-77.867198],
[40.831305,-77.843047],
[40.823346,-77.874715],
[40.814783,-77.854642],
[40.808623,-77.855536],
[40.812196,-77.856102],
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
[40.832941,-77.800758],
]

def distance(x, y):
    return math.sqrt((x[1] - y[1]) ** 2 + (x[0] - y[0]) ** 2)

def run_args(dnodes, *args, **kwargs):
    world = World(dnodes, distance)
    solver = Solver(**kwargs)

    solver_format = "\n".join([
        "solver:",
        "lim={w.limit}",
        "rho={w.rho}, Q={w.q}",
        "alpha={w.alpha}, beta={w.beta}",
        "elite={w.elite}"
        ])

    print(solver_format.format(w=solver))

    col = "{!s:<26}\t{:<26}"
    div = "-" * (26 + 26)
    head = col.format("Time taken", "Distance covered")
    col = col.replace('<', '>', 1)

    print()
    print(head)
    print(div)

    fast = None
    start_t= time.time()
    for x, ant in enumerate(solver.solutions(world)):
        fast= ant
        fast_time = timedelta(seconds=(time.time() - start_t))
        print(col.format(fast_time, ant.distance))
    total_t = timedelta(seconds=(time.time() - start_t))

    print(div)
    print("best sol:")
    for x, n in zip(fast.visited, fast.tour):
        print("  {:>9} = {}".format(x, n))

    print("Sol value: {}".format(fast.distance))
    print("found at  {} out of {} sec.".format(fast_time, total_t))


if __name__ == '__main__':
    epilog = "\n".join([
        '  * 0.5 <= alpha <= 1',
        ])

    dnodes = {
        38: ADD_COORDS_38
    }[args.dataset]

    run_args(dnodes, **args.__dict__)