import customtkinter
import random
import data
import time
import word_list_generator as word_list 
from config import *

customtkinter.set_default_color_theme("colour_theme.json")
customtkinter.set_appearance_mode("dark")

class Main(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure properties
        self.geometry("{width}x1080+{x}+{y}".format(
            height = app_height * 0.9683,
            width = app_width,
            x = int((screen_width / 2) - (app_width / 2)),
            y = 0)
        )

        self.geometry("{width}x{height}".format(
            height = app_height * 0.935,
            width = app_width)
        )

        # configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Margins
        self.left_margin = customtkinter.CTkFrame(self, height=app_height, fg_color="gray10")
        self.left_margin.grid(row=0, column = 0, sticky="nsew")
        self.right_margin = customtkinter.CTkFrame(self, height=app_height, fg_color="gray10")
        self.right_margin.grid(row=0, column=2, sticky="nsew")

        # Init with Menu display frame
        self.display = None
        self.open_frame(MenuFrame(self))
        self.minsize(int(app_width / 2), int(app_height / 5))

    def open_frame(self, frameObj):
        # remove old display frame
        if self.display:
            self.display.destroy()

        # add new display frame
        self.display = frameObj
        self.display.grid(row=0, column=1, sticky="nsew")
    
        # event binding
        if isinstance(frameObj, GameFrame):
            self.bind("<Key>", self.display.input_letter)
            self.bind("<Return>", self.display.check_word)
            self.bind("<Left>", lambda e: self.display.cycle_letter(event=e, forwards=False))
            self.bind("<Right>", lambda e: self.display.cycle_letter(event=e, forwards=True))
            self.bind("<Tab>", lambda e: self.display.cycle_letter(event=e, forwards=True))
            self.bind("<BackSpace>", self.display.clear_letter)

    def show_popup(self, popupObj):
        popupObj.place(relx = 0.5, rely = 0.5, anchor = "center")
        return popupObj


# --- CUSTOM FRAMES ---

class CustomFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        self.padding_x = customtkinter.CTkFrame(self, width = app_width / 2.6, height = 0, fg_color="yellow")
        self.padding_x.grid(row=0, column=0, sticky="nesw")

    def update_padding(self, columnspan):
        self.padding_x.grid_configure(columnspan=columnspan)

# - MENU FRAME -
class MenuFrame(CustomFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        # Title
        self.title = customtkinter.CTkLabel(self, text="Wordle", font=("Roboto", title_size))
        self.title.grid(row=1, column=0, pady=25)

        # Menu Buttons
        self.basic_wordle_btn = customtkinter.CTkButton(self, text="Basic Wordle", font=("Roboto", subtitle_size), width = app_width / 3, command=self.wordle_selection)
        self.basic_wordle_btn.grid(row=2, column=0, pady=(0,5), padx=25)

    def wordle_selection(self):
        main.open_frame(WordleSelectionFrame(main))

    def start_game(self):
        main.open_frame(GameFrame(main))


# - WORDLE SELECTION FRAME -
class WordleSelectionFrame(CustomFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master)

        # load wordle basic data
        data.load_profile("wordle_basic")

        # custom vars
        self.word_length = 3

        # Buttons
        self.title = customtkinter.CTkLabel(self, text="Wordle Basic", font=("Roboto", title_size))
        self.title.grid(row=1, column=0, columnspan = 3, sticky="nesw", pady=25)

        self.length_lbl = customtkinter.CTkLabel(self, text="Word Length", font=("Roboto", popup_text_size))
        self.length_lbl.grid(row=2, column=0, columnspan = 3, sticky="nesw")

        self.word_length_label = customtkinter.CTkLabel(self, text=3, font=("Roboto", popup_text_size))
        self.word_length_label.grid(row=3, column=1, padx=5)

        self.length_decrease_btn = customtkinter.CTkButton(self, width=btn_text_size + 20, height=btn_text_size + 15, text="<", font=("Roboto", btn_text_size), command=lambda: [self.change_length(-1), self.update_word_count()])
        self.length_decrease_btn.grid(row=3, column=0)

        self.length_increase_btn = customtkinter.CTkButton(self, width=btn_text_size + 20, height=btn_text_size + 15, text=">", font=("Roboto", btn_text_size), command=lambda: [self.change_length(1), self.update_word_count()])
        self.length_increase_btn.grid(row=3, column=2)

        self.play_btn = customtkinter.CTkButton(self, text="Play", font=("Roboto", btn_text_size), command=self.start_game)
        self.play_btn.grid(row=4, column=0, columnspan = 3, padx=10, pady=10)

        # word selection
        self.word_count = 0
        self.word_count_lbl = customtkinter.CTkLabel(self, text=f"Words: {self.word_count}", font = ("Roboto", subtitle_size))
        self.word_count_lbl.grid(row=5, column = 0, columnspan=3, pady=(25, 5))

        # adverbs
        self.adverbs_val = customtkinter.Variable(value=data.profile_data["wordle_basic"]["adverbs"])
        self.adverbs_switch = customtkinter.CTkSwitch(self, switch_width=switch_size, switch_height=switch_size /2,
                                                       text="Adverbs", font=("Roboto", popup_text_size),
                                                       variable=self.adverbs_val, onvalue=True, offvalue=False,
                                                       command=lambda: [data.update_profile("adverbs", self.adverbs_switch.get()), self.update_word_count()])
        self.adverbs_switch.grid(row=6, column=1, sticky="nesw", pady=5)

        # adjectives
        self.adjectives_val = customtkinter.Variable(value=data.profile_data["wordle_basic"]["adjectives"])
        self.adjectives_switch = customtkinter.CTkSwitch(self, switch_width=switch_size, switch_height=switch_size /2,
                                                       text="Adjectives", font=("Roboto", popup_text_size),
                                                       variable=self.adjectives_val, onvalue=True, offvalue=False,
                                                       command=lambda: [data.update_profile("adjectives", self.adjectives_switch.get()), self.update_word_count()])
        self.adjectives_switch.grid(row=7, column=1, sticky="nesw", pady=5)

        # nouns
        self.nouns_val = customtkinter.Variable(value=data.profile_data["wordle_basic"]["nouns"])
        self.nouns_switch = customtkinter.CTkSwitch(self, switch_width=switch_size, switch_height=switch_size /2,
                                                       text="Nouns", font=("Roboto", popup_text_size),
                                                       variable=self.nouns_val, onvalue=True, offvalue=False,
                                                       command=lambda: [data.update_profile("nouns", self.nouns_switch.get()), self.update_word_count()])
        self.nouns_switch.grid(row=8, column=1, sticky="nesw", pady=5)

        # verbs
        self.verbs_val = customtkinter.Variable(value=data.profile_data["wordle_basic"]["verbs"])
        self.verbs_switch = customtkinter.CTkSwitch(self, switch_width=switch_size, switch_height=switch_size /2,
                                                       text="Verbs", font=("Roboto", popup_text_size),
                                                       variable=self.verbs_val, onvalue=True, offvalue=False,
                                                       command=lambda: [data.update_profile("verbs", self.verbs_switch.get()), self.update_word_count()])
        self.verbs_switch.grid(row=9, column=1, sticky="nesw", pady=5)

        # british_english
        self.british_english_val = customtkinter.Variable(value=data.profile_data["wordle_basic"]["british_english"])
        self.british_english_switch = customtkinter.CTkSwitch(self, switch_width=switch_size, switch_height=switch_size /2,
                                                       text="British English", font=("Roboto", popup_text_size),
                                                       variable=self.british_english_val, onvalue=True, offvalue=False,
                                                       command=lambda: [data.update_profile("british_english", self.british_english_switch.get()), self.update_word_count()])
        self.british_english_switch.grid(row=10, column=1, sticky="nesw", pady=5)

        # american_english
        self.american_english_val = customtkinter.Variable(value=data.profile_data["wordle_basic"]["american_english"])
        self.american_english_switch = customtkinter.CTkSwitch(self, switch_width=switch_size, switch_height=switch_size /2,
                                                       text="American English", font=("Roboto", popup_text_size),
                                                       variable=self.american_english_val, onvalue=True, offvalue=False,
                                                       command=lambda: [data.update_profile("american_english", self.american_english_switch.get()), self.update_word_count()])
        self.american_english_switch.grid(row=11, column=1, sticky="nesw", pady=5)

        self.update_padding(3)
        self.update_word_count()

    def update_word_count(self):
        word_list.load_word_list(self.word_length)
        self.word_count = len(word_list.game_word_list)
        self.word_count_lbl.configure(text = f"{self.word_count} Words")

    def change_length(self, num):
        # clamp word length between 3 and 12
        self.word_length = min(12, max(3, self.word_length + num))
        # update visuals
        self.word_length_label.configure(text=self.word_length)

    def start_game(self):
        if self.word_count >= 10:
            main.open_frame(GameFrame(main, word_length=self.word_length))


# - GAME FRAME -
class GameFrame(CustomFrame):
    def __init__(self, master, word_length, **kwargs):
        super().__init__(master)

        # custom vars
        self.attempts = 0
        self.max_attempts = 7
        self.word_length = word_length
        self.word_inputs : list[WordInputBox] = list()
        self.target_word = random.choice(word_list.game_word_list)
        self.end_popup = None
        # endgame stats
        self.elapsed_time = 0
        self.start_time = time.time()

        print(self.target_word)

        # word tracker
        tracker_text = " ".join(word_length * ["_"]).upper()
        self.tracker_lbl = customtkinter.CTkLabel(self, text=tracker_text, font=(None, 45))
        self.tracker_lbl.grid(row=1, column=0, pady=15)

        # start game
        self.start()
    
    def start(self):
        self.add_word_input()
        self.focus_force()

    def reset(self, word_length):
        main.open_frame(GameFrame(main, word_length=word_length))
        self.destroy()

    def destroy(self):
        if self.end_popup:
            self.end_popup.destroy()
        return super().destroy()
            
    def add_word_input(self):
        new_word_input = WordInputBox(self, word_length=self.word_length)
        self.word_inputs.append(new_word_input)
        new_word_input.grid(row=len(self.word_inputs) + 2, column=0)

    # state checks
    def game_check(self, word):
        self.attempts += 1
        # guessed correctly
        if word == self.target_word:
            self.end_game(True)
        # check attempts if not guessed correctly
        elif self.attempts == self.max_attempts:
            self.end_game(False)
        # add word input if has attempts left
        else:
            self.add_word_input()
    
    def check_word(self, event):
        self.word_inputs[-1].word_check()

    # letter handling
    
    def input_letter(self, event):
        if event.char in "abcdefghijklmnopqrstuvwxyz" and event.char != "":
            char = event.char.upper()
            # update letter with key
            word_input = self.word_inputs[-1]
            word_input.letters[word_input.letter_index].configure(text = char)
            # cycle letter
            word_input.next_letter()
    
    def cycle_letter(self, event, forwards : bool = True, no_wrap : bool = False):
        word_input = self.word_inputs[-1]
        if forwards:
            word_input.next_letter()
        else:
            # stop backspace wrap if specified
            if no_wrap:
                if word_input.letter_index != 0:
                    word_input.prev_letter()
            else:
                word_input.prev_letter()

    def clear_letter(self, event):
        word_input = self.word_inputs[-1]
        word_input.letters[word_input.letter_index].configure(text = "  ")
        self.cycle_letter(event, False, True)

    # tracker

    def update_tracker(self, index, char):
        # insert character at index
        current_text = self.tracker_lbl.cget("text").split()
        current_text[index] = char
        # update label text
        self.tracker_lbl.configure(text = " ".join(current_text).upper())

    # game state

    def end_game(self, is_win):
        # unbind events
        main.unbind("<Key>")
        main.unbind("<Return>")
        main.unbind("<Left>")
        main.unbind("<Right>")
        main.unbind("<BackSpace>")

        # load data
        data.load_data()
        self.current_game_data = data.data["wordle_basic"][f"{self.word_length}"]

        # update streak data
        if is_win:
            self.current_game_data["streak"] += 1
        else:
            self.current_game_data["streak"] = 0

        # update highest streak data
        if self.current_game_data["streak"] > self.current_game_data["high_streak"]:
            self.current_game_data["high_streak"] = self.current_game_data["streak"]

        # calc time
        end_time = time.time()
        self.elapsed_time = end_time - self.start_time

        # update time data
        if self.current_game_data["time"] == None or self.elapsed_time < self.current_game_data["time"]:
            index = int(str(self.elapsed_time).find("."))
            deci_time = float(str(self.elapsed_time)[0:index+4])
            self.current_game_data["time"] = deci_time

        # show popup
        self.end_popup = main.show_popup(self.EndGamePopup(main, self, is_win))

        # save data
        data.save_data()

    class EndGamePopup(customtkinter.CTkFrame):
        def __init__(self, master, game_frame, is_win, **kwargs):
            super().__init__(master)

            # configure properties
            self.configure(border_width = 2)

            # custom vars
            self.game_frame = game_frame
            
            # UI
            # result text
            self.result_text = "default"
            if is_win:
                self.result_text = "Good Job!"
            else:
                self.result_text = "Good Try!" 

            self.result = customtkinter.CTkLabel(self, text=self.result_text, font=("Roboto", popup_text_size))
            self.result.grid(row=0, column=0, columnspan=2, pady=(15,0))

            # create attempts overview
            self.overview = customtkinter.CTkFrame(self)
            row_i = 0
            for word_input in game_frame.word_inputs:
                # init word frame
                frame = customtkinter.CTkFrame(self.overview)
                # add coloured icons for letters
                column_i = 0
                for letter_input in word_input.letters:
                    icon = customtkinter.CTkFrame(frame, width=overview_letter_size, height=overview_letter_size, fg_color=letter_input.cget("fg_color"))
                    icon.grid(row=0, column=column_i, padx=2.5)
                    column_i += 1
                # add word frame
                frame.grid(row=row_i, column=0, pady=2.5)
                row_i += 1
            # add overview
            self.overview.grid(row=1, columnspan=2, pady=(10, 10))

            self.stats_frame = customtkinter.CTkFrame(self)
            self.stats_frame.grid(row=2, column=0, columnspan=3, pady=(0,10))

            
            # time display
            # title
            title_font = customtkinter.CTkFont("Roboto", btn_text_size, underline=True)
            self.time_title_lbl = customtkinter.CTkLabel(self.stats_frame, text="Time", font=title_font)
            self.time_title_lbl.grid(row=0, column=0, pady=(5,1))
            if is_win:
                # current time
                self.deci_index = str(game_frame.elapsed_time).find(".")
                self.time_lbl = customtkinter.CTkLabel(self.stats_frame, text="Current: " + f"{game_frame.elapsed_time}"[0:self.deci_index+4] + "s", font=("Roboto", btn_text_size))
                self.time_lbl.grid(row=1, column=0, padx=10, pady=(0,1))
            # best time
            self.best_time = game_frame.current_game_data["time"]
            self.best_time_lbl = customtkinter.CTkLabel(self.stats_frame, text=f"Best: {self.best_time}s", font=("Roboto", btn_text_size))
            self.best_time_lbl.grid(row=2, column=0, pady=(0,5))

            # streak display
            # streak title
            self.streak_title_lbl = customtkinter.CTkLabel(self.stats_frame, text="Streak", font=title_font)
            self.streak_title_lbl.grid(row=3, column=0, pady=(0,1))
            if is_win:
                # current streak
                streak_data = game_frame.current_game_data["streak"]
                self.streak_lbl = customtkinter.CTkLabel(self.stats_frame, text= f"Current: x{streak_data}", font=customtkinter.CTkFont("Roboto", btn_text_size))
                self.streak_lbl.grid(row=4, column=0, pady=(0, 1))
            # highest streak display
            high_streak_data = game_frame.current_game_data["high_streak"]
            self.high_streak_lbl = customtkinter.CTkLabel(self.stats_frame, text= f"Best: x{high_streak_data}", font=customtkinter.CTkFont("Roboto", btn_text_size))
            self.high_streak_lbl.grid(row=5, column=0, pady=(0, 5))

            # restart game button
            self.restart_btn = customtkinter.CTkButton(self, text="Play Again", command= lambda l=game_frame.word_length: game_frame.reset(l))
            self.restart_btn.grid(row=3, column=0, padx=(50, 25), pady=(0, 25))

            # return to menu button
            self.menu_btn = customtkinter.CTkButton(self, text="Main Menu", command= lambda f=MenuFrame(main): main.open_frame(f))
            self.menu_btn.grid(row=3, column=1, padx=(25, 50), pady=(0, 25))
    

class WordInputBox(customtkinter.CTkFrame):
    def __init__(self, master, word_length, **kwargs):
        super().__init__(master, **kwargs)

        # configure args
        self.configure(
            width = app_width,
            height = app_height / 10
        )
        # custom vars
        self.word_length = word_length
        self.letters : list[LetterInputBox] = list()
        self.add_letters(self.word_length)

        # auto focus 1st letter
        self.letter_index = 0
        self.letters[0].update_focus()

    def add_letters(self, num : int):
        for i in range(0,num):
            new_letter = LetterInputBox(self, i)
            new_letter.grid(row = 0, column = i)
            self.letters.append(new_letter)

    def word_check(self):
        # build word and check if all letters valid
        guess = ""
        for chrBox in self.letters:
            letter = chrBox.cget("text").lower()
            if letter in "abcdefghijklmnopqrstuvwxyz":
                guess += letter
            else:
                guess += " "
        # check if valid word
        if " " in guess:
            return
        # check against list
        found = False
        for list in word_list.game_word_list:
            if guess in list:
                found = True
                break
        if found:
            # visual display correct letters
            for chrBox in self.letters:
                chrBox.letter_check()
            # call Game check
            self.master.game_check(guess)

    def next_letter(self):
        letter_index = self.letter_index
        current_letter = self.letters[self.letter_index]
        # unfocus previous letter
        if current_letter:
            current_letter.update_focus(False)
        # focus next letter
        if letter_index != len(self.letters) - 1:
            current_letter = self.letters[self.letter_index + 1]
            current_letter.update_focus(True)
            self.letter_index += 1
        else:
            current_letter = self.letters[0]
            current_letter.update_focus(True)
            self.letter_index = 0

    def prev_letter(self):
        letter_index = self.letter_index
        current_letter = self.letters[self.letter_index]
        # unfocus current letter
        if current_letter:
            current_letter.update_focus(False)
        # focus previous letter
        if letter_index != 0:
            current_letter = self.letters[self.letter_index - 1]
            current_letter.update_focus(True)
            self.letter_index -= 1
        else:
            current_letter = self.letters[len(self.letters) - 1]
            current_letter.update_focus(True)
            self.letter_index = len(self.letters) - 1


class LetterInputBox(customtkinter.CTkLabel):
    def __init__(self, master, index, **kwargs):
        super().__init__(master, **kwargs)

        # configure entry args
        self.configure(
            text = "  ",
            width = app_height / 18,
            height = app_height / 18,
            justify = "center",
            font = ("Roboto", letter_text_size),
        )
        # custom args
        self.index = index

    # check if letter matches target word at index
    def letter_check(self):
        # green if yes
        colour = ""
        char = self.cget("text").lower()
        if (char == main.display.target_word[self.index]):
            colour = "green"
            main.display.update_tracker(self.index, char) # call update_tracker from GameFrame
        elif (char in main.display.target_word):
            colour = "DarkOrange2"
        else:
            colour = "Red3"
        # update configuration
        self.configure(
            state = "disabled",
            fg_color = colour,
            font = customtkinter.CTkFont("Roboto", letter_text_size, underline=False)
        )
    
    def update_focus(self, has_focus = True):
        if has_focus:
            new_font = customtkinter.CTkFont("Roboto", letter_text_size, underline=True)
        else:
            new_font = customtkinter.CTkFont("Roboto", letter_text_size, underline=False)
        # update font
        self.configure(
            font = new_font
        )

main : Main = Main()
main.mainloop()