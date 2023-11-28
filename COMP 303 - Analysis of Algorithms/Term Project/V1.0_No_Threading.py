import tkinter as tk
import time

# Recursive Tower of Hanoi Algorithm
def recursive_hanoi(n, source, target, auxiliary):
    if n > 0:
        # Move n - 1 discs from source to auxiliary, using target as auxiliary
        recursive_hanoi(n - 1, source, auxiliary, target)

        # Update output and movements count
        output_text.insert(tk.END, f"Move disk {n} from {source} to {target}\n")
        update_movements_count()

        # Move the n - 1 discs from auxiliary to target, using source as auxiliary
        recursive_hanoi(n - 1, auxiliary, target, source)


# Iterative Tower of Hanoi Algorithm
def iterative_hanoi(n, source, target, auxiliary):
    if n % 2 == 0:
        auxiliary, target = target, auxiliary

    for i in range(1, 2 ** n):
        if i % 3 == 1:
            move_disks_between_poles(source, target)
        elif i % 3 == 2:
            move_disks_between_poles(source, auxiliary)
        else:
            move_disks_between_poles(auxiliary, target)


def move_disks_between_poles(fp, tp):
    output_text.insert(tk.END, f"Move disk from {fp} to {tp}\n")
    update_movements_count()


def update_movements_count():
    movements_count.set(int(movements_count.get()) + 1)


# UI Functions
def run_algorithm():
    num_discs = int(discs_entry.get())
    selected_algorithm = algorithm_choice.get()
    output_text.delete(1.0, tk.END)  # Clear previous output
    movements_count.set(0)  # Reset movements count

    start_time = time.time()  # Start time measurement

    if selected_algorithm == "Recursive":
        recursive_hanoi(num_discs, 'A', 'C', 'B')
    elif selected_algorithm == "Iterative":
        iterative_hanoi(num_discs, 'A', 'C', 'B')

    end_time = time.time()  # End time measurement
    execution_time = end_time - start_time

    update_movements_count_label()
    update_runtime_label(execution_time)
def update_movements_count_label():
    count_label.config(text=f"Total Movements: {movements_count.get()}")

def update_runtime_label(time_taken):
    runtime_label.config(text=f"Runtime: {time_taken:.6f} seconds")

# Creating the UI
root = tk.Tk()
root.title("Tower of Hanoi (V1.0 No Threading)")

algorithm_choice = tk.StringVar()
algorithm_choice.set("Recursive")

algorithm_frame = tk.Frame(root)
algorithm_frame.pack()

tk.Label(algorithm_frame, text="Select Algorithm:").pack()
tk.Radiobutton(algorithm_frame, text="Recursive", variable=algorithm_choice, value="Recursive").pack()
tk.Radiobutton(algorithm_frame, text="Iterative", variable=algorithm_choice, value="Iterative").pack()

runtime_label = tk.Label(root, text="Runtime: 0.000000 seconds")
runtime_label.pack()

discs_frame = tk.Frame(root)
discs_frame.pack()

tk.Label(discs_frame, text="Number of Discs:").pack()
discs_entry = tk.Entry(discs_frame)
discs_entry.pack()

tk.Button(root, text="Run Algorithm", command=run_algorithm).pack()

output_frame = tk.Frame(root)
output_frame.pack()

output_label = tk.Label(output_frame, text="Output:")
output_label.pack()

output_text = tk.Text(output_frame, height=10, width=50)
output_text.pack()

movements_count = tk.StringVar()
movements_count.set(0)
count_label = tk.Label(root, text="Total Movements: 0")
count_label.pack()

made_by_label = tk.Label(root, text="Made by: Group 3\nBogdan Dorantes, Yasir Beydili, Sena Gungormez, Doruk Gungormez")
made_by_label.pack()

root.mainloop()
