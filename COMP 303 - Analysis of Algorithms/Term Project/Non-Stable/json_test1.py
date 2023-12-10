# Made by: Group 3 => Bogdan Itsam Dorantes-Nikolaev, Ahmet Yasir Beydili, Sena Gungormez, Doruk Gungormez
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import json

# Add a flag to indicate if the algorithm should stop
should_stop = False

# Add data structure to store moves for JSON export
move_data = []

# Recursive Tower of Hanoi Algorithm
def recursive_hanoi(n, source, target, auxiliary):
    if n > 0:
        recursive_hanoi(n - 1, source, auxiliary, target)
        move = {"moveNumber": len(move_data) + 1, "disk": n, "fromPole": source, "toPole": target}
        move_data.append(move)
        output_text.insert(tk.END, f"Move disk {n} from {source} to {target}\\n")
        update_movements_count()
        recursive_hanoi(n - 1, auxiliary, target, source)

# Iterative Tower of Hanoi Algorithm
def iterative_hanoi(n, source, target, auxiliary):
    # Initialization of pole states
    poles = {source: list(range(n, 0, -1)), auxiliary: [], target: []}

    # Function to make a legal move between two poles
    def make_legal_move(pole1, pole2):
        if not poles[pole1]:
            poles[pole1].append(poles[pole2].pop())
        elif not poles[pole2]:
            poles[pole2].append(poles[pole1].pop())
        elif poles[pole1][-1] > poles[pole2][-1]:
            poles[pole1].append(poles[pole2].pop())
        else:
            poles[pole2].append(poles[pole1].pop())
        move = {"moveNumber": len(move_data) + 1, "disk": poles[pole2][-1], "fromPole": pole1, "toPole": pole2}
        move_data.append(move)
        output_text.insert(tk.END, f"Move disk {poles[pole2][-1]} from {pole1} to {pole2}\\n")

    total_moves = 2 ** n - 1
    for i in range(total_moves):
        if i % 3 == 0:
            make_legal_move(source, target)
        elif i % 3 == 1:
            make_legal_move(source, auxiliary)
        elif i % 3 == 2:
            make_legal_move(auxiliary, target)

# Update the movements count on the GUI
def update_movements_count():
    current_count = int(movements_count_label["text"])
    movements_count_label.config(text=str(current_count + 1))

# Start the algorithm based on the selected method
def start_algorithm():
    global start_time
    start_time = time.time()
    move_data.clear()
    output_text.delete('1.0', tk.END)
    movements_count_label.config(text="0")
    num_disks_value = num_disks.get()
    if method_var.get() == 'Recursive':
        threading.Thread(target=recursive_hanoi, args=(num_disks_value, 'A', 'C', 'B')).start()
    else:
        threading.Thread(target=iterative_hanoi, args=(num_disks_value, 'A', 'C', 'B')).start()

# Function to export the moves to a JSON file
def export_to_json():
    if messagebox.askyesno("Export to JSON", "Do you want to export the results to a JSON file?"):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = {
                "towerOfHanoi": {
                    "numDisks": num_disks.get(),
                    "moves": move_data,
                    "totalMoves": len(move_data),
                    "runtimeInSeconds": round(time.time() - start_time, 2)
                }
            }
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

# Creating the main window
window = tk.Tk()
window.title("Tower of Hanoi")

# Creating the frame for controls
controls_frame = tk.Frame(window)
controls_frame.pack(side=tk.TOP, pady=(5, 0))

# Number of disks control
tk.Label(controls_frame, text="Number of disks:").pack(side=tk.LEFT)
num_disks = tk.Scale(controls_frame, from_=1, to=10, orient=tk.HORIZONTAL)
num_disks.pack(side=tk.LEFT)

# Method selection radio buttons
method_var = tk.StringVar()
method_var.set("Recursive")
tk.Radiobutton(controls_frame, text="Recursive", variable=method_var, value="Recursive").pack(side=tk.LEFT)
tk.Radiobutton(controls_frame, text="Iterative", variable=method_var, value="Iterative").pack(side=tk.LEFT)

# Start button
tk.Button(controls_frame, text="Start", command=start_algorithm).pack(side=tk.LEFT)

# Output text area
output_text = tk.Text(window, height=15, width=50)
output_text.pack(pady=(5, 0))

# Movements count label
movements_count_label = tk.Label(window, text="0")
movements_count_label.pack()

# Run the main event loop
window.mainloop()

# At the end of the algorithm execution (both recursive and iterative), call the export_to_json function
export_to_json()
