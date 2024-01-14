import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
import socket


class UDPGame:
    def __init__(self, root):
        self.root = root
        self.client_seq = 1
        self.server_seq = 1
        self.client_ack = 0
        self.server_ack = 0
        self.packet_length = 0
        self.is_auto_mode = False
        self.timeout_duration = 0
        self.points = 3
        self.timeout_timer_id = None  # Timer ID to keep track of the timeout
        self.last_sent_packet = None  # Store the last sent packet
        self.response_received = False  # Flag to track if a response has been received
        self.setup_gui()

        # Create UDP sockets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(("127.0.0.1", 12345))  # Bind server socket to localhost and port 12345

    def setup_gui(self):
        self.points_label = tk.Label(self.root, text=f"Points: {self.points}", font=("Helvetica", 16))
        self.points_label.grid(row=0, column=0, columnspan=2)

        self.log_textbox = scrolledtext.ScrolledText(self.root, height=10, state='disabled')
        self.log_textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Frames for Client and Server
        self.client_frame = tk.LabelFrame(self.root, text="Client")
        self.client_frame.grid(row=2, column=0, padx=10, pady=10)

        self.server_frame = tk.LabelFrame(self.root, text="Server")
        self.server_frame.grid(row=2, column=1, padx=10, pady=10)

        # Client Widgets
        tk.Label(self.client_frame, text="SEQ Number:").grid(row=0, column=0)
        self.client_seq_label = tk.Label(self.client_frame, text="1")
        self.client_seq_label.grid(row=0, column=1)

        tk.Label(self.client_frame, text="ACK Number:").grid(row=1, column=0)
        self.client_ack_label = tk.Label(self.client_frame, text="0")
        self.client_ack_label.grid(row=1, column=1)

        self.send_button = tk.Button(self.client_frame, text="Send Packet", command=self.send_packet)
        self.send_button.grid(row=2, column=0, columnspan=2)

        # Server Widgets
        tk.Label(self.server_frame, text="SEQ Number:").grid(row=0, column=0)
        self.server_seq_label = tk.Label(self.server_frame, text="1")
        self.server_seq_label.grid(row=0, column=1)

        tk.Label(self.server_frame, text="ACK Number:").grid(row=1, column=0)
        self.server_ack_label = tk.Label(self.server_frame, text="0")
        self.server_ack_label.grid(row=1, column=1)

        self.auto_mode_check = tk.Checkbutton(self.server_frame, text="Automatic Mode", command=self.toggle_auto_mode)
        self.auto_mode_check.grid(row=2, column=0, columnspan=2)

        # Timeout Duration
        self.timeout_duration = simpledialog.askinteger("Timeout Duration", "Enter timeout duration in seconds:",
                                                        parent=self.root)

    def toggle_auto_mode(self):
        self.is_auto_mode = not self.is_auto_mode

    def log_packet(self, message, is_error=False):
        self.log_textbox.config(state='normal')
        if is_error:
            self.log_textbox.insert(tk.END, "ERROR: " + message + "\n", 'error')
        else:
            self.log_textbox.insert(tk.END, message + "\n")
        self.log_textbox.config(state='disabled')
        self.log_textbox.yview(tk.END)

    def update_points(self, points_change):
        self.points += points_change
        self.points_label.config(text=f"Points: {self.points}")
        if points_change > 0:
            self.points_label.config(bg='green')
        else:
            self.points_label.config(bg='red')

        if self.points < 0:
            messagebox.showinfo("Game Over", "Game over! Your points fell below zero.")
            self.root.destroy()

    def send_packet(self):
        packet_length = simpledialog.askinteger("Packet Length", "Enter packet length:", parent=self.root)
        if packet_length is None:
            return

        self.client_seq = (self.client_seq + packet_length) % 100
        self.client_ack = self.server_seq
        self.update_labels()

        packet_data = f"{self.client_seq},{self.client_ack},{packet_length}".encode()
        self.client_socket.sendto(packet_data, ("127.0.0.1", 12345))  # Send packet to server

        self.log_packet(f"Client sent packet: SEQ={self.client_seq}, ACK={self.client_ack}, Length={packet_length}")
        self.last_sent_packet = (self.client_seq, self.client_ack, packet_length)  # Store the last sent packet
        self.response_received = False  # Reset response flag

        if not self.is_auto_mode:
            # Schedule the new timeout immediately if not in automatic mode
            self.schedule_timeout()

        self.receive_packet(packet_length)

    def receive_packet(self, packet_length):
        if not self.is_auto_mode:
            # In manual mode, you can enter SEQ and ACK manually
            expected_server_seq = (self.server_seq + packet_length) % 100
            expected_server_ack = self.client_seq

            server_seq = simpledialog.askinteger("Server SEQ", "Enter server SEQ number:", parent=self.root)
            server_ack = simpledialog.askinteger("Server ACK", "Enter server ACK number:", parent=self.root)

            if server_seq is None or server_ack is None:
                return  # User cancelled

            if server_seq != expected_server_seq or server_ack != expected_server_ack:
                self.log_packet(
                    f"Incorrect Server Response: Expected SEQ={expected_server_seq}, ACK={expected_server_ack}, but got SEQ={server_seq}, ACK={server_ack}",
                    is_error=True)
                self.update_points(-1)
            else:
                self.server_seq = server_seq
                self.server_ack = server_ack
                self.update_labels()
                self.log_packet(
                    f"Server received packet: SEQ={self.server_seq}, ACK={self.server_ack}, Length={packet_length}")
                self.update_points(1)

        else:
            # In automatic mode, server responds automatically
            if self.is_auto_mode:
                self.server_seq = (self.server_seq + packet_length) % 100
                self.server_ack = self.client_seq
                self.response_received = True  # Set response flag
                self.update_labels()
                self.log_packet(
                    f"Server received packet: SEQ={self.server_seq}, ACK={self.server_ack}, Length={packet_length}")

            if not self.is_auto_mode:
                # If not in automatic mode, schedule the new timeout after server response
                self.schedule_timeout()

        self.response_received = True  # Set response flag

    def update_labels(self):
        self.client_seq_label.config(text=str(self.client_seq))
        self.client_ack_label.config(text=str(self.client_ack))
        self.server_seq_label.config(text=str(self.server_seq))
        self.server_ack_label.config(text=str(self.server_ack))

    def schedule_timeout(self):
        if self.timeout_timer_id:
            self.root.after_cancel(self.timeout_timer_id)
        self.timeout_timer_id = self.root.after(self.timeout_duration * 1000, self.timeout_handler)

    def timeout_handler(self):
        if not self.response_received:
            self.log_packet("Timeout occurred", is_error=True)
            self.update_points(-1)  # Deduct a point for a timeout

            # Resend the last sent packet
            if self.last_sent_packet:
                self.log_packet("Retransmitting packet...")
                self.receive_packet(self.last_sent_packet[2])  # Resend the same packet
                self.update_points(-1)  # Deduct a point for retransmission

        else:
            self.log_packet("Timeout occurred after server response", is_error=True)
            self.update_points(-1)  # Deduct a point for a timeout after server response

        self.schedule_timeout()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("UDP SEQ ACK Game")
    game = UDPGame(root)
    root.mainloop()
