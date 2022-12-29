from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tk_message


def root_window_resize_picture(label_size):
    global picture
    """ Function : picture resize
        fit the longest size of width or height with scale of picture """
    label_scale = label_size[0] / label_size[1]
    picture_scale = picture.size[0] / picture.size[1]
    if label_scale >= picture_scale:
        height = label_size[1]
        width = int(height * picture_scale)
    else:
        width = label_size[0]
        height = int(width * picture_scale)
    picture = picture.resize((width, height))


def root_window_check_file_path(_picture_path):
    if _picture_path == "":
        return False
    return True


def root_window_choose_file():
    global picture_path
    picture_path = filedialog.askopenfilename()  # 绝对路径
    print(picture_path)


def root_window_change_picture():
    global picture
    global picture_path
    global image_label
    global root
    global pic
    global screen_size
    root_window_choose_file()
    try:
        picture = Image.open(picture_path)
        pic['obj'] = picture
        print(pic)
        image_label.config(width=int(screen_size[0] * 0.4), height=int(screen_size[1] * 0.4))
        _label_size = (image_label.cget('width'), image_label.cget('height'))
        root_window_resize_picture(_label_size)
        picture = ImageTk.PhotoImage(picture)

        # 对抗python垃圾回收机制，这两行不冲突
        image_label.config(image=picture)
        image_label.image = picture
    except Exception as e:
        print(e)


def init_root_GUI():
    global screen_size
    global root_window
    global image_label
    global change_picture_button
    global button_frame
    global root
    global image_frame

    _current_dimension = (int(screen_size[0] * 0.8), int(screen_size[1] * 0.8))
    _init_geometry = str(_current_dimension[0]) + "x" + str(_current_dimension[1])  # width x height
    root_window.geometry(_init_geometry)
    root_window.title("Simple Photo Tools v1.0")
    image_label.config(width=75, height=10)
    image_label.pack()
    image_frame.grid(row=0, column=1, padx='5px')
    change_picture_button.grid(row=0, column=1, pady='6px')
    to_resize_button.grid(row=1, column=1, pady='6px')
    save_picture_button.grid(row=2, column=1, pady='6px')
    button_frame.grid(row=0, column=2, padx='6px')
    root.pack()
    root_window.resizable(False, False)
    root_window.mainloop()


def init_resize_GUI():
    global temp_size
    global temp_picture
    global resize_window
    global width_text_field
    global height_text_field

    resize_window = tk.Toplevel()
    resize_window.geometry('300x180')
    resize_window.resizable(False, False)
    resize_label_frame = tk.Frame(resize_window, bg='#00ff22')
    resize_label1 = tk.Label(resize_label_frame, width=5, text="width")  # width-text-label
    resize_label2 = tk.Label(resize_label_frame, width=5, text="height")  # height-text-label
    width_text_field = tk.Text(resize_label_frame, width=10, height=1)  # width-text-field
    height_text_field = tk.Text(resize_label_frame, width=10, height=1)  # height-text-field
    resize_window_button_frame = tk.Frame(resize_window)
    resize_window_start_button = tk.Button(resize_window_button_frame, text="start", command=resize_window_resize)
    resize_window_confirm_button = tk.Button(resize_window_button_frame, text="Confirm", command=resize_window_confirm)
    resize_window_cancel_button = tk.Button(resize_window_button_frame, text="Cancel", command=resize_window_close)

    temp_size = (0, 0)
    temp_picture = None

    width_text_field.delete('1.0', tk.END)
    height_text_field.delete('1.0', tk.END)

    resize_label1.pack()
    width_text_field.pack()
    resize_label2.pack()
    height_text_field.pack()
    resize_label_frame.pack()

    resize_window_start_button.grid(row=1, column=1, pady='3px', padx='10px')
    resize_window_confirm_button.grid(row=1, column=2, pady='3px', padx='10px')
    resize_window_cancel_button.grid(row=1, column=3, pady='3px', padx='10px')
    resize_window_button_frame.pack()

    resize_window.mainloop()


def resize_window_resize():
    global pic
    global width_text_field
    global height_text_field
    global temp_size
    global temp_picture

    initial_size = pic['obj'].size
    try:
        width = int(width_text_field.get('1.0', tk.END))
        height = int(height_text_field.get('1.0', tk.END))
        if 50 > width > 0 or 50 > height > 0:
            tk_message.showerror(title='Error', message="Please Check You Picture Details")
        temp_picture = pic['obj'].resize((width, height))
        temp_size = (width, height)
        tk_message.showinfo(title="Finished", message="Resize Picture Successfully")
    except Exception as e:
        print(e)
        tk_message.showerror(title='Error', message="Please Check You Picture Details")
        pass


def resize_window_confirm():
    global resize_window
    global temp_picture
    global pic
    if temp_picture is not None:
        pic['obj'] = temp_picture
        resize_window.destroy()
    else:
        tk_message.showerror(title='Error', message="Please Check You Picture Details")


def resize_window_close():
    global resize_window
    global temp_picture
    temp_picture = None
    resize_window.destroy()


def init_save_GUI():
    global pic
    if pic['obj'] is not None:
        save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('picture', '*.png *.jpg'), ('All files', '*')])
        try:
            pic['obj'].save(save_path)
        except Exception as e:
            tk_message.showerror(title='Error', message="No Picture File can be Saved")
    else:
        tk_message.showerror(title='Error', message="No Picture File can be Saved")


if __name__ == "__main__":
    picture = None
    picture_path = ""
    pic = dict()
    pic['path'] = picture_path
    pic['obj'] = picture

    # root_window
    root_window = tk.Tk()
    root = tk.Frame(root_window)
    screen_size = (root_window.winfo_screenwidth(), root_window.winfo_screenheight())

    image_frame = tk.Frame(root, bg="#FF5533", bd=3, class_='good')
    image_label = tk.Label(image_frame, text="PICTURE")

    button_frame = tk.Frame(root, bd=3, class_='good')
    change_picture_button = tk.Button(button_frame, width=20, text="Choose Picture", command=root_window_change_picture)
    to_resize_button = tk.Button(button_frame, width=20, text="Resize Picture", command=init_resize_GUI)
    save_picture_button = tk.Button(button_frame, width=20, text="Save", command=init_save_GUI)

    # resize_window
    resize_window = None
    width_text_field = None
    height_text_field = None
    temp_size = (0, 0)
    temp_picture = None

    init_root_GUI()
