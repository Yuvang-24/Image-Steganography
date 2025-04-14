from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk
from stegano import lsb  # pip install stegano

# Initialize the root window
root = Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#2f4155")

# Global variable for secret image
secret = None

# Functions
def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetypes=(("PNG file", "*.png"),
                                                     ("JPG File", "*.jpg"),
                                                     ("ALL file", "*.txt")))
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img, width=250, height=250)
    lbl.image = img

def Hide():
    global secret
    message = text1.get(1.0, END).strip()  # Get the text and remove any extra spaces/newlines
    
    if message:  # Check if the message is not empty
        if filename:  # Ensure an image is selected
            secret = lsb.hide(str(filename), message)
            text1.delete(1.0, END)
            text1.insert(END, "Message Hidden!")
        else:
            text1.delete(1.0, END)
            text1.insert(END, "No image selected!")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "Please enter a message to hide.")

def Show():
    try:
        clear_message = lsb.reveal(filename)
        text1.delete(1.0, END)
        text1.insert(END, clear_message)
    except IndexError:
        text1.delete(1.0, END)
        text1.insert(END, "No hidden message detected.")
    except Exception as e:
        text1.delete(1.0, END)
        text1.insert(END, f"Error: {str(e)}")

def save():
    if secret is not None:
        # Get the current working directory (where the script is running)
        project_directory = os.getcwd()  # This gets the path where your Python script is located
        
        # Print the directory for debugging
        print(f"Saving to: {project_directory}")
        
        # Define the full path to save the hidden image (in the same folder as the script)
        save_path = os.path.join(project_directory, "hidden.png")
        
        # Save the image with the hidden message in the same directory
        try:
            secret.save(save_path)
            print(f"Image saved successfully at {save_path}")  # Debug message
            text1.delete(1.0, END)
            text1.insert(END, f"Image saved with hidden message at '{save_path}'.")
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            text1.delete(1.0, END)
            text1.insert(END, f"Error saving image: {str(e)}")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "No secret image to save. Please hide data first.")

# Icon
image_icon = PhotoImage(file=r"C:\Image Steganography\logo.jpg")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file=r"C:\Image Steganography\dd.png")
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)

# Header Text
Label(root, text="CYBER SCIENCE", bg="#2f4155", fg="white", font="arial 25 bold").place(x=100, y=20)

# First Frame
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame
frame2 = Frame(root, bd=3, width=340, height=280, bg="white", relief=GROOVE)
frame2.place(x=350, y=80)

text1 = Text(frame2, font="Roboto 20", bg="white", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)

# Scrollbar
scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth Frame
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo File", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Start the Tkinter event loop
root.mainloop()
