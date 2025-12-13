import tkinter as tk
from tkinter import messagebox

class CacheLine:
    def __init__(self):
        self.block = None
        self.valid = False


class AssociativeCache:
    def __init__(self, size):
        self.cache = [CacheLine() for _ in range(size)]

    def access(self, block):
        for line in self.cache:
            if line.valid and line.block == block:
                return "HIT", "Block found by parallel tag comparison"

        for line in self.cache:
            if not line.valid:
                line.block = block
                line.valid = True
                return "MISS", "Placed in empty cache line"

        replaced = self.cache[0].block
        self.cache[0].block = block
        return "MISS", f"Cache full → replaced block {replaced}"


class SimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Associative Mapping Simulator")
        self.root.configure(bg="#f4f6f8")
        self.build_input_screen()

    def fit_to_content(self, widget):
        self.root.update_idletasks()
        w = widget.winfo_reqwidth() + 40
        h = widget.winfo_reqheight() + 40
        self.root.geometry(f"{w}x{h}")
        self.root.resizable(False, False)

    def build_input_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg="white", padx=50, pady=50)
        frame.pack()

        tk.Label(
            frame,
            text="Associative Mapping Cache Simulator",
            font=("Segoe UI", 24, "bold"),
            bg="white"
        ).pack(pady=30)

        tk.Label(frame, text="Cache Size",
                 font=("Segoe UI", 14), bg="white").pack(anchor="w")
        self.cache_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        self.cache_entry.pack(pady=10)

        tk.Label(frame, text="Block Access Sequence",
                 font=("Segoe UI", 14), bg="white").pack(anchor="w", pady=(20, 0))
        self.seq_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        self.seq_entry.pack(pady=10)

        tk.Button(
            frame,
            text="Run Simulation",
            font=("Segoe UI", 15, "bold"),
            bg="#2563eb",
            fg="white",
            padx=30,
            pady=12,
            command=self.start_simulation
        ).pack(pady=40)

        self.fit_to_content(frame)

    def start_simulation(self):
        try:
            size = int(self.cache_entry.get())
            self.sequence = list(map(int, self.seq_entry.get().split()))
        except:
            messagebox.showerror("Input Error", "Invalid input")
            return

        self.cache = AssociativeCache(size)
        self.step = 0
        self.build_simulation_screen()
        self.run_step()

    def build_simulation_screen(self):
        self.clear()

        container = tk.Frame(self.root, bg="#f4f6f8", padx=20, pady=20)
        container.pack()

        header = tk.Label(
            container,
            text="Associative Mapping – Live Simulation",
            font=("Segoe UI", 20, "bold"),
            bg="#1e293b",
            fg="white",
            pady=15
        )
        header.pack(fill="x")

        tk.Label(
            container,
            text="Access Sequence",
            font=("Segoe UI", 16, "bold"),
            bg="#f4f6f8"
        ).pack(pady=(20, 10))

        self.seq_frame = tk.Frame(container, bg="#f4f6f8")
        self.seq_frame.pack(pady=10)

        self.seq_labels = []
        for blk in self.sequence:
            lbl = tk.Label(
                self.seq_frame,
                text=str(blk),
                font=("Segoe UI", 14),
                width=4,
                height=2,
                relief="solid",
                bg="white"
            )
            lbl.pack(side="left", padx=6)
            self.seq_labels.append(lbl)

        self.status_label = tk.Label(
            container,
            font=("Segoe UI", 18, "bold"),
            bg="#f4f6f8"
        )
        self.status_label.pack(pady=20)

        self.action_label = tk.Label(
            container,
            font=("Segoe UI", 13),
            bg="#f4f6f8"
        )
        self.action_label.pack()

        self.table_frame = tk.Frame(container, bg="#f4f6f8")
        self.table_frame.pack(pady=30)

        self.draw_table()
        self.fit_to_content(container)

    def draw_table(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.table_frame,
            text="Cache Line",
            font=("Segoe UI", 14, "bold"),
            width=18,
            relief="solid"
        ).grid(row=0, column=0)

        tk.Label(
            self.table_frame,
            text="Stored Block",
            font=("Segoe UI", 14, "bold"),
            width=18,
            relief="solid"
        ).grid(row=0, column=1)

        for i, line in enumerate(self.cache.cache):
            tk.Label(
                self.table_frame,
                text=i,
                font=("Segoe UI", 13),
                width=18,
                relief="solid"
            ).grid(row=i+1, column=0)

            val = line.block if line.valid else "EMPTY"
            tk.Label(
                self.table_frame,
                text=val,
                font=("Segoe UI", 13),
                width=18,
                relief="solid"
            ).grid(row=i+1, column=1)

    def run_step(self):
        if self.step >= len(self.sequence):
            self.status_label.config(
                text="Simulation Completed",
                fg="#2563eb"
            )
            return

        for i, lbl in enumerate(self.seq_labels):
            if i < self.step:
                lbl.config(bg="#e5e7eb")
            elif i == self.step:
                lbl.config(bg="#93c5fd")
            else:
                lbl.config(bg="white")

        block = self.sequence[self.step]
        result, action = self.cache.access(block)

        color = "#16a34a" if result == "HIT" else "#dc2626"
        self.status_label.config(
            text=f"Accessing Block {block} → {result}",
            fg=color
        )
        self.action_label.config(text=action)

        self.draw_table()
        self.step += 1
        self.root.after(1200, self.run_step)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()


root = tk.Tk()
SimulatorGUI(root)
root.mainloop()
