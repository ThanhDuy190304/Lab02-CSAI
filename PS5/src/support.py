from typing import Tuple
from itertools import combinations
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
from KnowledgeBase import Clause, Literal, KnowledgeBase

input_path = Path("./input.txt")
output_path = Path("./output.txt")


def read_file(file_path: Path) -> Tuple[str, NDArray[np.str_]]:
    with file_path.open("r") as file:
        alpha = file.readline().strip()
        num_clause = int(file.readline().strip())
        clauses = np.array([file.readline().strip() for _ in range(num_clause)], dtype=str)
    return alpha, clauses


def write_file(file_path: Path, content: list):
    with file_path.open("w") as file:
        for line in content:
            file.write(f"{line}\n")

def process_alpha(alpha: str) -> NDArray[np.object_]:
    clauses = []
    str_literals = alpha.split('OR')
    for str_literal in str_literals:
        str_literal = str_literal.strip()
        is_negation = str_literal.startswith("-")
        symbol = str_literal.lstrip("-")
        literal = Literal(symbol, is_negation)
        clause = Clause()
        clause.add(literal.negate())  # Thêm literal đã phủ định vào clause
        clauses.append(clause)
    return np.array(clauses, dtype=Clause)

def PL_Resolve(clause1: Clause, clause2: Clause):
    resolvents = set()
    for literal1 in clause1.literals:
        for literal2 in clause2.literals:
            if Literal.is_opposite(literal1, literal2):
                new_clause1 = clause1.remove(literal1)
                new_clause2 = clause2.remove(literal2)
                new_clause = Clause.mergeClauses(new_clause1, new_clause2)
                if new_clause.is_empty():
                    return resolvents, True
                if new_clause.is_meaningless():
                    continue
                resolvents.add(new_clause)
    
    return resolvents, False


def PL_Resolution(kb: KnowledgeBase, alpha: str):
    processed_alpha_clauses = process_alpha(alpha)
    
    for clause in processed_alpha_clauses:
        kb.add(clause)

    clauses = set(kb.clauses) 
    new = set()
    processed_pairs = set()
    output_lines = []  
    has_empty = False

    while True:        
        for clause1, clause2 in combinations(clauses, 2):   
            pair = frozenset([clause1, clause2])
            if pair not in processed_pairs:
                processed_pairs.add(pair)
                resolvents, has_empty_clause = PL_Resolve(clause1, clause2)
                if has_empty_clause:
                    has_empty = True 
                    continue  
                new.update(resolvents)   

        if(has_empty):
            new = new - clauses
            output_lines.append(len(new) + 1)
            for clause in new:
                output_lines.append(str(clause))
            output_lines.append('{}')
            output_lines.append("YES")          
            return output_lines  
        
        elif new.issubset(clauses):
            output_lines.append(0)
            output_lines.append("NO")
            return output_lines
        
        new = new - clauses 
        output_lines.append(len(new))
        for clause in new:
            output_lines.append(str(clause))
         
        clauses.update(new) 
        new.clear()


def main():
    input_path = Path("./input.txt")
    output_path = Path("./output.txt")

    alpha, clauses = read_file(input_path)

    kb = KnowledgeBase()
    kb.build_KnowledgeBase(clauses)

    output = PL_Resolution(kb, alpha)
    write_file(output_path, output)



