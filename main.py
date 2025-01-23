import os
import tkinter as tk
from tkinter import ttk
import ltlogic
import math
from PIL import Image, ImageTk

# Create the main application window
root = tk.Tk()
root.title("Lesbotron5000")
root.geometry("900x600")  # Set window size

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Load images")

# Tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Render video")

# Layout for Tab 1
# Create a frame for the left section (textboxes and buttons)
left_frame_tab1 = tk.Frame(tab1)
left_frame_tab1.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Add textboxes and buttons to the left frame
tk.Label(left_frame_tab1, text=f"Vertical Distance").pack(pady=5)
tk.Entry(left_frame_tab1).pack(pady=5)
tk.Label(left_frame_tab1, text=f"Horizontal Distance").pack(pady=5)
tk.Entry(left_frame_tab1).pack(pady=5)
tk.Label(left_frame_tab1, text=f"Picture Height").pack(pady=5)
tk.Entry(left_frame_tab1).pack(pady=5)
tk.Label(left_frame_tab1, text=f"Picture Width").pack(pady=5)
tk.Entry(left_frame_tab1).pack(pady=5)

tk.Button(left_frame_tab1, text="Apply").pack(pady=7)
tk.Button(left_frame_tab1, text="Load .pdf", command=ltlogic.loadPDF).pack(pady=5)
tk.Button(left_frame_tab1, text="Export pictures").pack(pady=5)

# Create a highlighted picture frame for the right section
right_frame_tab1 = tk.Frame(tab1, bd=2, relief="solid", padx=10, pady=10)
right_frame_tab1.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# DocPicture fills the frame
doc_picture = tk.Label(right_frame_tab1, text="DocPicture", bg="gray")
doc_picture.pack(expand=True, fill=tk.BOTH)

nav_button_frame = tk.Frame(right_frame_tab1)
nav_button_frame.pack(pady=5)

prev_button = tk.Button(nav_button_frame, text="<")
prev_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(nav_button_frame, text=">")
next_button.pack(side=tk.RIGHT, padx=5)

# Layout for Tab 2
# Create a frame for the left section (textbox and button)
left_frame_tab2 = tk.Frame(tab2)
left_frame_tab2.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

image_references = {}

def cloadImages():
    picdir = ".export"
    imgs = []
    global image_references

    for root, dirs, files in os.walk(picdir):
        for file in files:
            imgs.append(os.path.join(root, file))

    rows = math.ceil(len(imgs) / 4)

    for i in imgs:
        row = 0;
        for col in range(4):  # Adjust columns as needed
            image = Image.open(i)
            image = image.resize((20, 20))
            timage = ImageTk.PhotoImage(image)

            image_references[(row, col)] = timage

            pic_label = tk.Label(
                picture_frame,
                image = timage,
                width=20,  # Placeholder width
                height=10,  # Placeholder height
            )
            pic_label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        row += 1

# Add textbox and button to the left frame
tk.Button(left_frame_tab2, text="Load images", command=cloadImages).pack(pady=5)
tk.Label(left_frame_tab2, text="Framerate").pack(pady=5)
framerate = tk.Entry(left_frame_tab2)
framerate.pack(pady=5)



# Create a highlighted picture frame for the right section
right_frame_tab2 = tk.Frame(tab2, bd=2, relief="solid", padx=10, pady=10)
right_frame_tab2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add a canvas with a scrollbar for the picture grid
canvas = tk.Canvas(right_frame_tab2)
scrollbar = tk.Scrollbar(right_frame_tab2, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create the picture frame within the canvas
picture_frame = tk.Frame(canvas)

# Configure the canvas to scroll
canvas.create_window((0, 0), window=picture_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add Pictures to the grid inside the picture frame


# Configure the grid to scale pictures
for col in range(4):
    picture_frame.grid_columnconfigure(col, weight=1)
for row in range(5):
    picture_frame.grid_rowconfigure(row, weight=1)

# Update the canvas scroll region whenever the frame changes
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

picture_frame.bind("<Configure>", on_frame_configure)

# Run the application

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)

def renderVideo():
    import ffmpeg
    import glob

    picdir = ".export"
    fps = framerate.get()

    if fps == "" or fps == None:
        tk.messagebox.showerror("Error", "Please enter video framerate")
        return

    file_pattern = os.path.join(os.getcwd(), picdir, "*.jpeg")  # Change extension if needed
    input_files = glob.glob(file_pattern)
    print(input_files)

    with open('file_list.txt', 'w') as f:
        for file in input_files:
            f.write(f"file '{file}'\n".replace("\\", "/"))

    ffmpeg.input(os.path.join(os.getcwd(), 'file_list.txt'), format='concat', safe=0).output("out.mp4", r=fps).run(overwrite_output=True)


tk.Button(left_frame_tab2, text="Render video", command=renderVideo).pack(pady=5)

root.mainloop()