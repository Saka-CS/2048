import customtkinter as ctk
from settings import *


class Number(ctk.CTkLabel):
    def __init__(self, parent, radius, text, color, row_size, column_size, x_original_size, y_original_size, x_position, y_position, font, text_color):
        super().__init__(master=parent, corner_radius=radius, text=text, fg_color=color, font=(font, 110 / row_size), text_color=text_color, )
        self.x_position = x_position
        self.y_position = y_position
        self.x_original_size = x_original_size
        self.y_original_size = y_original_size
        self.y_unit = (1 / column_size)
        self.x_unit = (1 / row_size)

    def expand(self, number):
        x_expand_ratio = (self.x_unit - self.x_original_size) / 3
        y_expand_ratio = (self.y_unit - self.y_original_size) / 3

        if (number < 3):
            self.y_original_size += y_expand_ratio
            self.x_original_size += x_expand_ratio
            self.place(relx=self.x_position, rely=self.y_position, relwidth=self.x_original_size, relheight=self.y_original_size, anchor="center")
        else:
            self.y_original_size -= y_expand_ratio
            self.x_original_size -= x_expand_ratio
            self.place(relx=self.x_position, rely=self.y_position, relwidth=self.x_original_size, relheight=self.y_original_size, anchor="center")