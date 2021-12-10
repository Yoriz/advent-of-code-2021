import tkinter as tk
from tkinter import ttk
from typing import Optional
import day8


class DisplayFrame(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.label = ttk.Label(
            self,
            font="TkFixedFont",
        )
        self.label.pack(padx=2, pady=2)
        display = day8.Display()
        self.update_display(display)

    def update_display(self, display: day8.Display) -> None:
        self.label.config(text=str(display))


class UniqueDisplays(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.display_frames: list[DisplayFrame] = []
        for row in range(2):
            for column in range(5):
                display_frame = DisplayFrame(
                    self, highlightbackground="black", highlightthickness=2
                )
                self.display_frames.append(display_frame)
                display_frame.grid(row=row, column=column)

    def update_displays(self, unique_displays: list[day8.Display]) -> None:
        for display_frame, display in zip(self.display_frames, unique_displays):
            display_frame.update_display(display=display)


class OutputDisplays(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.display_frames: list[DisplayFrame] = []
        for column in range(4):
            display_frame = DisplayFrame(
                self, highlightbackground="black", highlightthickness=2
            )
            self.display_frames.append(display_frame)
            display_frame.grid(row=0, column=column)

    def update_displays(self, outpur_displays: list[day8.Display]) -> None:
        for display_frame, display in zip(self.display_frames, outpur_displays):
            display_frame.update_display(display=display)


class ButtonFrame(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.button_load = ttk.Button(self, text="Load Next Entry")
        self.button_load.grid(row=0, column=0)
        self.button_decode = ttk.Button(self, text="Decode Entry")
        self.button_decode.grid(row=0, column=1)


class MainFrame(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        label = ttk.Label(self, text="Unique Displays")
        label.pack(padx=5, pady=5)
        self.unique_displays = UniqueDisplays(self)
        self.unique_displays.pack(padx=5, pady=5)
        label = ttk.Label(self, text="Output Displays")
        label.pack(padx=5, pady=5)
        self.output_displays = OutputDisplays(self)
        self.output_displays.pack(padx=5, pady=5)
        label = ttk.Label(self, text="Entry")
        label.pack(padx=5, pady=5)
        self.entry_label = ttk.Label(self)
        self.entry_label.pack(padx=5, pady=5)
        self.button_frame = ButtonFrame(self)
        self.button_frame.pack(padx=5, pady=5)

        button_load = self.button_frame.button_load
        button_load.bind("<Button-1>", self.on_button_load)
        button_decode = self.button_frame.button_decode
        button_decode.bind("<Button-1>", self.on_button_decode)

        data = day8.iter_data(day8.FILENAME)
        self.entrys = day8.iter_entrys(data)
        self.current_entry: Optional[day8.Entry] = None

    def update_entry_label(self, text: str):
        self.entry_label.config(text=text)

    def on_button_load(self, event):
        self.current_entry = next(self.entrys)
        self.update_entry_label(self.current_entry.line)
        self.unique_displays.update_displays(self.current_entry.unique_displays)
        self.output_displays.update_displays(self.current_entry.output_displays)

    def on_button_decode(self, event):
        current_entry = self.current_entry
        if not current_entry:
            return
        convertor = day8.get_display_convertor(current_entry)

        unique_displays = current_entry.unique_displays[:]
        for index, display in enumerate(unique_displays):
            unique_displays[index] = convertor[display]
        self.unique_displays.update_displays(unique_displays)

        output_displays = current_entry.output_displays[:]
        for index, display in enumerate(output_displays):
            output_displays[index] = convertor[display]
        self.output_displays.update_displays(unique_displays)


def main():
    app = tk.Tk()
    app.geometry("600x600")
    main_frame = MainFrame(app)
    main_frame.pack(padx=5, pady=5)

    app.mainloop()


if __name__ == "__main__":
    main()
