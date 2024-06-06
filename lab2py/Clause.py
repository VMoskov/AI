class Clause:
    counter = 0

    def __init__(self, index, clause=None, literals=None, parents=None):
        self.clause = clause.lower() if clause else ' v '.join(str(literal) for literal in literals)
        self.clause = self.clause.upper() if self.clause == 'nil' else self.clause
        self.literals = literals if literals else frozenset(clause.lower().split(' v '))
        self.parents = parents
        self.index = index

    def __str__(self):
        return (f'{self.index}. {self.clause}' +
                (f' ({self.parents[0].index}, {self.parents[1].index})' if self.parents else ''))

    @staticmethod
    def negate(clause):
        """Negate a clause."""
        literals = {f'~{literal}' if not literal.startswith('~') else literal[1:] for literal in clause.literals}
        return [Clause(index=Clause.counter + i, literals=frozenset([literal])) for i, literal in enumerate(literals)]

    @staticmethod
    def pl_resolution(input_clauses, goal):
        """PL-Resolution algorithm for propositional logic."""
        input_clauses = Clause.simplify(input_clauses)
        new_clauses = set()
        sos = set(goal)
        Clause.counter = len(input_clauses) + len(sos) + 1
        last = None

        while True:
            pairs = [(ci, cj) for ci in sos for cj in input_clauses | sos if ci != cj]
            for c1, c2 in pairs:
                resolvent = Clause.resolve(c1, c2)
                last = resolvent if resolvent else last

                if resolvent is None:
                    return True, Clause(index=Clause.counter, clause='NIL', parents=(c1, c2))
                if isinstance(resolvent, set):
                    continue

                new_clauses.add(resolvent)
                new_clauses = Clause.simplify(new_clauses)
                Clause.counter += 1

            if new_clauses.issubset(sos):
                return False, last if len(new_clauses) > 0 else None

            sos |= new_clauses

    @staticmethod
    def resolve(c1, c2):
        """Resolve two clauses."""
        for literal in c1.literals:
            complement = f'~{literal}' if not literal.startswith('~') else literal[1:]
            if complement in c2.literals:
                resolvent = (c1.literals | c2.literals) - {literal, complement}
                if not resolvent:
                    return None
                return Clause(index=Clause.counter, literals=resolvent, parents=(c1, c2))
        return set()

    @staticmethod
    def simplify(clauses):
        """Remove redundant clauses."""
        simplified = set()
        for clause in clauses:
            if not Clause.is_superset(clause, simplified) and not Clause.is_tautology(clause):
                simplified.add(clause)
        return simplified

    @staticmethod
    def is_superset(clause, clauses):
        """Check if a clause is a subset of any clause in the list."""
        return any(clause.literals.issuperset(c.literals) for c in clauses)

    @staticmethod
    def is_tautology(clause):
        """Check if a clause is a tautology."""
        return any(f'~{literal}' in clause.literals for literal in clause.literals)

    @staticmethod
    def trace(clause, path=None):
        """Trace back the resolution steps."""
        if path is None:
            path = []
        path.append(clause) if clause not in path else None
        if clause.parents:
            parent1, parent2 = clause.parents
            path = Clause.trace(parent1, path)
            path = Clause.trace(parent2, path)
        return sorted(path, key=lambda x: x.index)
