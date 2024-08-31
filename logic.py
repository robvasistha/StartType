import time
import json
import tkinter as tk


class TypingTestLogic:
    def __init__(self, ui) -> None:
        self.ui = ui
        self.wpm_history = []
        self.raw_wpm_history = []
        self.correct_typed_chars = 0
        self.raw_typed_chars = 0

    def initialize_test(self) -> None:
        self.ui.current_word_index = 0
        self.ui.correct_chars = 0
        self.ui.total_chars = len(self.ui.current_text.replace(" ", ""))
        self.wpm_history = []
        self.raw_wpm_history = []
        self.correct_typed_chars = 0
        self.raw_typed_chars = 0
        self.ui.current_correctness = [""] * len(self.ui.current_text)

    def start_test_on_type(self, event=None) -> None:
        if self.ui.start_time is None:
            self.ui.start_time = time.time()
            self.update_timer()

    def update_displayed_text(self, event=None) -> None:
        if event.keysym == "space":
            self.update_wpm_history()
            typed_word = self.ui.entry.get().strip()

            if typed_word == self.ui.words[self.ui.current_word_index]:
                self.correct_typed_chars += len(typed_word) + 1  # +1 for the space
            self.raw_typed_chars += len(typed_word) + 1

            if self.ui.current_word_index < len(self.ui.words) - 1:
                self.ui.current_word_index += 1
                self.ui.entry.delete(0, tk.END)
            return

        typed_text = self.ui.entry.get()
        current_position = sum(len(word) + 1 for word in self.ui.words[:self.ui.current_word_index])

        for i, char in enumerate(typed_text):
            if current_position + i < len(self.ui.current_text):
                self.raw_typed_chars += 1
                if char == self.ui.current_text[current_position + i]:
                    self.ui.current_correctness[current_position + i] = "correct"
                else:
                    self.ui.current_correctness[current_position + i] = "incorrect"

        self.update_text_display()

        if current_position + len(typed_text) >= len(self.ui.current_text):
            self.calculate_results()

    def update_text_display(self) -> None:
        self.ui.text_display.config(state="normal")
        self.ui.text_display.delete("1.0", "end")

        for i, char in enumerate(self.ui.current_text):
            if self.ui.current_correctness[i] == "correct":
                self.ui.text_display.insert("end", char, ("correct",))
            elif self.ui.current_correctness[i] == "incorrect":
                self.ui.text_display.insert("end", char, ("incorrect",))
            else:
                self.ui.text_display.insert("end", char)

        self.ui.text_display.tag_configure("correct", foreground="green")
        self.ui.text_display.tag_configure("incorrect", foreground="red")
        self.ui.text_display.config(state="disabled")

    def update_timer(self) -> None:
        if self.ui.start_time:
            self.ui.time_elapsed = time.time() - self.ui.start_time
            self.ui.timer_label.config(text=f"Time: {int(self.ui.time_elapsed)}s")

            raw_wpm = (self.raw_typed_chars / 5) / (self.ui.time_elapsed / 60)
            self.ui.raw_wpm_label.config(text=f"Raw WPM: {raw_wpm:.2f}")

            wpm = (self.correct_typed_chars / 5) / (self.ui.time_elapsed / 60)
            self.ui.wpm_label.config(text=f"WPM: {wpm:.2f}")

            self.ui.root.after(1000, self.update_timer)

    def update_wpm_history(self) -> None:
        if self.ui.start_time:
            current_time = time.time() - self.ui.start_time
            raw_wpm = (self.raw_typed_chars / 5) / (current_time / 60)
            wpm = (self.correct_typed_chars / 5) / (current_time / 60)
            self.raw_wpm_history.append(raw_wpm)
            self.wpm_history.append(wpm)

    def calculate_results(self) -> None:
        time_taken = self.ui.time_elapsed
        correct_char_count = sum(1 for i in range(len(self.ui.current_correctness)) if self.ui.current_correctness[i] == "correct" and self.ui.current_text[i] != " ")
        total_chars_excluding_spaces = self.ui.total_chars
        accuracy = (correct_char_count / total_chars_excluding_spaces) * 100

        wpm = (self.correct_typed_chars / 5) / (time_taken / 60)
        raw_wpm = (self.raw_typed_chars / 5) / (time_taken / 60)

        self.ui.show_summary(wpm, raw_wpm, accuracy)

    def save_text(self) -> None:
        new_text = self.ui.text_entry.get()
        if new_text:
            self.ui.texts = [new_text]  # Replace any existing text with the new one
            with open("text.json", "w") as file:
                json.dump(self.ui.texts, file)
            self.ui.start_main_window()

    def load_texts(self) -> None:
        try:
            with open("text.json", "r") as file:
                self.ui.texts = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.ui.texts = []
