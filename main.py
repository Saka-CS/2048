import customtkinter as ctk
from random import choices
from settings import *
from Number import *
from tkinter import Label
from ctypes import windll, byref, sizeof, c_int
from PIL import Image


def game_exit(get_good, controller, max_score):
    settings_file = open("game_settings.txt", "w")
    if(get_good):
        settings_file.write("T\n")
    else:
        settings_file.write("F\n")
    for i in max_score:
        settings_file.write(str(i.get()))
        settings_file.write("\n")
    settings_file.close()
    controller.destroy()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # basic settings
        self.geometry("600x800")
        self.title("2048")
        self.minsize(600, 800)
        self.resizable(False, False)
        
        music = settings_file.readline()
        self.best_score = [0] * 10
        for i in range(10):
            self.best_score[i] = ctk.IntVar(value=int(settings_file.readline()))

        self.BUTTON_FONT = ctk.CTkFont(
            family="Helvetica",
            size=20,
        )
        self.NUMBERS_FONT = ctk.CTkFont(
            family="Helvetica",
        )
        self.TITLE_FONT = ctk.CTkFont(
            family="Shadow",
            size=125,
        )

        # container
        self.container = ctk.CTkFrame(self)

        self.container.pack(expand=True, fill="both")

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.frame = {}

        for F in (Menu, StartMenu):
            frame = F(self.container, self)
            self.frame[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont, size=None):
        if(cont == Playing):
            frame = cont(self.container, self, size)
            self.frame[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        elif(cont == Settings):
            frame = cont(self.container, self)
            self.frame[cont] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        frame = self.frame[cont]
        frame.tkraise()


class Menu(ctk.CTkFrame):
    def __init__(self, parent, controller, size=None):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)

        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="a")

        # defining
        self.title_image = Label(self, text="2048", fg="#776e65", bg=BACKGROUND_COLOR, font=controller.TITLE_FONT)
        self.start_button = ctk.CTkButton(
            self,
            text="Start Game",
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            font=controller.BUTTON_FONT,
            command=lambda: controller.show_frame(StartMenu))
        self.setting_button = ctk.CTkButton(
            self,
            text="Setting",
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            font=controller.BUTTON_FONT,
            command=lambda: controller.show_frame(Settings)
        )
        self.quit_button = ctk.CTkButton(
            self,
            text="Quit",
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            font=controller.BUTTON_FONT,
            command=lambda: game_exit(False, controller, controller.best_score)
        )

        # placing
        self.title_image.grid(row=1, column=1, columnspan=4, sticky="nsew")
        self.start_button.grid(row=3, column=2, columnspan=2, sticky="nsew", pady=10)
        self.setting_button.grid(row=4, column=2, columnspan=2, sticky="nsew", pady=10)
        self.quit_button.grid(row=5, column=2, columnspan=2, sticky="nsew", pady=10)

        self.pack(expand=True, fill="both")


class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)

        # define
        self.number = 5
        self.image_array = [0 for i in range(11)]
        for i in range(1, 11):
            image = Image.open(f"Font to Install/{i}.png")
            self.image_array[i] = ctk.CTkImage(image, size=(300, 311))
        self.example_image = ctk.CTkButton(self, text="", image=self.image_array[self.number], hover=False, fg_color=BACKGROUND_COLOR)
        self.right_button = ctk.CTkButton(self, text=">", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, corner_radius=5, command=lambda: self.update(1))
        self.left_button = ctk.CTkButton(self, text="<", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, corner_radius=5, command=lambda: self.update(-1))


        self.start_button = ctk.CTkButton(self, text="Start", font=controller.BUTTON_FONT, hover_color=BUTTON_HOVER_COLOR, fg_color=BUTTON_COLOR, command=lambda: controller.show_frame(Playing, self.number))
        self.return_to_menu = ctk.CTkButton(self, text="<", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, command=lambda: controller.show_frame(Menu))

        # place
        self.example_image.place(relx=0.5, rely=0.3, relwidth=0.6, relheight=0.4, anchor="center")
        self.right_button.place(relx=0.73, rely=0.7, relwidth=0.04, relheight=0.05, anchor="center")
        self.start_button.place(relx=0.5, rely=0.7, relwidth=0.4, relheight=0.05, anchor="center")
        self.left_button.place(relx=0.27, rely=0.7, relwidth=0.04, relheight=0.05, anchor="center")
        self.return_to_menu.place(relx=0.05, rely=0.05, relwidth=0.04, relheight=0.05, anchor="center")

    def update(self, num):
        if(self.number <= 1 and num == -1):
            return
        elif(self.number >= 10 and num == 1):
            return
        self.number += num
        self.example_image.destroy()
        self.example_image = ctk.CTkButton(self, text="", image=self.image_array[self.number], hover=False,
                                           fg_color=BACKGROUND_COLOR)
        self.example_image.place(relx=0.5, rely=0.3, relwidth=0.6, relheight=0.4, anchor="center")



class Playing(ctk.CTkFrame):
    def __init__(self, parent, controller, size):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        self.controller = controller
        self.controller.bind("<KeyPress>", self.math_shit)
        self.score = ctk.IntVar(value=0)

        # define
        self.gameboard = ctk.CTkFrame(self, fg_color=GAMEBOARD_COLOR)
        self.row_size = size
        self.column_size = size
        self.number_width = (1 / self.row_size) * 0.9
        self.number_height = (1 / self.column_size) * 0.9
        self.array_of_numbers = [[0 for i in range(self.column_size)] for j in range(self.row_size)]
        self.displayed_items = [[0 for i in range(self.column_size)] for j in range(self.row_size)]
        self.moved_items = [[False for i in range(self.column_size)] for j in range(self.row_size)]
        self.number_colors = {
            2: NUMBER2_COLOR,
            4: NUMBER4_COLOR,
            8: NUMBER8_COLOR,
            16: NUMBER16_COLOR,
            32: NUMBER32_COLOR,
            64: NUMBER64_COLOR,
            128: NUMBER128_COLOR,
            256: NUMBER256_COLOR,
            512: NUMBER512_COLOR,
            1024: NUMBER1024_COLOR,
            2048: NUMBER2048_COLOR,
            7: COOL_BLACK,
            77: COOL_BLACK,
            '?': COOL_BLACK,
            '/': COOL_BLACK
        }

        # place
        self.gameboard.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.7, anchor="center")
        for row in range(self.row_size):
            for column in range(self.column_size):
                x = (1 / self.row_size) * column + (1 / (self.row_size * 2))
                y = (1 / self.column_size) * row + (1 / (self.column_size * 2))
                ctk.CTkLabel(
                    self.gameboard,
                    text="",
                    fg_color=NUMBER_BACKGROUND,
                    corner_radius=15,).place(relx=x, rely=y, relwidth=self.number_width, relheight=self.number_height, anchor="center")

        # game elements
        self.score_label = ctk.CTkLabel(self, textvariable=self.score, width=90, height=40, fg_color=BUTTON_COLOR, corner_radius=5)
        self.score_label_max = ctk.CTkLabel(self, textvariable=controller.best_score[size - 1], width=90, height=40, fg_color=BUTTON_COLOR, corner_radius=5)
        self.exit_game = ctk.CTkButton(self, text="<", fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, command=lambda: controller.show_frame(Menu))

        # place
        self.score_label.place(relx=0.6, rely=0.15)
        self.score_label_max.place(relx=0.8, rely=0.15)
        self.exit_game.place(relx=0.05, rely=0.05, relwidth=0.04, relheight=0.05, anchor="center")

        self.adding_numbers()
        self.display()

    def adding_numbers(self):
        available_indexes = []
        for row in range(self.row_size):
            for column in range(self.column_size):
                if self.array_of_numbers[row][column] == 0:
                    available_indexes.append([row, column])

        index = choices(available_indexes)
        possible_outcome = (7, '/', '?', 16, 8, 4, 2)
        outcome_weights = (5, 15, 15, 5, 10, 100, 120)
        self.array_of_numbers[index[0][0]][index[0][1]] = (choices(possible_outcome, weights=outcome_weights))[0]
        self.moved_items[index[0][0]][index[0][1]] = True

    def delete(self):
        for row in self.displayed_items:
            for item in row:
                if item:
                    item.destroy()

    def display(self):
        for row_num, row in enumerate(self.array_of_numbers):
            for column_num, column in enumerate(row):
                if column != 0:
                    x = (1 / self.row_size) * column_num + (1 / (self.row_size * 2))
                    y = (1 / self.column_size) * row_num + (1 / (self.column_size * 2))
                    if (column == '/' or column == '?'):
                        background_color = "black"
                    elif column > 2048:
                        background_color = "black"
                    else:
                        background_color = self.number_colors[column]
                    number_color = NUMBER_BLACK_COLOR if column == 2 or column == 4 else NUMBER_WHITE_COLOR
                    self.displayed_items[row_num][column_num] = Number(
                        parent=self.gameboard,
                        text=str(column),
                        radius=15,
                        color=background_color,
                        text_color=number_color,
                        column_size=self.column_size,
                        row_size=self.row_size,
                        x_original_size=self.number_width,
                        y_original_size=self.number_height,
                        x_position=x,
                        y_position=y,
                        font=self.controller.NUMBERS_FONT
                    )
                    self.displayed_items[row_num][column_num].place(relx=x, rely=y, relwidth=self.number_width, relheight=self.number_height, anchor="center")

    def animation(self):
        do_animation = []
        for row_number, row in enumerate(self.moved_items):
            for column_number, item in enumerate(row):
                if item:
                    do_animation.append(self.displayed_items[row_number][column_number])

        for i in range(6):
            for item in do_animation:
                item.expand(i)
            self.update()

    def math_shit(self, event):
        self.controller.unbind("<KeyPress>")
        self.moved_items = [[False for i in range(self.column_size)] for j in range(self.row_size)]
        self.merged_items = [[False for i in range(self.column_size)] for j in range(self.row_size)]
        item_movement = False

        if event.char == 'd' or event.char == 'D':
            for row_num, row in enumerate(self.array_of_numbers):
                for column_num, column in enumerate(reversed(row)):
                    if column != 0:
                        column_num = self.column_size - 1 - column_num
                        move = 1
                        while column_num + move < self.column_size:
                            if self.array_of_numbers[row_num][column_num + move] == 0:
                                move += 1
                                if column_num + move == self.column_size:
                                    self.array_of_numbers[row_num][column_num + move - 1] = self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num + move - 1] = True
                                    break
                            elif(self.array_of_numbers[row_num][column_num] == '/' and not self.merged_items[row_num][column_num + move]):
                                if(self.array_of_numbers[row_num][column_num + move] == 2 or
                                        self.array_of_numbers[row_num][column_num + move] == '/' or
                                        self.array_of_numbers[row_num][column_num + move] == '?' or
                                        self.array_of_numbers[row_num][column_num + move] == 7 or
                                        self.array_of_numbers[row_num][column_num + move] == 77
                                        ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num + move - 1] = \
                                    self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num + move - 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num + move] = int(self.array_of_numbers[row_num][column_num + move] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num + move])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move] = True
                                self.merged_items[row_num][column_num + move] = True
                                break
                            elif(self.array_of_numbers[row_num][column_num + move] == '/' and not self.merged_items[row_num][column_num + move]):
                                if (self.array_of_numbers[row_num][column_num] == 2 or
                                        self.array_of_numbers[row_num][column_num] == '/' or
                                        self.array_of_numbers[row_num][column_num] == '?' or
                                        self.array_of_numbers[row_num][column_num] == 7 or
                                        self.array_of_numbers[row_num][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num + move - 1] = self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num + move - 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num + move] = int(
                                    self.array_of_numbers[row_num][column_num] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move] = True
                                self.merged_items[row_num][column_num + move] = True
                                break


                            elif (self.array_of_numbers[row_num][column_num] == '?' and not self.merged_items[row_num][
                                column_num + move]):
                                if (self.array_of_numbers[row_num][column_num + move] == '/' or
                                        self.array_of_numbers[row_num][column_num + move] == '?' or
                                        self.array_of_numbers[row_num][column_num + move] == 7 or
                                        self.array_of_numbers[row_num][column_num + move] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num + move - 1] = \
                                        self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num + move - 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num + move] = int(
                                    self.array_of_numbers[row_num][column_num + move] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num + move])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move] = True
                                self.merged_items[row_num][column_num + move] = True
                                break
                            elif (self.array_of_numbers[row_num][column_num + move] == '?' and not
                            self.merged_items[row_num][column_num + move]):
                                if (self.array_of_numbers[row_num][column_num] == '/' or
                                        self.array_of_numbers[row_num][column_num] == '?' or
                                        self.array_of_numbers[row_num][column_num] == 7 or
                                        self.array_of_numbers[row_num][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num + move - 1] = \
                                    self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num + move - 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num + move] = int(
                                    self.array_of_numbers[row_num][column_num] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move] = True
                                self.merged_items[row_num][column_num + move] = True
                                break


                            elif (self.array_of_numbers[row_num][column_num] == self.array_of_numbers[row_num][column_num + move]
                                and not self.merged_items[row_num][column_num + move]):

                                if(self.array_of_numbers[row_num][column_num] == 7):
                                    self.array_of_numbers[row_num][column_num + move] = (self.array_of_numbers[row_num][column_num] * 10) + 7
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num + move])
                                elif(self.array_of_numbers[row_num][column_num] == 77):
                                    self.array_of_numbers[row_num][column_num + move] = 2048
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num + move])
                                else:
                                    self.array_of_numbers[row_num][column_num + move] = self.array_of_numbers[row_num][column_num] * 2
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num] * 2)

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move] = True
                                self.merged_items[row_num][column_num + move] = True
                                break

                            elif(self.array_of_numbers[row_num][column_num] == 7 and
                                 self.array_of_numbers[row_num][column_num + move] == 77 or
                                 self.array_of_numbers[row_num][column_num] == 77 and
                                 self.array_of_numbers[row_num][column_num + move] == 7):

                                self.array_of_numbers[row_num][column_num + move] = 1024
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num + move])
                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move] = True
                                self.merged_items[row_num][column_num + move] = True
                                break
                            elif move == 1:
                                break
                            else:
                                self.array_of_numbers[row_num][column_num + move - 1] = self.array_of_numbers[row_num][column_num]
                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num + move - 1] = True
                                break

        elif event.char == 's' or event.char == 'S':
            for row_num, row in enumerate(reversed(self.array_of_numbers)):
                for column_num, column in enumerate(row):
                    if column != 0:
                        move = 1
                        temp_row = self.row_size - 1 - row_num
                        while temp_row + move < self.row_size:
                            if self.array_of_numbers[temp_row + move][column_num] == 0:
                                move += 1
                                if temp_row + move == self.row_size:
                                    self.array_of_numbers[temp_row + move - 1][column_num] = self.array_of_numbers[temp_row][
                                        column_num]
                                    self.array_of_numbers[temp_row][column_num] = 0
                                    item_movement = True
                                    self.moved_items[temp_row + move - 1][column_num] = True
                                    break
                            elif (self.array_of_numbers[temp_row][column_num] == '/' and not self.merged_items[temp_row + move][
                                column_num]):
                                if (self.array_of_numbers[temp_row + move][column_num] == 2 or
                                        self.array_of_numbers[temp_row + move][column_num] == '/' or
                                        self.array_of_numbers[temp_row + move][column_num] == '?' or
                                        self.array_of_numbers[temp_row + move][column_num] == 7 or
                                        self.array_of_numbers[temp_row + move][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[temp_row + move - 1][column_num] = \
                                        self.array_of_numbers[temp_row][column_num]
                                    self.array_of_numbers[temp_row][column_num] = 0
                                    item_movement = True
                                    self.moved_items[temp_row + move - 1][column_num] = True
                                    break

                                self.array_of_numbers[temp_row + move][column_num] = int(
                                    self.array_of_numbers[temp_row + move][column_num] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[temp_row + move][column_num])

                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move][column_num] = True
                                self.merged_items[temp_row + move][column_num] = True
                                break
                            elif (self.array_of_numbers[temp_row + move][column_num] == '/' and not
                            self.merged_items[temp_row + move][column_num]):
                                if (self.array_of_numbers[temp_row][column_num] == 2 or
                                        self.array_of_numbers[temp_row][column_num] == '/' or
                                        self.array_of_numbers[temp_row][column_num] == '?' or
                                        self.array_of_numbers[temp_row][column_num] == 7 or
                                        self.array_of_numbers[temp_row][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[temp_row + move - 1][column_num] = \
                                    self.array_of_numbers[temp_row][column_num]
                                    self.array_of_numbers[temp_row][column_num] = 0
                                    item_movement = True
                                    self.moved_items[temp_row + move - 1][column_num] = True
                                    break

                                self.array_of_numbers[temp_row + move][column_num] = int(
                                    self.array_of_numbers[temp_row][column_num] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[temp_row][column_num])

                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move][column_num] = True
                                self.merged_items[temp_row + move][column_num] = True
                                break

                            elif (self.array_of_numbers[temp_row][column_num] == '?' and not self.merged_items[temp_row + move][
                                column_num]):
                                if (self.array_of_numbers[temp_row + move][column_num] == '/' or
                                        self.array_of_numbers[temp_row + move][column_num] == '?' or
                                        self.array_of_numbers[temp_row + move][column_num] == 7 or
                                        self.array_of_numbers[temp_row + move][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[temp_row + move - 1][column_num] = \
                                        self.array_of_numbers[temp_row][column_num]
                                    self.array_of_numbers[temp_row][column_num] = 0
                                    item_movement = True
                                    self.moved_items[temp_row + move - 1][column_num] = True
                                    break

                                self.array_of_numbers[temp_row + move][column_num] = int(
                                    self.array_of_numbers[temp_row + move][column_num] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[temp_row + move][column_num])

                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move][column_num] = True
                                self.merged_items[temp_row + move][column_num] = True
                                break
                            elif (self.array_of_numbers[temp_row + move][column_num] == '?' and not
                            self.merged_items[temp_row + move][column_num]):
                                if (self.array_of_numbers[temp_row][column_num] == '/' or
                                        self.array_of_numbers[temp_row][column_num] == '?' or
                                        self.array_of_numbers[temp_row][column_num] == 7 or
                                        self.array_of_numbers[temp_row][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[temp_row + move - 1][column_num] = \
                                    self.array_of_numbers[temp_row][column_num]
                                    self.array_of_numbers[temp_row][column_num] = 0
                                    item_movement = True
                                    self.moved_items[temp_row + move - 1][column_num] = True
                                    break

                                self.array_of_numbers[temp_row + move][column_num] = int(
                                    self.array_of_numbers[temp_row][column_num] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[temp_row][column_num])

                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move][column_num] = True
                                self.merged_items[temp_row + move][column_num] = True
                                break


                            elif (self.array_of_numbers[temp_row][column_num] == self.array_of_numbers[temp_row + move][column_num] and not self.merged_items[temp_row + move][column_num]):
                                if (self.array_of_numbers[temp_row][column_num] == 7):
                                    self.array_of_numbers[temp_row + move][column_num] = (self.array_of_numbers[temp_row][
                                                                                             column_num] * 10) + 7
                                    self.score.set(self.score.get() + self.array_of_numbers[temp_row + move][column_num])
                                elif (self.array_of_numbers[temp_row][column_num] == 77):
                                    self.array_of_numbers[temp_row + move][column_num] = 2048
                                    self.score.set(self.score.get() + self.array_of_numbers[temp_row + move][column_num])
                                else:
                                    self.array_of_numbers[temp_row + move][column_num] = self.array_of_numbers[temp_row][
                                                                                            column_num] * 2
                                    self.score.set(self.score.get() + self.array_of_numbers[temp_row][column_num] * 2)

                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move][column_num] = True
                                self.merged_items[temp_row + move][column_num] = True
                                break
                            elif (self.array_of_numbers[temp_row][column_num] == 7 and
                                  self.array_of_numbers[temp_row + move][column_num] == 77 or
                                  self.array_of_numbers[temp_row][column_num] == 77 and
                                  self.array_of_numbers[temp_row + move][column_num] == 7):

                                self.array_of_numbers[temp_row + move][column_num] = 1024
                                self.score.set(self.score.get() + self.array_of_numbers[temp_row + move][column_num])
                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move][column_num] = True
                                self.merged_items[temp_row + move][column_num] = True
                                break
                            elif move == 1:
                                break
                            else:
                                self.array_of_numbers[temp_row + move - 1][column_num] = self.array_of_numbers[temp_row][column_num]
                                self.array_of_numbers[temp_row][column_num] = 0
                                item_movement = True
                                self.moved_items[temp_row + move - 1][column_num] = True
                                break

        elif event.char == 'a' or event.char == 'A':
            for row_num, row in enumerate(self.array_of_numbers):
                for column_num, column in enumerate(row):
                    if column != 0:
                        move = 1
                        while column_num - move > -1:
                            if self.array_of_numbers[row_num][column_num - move] == 0:
                                move += 1
                                if column_num - move == -1:
                                    self.array_of_numbers[row_num][column_num - move + 1] = self.array_of_numbers[row_num][
                                        column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num - move + 1] = True
                                    break

                            elif (self.array_of_numbers[row_num][column_num] == '/' and not self.merged_items[row_num][
                                column_num - move]):
                                if (self.array_of_numbers[row_num][column_num - move] == 2 or
                                        self.array_of_numbers[row_num][column_num - move] == '/' or
                                        self.array_of_numbers[row_num][column_num - move] == '?' or
                                        self.array_of_numbers[row_num][column_num - move] == 7 or
                                        self.array_of_numbers[row_num][column_num - move] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num - move + 1] = \
                                        self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num - move + 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num - move] = int(
                                    self.array_of_numbers[row_num][column_num - move] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num - move])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move] = True
                                self.merged_items[row_num][column_num - move] = True
                                break
                            elif (self.array_of_numbers[row_num][column_num - move] == '/' and not
                            self.merged_items[row_num][column_num - move]):
                                if (self.array_of_numbers[row_num][column_num] == 2 or
                                        self.array_of_numbers[row_num][column_num] == '/' or
                                        self.array_of_numbers[row_num][column_num] == '?' or
                                        self.array_of_numbers[row_num][column_num] == 7 or
                                        self.array_of_numbers[row_num][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num - move + 1] = \
                                    self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num - move + 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num - move] = int(
                                    self.array_of_numbers[row_num][column_num] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move] = True
                                self.merged_items[row_num][column_num - move] = True
                                break

                            elif (self.array_of_numbers[row_num][column_num] == '?' and not self.merged_items[row_num][
                                column_num - move]):
                                if (self.array_of_numbers[row_num][column_num - move] == '/' or
                                        self.array_of_numbers[row_num][column_num - move] == '?' or
                                        self.array_of_numbers[row_num][column_num - move] == 7 or
                                        self.array_of_numbers[row_num][column_num - move] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num - move + 1] = \
                                        self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num - move + 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num - move] = int(
                                    self.array_of_numbers[row_num][column_num - move] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num - move])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move] = True
                                self.merged_items[row_num][column_num - move] = True
                                break
                            elif (self.array_of_numbers[row_num][column_num - move] == '?' and not
                            self.merged_items[row_num][column_num - move]):
                                if (self.array_of_numbers[row_num][column_num] == '/' or
                                        self.array_of_numbers[row_num][column_num] == '?' or
                                        self.array_of_numbers[row_num][column_num] == 7 or
                                        self.array_of_numbers[row_num][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num][column_num - move + 1] = \
                                    self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num][column_num - move + 1] = True
                                    break

                                self.array_of_numbers[row_num][column_num - move] = int(
                                    self.array_of_numbers[row_num][column_num] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move] = True
                                self.merged_items[row_num][column_num - move] = True
                                break


                            elif (self.array_of_numbers[row_num][column_num] == self.array_of_numbers[row_num][column_num - move]
                                  and not self.merged_items[row_num][column_num - move]):

                                if (self.array_of_numbers[row_num][column_num] == 7):
                                    self.array_of_numbers[row_num][column_num - move] = (self.array_of_numbers[row_num][
                                                                                             column_num] * 10) + 7
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num - move])
                                elif (self.array_of_numbers[row_num][column_num] == 77):
                                    self.array_of_numbers[row_num][column_num - move] = 2048
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num - move])
                                else:
                                    self.array_of_numbers[row_num][column_num - move] = self.array_of_numbers[row_num][
                                                                                            column_num] * 2
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num] * 2)

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move] = True
                                self.merged_items[row_num][column_num - move] = True
                                break

                            elif (self.array_of_numbers[row_num][column_num] == 7 and
                                  self.array_of_numbers[row_num][column_num - move] == 77 or
                                  self.array_of_numbers[row_num][column_num] == 77 and
                                  self.array_of_numbers[row_num][column_num - move] == 7):

                                self.array_of_numbers[row_num][column_num - move] = 1024
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num - move])
                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move] = True
                                self.merged_items[row_num][column_num - move] = True
                                break

                            elif move == 1:
                                break
                            else:
                                self.array_of_numbers[row_num][column_num - move + 1] = self.array_of_numbers[row_num][column_num]
                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num][column_num - move + 1] = True
                                break

        elif event.char == 'w' or event.char == 'W':
            for row_num, row in enumerate(self.array_of_numbers):
                for column_num, column in enumerate(row):
                    if column != 0:
                        move = 1
                        while row_num - move > -1:
                            if self.array_of_numbers[row_num - move][column_num] == 0:
                                move += 1
                                if row_num - move == -1:
                                    self.array_of_numbers[row_num - move + 1][column_num] = self.array_of_numbers[row_num][
                                        column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num - move + 1][column_num] = True
                                    break


                            elif (self.array_of_numbers[row_num][column_num] == '/' and not self.merged_items[row_num - move][
                                column_num]):
                                if (self.array_of_numbers[row_num - move][column_num] == 2 or
                                        self.array_of_numbers[row_num - move][column_num] == '/' or
                                        self.array_of_numbers[row_num - move][column_num] == '?' or
                                        self.array_of_numbers[row_num - move][column_num] == 7 or
                                        self.array_of_numbers[row_num - move][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num - move + 1][column_num] = \
                                        self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num - move + 1][column_num] = True
                                    break

                                self.array_of_numbers[row_num - move][column_num] = int(
                                    self.array_of_numbers[row_num - move][column_num] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num - move][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move][column_num] = True
                                self.merged_items[row_num - move][column_num] = True
                                break
                            elif (self.array_of_numbers[row_num - move][column_num] == '/' and not
                            self.merged_items[row_num - move][column_num]):
                                if (self.array_of_numbers[row_num][column_num] == 2 or
                                        self.array_of_numbers[row_num][column_num] == '/' or
                                        self.array_of_numbers[row_num][column_num] == '?' or
                                        self.array_of_numbers[row_num][column_num] == 7 or
                                        self.array_of_numbers[row_num][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num - move + 1][column_num] = \
                                    self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num - move + 1][column_num] = True
                                    break

                                self.array_of_numbers[row_num - move][column_num] = int(
                                    self.array_of_numbers[row_num][column_num] / 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move][column_num] = True
                                self.merged_items[row_num - move][column_num] = True
                                break

                            elif (self.array_of_numbers[row_num][column_num] == '?' and not self.merged_items[row_num - move][
                                column_num]):
                                if (self.array_of_numbers[row_num - move][column_num] == '/' or
                                        self.array_of_numbers[row_num - move][column_num] == '?' or
                                        self.array_of_numbers[row_num - move][column_num] == 7 or
                                        self.array_of_numbers[row_num - move][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num - move + 1][column_num] = \
                                        self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num - move + 1][column_num] = True
                                    break

                                self.array_of_numbers[row_num - move][column_num] = int(
                                    self.array_of_numbers[row_num - move][column_num] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num - move][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move][column_num] = True
                                self.merged_items[row_num - move][column_num] = True
                                break
                            elif (self.array_of_numbers[row_num - move][column_num] == '?' and not
                            self.merged_items[row_num - move][column_num]):
                                if (self.array_of_numbers[row_num][column_num] == '/' or
                                        self.array_of_numbers[row_num][column_num] == '?' or
                                        self.array_of_numbers[row_num][column_num] == 7 or
                                        self.array_of_numbers[row_num][column_num] == 77
                                ):
                                    if move == 1:
                                        break
                                    self.array_of_numbers[row_num - move + 1][column_num] = \
                                    self.array_of_numbers[row_num][column_num]
                                    self.array_of_numbers[row_num][column_num] = 0
                                    item_movement = True
                                    self.moved_items[row_num - move + 1][column_num] = True
                                    break

                                self.array_of_numbers[row_num - move][column_num] = int(
                                    self.array_of_numbers[row_num][column_num] * 2)
                                self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num])

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move][column_num] = True
                                self.merged_items[row_num - move][column_num] = True
                                break


                            elif (self.array_of_numbers[row_num][column_num] == self.array_of_numbers[row_num - move][column_num] and not self.merged_items[row_num - move][column_num]):
                                if (self.array_of_numbers[row_num][column_num] == 7):
                                    self.array_of_numbers[row_num - move][column_num] = (self.array_of_numbers[
                                                                                              row_num][
                                                                                              column_num] * 10) + 7
                                    self.score.set(
                                        self.score.get() + self.array_of_numbers[row_num - move][column_num])
                                elif (self.array_of_numbers[row_num][column_num] == 77):
                                    self.array_of_numbers[row_num - move][column_num] = 2048
                                    self.score.set(
                                        self.score.get() + self.array_of_numbers[row_num - move][column_num])
                                else:
                                    self.array_of_numbers[row_num - move][column_num] = \
                                    self.array_of_numbers[row_num][
                                        column_num] * 2
                                    self.score.set(self.score.get() + self.array_of_numbers[row_num][column_num] * 2)

                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move][column_num] = True
                                self.merged_items[row_num - move][column_num] = True
                                break

                            elif (self.array_of_numbers[row_num][column_num] == 7 and
                                  self.array_of_numbers[row_num - move][column_num] == 77 or
                                  self.array_of_numbers[row_num][column_num] == 77 and
                                  self.array_of_numbers[row_num - move][column_num] == 7):

                                self.array_of_numbers[row_num - move][column_num] = 1024
                                self.score.set(self.score.get() + self.array_of_numbers[row_num - move][column_num])
                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move][column_num] = True
                                self.merged_items[row_num - move][column_num] = True
                                break

                            elif move == 1:
                                break
                            else:
                                self.array_of_numbers[row_num - move + 1][column_num] = self.array_of_numbers[row_num][column_num]
                                self.array_of_numbers[row_num][column_num] = 0
                                item_movement = True
                                self.moved_items[row_num - move + 1][column_num] = True
                                break

        if item_movement:
            self.delete()
            self.adding_numbers()
            if(self.score.get() > self.controller.best_score[self.column_size - 1].get()):
                self.controller.best_score[self.column_size - 1].set(self.score.get())
            self.display()
            self.animation()
        self.controller.bind("<KeyPress>", self.math_shit)


class Settings(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)

        button = ctk.CTkButton(self, fg_color="transparent", text="I did not have time to add settings", command=lambda: game_exit(True, controller, controller.best_score))
        button.pack(expand=True, fill="both")

ctk.set_appearance_mode("dark")
settings_file = open("game_settings.txt", "r")
app = App()


app.mainloop()
