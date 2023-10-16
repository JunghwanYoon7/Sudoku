import random
import wx
import ctypes
app = wx.App()


class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Sudoku', size=(430, 430))
        self.panel = wx.Panel(self)
        spacer = 0
        self.generate_btn = wx.Button(self.panel, label='Generate Board', size=(100, 30), pos=(300, 35))
        solve_btn = wx.Button(self.panel, label=' Auto solve board', size=(100, 30), pos=(300, 70))
        # start of the program , setting the values of the square,
        self.grid_size = 3
        total_number = 9
        self.count = 0
        self.arr = []

        # for loop that creates the sudoku board as a 4d array

        ##______________________________________________________________________________________________________________________

        self.generate_btn.Bind(wx.EVT_BUTTON, self.on_generate_press)
    def on_generate_press(self, *args):
        block_row_start = 5
        block_column_start = 5

        # start of iteration through board
        for r in range(3):
            for c in range(3):
                # start of iteration through block
                unit_row = block_row_start
                unit_column = block_column_start
                for i in range(3):
                    unit_row = block_row_start
                    for j in range(3):
                        self.text_ctrl = wx.TextCtrl(self.panel, size=(30, 30), pos=(unit_row, unit_column))
                        self.text_ctrl.SetValue(str(self.arr[r][c][i][j]))
                        unit_row += 30
                    unit_column += 30
                block_row_start += 95
            block_row_start = 5
            block_column_start += 95

        self.Show()

    def generate_arr(self):
        for i in range(self.grid_size):
            column = []
            for k in range(self.grid_size):
                column.append(create_blank())
                self.count += 1
            self.arr.append(column)
        coordinate_list = []
        for r in range(3):
            for c in range(3):
                coordinate_list.append([r, c])
        ##______________________________________________________________________________________________________________________
        for r in range(3):
            for c in range(3):
                # pass through coordinates and check block
                self.arr[r][c] = check_block(self.arr, coordinate_list, r, c, 0)

        for i in range(self.grid_size):
            for k in range(3):
                line = ""
                for j in range(self.grid_size):
                    line += str(self.arr[i][j][k])
        for i in range(self.grid_size):
            for k in range(3):
                line = ""
                for j in range(self.grid_size):
                    line += str(self.arr[i][j][k])
                print(line)
        generate_blank_spaces(self.arr)

        empty_spot_list = []

        for r in range(3):
            for c in range(3):
                for i in range(3):
                    for j in range(3):
                        if self.arr[r][c][i][j] == 0:
                            empty_spot_list.append([r, c, i, j])
        return self.arr


def board_solver(arr, empty_spots, coordinate_list, q, w, recurs):
    anchor_r = q
    anchor_c = w
    p = []

    for i in range(len(empty_spots)):
        if empty_spots[i][0] == q and empty_spots[i][1] == w:
            p.append(empty_spots[i])

    randomlol = p

    if recurs > 5:
        z = []
        for r in range(3):
            for c in range(3):
                z.append([r, c])
        current = z.index([q, w]) + 1
        for k in range(len(empty_spots)):
            arr[empty_spots[k][0]][empty_spots[k][1]][empty_spots[k][2]][empty_spots[k][3]] = 0
        for i in range(current):
            recurs_r = z[i][0]
            recurs_c = z[i][1]
            arr[recurs_r][recurs_c] = board_solver(arr, empty_spots, coordinate_list, recurs_r, recurs_c, 0)

    for l in range(len(p)):
        r = p[l][0]
        c = p[l][1]
        i = p[l][2]
        j = p[l][3]
        return_value = return_valid_value(arr, r, c, i, j)
        if return_value == False:
            recurs += 1
            for k in range(len(p)):
                arr[p[k][0]][p[k][1]][p[k][2]][p[k][3]] = 0
            arr[p[k][0]][p[k][1]] = board_solver(arr, empty_spots, coordinate_list, p[k][0], p[k][1], recurs)
        else:
            arr[r][c][i][j] = return_value

    return arr[q][w]


def create_blank():
    # creates the blank blocks to fill out the sudoku board
    create_blank_block = []
    for i in range(3):
        col = []
        for k in range(3):
            col.append(0)
        create_blank_block.append(col)
    return create_blank_block


def return_valid_value(arr, q, w, e, r):
    # setting the values for where the method has to check for values
    anchor_r = q
    anchor_c = w
    anchor_i = e
    anchor_j = r

    # creates a list of valid numbers that the method will take out
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # checks if there is already a number in the space , if there is a number return the number
    if arr[q][w][e][r] == 0:
        # this loop checks if the row matches up with the unit and takes out numbers from "list" that already exist
        # in the row
        for r in range(3):
            if r == anchor_r:
                for c in range(3):
                    for i in range(3):
                        if anchor_i == i:
                            for j in range(3):
                                if int(arr[r][c][i][j]) in list:
                                    list.remove(int(arr[r][c][i][j]))
        # this loop checks if the column matches up with the unit and takes out numbers from "list" that already exist in the column
        for r in range(3):
            for c in range(3):
                if c == anchor_c:
                    for i in range(3):
                        for j in range(3):
                            if j == anchor_j:
                                if int(arr[r][c][i][j]) in list:
                                    list.remove(int(arr[r][c][i][j]))
        # same condition as before
        for i in range(3):
            for j in range(3):
                if int(arr[q][w][i][j]) in list:
                    list.remove(int(arr[q][w][i][j]))
        if len(list) == 0:
            return False
        return random.choice(list)
    else:
        return arr[q][w][e][r]


def create_seed():
    # creates a seed for the sudoku board to build off of
    create_row_column = []
    count = 0
    random_order = random.sample(range(1, 10), 9)
    for i in range(3):
        col = []
        for k in range(3):
            col.append(random_order[count])
            count += 1
        create_row_column.append(col)
    return create_row_column


def check_block(arr, coordinate, q, w, recurs):
    anchor_r = q
    anchor_c = w
    p = []
    if recurs > 3:
        anchor_coord = (int(coordinate.index([q, w]) - 1))
        prev_r = coordinate[anchor_coord][0]
        prev_c = coordinate[anchor_coord][1]
        arr[prev_r][prev_c] = create_blank()
        for i in range(3):
            for j in range(3):
                arr[prev_r][prev_c] = check_block(arr, coordinate, prev_r, prev_c, 0)

    for i in range(3):
        for j in range(3):
            return_value = return_valid_value(arr, anchor_r, anchor_c, i, j)
            if return_value == False:
                recurs += 1
                arr[q][w] = create_blank()
                arr[q][w] = check_block(arr, coordinate, anchor_r, anchor_c, recurs)
            else:
                arr[anchor_r][anchor_c][i][j] = return_value
    return arr[q][w]


def generate_blank_spaces(arr):
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for r in range(3):
        for c in range(3):
            rand_range = random.randint(4, 7)
            out_list = random.sample(list, rand_range)
            for i in range(3):
                for j in range(3):
                    if arr[r][c][i][j] in out_list:
                        arr[r][c][i][j] = 0


def main():
    # start of the program , setting the values of the square,
    grid_size = 3
    total_number = 9
    count = 0
    arr = []
    # for loop that creates the sudoku board as a 4d array
    for i in range(grid_size):
        column = []
        for k in range(grid_size):
            column.append(create_blank())
            count += 1
        arr.append(column)
    for i in range(grid_size):
        for k in range(3):
            line = ""
            for j in range(grid_size):
                line += str(arr[i][j][k])
            print(line)
    print("________________________________________________________")
    coordinate_list = []
    for r in range(3):
        for c in range(3):
            coordinate_list.append([r, c])

    for r in range(3):
        for c in range(3):
            # pass through coordinates and check block
            arr[r][c] = check_block(arr, coordinate_list, r, c, 0)

    for i in range(grid_size):
        for k in range(3):
            line = ""
            for j in range(grid_size):
                line += str(arr[i][j][k])
            print(line)

    print("________________________________________________________")

    generate_blank_spaces(arr)

    for i in range(grid_size):
        for k in range(3):
            line = ""
            for j in range(grid_size):
                line += str(arr[i][j][k])
            print(line)

    empty_spot_list = []

    for r in range(3):
        for c in range(3):
            for i in range(3):
                for j in range(3):
                    if arr[r][c][i][j] == 0:
                        empty_spot_list.append([r, c, i, j])

    for r in range(3):
        for c in range(3):
            # pass through coordinates and check block
            solved = board_solver(arr, empty_spot_list, coordinate_list, r, c, 0)
            arr[r][c] = solved

    print("________________________________________________________")

    for i in range(grid_size):
        for k in range(3):
            line = ""
            for j in range(grid_size):
                line += str(arr[i][j][k])
            print(line)


if __name__ == "__main__":
    arr = []

    app = wx.App()
    frame = MyFrame()
    arr = frame.generate_arr()
    app.MainLoop()
    # main()
