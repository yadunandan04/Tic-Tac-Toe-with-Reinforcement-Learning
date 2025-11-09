import tkinter as tk
from tkinter import messagebox, ttk
import random
import pickle

# ---------------- RL AGENT CLASS ----------------
class QLearningAgent:
    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_state_key(self, state):
        return ''.join(state)

    def choose_action(self, state, available_actions, greedy=False):
        key = self.get_state_key(state)
        if random.random() < self.epsilon and not greedy:
            return random.choice(available_actions)
        q_values = [self.q_table.get((key, a), 0) for a in available_actions]
        max_q = max(q_values)
        best_actions = [a for a, q in zip(available_actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        key = self.get_state_key(state)
        next_key = self.get_state_key(next_state)
        old_q = self.q_table.get((key, action), 0)
        if done:
            target = reward
        else:
            future_q = max([self.q_table.get((next_key, a), 0) for a in range(9)], default=0)
            target = reward + self.gamma * future_q
        self.q_table[(key, action)] = old_q + self.alpha * (target - old_q)


    


# ---------------- GAME CLASS ----------------
class TicTacToeRL:
    def __init__(self, root):
        self.root = root
        self.root.title("🕹️ Tic-Tac-Toe RL (Retro Arcade Edition)")
        self.root.configure(bg="#111")

        self.agent = QLearningAgent()
        self.player_symbol = "X"
        self.agent_symbol = "O"
        self.current_player = "X"
        self.difficulty = "Easy"

        self.buttons = []
        self.state = [" " for _ in range(9)]

        self.build_ui()

    def build_ui(self):
        style = ttk.Style()
        style.configure("TButton", font=("Press Start 2P", 10), padding=10, relief="flat")
        style.map("TButton", background=[("active", "#0ff")], foreground=[("active", "black")])

        tk.Label(self.root, text="Tic-Tac-Toe RL", font=("Press Start 2P", 16), fg="#0ff", bg="#111").grid(row=0, column=0, columnspan=4, pady=10)

        # Game grid
        grid_frame = tk.Frame(self.root, bg="#111")
        grid_frame.grid(row=1, column=0, padx=20, pady=20)
        for i in range(9):
            btn = tk.Button(grid_frame, text=" ", font=("Consolas", 32, "bold"), width=3, height=1,
                            bg="#333", fg="white", relief="flat", command=lambda i=i: self.make_move(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        # Controls frame
        control_frame = tk.Frame(self.root, bg="#111")
        control_frame.grid(row=1, column=1, sticky="n")

        tk.Label(control_frame, text="Difficulty:", font=("Press Start 2P", 8), fg="#0ff", bg="#111").pack(pady=5)
        for diff in ["Easy", "Medium", "Hard"]:
            ttk.Radiobutton(control_frame, text=diff, value=diff, variable=tk.StringVar(value=self.difficulty),
                            command=lambda d=diff: self.set_difficulty(d)).pack(anchor="w", pady=2)

        tk.Label(control_frame, text="Play as:", font=("Press Start 2P", 8), fg="#0ff", bg="#111").pack(pady=10)
        self.symbol_choice = tk.StringVar(value="X")
        ttk.Radiobutton(control_frame, text="X", variable=self.symbol_choice, value="X", command=self.set_symbol).pack(anchor="w")
        ttk.Radiobutton(control_frame, text="O", variable=self.symbol_choice, value="O", command=self.set_symbol).pack(anchor="w")

        ttk.Button(control_frame, text="New Game", command=self.new_game).pack(pady=8)
        ttk.Button(control_frame, text="Train Agent", command=self.open_training_popup).pack(pady=8)

        ttk.Button(control_frame, text="Save Q-Table", command=self.save_qtable).pack(pady=8)
        ttk.Button(control_frame, text="Load Q-Table", command=self.load_qtable).pack(pady=8)
        ttk.Button(control_frame, text="Reset Q-Table", command=self.reset_qtable).pack(pady=8)

        self.status_label = tk.Label(self.root, text="Your turn!", font=("Press Start 2P", 8), fg="#0f0", bg="#111")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

    # ------------------- GAME LOGIC -------------------
    def set_difficulty(self, diff):
        self.difficulty = diff
        self.status_label.config(text=f"Difficulty: {diff}")

    def set_symbol(self):
        self.player_symbol = self.symbol_choice.get()
        self.agent_symbol = "O" if self.player_symbol == "X" else "X"
        self.new_game()

    def new_game(self):
        """Reset the board and start a new round."""
        self.state = [" " for _ in range(9)]
        self.current_player = "X"
        for b in self.buttons:
            b.config(text=" ", bg="#333", state="normal")  # <-- re-enable buttons

        self.status_label.config(text=f"Your turn! ({self.player_symbol})", fg="#0f0")

        if self.player_symbol == "O":
            # if player chose O, agent starts first
            self.root.after(500, self.agent_move)

        if self.player_symbol == "O":
            self.root.after(500, self.agent_move)

    def available_actions(self):
        return [i for i, s in enumerate(self.state) if s == " "]

    def make_move(self, index):
        if self.state[index] != " " or self.current_player != self.player_symbol:
            return
        self.state[index] = self.player_symbol
        self.buttons[index].config(text=self.player_symbol, fg="#0ff")
        if self.check_winner(self.player_symbol):
            self.end_game("You win! 🏆")
            return
        elif " " not in self.state:
            self.end_game("Draw! 🤝")
            return
        self.current_player = self.agent_symbol
        self.root.after(400, self.agent_move)

    def agent_move(self):
        actions = self.available_actions()
        if not actions:
            return
        if self.difficulty == "Easy":
            move = random.choice(actions)
        elif self.difficulty == "Medium":
            move = self.agent.choose_action(self.state, actions)
        else:
            move = self.agent.choose_action(self.state, actions, greedy=True)
        self.state[move] = self.agent_symbol
        self.buttons[move].config(text=self.agent_symbol, fg="#f00")

        if self.check_winner(self.agent_symbol):
            self.end_game("Agent wins! 💀")
        elif " " not in self.state:
            self.end_game("Draw! 🤝")
        else:
            self.current_player = self.player_symbol

    def check_winner(self, symbol):
        combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for (a,b,c) in combos:
            if self.state[a] == self.state[b] == self.state[c] == symbol:
                for i in (a,b,c):
                    self.buttons[i].config(bg="#0f0")
                return True
        return False

    def end_game(self, message):
        """Display game result and stop automatic restart."""
        self.status_label.config(text=message)
        for b in self.buttons:
            b.config(state="disabled")  # prevent further clicks

    # ---------------- RL TRAINING ----------------
    
    def open_training_popup(self):
        """Popup window to set training parameters."""
        popup = tk.Toplevel(self.root)
        popup.title("⚙️ Train RL Agent")
        popup.configure(bg="#111")
        popup.geometry("320x300")
        popup.resizable(False, False)

        tk.Label(popup, text="Train Reinforcement Agent", font=("Press Start 2P", 10),
                 fg="#0ff", bg="#111").pack(pady=10)

        # --- Parameter fields ---
        tk.Label(popup, text="Episodes:", font=("Consolas", 11), fg="white", bg="#111").pack()
        episodes_entry = tk.Entry(popup, font=("Consolas", 11), justify="center")
        episodes_entry.insert(0, "10000")
        episodes_entry.pack(pady=5)

        tk.Label(popup, text="Learning rate (alpha):", font=("Consolas", 11), fg="white", bg="#111").pack()
        alpha_entry = tk.Entry(popup, font=("Consolas", 11), justify="center")
        alpha_entry.insert(0, str(self.agent.alpha))
        alpha_entry.pack(pady=5)

        tk.Label(popup, text="Discount factor (gamma):", font=("Consolas", 11), fg="white", bg="#111").pack()
        gamma_entry = tk.Entry(popup, font=("Consolas", 11), justify="center")
        gamma_entry.insert(0, str(self.agent.gamma))
        gamma_entry.pack(pady=5)

        tk.Label(popup, text="Exploration rate (epsilon):", font=("Consolas", 11), fg="white", bg="#111").pack()
        epsilon_entry = tk.Entry(popup, font=("Consolas", 11), justify="center")
        epsilon_entry.insert(0, str(self.agent.epsilon))
        epsilon_entry.pack(pady=5)

        def start_training():
            try:
                episodes = int(episodes_entry.get())
                self.agent.alpha = float(alpha_entry.get())
                self.agent.gamma = float(gamma_entry.get())
                self.agent.epsilon = float(epsilon_entry.get())
                popup.destroy()
                self.train_agent(episodes)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values!")

        ttk.Button(popup, text="Start Training", command=start_training).pack(pady=15)

    def train_agent(self, episodes=10000):
        """Train the RL agent using self-play for a given number of episodes."""
        for ep in range(episodes):
            state = [" " for _ in range(9)]
            current = "X"
            done = False

            while not done:
                actions = [i for i, s in enumerate(state) if s == " "]
                if not actions:
                    break

                action = self.agent.choose_action(state, actions)
                state[action] = current

                # Check for winner or draw
                if self.check_static_winner(state, current):
                    reward = 1 if current == "O" else -1
                    done = True
                elif " " not in state:
                    reward = 0.5
                    done = True
                else:
                    reward = 0
                    current = "O" if current == "X" else "X"

                # Update the Q-table
                self.agent.update(state, action, reward, state, done)

            # Optional live progress update
            if ep % 1000 == 0:
                self.status_label.config(text=f"Training... {ep}/{episodes}")
                self.root.update_idletasks()

        messagebox.showinfo("Training", f"Agent training completed ({episodes} episodes)!")
        self.status_label.config(text="Training complete ✅")


    def check_static_winner(self, s, symbol):
        combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(s[a] == s[b] == s[c] == symbol for a,b,c in combos)

    # ---------------- FILE OPS ----------------
    def save_qtable(self):
        with open("qtable.pkl", "wb") as f:
            pickle.dump(self.agent.q_table, f)
        messagebox.showinfo("Saved", "Q-table saved successfully!")

    def load_qtable(self):
        try:
            with open("qtable.pkl", "rb") as f:
                self.agent.q_table = pickle.load(f)
            messagebox.showinfo("Loaded", "Q-table loaded!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No Q-table file found.")

    def reset_qtable(self):
        self.agent.q_table = {}
        messagebox.showinfo("Reset", "Q-table cleared!")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    try:
        import pyglet
        pyglet.font.add_file("PressStart2P-Regular.ttf")  # Optional retro font
    except:
        pass
    root = tk.Tk()
    app = TicTacToeRL(root)
    root.mainloop()
