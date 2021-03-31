from tkinter.messagebox import showerror
from tkinter.filedialog import *
from tkinter.font import *

from PIL import ImageTk, Image


def logic_code():
    #print("hello")
    secret_msg=msg.get()
    print(secret_msg)
    img=Image.open(img_name,'r')
    if len(secret_msg)==0:
        raise ValueError("data is empty")
    global newimg
    newimg=img.copy()
    #print(list(newimg.getdata()))
    #print()

    w=newimg.size[0]
    x,y=0,0
    for pixel in modify_pix(newimg.getdata(),secret_msg):
        newimg.putpixel((x,y),pixel)
        if x==w-1:
            x=0
            y+=1
        else:
            x+=1
    #print(list(newimg.getdata()))
    #print(decode())
    newimg.save("my_img.jpg")

def modify_pix(pix,msg):
    datalist=[]
    for i in msg:
        datalist.append(format(ord(i),'08b'))
    lendata=len(datalist)
    i_data=iter(pix)

    for i in range(lendata):
        pix=[value for value in i_data.__next__()[:3]+i_data.__next__()[:3]+i_data.__next__()[:3]]

        #odd for 1 and even for 0
        for j in range(0,8):
            if datalist[i][j]=='0' and pix[j]%2!=0:
                pix[j]-=1
            elif datalist[i][j]=='1' and pix[j]%2==0:
                if pix[j]!=0:
                    pix[j]-=1
                else:
                    pix[j]+=1
        if i==lendata-1:
            if pix[-1]%2==0:
                if pix[-1]!=0:
                    pix[-1]-=1
                else:
                    pix[-1]+=1
        else:
            if pix[-1]%2!=0:
                pix[-1]-=1
        pix=tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def decode():
    img=newimg
    print(type(img))
    #img=Image.open(newimg,'r')

    data=''
    img_data=iter(img.getdata())
    while(True):
        pixels=[value for value in img_data.__next__()[:3]+img_data.__next__()[:3]+img_data.__next__()[:3]]
        binstr=''
        for i in pixels[:8]:
            if i%2==0:
                binstr+='0'
            else:
                binstr+='1'
        data+=chr(int(binstr,2))
        if pixels[-1]%2!=0:
            return data

def get_decode_msg():
    if secret_pin.get()==pin.get():
        str = decode()
        print(str)
        decode_msg_entry.delete("1.0", END)
        decode_msg_entry.insert(END, str)
    else:
        showerror("ERROR", "YOUR PIN IS WRONG.PLEASE ENTER THE CORRECT PIN TO DECODE THE MESSAGE")

def show_img2():
    #img = Image.open(newimg, 'r')
    normal_img = ImageTk.PhotoImage(newimg)
    r = Toplevel(right_frame)
    show_label = Label(r, image=normal_img)
    show_label.pack(side=TOP)
    r.mainloop()

def show_img1():
    img = Image.open(img_name)
    print(type(img))
    #img_name = img_name.resize((100, 80), Image.ANTIALIAS)
    normal_img = ImageTk.PhotoImage(img)
    r = Toplevel(left_frame)
    show_label = Label(r, image=normal_img)
    show_label.pack(side=TOP)
    r.mainloop()

def choose_image():
    global img_name
    img_name = askopenfilename( defaultextension=".jpg",filetypes=[("All files", "*.*"),("image","*.jpg")])

root=Tk()
root.title("  IMAGE HIDER  ")
root.geometry('900x900')
root.configure(background='#FFA500')
left_frame = Frame(root, bg="cyan", height=100, width=600)
left_frame.pack(side=LEFT, padx=10, fill=BOTH)
img_name="img.jpg"
label1 = Label(left_frame, text="CHOOSE IMAGE : ", font="lucida 15 bold")
label1.place(x=10, y=15)
b1=Button(left_frame, text="choose image", font="lucida 15 bold", relief=SUNKEN,fg='red',command=choose_image,activebackground="green",activeforeground="white")
pin_label = Label(left_frame, text="Enter your secret pin : ", font="lucida 15 bold")
pin_label.place(x=10, y=80)
secret_pin = StringVar()
pin_entry = Entry(left_frame, textvariable=secret_pin, font="lucida 15 bold")
pin_entry.place(x=250, y=80)

msg_label = Label(left_frame, text="Enter your secret message : ", font="lucida 15 bold")
msg_label.place(x=10, y=150)
msg=StringVar()
msg_entry = Entry(left_frame,textvariable=msg, font="lucida 15 bold",  width=40)
msg_entry.place(x=20, y=200)
b2=Button(left_frame, text="Show Image", font="lucida 15 bold", height=5, width=10,
           command=show_img1,relief=SUNKEN,fg='red',activebackground="green",activeforeground="white")
b3=Button(left_frame, text="ENCODE", font="lucida 15 bold", command=logic_code,
           width=10, height=5,relief=SUNKEN,fg="red",activebackground="green",activeforeground="white")

b1.place(x=200, y=10)
b2.place(x=50, y=500)
b3.place(x=250, y=500)

# right frame
right_frame = Frame(root, bg="yellow")
right_frame.pack(side=RIGHT, padx=10, fill=BOTH, anchor=W)

pin_label = Label(right_frame, text="Enter your secret pin : ", font="lucida 15 bold")
pin_label.grid(row=0, column=0, pady=10)
pin = StringVar()
pin_entry = Entry(right_frame, textvariable=pin, font="lucida 15 bold")
pin_entry.grid(row=0, column=1, pady=10)

msg_label = Label(right_frame, text="Enter your secret message : ", font="lucida 15 bold")
msg_label.grid(row=3, column=0, padx=10)
decode_msg_entry = Text(right_frame, font="lucida 15 bold", height=5,width=35)
decode_msg_entry.grid(row=4, column=1, pady=10, padx=20)
b4=Button(right_frame, text="Show Image", font="lucida 15 bold", height=5, width=10,command=show_img2,relief=SUNKEN,activebackground="green",activeforeground="white").grid(row=5, column=0, pady=10)
decode_button = Button(right_frame, text="Decode", font="lucida 15 bold", command=get_decode_msg, relief=SUNKEN,activebackground="green",activeforeground="white",width=10, height=5)
decode_button.grid(row=5, column=1, pady=10)

# centre part
project = Frame(right_frame, bd=10, width=12, height=3, bg="red")
project.place(x=40, y=450)
font = Font(size=25, weight='bold', underline=1)
l_title = Label(project,
                    text="WELCOME \n TO MY FIRST SECRET MESSAGE  \n HIDER  SOFTWARE TO \n HIDE THE SECRET\n MESSAGE IMAGE",
                    font=font, justify=CENTER, pady=10, padx=40)
l_title.pack()

root.mainloop()
