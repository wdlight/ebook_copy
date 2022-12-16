import pyautogui
import sys
import datetime, time
from pynput.mouse import Listener  # pip install pynput
import winsound 

btn_next = pyautogui.locateOnScreen("next_button.png", grayscale=True)
print (f" next button location : [{btn_next}]")

while btn_next is None:
    btn_next = pyautogui.locateOnScreen("next_button.png", grayscale=True)
    if btn_next is None:
        pyautogui.prompt(" Check out the next button and Retry.")
    

## File name 지정
book_name = pyautogui.prompt("ebook 파일명을 지정하고 \n각 scan 영역 4개 point를 Click하세요!!.", "ebook")
print( f"ebook filename: [{book_name}]" )


## capture 위치 정하기.
# 화면click 시 위치 받아 오기.
from pynput.mouse import Listener

coord = []

def on_click(x,y, button, pressed):
        if pressed:
            x = int(x)
            y = int(y)
            coord.append((x,y)) # You can use a list also here.
            print( f" each click - input coord: {coord}")   
            if len(coord) == 4:
                print( f"input coord: {coord}")  
                listener.stop()  
                
            return
with Listener( #on_move=on_move, on_scroll=on_scroll,
                    on_click=on_click ) as listener: 
    listener.join()

## 화면 영역 설정 
# 3개의 포인터 중 가장 큰 값으로 영역 잡기.
import numpy as np

min_x = np.min( coord, axis=0)[0]
min_y = np.min( coord, axis=0)[1]
max_x = np.max( coord, axis=0)[0]
max_y = np.max( coord, axis=0)[1]

topleft = ( min_x, min_y )
bottomright = ( max_x, max_y )

print( f"scan position : {topleft},{bottomright}")

from PIL import Image

def copyImage(page):    
    book_page = f"{book_name}_{page}.png"    
    pyautogui.screenshot( book_page, region = (min_x,min_y, max_x - min_x, max_y - min_y ))

###########################################
## 마지막 페이지  받아오기
pages = pyautogui.prompt( f" {min_x},{min_y}, ({max_x}, {max_y}) is located. \n input how many pages would you like to scan ? \n click four times for each end of the book edge. ")
print (f"pages: {pages}")


###########################################
## Scan each images..
import os
out_dir = book_name
os.mkdir (out_dir)
os.chdir(out_dir)

for i in range( 0, int(pages) + 1):
    ##
    print (f"current page{i}")    
    copyImage(i)
    #2. nextButton
    pyautogui.moveTo(btn_next)
    pyautogui.click(btn_next)

    pyautogui.sleep(0.5)

img_name = f"{book_name}_0.png" #
img_1 = Image.open(img_name)
img_main = img_1.convert('RGB')

img_list = []
for i in range( 1, int(pages) + 1 ):
    img_name = f"{book_name}_{i}.png"
    print ( f" file appending: {img_name}")
    img_1 = Image.open(img_name)
    img_rgb_1 = img_1.convert('RGB')
    img_list.append( img_rgb_1)


print ( "Start to Export pdf")
img_main.save(f'{book_name}.pdf', 
                save_all=True, 
                append_images=img_list)

print ( "Program Ends normally.")
    
    





