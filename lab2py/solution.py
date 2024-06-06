from DataLoader import DataLoader
from Clause import Clause
from pathlib import Path
import argparse


def group_clauses(input_clauses):
    goal_clause = input_clauses[-1]
    Clause.counter = len(input_clauses)
    negate_goal_clause = Clause.negate(goal_clause)
    Clause.counter += len(negate_goal_clause)
    input_clauses = frozenset(input_clauses[:-1])
    return input_clauses, goal_clause, negate_goal_clause


def print_clauses(clauses):
    print('\n'.join([str(clause) for clause in sorted(clauses, key=lambda x: x.index)] + ['===============']))


def format_path(path, clauses):
    [setattr(clause, 'index', len(clauses) + idx + 1) for idx, clause in enumerate(path)]


def print_result(result, path, goal_clause):
    print('\n'.join([str(clause) for clause in path] + ['===============']))
    print(f'[CONCLUSION]: {goal_clause.clause} is {"true" if result else "unknown"}\n')


parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')

resolution_parser = subparser.add_parser('resolution')
resolution_parser.add_argument('resolution_path', type=str)

cooking_parser = subparser.add_parser('cooking')
cooking_parser.add_argument('cooking_path', type=str)
cooking_parser.add_argument('cooking_input_path', type=str)


if __name__ == '__main__':
    args = parser.parse_args()
    data_manager = DataLoader()

    if args.command == 'resolution':
        path = Path(args.resolution_path)
        data = data_manager.load_data(path)

        clauses = [Clause(index=idx + 1, clause=line) for idx, line in enumerate(data)]
        input_clauses, goal_clause, negate_goal_clause = group_clauses(clauses)
        print_clauses(input_clauses | set(negate_goal_clause))

        result, final_clause = Clause.pl_resolution(input_clauses, negate_goal_clause)
        path = Clause.trace(final_clause) if final_clause else []
        path = [clause for clause in path if clause not in input_clauses | set(negate_goal_clause)]

        format_path(path, clauses)
        print_result(result, path, goal_clause)

    if args.command == 'cooking':
        cooking_path = Path(args.cooking_path)
        cooking_input_path = Path(args.cooking_input_path)

        data = data_manager.load_data(cooking_path)
        input_data = data_manager.load_data(cooking_input_path)

        input_clauses = [Clause(index=idx + 1, clause=line) for idx, line in enumerate(data)]

        for line in input_data:
            Clause.counter = len(input_clauses) + 1
            new_clause = Clause(index=Clause.counter, clause=line[:-2])
            command = line[-1]
            print(f"User's command: {line}")

            if command == '?':
                negate_goal_clause = Clause.negate(new_clause)
                Clause.counter += len(negate_goal_clause)
                print_clauses(input_clauses + negate_goal_clause)

                result, final_clause = Clause.pl_resolution(input_clauses, negate_goal_clause)

                path = Clause.trace(final_clause) if final_clause else []

                path = [clause for clause in path if clause not in set(input_clauses) | set(negate_goal_clause)]

                format_path(path, input_clauses + negate_goal_clause)
                print_result(result, path, new_clause)

            elif command == '+':
                input_clauses.append(new_clause)
                print(f'added: {new_clause.clause}\n')

            elif command == '-':
                input_clauses = [clause for clause in input_clauses if clause.clause != new_clause.clause]
                [setattr(clause, 'index', idx + 1) for idx, clause in enumerate(input_clauses)]
                print(f'removed: {new_clause.clause}\n')
