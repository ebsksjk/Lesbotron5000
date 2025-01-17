import tkinter as tk
from tkinter import filedialog as fd
import os
import fitz
from tkinter import messagebox
from pathlib import Path
import io
from PIL import Image, ImageTk

configFile = ".lb5000"
picdir = ".export"

def loadPDF():
    filename = fd.askopenfilename()
    autoextract = False

    if filename and os.path.isfile(filename) and filename.endswith(".pdf"):
        cf = open(configFile,"w")
        cf.write(filename)
        cf.close()

        print(Path(picdir).mkdir(parents=True, exist_ok=True))

        pfile = fitz.open(filename)

        for pi in range(len(pfile)):
            page = pfile.load_page(pi)  # load the page
            image_list = page.get_images(full=True)  # get images on the page

            # printing number of images found in this page
            if image_list:
                if autoextract:
                    extractPictures(image_list, picdir, filename, pfile, pi, page)

                print(f"[+] Found a total of {len(image_list)} images on page {pi}")
                if len(image_list) > 1 and not autoextract:
                    answer = messagebox.askyesnocancel("Multiple Images",
                                                       f"Multiple Images found on page {pi}. Do you want to extract them automatically (yes), only on this page (no) or abort (cancel)?")
                    if answer is None:
                        return
                    if answer:
                        #extract pictures from this site and all following
                        autoextract = True
                        extractPictures(image_list, picdir, filename, pfile, pi, page)
                    if not answer:
                        #extract only pictures from this site
                        extractPictures(image_list, picdir, filename, pfile, pi, page)


            else:
                print("[!] No images found on page", pi)

def extractPictures(imgArr, path, f, pfile, pi, page):
    filename = os.path.basename(f)
    print(f"path is {path}; image name is {filename}; cwd is {os.getcwd()}")
    #imgArr.sort(key=lambda x: (x[0], x[1]))

    images = []

    for img in imgArr:
        xref = img[0]
        if isinstance(xref, int) and xref > 0:
            try:
                # Try extracting the image, which will fail if it's not a valid image reference
                image_data = pfile.extract_image(xref)
                image_bytes = image_data["image"]
                image_ext = image_data["ext"]  # Get the image's extension (e.g., jpeg, png)

                # Get the image's bounding box (position)
                #bbox = page.get_image_bbox(xref)
                #x0, y0, x1, y1 = bbox  # Extract bounding box coordinates (x0, y0, x1, y1)

                # Store the image details along with its position
                images.append({
                    "page": pi,
                    "xref": xref,
                    #"x0": x0, "y0": y0, "x1": x1, "y1": y1,
                    "data": image_bytes,
                    "ext": image_ext
                })
            except Exception as e:
                print(f"Error extracting image from xref {xref}: {e}")
                continue  # Skip non-image objects or invalid xrefs
        else:
            print(f"Skipping non-image object with xref {xref}")

    #images.sort(key=lambda i: (round(i["y0"] / 5), i["x0"]))

    for image_index, img in enumerate(images):
        image_bytes = img["data"]

        # get the image extension
        image_ext = img["ext"]

        # save the image
        img_ind = "%03d"%image_index
        print(img_ind)
        image_name = f"{filename}_image{pi + 1}_{img_ind}.{image_ext}"
        with open(os.path.join(os.getcwd(), path, image_name), "wb") as image_file:
            image_file.write(image_bytes)
            print(f"[+] Image saved as {os.path.join(os.getcwd(),path, image_name)}")
