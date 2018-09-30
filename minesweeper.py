import random


class Cell:
    def __init__(self, coords):
        self.num_adjacent_mines = 0
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.coords = coords

    def get_visual_representation(self):
        if self.flagged:
            return "[F]"
        if not self.revealed:
            return "[ ]"
        elif self.is_mine:
            return "[*]"
        else:
            return "[{}]".format(self.num_adjacent_mines)

    def __str__(self):
        return str(self.coords)

    def __repr__(self):
        return self.__str__()


class Game:
    def __init__(self, num_rows=8, num_cols=8, num_mines=10):
        # TODO: Throw exception when num_mines >= num_cells or set num_mines to be one less than the product.

        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_mines = num_mines
        self.board = []
        self.__make_board()

    def play(self):
        self.__print_board()
        while True:
            user_input = self.__get_input()
            cell = user_input['cell']
            if not cell:
                print('Bye!')
                break
            if user_input['flag']:
                cell.flagged = not cell.flagged
            else:
                cell.revealed = True
                if cell.is_mine:
                    self.__print_board()
                    print('AHHH!')
                    break
                elif cell.num_adjacent_mines == 0:
                    self.__reveal_cells_around_zero(cell)
            self.__print_board()

    def __make_board(self):
        all_cells = []

        for row_index in range(self.num_rows):
            row = []
            self.board.append(row)
            for col_index in range(self.num_cols):
                cell = Cell((row_index, col_index))
                row.append(cell)
                all_cells.append(cell)

        for cell in random.sample(all_cells, self.num_mines):
            cell.is_mine = True

        for row_index in range(len(self.board)):
            for col_index in range(len(self.board[row_index])):
                cell = self.board[row_index][col_index]
                if cell.is_mine:
                    continue
                adjacent_cells = self._get_adjacent_cells(cell)
                cell.num_adjacent_mines = sum(cell.is_mine for cell in adjacent_cells)

    def __reveal_cells_around_zero(self, cell):
        adjacent_cells = self._get_adjacent_cells(cell)
        for adjacent_cell in adjacent_cells:
            was_revealed_before = adjacent_cell.revealed
            adjacent_cell.revealed = True
            if adjacent_cell.num_adjacent_mines == 0 and not was_revealed_before:
                self.__reveal_cells_around_zero(adjacent_cell)

    def __get_input(self):
        coord_string = input(
            'Coordinates, please! x,y format, starting with 0,0. To flag, put "f" first: f0,0. (q to quit)\n'
        )
        while True:
            flag = False
            try:
                if coord_string == 'q':
                    return None
                else:
                    if coord_string[0] == 'f':
                        flag = True
                        coord_string = coord_string[1:]
                    coords = [int(i.strip()) for i in coord_string.split(',')]
                    cell = self.board[coords[0]][coords[1]]
                    if cell.flagged and not flag:
                        coord_string = input('Can\'t reveal a flagged cell. Try again.\n')
                    else:
                        return {'cell': self.board[coords[0]][coords[1]], 'flag': flag, 'coords': coords}
            except:
                coord_string = input('INVALID COORDINATES. Try again.\n')

    def __print_board(self):
        for row in self.board:
            print(''.join([cell.get_visual_representation() for cell in row]))

    def _get_adjacent_cells(self, cell):
        adjacent_cells = []
        for row_diff in [-1, 0, 1]:
            for col_diff in [-1, 0, 1]:
                target_cell_coords = (cell.coords[0] + row_diff, cell.coords[1] + col_diff)
                # Don't look outside of the board.
                if (target_cell_coords[0] < 0 or target_cell_coords[0] >= self.num_rows or
                    target_cell_coords[1] < 0 or target_cell_coords[1] >= self.num_cols):
                    continue
                # Skip current cell.
                if row_diff == 0 and col_diff == 0:
                    continue
                adjacent_cells.append(self.board[target_cell_coords[0]][target_cell_coords[1]])
        return adjacent_cells


Game(num_rows=8, num_cols=8, num_mines=10).play()
