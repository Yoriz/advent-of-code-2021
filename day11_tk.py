import tkinter as tk
from tkinter import ttk
import day11


class GridDisplay(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.labels: list[list[ttk.Label]] = []

    def create_grid_labels(self, grid_size: day11.GridSize):
        for y in range(grid_size.max_point.y):
            label_row: list[ttk.Label] = []
            for x in range(grid_size.max_point.x):
                label = ttk.Label(
                    self,
                    font=("TkFixedFont", 20),
                    width=2,
                    borderwidth=1,
                    relief="ridge",
                    anchor="s",
                )
                label_row.append(label)
                label.grid(row=y, column=x)
            self.labels.append(label_row)

    def update_all(self, octopus_grid: day11.OctopusGrid) -> None:
        for label_row, octopus_row in zip(self.labels, octopus_grid.octopuses):
            for label, octopus in zip(label_row, octopus_row):
                label.config(text=octopus.energy_level)


class MainFrame(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.grid_display = GridDisplay(self)
        self.grid_display.pack(padx=2, pady=2)
        self.step_label = ttk.Label(self, font="TkFixedFont")
        self.step_label.pack(padx=2, pady=2)
        button_next_step = ttk.Button(self, text="Next Step")
        button_next_step.pack(padx=2, pady=2)
        button_next_step.bind("<Button-1>", self.on_button_next_step)

        data = day11.iter_data(filename=day11.FILENAME)
        octopuses = day11.create_octopuses(lines=data)
        grid_size = day11.GridSize(
            max_point=day11.Point(x=len(octopuses[0]), y=len(octopuses))
        )
        self.grid_display.create_grid_labels(grid_size=grid_size)
        self.octopus_grid = day11.OctopusGrid(octopuses=octopuses, grid_size=grid_size)
        self.update_grid_display(self.octopus_grid)
        self.step = 0
        self.updating_flash_step = False

    def update_grid_display(self, octopus_grid: day11.OctopusGrid) -> None:
        self.grid_display.update_all(octopus_grid=octopus_grid)

    def update_step_label(self, text: str) -> None:
        self.step_label.config(text=text)

    def flash_step(self) -> None:
        self.updating_flash_step = True
        octopuses_wanting_to_flash = self.octopus_grid.octopuses_wanting_to_flash()
        if not octopuses_wanting_to_flash:
            self.octopus_grid.reset_octopuses_if_flashed()
            self.update_grid_display(self.octopus_grid)
            self.updating_flash_step = False
            return None
        self.octopus_grid.flash_octopuses(octopuses_wanting_to_flash)
        self.update_grid_display(self.octopus_grid)
        self.after(500, self.flash_step)

    def on_button_next_step(self, event):
        if self.updating_flash_step:
            return
        self.step += 1
        self.update_step_label(text=f"Step: {self.step}")
        self.octopus_grid.step()
        self.update_grid_display(self.octopus_grid)
        self.flash_step()


def main():
    app = tk.Tk()
    # app.geometry("600x600")
    main_frame = MainFrame(app)
    main_frame.pack(padx=5, pady=5)
    app.mainloop()


if __name__ == "__main__":
    main()
