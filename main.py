import tkinter as tk
from tkinter import messagebox

class SimplexMethod:
    def __init__(self, root):
        self.root = root
        self.root.title("Simplex Method")
        self.root.geometry("500x500")  # Setting initial window size

        self.create_interface()

    def create_interface(self):
        # Creating a frame for better structure
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=5)

        # Title label
        title_label = tk.Label(self.main_frame, text="Simplex Method", font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)

        # Labels and Entry for user input
        labels = ["Infantry Cost:", "Cavalry Cost:", "Knight Cost:",
                  "Infantry Training Time (hours):", "Cavalry Training Time (hours):", "Knight Training Time (hours):",
                  "Enemy Soldiers:", "Training Days:"]
        self.entries = []

        for label_text in labels:
            label = tk.Label(self.main_frame, text=label_text, font=('Arial', 10))
            label.pack()
            entry = tk.Entry(self.main_frame)
            entry.pack()
            self.entries.append(entry)

        solve_button = tk.Button(self.main_frame, text="Solve", command=self.solve_task, bg='green', fg='white', font=('Arial', 12))
        solve_button.pack(pady=20)

    def solve_task(self):
        try:
            user_input = [float(entry.get()) for entry in self.entries]
            result = self.simplex(*user_input)
            self.display_result(result, user_input)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical values.")

    def simplex(self, infantry_cost, cavalry_cost, knight_cost, infantry_time, cavalry_time, knight_time, enemy_soldiers, training_time):
        table = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [1, -(infantry_time + knight_time * 3), 1, 0, infantry_cost + knight_cost * 3],
            [1, -(cavalry_time + knight_time * 3), 0, 1, cavalry_cost + knight_cost * 3],
            [-enemy_soldiers / 2, training_time, 0, 0]
        ]
        basis = [2, 3]
        while True:
            pivot_col = min(table[-1])
            if pivot_col >= 0:
                break
            pivot_col_ind = table[-1].index(pivot_col)
            min_ratio = float('inf')
            pivot_row_ind = -1
            for i in range(1, len(table) - 1):
                if table[i][pivot_col_ind] > 0:
                    ratio = table[i][-1] / table[i][pivot_col_ind]
                    if ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row_ind = i
            pivot_element = table[pivot_row_ind][pivot_col_ind]
            index_in_basis = basis.index(pivot_row_ind)
            basis[index_in_basis] = pivot_col_ind
            table[basis[index_in_basis]] = table[pivot_row_ind]
            table[pivot_row_ind] = [0, 0, 0, 0, 0]
            pivot_row_ind = basis[index_in_basis]
            table1 = table.copy()
            for i in range(len(table[pivot_row_ind])):
                table[pivot_row_ind][i] /= pivot_element
            for i in range(len(table)):
                if i != pivot_row_ind and i in basis or i == 4:
                    for j in range(len(table[i])):
                        if i != 4 and j in basis:
                            if j == pivot_col_ind:
                                table[i][j] = 0
                            else:
                                table[i][j] = 1
                        else:
                            table[i][j] = table1[i][j] - (table1[i][pivot_col_ind] * table1[pivot_row_ind][j]) / pivot_element
        return table

    def display_result(self, result, user_input):
        result_window = tk.Toplevel(self.root)
        result_window.geometry("100x100")
        result_window.title("Result")
        minimalized = (user_input[6] / 2) * result[0][4] - user_input[7] * result[1][4]
        infantry_amount = result[4][2]
        cavalry_amount = result[4][3]
        knight_amount = 3 * (infantry_amount + cavalry_amount)

        result_label = tk.Label(result_window, text=f"Minimal Cost: {minimalized}\n"
                                                  f"Infantry Quantity: {infantry_amount}\n"
                                                  f"Cavalry Quantity: {cavalry_amount}\n"
                                                  f"Knight Quantity: {knight_amount}\n")
        result_label.pack()

def main():
    root = tk.Tk()
    simplex_method = SimplexMethod(root)
    root.mainloop()

if __name__ == "__main__":
    main()
