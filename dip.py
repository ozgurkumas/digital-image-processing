import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter

class PhotoViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Viewer App")
        self.heigth = 600
        self.width = 800
        self.root.geometry(str(self.width)+"x"+str(self.heigth)) # "800x600"
        root.resizable(False, False)

        self.image_label = tk.Label(root)
        self.image_label.pack(side="top")

        self.select_button = tk.Button(root, text="Dosya Seç", command=self.open_file_dialog)
        self.select_button.place(x=100,y=500)

        self.rotate_button = tk.Button(root, text="Döndür (90°)", command=self.rotate_image)
        self.rotate_button.place(x=200,y=500)

        self.blur_button = tk.Button(root, text="Blur", command=lambda: self.apply_filter("blur"))
        self.blur_button.place(x=300, y=500)

        self.laplac_button = tk.Button(root, text="Laplacian", command=lambda: self.apply_filter("laplacian"))
        self.laplac_button.place(x=400, y=500)

        self.alt_laplac_button = tk.Button(root, text="Laplacian2", command=lambda: self.apply_filter("alt_laplacian"))
        self.alt_laplac_button.place(x=500, y=500)

        self.smooth_button = tk.Button(root, text="Smooth", command=lambda: self.apply_filter("smooth"))
        self.smooth_button.place(x=600, y=500)

        self.noise_button = tk.Button(root, text="Noise", command=lambda: self.apply_filter("noise"))
        self.noise_button.place(x=100, y=550)

        self.mode_button = tk.Button(root, text="Mode", command=lambda: self.apply_filter("mode"))
        self.mode_button.place(x=200, y=550)

        self.find_edges_button = tk.Button(root, text="Find Edges", command=lambda: self.apply_filter("find_edges"))
        self.find_edges_button.place(x=300, y=550)

        self.undo_button = tk.Button(root, text="Undo", command=self.undo)
        self.undo_button.place(x=400, y=550)

        self.redo_button = tk.Button(root, text="Redo", command=self.redo)
        self.redo_button.place(x=500, y=550)

        self.save_button = tk.Button(root, text="Save Image", command=self.save_image_dialog)
        self.save_button.place(x=600, y=550)
        

        self.file_path = None
        self.rotated_image = None
        self.image_stack = []
        self.index = 0

        self.save_w = 0
        self.save_h = 0

    def save_image_dialog(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if file_path:
            self.save_image(file_path)
    
    def save_image(self, file_path):
        if self.rotated_image:
            w,h = self.rotated_image.size
            oran = int( ((self.save_w*self.save_h)/(w*h))**(1/2) )
            image = self.rotated_image
            image = image.resize((w*oran, h*oran), Image.LANCZOS)
            image.save(file_path)


    def multMatrix(self, matrix, k):
        for i in range(len(matrix)):
            matrix[i] *= k
    def addMatrix(self, matrix1, matrix2):
        for i in range(len(matrix1)):
            matrix1[i] += matrix2[i]

    def apply_filter(self, filter):
        laplacian = [0, -1, 0,
                     -1, 5, -1,
                     0, -1, 0]
        alt_laplacian = [-1, -1, -1,
                         -1, 9, -1,
                         -1, -1, -1]
        blur = [
                1, 1, 1, 1, 1,
                1, 0, 0, 0, 1,
                1, 0, 0, 0, 1,
                1, 0, 0, 0, 1,
                1, 1, 1, 1, 1 ]
        smooth = [1/9, 1/9, 1/9,
                1/9, 1/9, 1/9,
                1/9, 1/9, 1/9]
        find_edges = [
                    -1, -1, -1,
                    -1,  8, -1,
                    -1, -1, -1 ]
        laplac_filter = ImageFilter.Kernel((3, 3), laplacian, scale=1, offset=0)
        alt_laplac_filter = ImageFilter.Kernel((3, 3), alt_laplacian, scale=1, offset=0)
        blur = ImageFilter.Kernel((5, 5), blur, scale=16, offset=0)
        smooth = ImageFilter.Kernel((3, 3), smooth, scale=1, offset=0)
        find_edges = ImageFilter.Kernel((3, 3), find_edges, scale=1, offset=0)

        dic_ = { "blur": blur, "laplacian": laplac_filter, "alt_laplacian": alt_laplac_filter,
                 "smooth": smooth, "noise":ImageFilter.MedianFilter, "mode":ImageFilter.ModeFilter,
                 "find_edges":find_edges}
        self.rotated_image = self.rotated_image.filter(dic_[filter])
        
        if self.index == (len(self.image_stack) -1):
            self.index += 1
            self.image_stack.append(self.rotated_image)
        else:
            for i in range(0,  len(self.image_stack)-self.index-1 ):
                self.image_stack.pop()
            self.index += 1
            self.image_stack.append(self.rotated_image)
            
        if self.rotated_image:
            self.photo = ImageTk.PhotoImage(self.rotated_image)

            self.image_label.config(image=self.photo) #guncelle
            self.image_label.image = self.photo
    
    def undo(self):
        if self.index>0:
            self.index -= 1
            self.rotated_image = self.image_stack[self.index]

            self.photo = ImageTk.PhotoImage(self.rotated_image)

            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        
    def redo(self):
        if self.index < len(self.image_stack)-1:
            self.index += 1
            self.rotated_image = self.image_stack[self.index]

            self.photo = ImageTk.PhotoImage(self.rotated_image)

            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if self.file_path:
            self.display_image(self.file_path)
            self.convert_to_grayscale()
            self.image_stack = [self.rotated_image]

    def display_image(self, file_path):
        image = Image.open(file_path)
        width_, height_ = image.size
        self.save_w = width_
        self.save_h = height_
        boyut = self.heigth*2/3  # height(400)
        oran = width_ / height_ 
        image = image.resize((int(boyut * oran), int(boyut)), Image.LANCZOS)
        self.rotated_image = image
        self.photo = ImageTk.PhotoImage(self.rotated_image)

        self.image_label.config(image=self.photo)
        self.image_label.image = self.photo


    def rotate_image(self):
        if self.file_path and self.rotated_image:
            self.rotated_image = self.rotated_image.rotate(-90, expand=True)
            self.photo = ImageTk.PhotoImage(self.rotated_image)

            if self.index == (len(self.image_stack) -1):
                self.index += 1
                self.image_stack.append(self.rotated_image)
            else:
                for i in range(0,  len(self.image_stack)-self.index-1 ):
                    self.image_stack.pop()
                self.index += 1
                self.image_stack.append(self.rotated_image)

            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo


    def convert_to_grayscale(self):
        if self.rotated_image:
            self.rotated_image = self.rotated_image.convert("L") #grayscale
            self.photo = ImageTk.PhotoImage(self.rotated_image)

            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoViewerApp(root)
    root.mainloop()
