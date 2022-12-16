import pyautogui
import sys
import datetime, time
from pynput.mouse import Listener  # pip install pynput
import winsound 

btn_next = pyautogui.locateOnScreen("next_button.png", grayscale=True)
print (f" next button location : [{btn_next}]")

## File name 지정
book_name = pyautogui.prompt("ebook 파일명을 지정하세요.", "ebook")
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
min_x = 500
min_y = 500
max_x = 500
max_y = 500

for x,y in coord :
    print (f"{x},{y}")
    min_x =  x if x < min_x else  min_x
    min_y =  y if y < min_y else  min_y
    max_x =  x if x > max_x else  max_x
    max_y =  y if y > max_y else  max_y

topleft = ( min_x, min_y )
bottomright = ( max_x, max_y )

from PIL import Image

def copyImage(page):    
    book_page = f"{book_name}_{page}.png"    
    pyautogui.screenshot( book_page, region = (min_x,min_y, max_x, max_y ))

###########################################
## 마지막 페이지  받아오기
pages = pyautogui.prompt( f" {min_x},{min_y}, ({max_x}, {max_y}) is located. \n input how many pages would you like to scan ? \n click four times for each end of the book edge. ")
print (f"pages: {pages}")


###########################################
## Scan each images..
for i in range( 0, int(pages) ):
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
    img_name = f"HandsOnML/HandsOnML_SK_Keras_TF_{i}.png"
    print ( f" file appending: {img_name}")
    img_1 = Image.open(img_name)
    img_rgb_1 = img_1.convert('RGB')
    img_list.append( img_rgb_1)


print ( "Start to Export pdf")
img_main.save(f'{book_name}.pdf', 
                save_all=True, 
                append_images=img_list)

print ( "Program Ends normally.")
    
    





