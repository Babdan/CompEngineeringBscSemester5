# Made by: Group 3 => Bogdan Itsam Dorantes-Nikolaev, Ahmet Yasir Beydili, Sena Gungormez, Doruk Gungormez
import tkinter as tk
import threading
import time

# Add a flag to indicate if the algorithm should stop
should_stop = False

# Recursive Tower of Hanoi Algorithm
def recursive_hanoi(n, source, target, auxiliary):
    if n > 0:
        recursive_hanoi(n - 1, source, auxiliary, target)
        output_text.insert(tk.END, f"Move disk {n} from {source} to {target}\n")
        update_movements_count()
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
    global should_stop
    if not should_stop:
        output_text.insert(tk.END, f"Move disk from {fp} to {tp}\n")
        update_movements_count()
    else:
        update_loading_label("Algorithm execution stopped", "red")

def update_movements_count():
    movements_count.set(int(movements_count.get()) + 1)

def stop_algorithm():
    global should_stop
    should_stop = True
    update_loading_label("Algorithm execution stopped", "red")

# Thread Function for Algorithm Execution
def execute_algorithm():
    global should_stop

    try:
        num_discs = int(discs_entry.get())
        if num_discs <= 0:
            raise ValueError("Number of discs should be a positive integer")
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

        loading_label.config(text="Algorithm execution completed")
        update_loading_label("Algorithm execution completed")

        if should_stop:
            update_loading_label("Algorithm execution stopped", "red")
            should_stop = False  # Reset the flag

    except ValueError as ve:
        error_message = "Invalid input for number of discs"
        loading_label.config(text=error_message)
        update_loading_label(error_message, "red")
        output_text.insert(tk.END, f"Error: {ve}\n")
        print(f"Error occurred: {ve}")

    except Exception as e:
        error_message = "Algorithm execution stopped/encountered an error"
        loading_label.config(text=error_message)
        update_loading_label(error_message, "red")
        output_text.insert(tk.END, f"Error: {e}\n")
        print(f"Error occurred: {e}")

# UI Functions
def run_algorithm():
    global algorithm_thread
    if algorithm_thread is None or not algorithm_thread.is_alive():
        update_loading_label("Running algorithm...")
        loading_label.config(text="Running algorithm...")
        algorithm_thread = threading.Thread(target=execute_algorithm)
        algorithm_thread.start()
    else:
        update_loading_label("Algorithm is already running")
        loading_label.config(text="Algorithm is already running")

def update_movements_count_label():
    count_label.config(text=f"Total Movements: {movements_count.get()}")

def update_runtime_label(time_taken):
    runtime_label.config(text=f"Runtime: {time_taken:.6f} seconds")

def update_loading_label(status, color="green"):
    loading_label.config(text=status, bg=color)

root = tk.Tk()
root.title("Tower of Hanoi (BETA2.0 With Threading)")

algorithm_choice = tk.StringVar()
algorithm_choice.set("Recursive")

algorithm_frame = tk.Frame(root)
algorithm_frame.pack()

tk.Label(algorithm_frame, text="Select Algorithm:").pack()
tk.Radiobutton(algorithm_frame, text="Recursive", variable=algorithm_choice, value="Recursive").pack()
tk.Radiobutton(algorithm_frame, text="Iterative", variable=algorithm_choice, value="Iterative").pack()

loading_label = tk.Label(root, text="Ready to run algorithm", bg="green")
loading_label.pack()

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

output_text = tk.Text(output_frame, height=10, width=60)
output_text.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

movements_count = tk.StringVar()
movements_count.set(0)
count_label = tk.Label(root, text="Total Movements: 0")
count_label.pack()

stop_button = tk.Button(root, text="Stop Algorithm", command=stop_algorithm)
stop_button.pack()

made_by_label = tk.Label(root, text="Made by: Group 3\nBogdan Dorantes, Yasir Beydili, Sena Gungormez, Doruk Gungormez")
made_by_label.pack()

algorithm_thread = None

root.mainloop()
