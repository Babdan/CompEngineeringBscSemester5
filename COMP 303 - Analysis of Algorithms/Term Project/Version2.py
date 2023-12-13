# COMP303: «Analysis of Algorithms» Term Project, Instructor: Dr. Yassine Drias
# Made by: Group 3 => Bogdan Itsam Dorantes-Nikolaev, Ahmet Yasir Beydili, Sena Gungormez, Doruk Gungormez

# This program is a GUI application that demonstrates the Tower of Hanoi problem.
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
    # Initialization of pole states
    poles = {source: list(range(n, 0, -1)), auxiliary: [], target: []}

    # Function to make a legal move between two poles
    def make_legal_move(pole1, pole2):
        if not poles[pole1]:
            poles[pole1].append(poles[pole2].pop())
            output_text.insert(tk.END, f"Move disk {poles[pole1][-1]} from {pole2} to {pole1}\n")
        elif not poles[pole2]:
            poles[pole2].append(poles[pole1].pop())
            output_text.insert(tk.END, f"Move disk {poles[pole2][-1]} from {pole1} to {pole2}\n")
        elif poles[pole1][-1] > poles[pole2][-1]:
            poles[pole1].append(poles[pole2].pop())
            output_text.insert(tk.END, f"Move disk {poles[pole1][-1]} from {pole2} to {pole1}\n")
        else:
            poles[pole2].append(poles[pole1].pop())
            output_text.insert(tk.END, f"Move disk {poles[pole2][-1]} from {pole1} to {pole2}\n")
        update_movements_count()

    moves_required = 2 ** n - 1
    for i in range(1, moves_required + 1):
        if i % 3 == 1:
            make_legal_move(source, target)
        elif i % 3 == 2:
            make_legal_move(source, auxiliary)
        else:
            make_legal_move(auxiliary, target)


# Function to move disks between poles
def move_disks_between_poles(fp, tp, poles):
    global should_stop
    if not should_stop:
        disk = poles[fp].pop()
        poles[tp].append(disk)
        output_text.insert(tk.END, f"Move disk {disk} from {fp} to {tp}\n")
        update_movements_count()
    else:
        update_loading_label("Algorithm execution stopped", "red")


# Function to move top disk between two poles
def update_movements_count():
    movements_count.set(int(movements_count.get()) + 1)


# Function to stop algorithm execution
def stop_algorithm():
    global should_stop
    should_stop = True
    update_loading_label("Algorithm execution stopped", "red")


# Thread Function for Algorithm Execution
def execute_algorithm():
    global should_stop
    # Check if the number of discs is valid
    try:
        num_discs = int(discs_entry.get())
        if num_discs <= 0:
            # Raise an exception if the number of discs is not a positive integer
            raise ValueError("Number of discs should be a positive integer")
        selected_algorithm = algorithm_choice.get()     # Get the selected algorithm
        output_text.delete(1.0, tk.END)  # Clear previous output
        movements_count.set(0)  # Reset movements count

        start_time = time.time()  # Start time measurement

        if selected_algorithm == "Recursive":
            recursive_hanoi(num_discs, 'A', 'C', 'B')
        elif selected_algorithm == "Iterative":
            iterative_hanoi(num_discs, 'A', 'C', 'B')

        end_time = time.time()  # End time measurement
        execution_time = end_time - start_time  # Calculate execution time

        update_movements_count_label()  # Update movements count label
        update_runtime_label(execution_time)    # Update runtime label

        loading_label.config(text="Algorithm execution completed")
        update_loading_label("Algorithm execution completed")

        if should_stop: # Check if the algorithm was stopped
            update_loading_label("Algorithm execution stopped", "red")  # Update loading label
            should_stop = False  # Reset the flag

    except ValueError as ve:    # Catch the ValueError exception
        error_message = "Invalid input for number of discs"
        loading_label.config(text=error_message)
        update_loading_label(error_message, "red")
        output_text.insert(tk.END, f"Error: {ve}\n")
        print(f"Error occurred: {ve}")

    except Exception as e:  # Catch any other exception
        error_message = "Algorithm execution stopped/encountered an error"
        loading_label.config(text=error_message)
        update_loading_label(error_message, "red")
        output_text.insert(tk.END, f"Error: {e}\n")
        print(f"Error occurred: {e}")


# UI Functions
def run_algorithm():
    global algorithm_thread
    if algorithm_thread is None or not algorithm_thread.is_alive():     # Check if the algorithm is already running
        update_loading_label("Running algorithm...")    # Update loading label
        loading_label.config(text="Running algorithm...")
        algorithm_thread = threading.Thread(target=execute_algorithm)   # Create a new thread for algorithm execution
        algorithm_thread.start()    # Start the thread
    else:   # If the algorithm is already running
        update_loading_label("Algorithm is already running")
        loading_label.config(text="Algorithm is already running")


# Function to update movements count label
def update_movements_count_label():
    count_label.config(text=f"Total Movements: {movements_count.get()}")


# Function to update runtime label
def update_runtime_label(time_taken):
    runtime_label.config(text=f"Runtime: {time_taken:.6f} seconds")


# Function to update loading label
def update_loading_label(status, color="green"):
    loading_label.config(text=status, bg=color)


# Main Window
root = tk.Tk()
root.title("Tower of Hanoi V2.0")   # Set window title

algorithm_choice = tk.StringVar()   # Variable to store the selected algorithm
algorithm_choice.set("Recursive")   # Set default algorithm to Recursive

algorithm_frame = tk.Frame(root)    # Frame to store algorithm selection
algorithm_frame.pack()              # Pack the frame

tk.Label(algorithm_frame, text="Select Algorithm:").pack()  # Label for algorithm selection
tk.Radiobutton(algorithm_frame, text="Recursive", variable=algorithm_choice, value="Recursive").pack()
tk.Radiobutton(algorithm_frame, text="Iterative", variable=algorithm_choice, value="Iterative").pack()

loading_label = tk.Label(root, text="Ready to run algorithm", bg="green")   # Label to show algorithm status
loading_label.pack()

runtime_label = tk.Label(root, text="Runtime: 0.000000 seconds")    # Label to show algorithm runtime
runtime_label.pack()

discs_frame = tk.Frame(root)    # Frame to store number of discs input
discs_frame.pack()

tk.Label(discs_frame, text="Number of Discs:").pack()   # Label for number of discs input
discs_entry = tk.Entry(discs_frame)                     # Entry for number of discs input
discs_entry.pack()

tk.Button(root, text="Run Algorithm", command=run_algorithm).pack()   # Button to run algorithm

output_frame = tk.Frame(root)
output_frame.pack()

output_label = tk.Label(output_frame, text="Output:")   # Label for output
output_label.pack()

output_text = tk.Text(output_frame, height=10, width=60)    # Text widget for output
output_text.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(output_frame, command=output_text.yview)   # Scrollbar for output
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)                    # Configure scrollbar

movements_count = tk.StringVar()    # Variable to store the number of movements
movements_count.set(0)              # Set default value to 0
count_label = tk.Label(root, text="Total Movements: 0")   # Label to show the number of movements
count_label.pack()

stop_button = tk.Button(root, text="Stop Algorithm", command=stop_algorithm)    # Button to stop algorithm execution
stop_button.pack()

made_by_label = tk.Label(root, text="COMP303: «Analysis of Algorithms» Term Project By: Group 3\nBogdan Dorantes, Yasir Beydili, Sena Gungormez, Doruk Gungormez")  # Label to show the group members
made_by_label.pack()

algorithm_thread = None    # Variable to store the algorithm thread

root.mainloop()    # Start the main loop
