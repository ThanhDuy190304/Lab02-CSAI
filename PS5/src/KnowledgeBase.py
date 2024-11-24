import numpy as np
from numpy.typing import NDArray

class Literal:

    def __init__(self, symbol:str, is_negation: bool = False):
        self.symbol = symbol
        self.is_negation = is_negation
    
    def __str__(self):
        if self.is_negation:
            return f"-{self.symbol}"
        return self.symbol

    def __eq__(self, other) -> bool:
        return self.symbol == other.symbol and self.is_negation == other.is_negation
    
    def __hash__(self):
        return hash((self.symbol, self.is_negation))
    
    def negate(self):
        return Literal(self.symbol, not self.is_negation)

    @staticmethod
    def is_opposite(clause1, clause2):
        return clause1.symbol == clause2.symbol and clause1.is_negation != clause2.is_negation


class Clause:

    def __init__(self):
        self.literals = np.array([], dtype=Literal)

    def __eq__(self, other) -> bool:
        if len(self.literals) != len(other.literals):
            return False
        for literal1, literal2 in zip(self.literals, other.literals):
            if literal1 != literal2:
                return False
        return True
    
    def __hash__(self):
        return hash(frozenset(self.literals))

    def __str__(self): 
        if len(self.literals) == 0:
            return "{}"  
        literals_str = " OR ".join(str(literal) for literal in self.literals)
        return f"{literals_str}"
    
    def add(self, literal: Literal):
        self.literals = np.append(self.literals, literal)

    @staticmethod
    def convert_str_to_clause(str_clause: str):
        new_clause = Clause()
        str_literals = str_clause.split('OR')
        literals = []

        for str_literal in str_literals:
            str_literal = str_literal.strip()
            is_negation = str_literal.startswith("-")
            symbol = str_literal.lstrip("-")
            literal = Literal(symbol, is_negation)
            literals.append(literal)
        
        literals.sort(key=lambda literal: (literal.symbol, literal.is_negation))

        for literal in literals:
            new_clause.add(literal)
        
        return new_clause
    
    def remove(self, literal: Literal):
        filtered_literals = [lit for lit in self.literals if lit != literal]
        new_clause = Clause()
        new_clause.literals = np.array(filtered_literals, dtype=Literal)
        return new_clause

    @staticmethod
    def mergeClauses(clause1, clause2):
        if clause1 is None:
            clause1 = Clause()  
        if clause2 is None:
            clause2 = Clause() 
        new_clause = Clause()
        combined_literals = np.concatenate((clause1.literals, clause2.literals))  
        unique_literals = sorted(set(combined_literals), key=lambda x: (x.symbol, x.is_negation)) 
        new_clause.literals = np.array(unique_literals, dtype=Literal)
        return new_clause
    
    def is_empty(self):
        return self.literals.size == 0
    
    def is_meaningless(self):
        for i in range(len(self.literals)):
            for j in range(i + 1, len(self.literals)):
                if Literal.is_opposite(self.literals[i], self.literals[j]):
                    return True  
        return False



class KnowledgeBase:
    
    def __init__(self):
        self.clauses = np.array([], dtype=Clause)

    def add(self, clause: Clause):
        self.clauses = np.append(self.clauses, clause)

    def build_KnowledgeBase(self, clauses:NDArray[np.str_]):

        for str_clause in clauses:
            clause = Clause.convert_str_to_clause(str_clause)
            self.add(clause)
        




