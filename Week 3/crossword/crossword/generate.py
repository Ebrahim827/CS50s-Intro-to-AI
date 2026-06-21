import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )
        img.save(filename)

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.domains:
            words_to_remove = set()
            for word in self.domains[var]:
                if len(word) != var.length:
                    words_to_remove.add(word)
            for word in words_to_remove:
                self.domains[var].remove(word)

    def revise(self, x, y):
        revised = False
        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False

        i, j = overlap
        words_to_remove = set()

        for word_x in self.domains[x]:
            match_found = any(
                word_x[i] == word_y[j]
                for word_y in self.domains[y]
            )
            if not match_found:
                words_to_remove.add(word_x)
                revised = True

        for word in words_to_remove:
            self.domains[x].remove(word)

        return revised

    def ac3(self, arcs=None):
        if arcs is None:
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))
        else:
            queue = list(arcs)

        while queue:
            x, y = queue.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))

        return True

    def assignment_complete(self, assignment):
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False

        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        if word[i] != assignment[neighbor][j]:
                            return False

        return True

    def order_domain_values(self, var, assignment):
        def count_ruled_out(word):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        for neighbor_word in self.domains[neighbor]:
                            if word[i] != neighbor_word[j]:
                                count += 1
            return count

        return sorted(self.domains[var], key=count_ruled_out)

    def select_unassigned_variable(self, assignment):
        unassigned = [
            var for var in self.crossword.variables
            if var not in assignment
        ]

        return min(
            unassigned,
            key=lambda var: (
                len(self.domains[var]),
                -len(self.crossword.neighbors(var))
            )
        )

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for word in self.order_domain_values(var, assignment):
            assignment[var] = word

            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result

            del assignment[var]

        return None


def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()