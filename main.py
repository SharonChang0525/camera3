from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image,ImageTk
from datetime import datetime
import os
import glob

hasSelectPath = False
imgSize = 0.8

def drawPictureCount(number_files):
    pictureCount_text = Label(gui, text = 'picture num' + str(number_files), font = ('Arial', 20))
    pictureCount_text.grid(row=4, column=3)

def getFolderPath():
    # create folder (if not exist)
    cmd1 = 'mkdir ' + folderPath.get() + "/cam1/"
    os.system(cmd1)
    cmd2 = 'mkdir ' + folderPath.get() + "/cam2/"
    os.system(cmd2)
    cmd3 = 'mkdir ' + folderPath.get() + "/cam3/"
    os.system(cmd3)
    
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    pictureCount = len(glob.glob1(folderPath.get() + '/cam1/',"*.jpg"))
    drawPictureCount(pictureCount)
    hasSelectPath = True


def take_snapshot():
    success, img = camera.read()  # 从摄像头读取照片
    success2, img2 = camera2.read()  # 从摄像头读取照片
    success3, img3 = camera3.read()  # 从摄像头读取照片
    # print('file_list {}'.format(file_list))


    if success and success2 and success3:
        # photo name
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")

        #img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_AREA)
        pth = folderPath.get() + "/cam1/" + dt_string + ".jpg"

        #img2 = cv2.resize(img2, (640, 480), interpolation=cv2.INTER_AREA)
        pth2 = folderPath.get() + "/cam2/" + dt_string + ".jpg"

        #img3 = cv2.resize(img3, (640, 480), interpolation=cv2.INTER_AREA)
        pth3 = folderPath.get() + "/cam3/" + dt_string + ".jpg"

        # save image
        cv2.imwrite(pth, img)
        cv2.imwrite(pth2, img2)
        cv2.imwrite(pth3, img3)
	
        pictureCount = len(glob.glob1(folderPath.get() + '/cam1/',"*.jpg"))
        drawPictureCount(pictureCount)

def video_loop():
    success, img = camera.read()  # 从摄像头读取照片

    success2, img2 = camera2.read()  # 从摄像头读取照片
    success3, img3 = camera3.read()  # 从摄像头读取照片

    if success and success2 and success3 :
        # camera
        cv2.waitKey(1)
        img = cv2.resize(img, ((int)(640 * imgSize), (int)(480 * imgSize)), interpolation=cv2.INTER_AREA)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        # gui.after(1, video_loop)
    
        # camera2
        img2 = cv2.resize(img2, ((int)(640 * imgSize), (int)(480 * imgSize)), interpolation=cv2.INTER_AREA)
        cv2image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image2 = Image.fromarray(cv2image2)#将图像转换成Image对象
        
        imgtk2 = ImageTk.PhotoImage(image=current_image2)
        panel2.imgtk = imgtk2
        panel2.config(image=imgtk2)
	
	# camera3
        img3 = cv2.resize(img3, ((int)(640 * imgSize), (int)(480 * imgSize)), interpolation=cv2.INTER_AREA)
        cv2image3 = cv2.cvtColor(img3, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image3 = Image.fromarray(cv2image3)#将图像转换成Image对象
        
        imgtk3 = ImageTk.PhotoImage(image=current_image3)
        panel3.imgtk = imgtk3
        panel3.config(image=imgtk3)
	
        gui.after(1, video_loop)
    
    
gui = Tk()
gui.geometry("1600x1000")
gui.title("Camera 3")

#-- Camera Initialize --#
camera = cv2.VideoCapture(0)    #摄像头
camera2 = cv2.VideoCapture(1) 
camera3 = cv2.VideoCapture(2)

folderPath = StringVar()
a = Label(gui ,text="Enter folder name", font=('Arial', 15))
a.grid(row=0,column = 0)
E = Entry(gui,textvariable=folderPath, width=50)
E.grid(row=0,column=1)
btnFind = ttk.Button(gui, text="Browse Folder",command=getFolderPath, width=20)
btnFind.grid(row=0,column=2, sticky = 'w')

#-- Camera Show --#
panel = Label(gui)  # initialize image panel
panel.grid(row=2,column = 1)
panel_text = Label(gui ,text="cam1", font=('Arial', 20))
panel_text.grid(row=1,column = 1)

panel2 = Label(gui)  # initialize image panel
panel2.grid(row=2,column = 2)
panel_text2 = Label(gui ,text="cam2", font=('Arial', 20))
panel_text2.grid(row=1,column = 2)

panel3 = Label(gui)  # initialize image panel
panel3.grid(row=4,column = 1)
panel3_text = Label(gui ,text="cam3", font=('Arial', 20))
panel3_text.grid(row=3,column = 1)

gui.config(cursor="arrow")
btn = Button(gui, text="capture", command=take_snapshot, width=20, height=5, font=('Arial', 20))
btn.grid(row=4,column = 2)

#-- Picture Count --#
pictureCount = 0
#pictureCount_text = Label(gui ,text='picture num: ' + str(pictureCount), font=('Arial', 20))
#pictureCount_text.grid(row=4,column = 3)

drawPictureCount(0)
video_loop()

gui.mainloop()
# 当一切都完成后，关闭摄像头并释放所占资源
camera.release()
camera2.release()
camera3.release()
cv2.destroyAllWindows()
