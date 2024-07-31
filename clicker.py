import pyautogui
import time

time.sleep(10)

currentMouseX, currentMouseY = pyautogui.position() # Получаем XY координаты курсора.
print(currentMouseX, currentMouseY)
pyautogui.move(532, 801)