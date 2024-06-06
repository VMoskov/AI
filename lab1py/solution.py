import argparse
from DataLoader import DataLoader
from algorithms.BFS import BFS
from algorithms.UCS import UCS
from algorithms.ASTAR import ASTAR


def parse_arguments():
    args = argparse.ArgumentParser()
    args.add_argument('--alg', type=str, help='Search algorithm to use')
    args.add_argument('--ss', type=str, help='Search space path')
    args.add_argument('--h', type=str, help='Heuristic function path')
    args.add_argument('--check-optimistic', action='store_true', help='Check if heuristic is optimistic')
    args.add_argument('--check-consistent', action='store_true', help='Check if heuristic is consistent')
    return args.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    data_loader = DataLoader(args.ss)

    if args.alg == 'bfs':
        start, goal, nodes = data_loader.load_plain_data()
        bfs = BFS(start, goal, nodes)
        bfs.search()
        print(bfs)

    if args.alg == 'ucs':
        start, goal, nodes = data_loader.load_weighted_data()
        ucs = UCS(start, goal, nodes)
        ucs.search()
        print(ucs)

    if args.alg == 'astar' or args.check_optimistic or args.check_consistent:
        data_loader.heuristic_path = args.h
        start, goal, nodes = data_loader.load_weighted_data()
        heuristic = data_loader.load_heuristic()

        for state in nodes:
            nodes[state].set_heuristics(heuristic)

        astar = ASTAR(start, goal, nodes, path=args.h)
        astar.search()
        if args.alg == 'astar':
            print(astar)

        if args.check_optimistic:
            astar.check_optimistic()
        if args.check_consistent:
            astar.check_consistent()
