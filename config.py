
import ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

app_width = int(screen_width / 2)
app_height = screen_height

# widget sizes
# - Letter Overview -
overview_letter_size = int(app_height / 35)
# - switches -
switch_size = int(app_height / 25)

# text styles
# - Title -
title_size = int(app_height / 30)
subtitle_size = int(app_height / 40)
# - Popup -
popup_text_size = int(app_height/40)
# - Wordle Letters -
letter_text_size = int(app_height / 25)
# - Buttons -
btn_text_size = int(app_height / 50)