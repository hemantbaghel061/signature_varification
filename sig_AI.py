import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from PIL import Image, ImageTk
from signature import match

# Match Threshold
THRESHOLD = 85


def browsefunc(ent, img_label):
    filename = askopenfilename(filetypes=[
        ("Image Files", "*.jpeg;*.png;*.jpg")
    ])
    if filename:
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
        update_image(img_label, filename)


def capture_image_from_cam_into_temp(sign=1):
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow("Capture Signature")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("Capture Signature", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            img_name = f"./temp/test_img{sign}.png"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} saved!")
            break

    cam.release()
    cv2.destroyAllWindows()
    return True


def captureImage(ent, img_label, sign=1):
    filename = os.path.join(os.getcwd(), f'temp/test_img{sign}.png')

    res = messagebox.askquestion(
        'Capture Image', 'Press Space Bar to capture and ESC to exit')
    if res == 'yes':
        capture_image_from_cam_into_temp(sign=sign)
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)
        update_image(img_label, filename)


def checkSimilarity(path1, path2):
    if not path1 or not path2:
        messagebox.showerror("Error", "Please select both signature images!")
        return

    result = match(path1=path1, path2=path2)
    if result <= THRESHOLD:
        messagebox.showerror("Failure", f"Signatures do not match! Similarity: {result}%")
    else:
        messagebox.showinfo("Success", f"Signatures match! Similarity: {result}%")


def update_image(label, img_path):
    img = Image.open(img_path)
    img = img.resize((200, 100), Image.LANCZOS)  # Resize image
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img  # Keep reference


# GUI Setup
root = tk.Tk()
root.title("Signature Matching")
root.configure(bg='#90ee90')
root.geometry("550x500")

tk.Label(root, text="Compare Two Signatures:", font=12, bg='#90ee90').pack(pady=10)

# Signature 1
tk.Label(root, text="Signature 1", font=10, bg='#90ee90').place(x=10, y=60)
image1_path_entry = tk.Entry(root, font=10, width=40)
image1_path_entry.place(x=120, y=60)

image1_label = tk.Label(root, bg="white", width=200, height=100)
image1_label.place(x=120, y=90)

tk.Button(root, text="Capture", font=10,
          command=lambda: captureImage(image1_path_entry, image1_label, sign=1)).place(x=420, y=50)
tk.Button(root, text="Browse", font=10,
          command=lambda: browsefunc(image1_path_entry, image1_label)).place(x=420, y=90)

# Signature 2
tk.Label(root, text="Signature 2", font=10, bg='#90ee90').place(x=10, y=220)
image2_path_entry = tk.Entry(root, font=10, width=40)
image2_path_entry.place(x=120, y=220)

image2_label = tk.Label(root, bg="white", width=200, height=100)
image2_label.place(x=120, y=250)

tk.Button(root, text="Capture", font=10,
          command=lambda: captureImage(image2_path_entry, image2_label, sign=2)).place(x=420, y=210)
tk.Button(root, text="Browse", font=10,
          command=lambda: browsefunc(image2_path_entry, image2_label)).place(x=420, y=250)

# Compare Button
tk.Button(root, text="Compare", font=10,
          command=lambda: checkSimilarity(image1_path_entry.get(), image2_path_entry.get())).place(x=230, y=370)


bg_image = Image.open("sender.png")  # Replace with your image path
bg_image = bg_image.resize((500, 700))  # Resize to match the window
bg_photo = ImageTk.PhotoImage(bg_image)


root.mainloop()
