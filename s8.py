try:
    import tkinter as tk
    import serial as sl
except:
    import tkinter as tk
    import serial as sl
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import time



#str1 = '/dev/ttyUSB0'
#ser = sl.Serial(port=str1, baudrate=9600, )

## 함수 선언 부분 ##

def clickA():
    Trans = "A"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))

def clickB():
    Trans = "B"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))

def clickC():
    Trans = "C"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))

def clickD():
    Trans = "D"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))

def clickX():
    Trans = "X"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))

def clickY():
    Trans = "Y"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))

def clickZ():
    Trans = "Z"
    Trans = Trans.encode('utf-8')
    ser.write(Trans)
    print("TT" + str(Trans))


def clickClose():
    window.destroy()


def update_clock():
    abc = ser.readline()
    abc = str(abc)
    abcd = abc.split("-")

    temp = float(abcd[1])
    humi = float(abcd[2])
    form = float(abcd[3])
    pm10 = int(abcd[4])
    pm25 = int(abcd[5])
    pm01 = int(abcd[6])
    wait = int(abcd[7])
    speed = int(abcd[8])

    textValue1 = str(float(temp))
    textValue2 = str(float(humi))
    textValue3 = str(float(form))
    textValue4 = str(int(pm10))
    textValue5 = str(int(pm25))
#    textValue6 = str(int(pm01))
    textValue101 = str(int(wait))
    textValue102 = str(int(speed))

    label1.configure(text=textValue1)
    label2.configure(text=textValue2)
    label3.configure(text=textValue3)
    label4.configure(text=textValue4)
    label5.configure(text=textValue5)
#    label6.configure(text=textValue6)
    label101.configure(text=textValue101)
    label102.configure(text=textValue102)

    if pm25 <= 15:
        colorVal = "좋음 "
        colorcd = "blue"
    elif (pm25 > 15) and (pm25 <= 50):
        colorVal = "보통"
        colorcd = "lime"
    elif (pm25 > 50) and (pm25 <= 100):
        colorVal = "나쁨 "
        colorcd = "orange"
    else:
        colorVal = "심각 "
        colorcd = "red"
    
    ColorValue = colorVal
    label.configure(text=ColorValue)
    label.configure(fg=colorcd)
    window.after(100, update_clock)

def ChangeCB():
    ser = sl.Serial(
        port=str1.get(),
        baudrate=250000,
    )

## 메인 코드 부분 ##
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.attributes('-fullscreen', True)
window.config(cursor="none")

screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

canvas = Canvas(window, width=screen_w, height=screen_h, highlightthickness=0, borderwidth=0)
canvas.pack(fill="both", expand=True)

img = Image.open("/home/dkkim/Downloads/k8.png")
img = img.resize((screen_w, screen_h)) 
photo = ImageTk.PhotoImage(img)

canvas.create_image(0, 0, image=photo, anchor="nw")

style = ttk.Style(window)
style.theme_use("clam")

# Mac 느낌 ProgressBar 스타일 정의
style.configure("Mac.Horizontal.TProgressbar",
                troughcolor="#d6d6d6",      # 밝은 회색 배경
                background="#007aff",       # 맥OS 느낌 파란색
                lightcolor="#5eb8ff",       # 윗면 하이라이트
                darkcolor="#0051a8",        # 아래 그림자
                thickness=12,               # 얇고 세련되게
                bordercolor="#f2f2f2")

# 진행바 생성
progressbar = ttk.Progressbar(window,
                              style="Mac.Horizontal.TProgressbar",
                              length=300,
                              mode="determinate",
                              maximum=100)
progressbar.place(x=362, y=253)
progressbar.start(10)

# 상태 텍스트
label = tk.Label(window,
                 text="AI SYSTEM LOADING...",
                 font=("Helvetica Neue", 14),
                 fg="#333333",
                 bg="white")
label.place(x=362, y=222
)



'''
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", background='white')
progressbar2 = ttk.Progressbar(window, maximum=100, length=290, style="red.Horizontal.TProgressbar", mode="determinate")
progressbar2.start(7)
progressbar2.place(x=321, y=267)
'''

'''
pLabel = Label(window, image=photo)
'''

# btnClose.place(x=1780, y=1030)
'''

pLabel.place(x=0, y=32)
'''

'''추가부분 시작'''
# 상태 값, 1 온도 값, 2 습도 값, 3 포름알데히드 값, 4 PM10 값, 5 PM2.5 값, 6 PM1.0 값, 101 에어샤워 시간 값
label = tk.Label(text="", font=('Helvetica', 44), fg='black', bg='white')
label1 = tk.Label(text="", font=('Helvetica', 44), fg='black', bg='white', width='4',justify='right')
label2 = tk.Label(text="", font=('Helvetica', 44), fg='black', bg='white', width='4',justify='right')
label3 = tk.Label(text="", font=('Helvetica', 44), fg='black', bg='white', width='4',justify='right')
label4 = tk.Label(text="", font=('Helvetica', 44), fg='black', bg='white', width='3',justify='right')
label5 = tk.Label(text="", font=('Helvetica', 44), fg='black', bg='white', width='3',justify='right')
#label6 = tk.Label(text="", font=('Helvetica', 50), fg='black', bg='white', width='3',justify='right')
label101 = tk.Label(text="", font=('Helvetica', 44), fg='white', bg='limegreen', width='2')
label102 = tk.Label(text="", font=('Helvetica', 44), fg='white', bg='goldenrod', width='2')


# 상태 값, 1 온도 값, 2 습도 값, 3 포름알데히드 값, 4 PM10 값, 5 PM2.5 값, 6 PM1.0 값
label.place(x=924, y=321)
label1.place(x=1180, y=320)
label2.place(x=1464, y=320)
label3.place(x=1464, y=510)
label4.place(x=927, y=512)
label5.place(x=1200, y=512)
#label6.place(x=630, y=610)



from tkinter import simpledialog, messagebox

def quit_with_f12(event):
    print("F12 키로 종료됨")
    window.destroy()

window.bind("<F12>", quit_with_f12)

#update_clock()
window.mainloop()
