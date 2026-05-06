import tkinter as tk
from tkinter import colorchooser, messagebox

class SimpleDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python: Oddiy Rasm Chizish Dasturi")
        self.root.geometry("900x650") # Oyna hajmi
        self.root.configure(bg="#f0f0f0") # Fon rangi

        # --- Ichki o'zgaruvchilar ---
        self.pen_color = "black"    # Boshlang'ich rang
        self.eraser_color = "white" # O'chirgich rangi (fon bilan bir xil)
        self.pen_size = 5            # Boshlang'ich qalinlik
        self.old_x = None            # Chiziq boshi X
        self.old_y = None            # Chiziq boshi Y
        self.current_tool = "pen"   # Hozirgi asbob: 'pen' yoki 'eraser'

        # --- Interfeys qismlari ---

        # 1. Asboblar paneli (Yuqorida)
        self.toolbar = tk.Frame(self.root, bg="#dcdcdc", bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Rang tanlash tugmasi
        self.color_btn = tk.Button(self.toolbar, text="🎨 Rang Tanlash", 
                                   command=self.choose_color, bg="white", font=("Arial", 10))
        self.color_btn.pack(side=tk.LEFT, padx=10, pady=10)

        # Qalam tugmasi
        self.pen_btn = tk.Button(self.toolbar, text="✏️ Qalam", 
                                  command=self.use_pen, relief=tk.SUNKEN, font=("Arial", 10))
        self.pen_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # O'chirgich tugmasi
        self.eraser_btn = tk.Button(self.toolbar, text="🧽 O'chirgich", 
                                     command=self.use_eraser, font=("Arial", 10))
        self.eraser_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Qalinlikni tanlash (Slayder)
        self.size_label = tk.Label(self.toolbar, text="Qalinlik:", bg="#dcdcdc", font=("Arial", 10))
        self.size_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.size_slider = tk.Scale(self.toolbar, from_=1, to=30, orient=tk.HORIZONTAL, 
                                    command=self.change_size)
        self.size_slider.set(self.pen_size) # Boshlang'ich qiymat
        self.size_slider.pack(side=tk.LEFT, padx=5, pady=5)

        # Tozalash tugmasi (O'ngda)
        self.clear_btn = tk.Button(self.toolbar, text="🗑️ Hammasini Tozalash", 
                                    command=self.clear_canvas, bg="#ff9999", font=("Arial", 10, "bold"))
        self.clear_btn.pack(side=tk.RIGHT, padx=15, pady=10)


        # 2. Chizish maydoni (Canvas) - Pastda
        self.canvas = tk.Canvas(self.root, bg=self.eraser_color, width=900, height=550, bd=2, relief=tk.GROOVE)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # --- Sichqoncha hodisalarini bog'lash ---
        # Sichqoncha tugmasi bosilgan holda harakatlansa chizadi
        self.canvas.bind('<B1-Motion>', self.paint)
        # Sichqoncha tugmasi qo'yib yuborilsa chiziqni tugatadi
        self.canvas.bind('<ButtonRelease-1>', self.reset_coords)

    # --- Funksiyalar ---

    def paint(self, event):
        """Sichqoncha harakatlanganda chiziq chizish funksiyasi"""
        # Faqat oldingi nuqta mavjud bo'lsa chizamiz (chiziq uzilib qolmasligi uchun)
        if self.old_x and self.old_y:
            # Agar o'chirgich yoqilgan bo'lsa, fon rangida chizamiz
            color = self.eraser_color if self.current_tool == "eraser" else self.pen_color
            
            # Ikki nuqta orasida chiziq yaratish
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.pen_size, fill=color,
                                    capstyle=tk.ROUND, smooth=True)
        
        # Yangi chiziq boshi uchun hozirgi nuqtani saqlab qo'yamiz
        self.old_x = event.x
        self.old_y = event.y

    def reset_coords(self, event):
        """Sichqoncha tugmasi qo'yib yuborilganda koordinatalarni nolga tenglashtiradi"""
        # Bu funksiya har bir yangi chiziq alohida bo'lishini ta'minlaydi
        self.old_x = None
        self.old_y = None

    def choose_color(self):
        """Rang tanlash oynasini ochadi va qalam rangini o'zgartiradi"""
        # O'chirgich rejimidan chiqamiz
        self.use_pen() 
        
        color = colorchooser.askcolor(color=self.pen_color)[1] # Rang kodini olamiz (hex)
        if color:
            self.pen_color = color
            self.color_btn.configure(bg=color) # Tugma rangini ham yangilaymiz

    def use_pen(self):
        """Qalam rejimini yoqadi"""
        self.current_tool = "pen"
        # Tugmalar ko'rinishini yangilash (qaysi biri bosilganini ko'rsatish)
        self.pen_btn.configure(relief=tk.SUNKEN)
        self.eraser_btn.configure(relief=tk.RAISED)

    def use_eraser(self):
        """O'chirgich rejimini yoqadi"""
        self.current_tool = "eraser"
        # Tugmalar ko'rinishini yangilash
        self.eraser_btn.configure(relief=tk.SUNKEN)
        self.pen_btn.configure(relief=tk.RAISED)

    def change_size(self, size):
        """Slayder orqali qalam/o'chirgich qalinligini o'zgartiradi"""
        self.pen_size = int(size)

    def clear_canvas(self):
        """Foydalanuvchidan so'rab, butun maydonni tozalaydi"""
        confirm = messagebox.askyesno("Tasdiqlash", "Haqiqatan ham butun rasmni o'chirib tashlamoqchimisiz?")
        if confirm:
            self.canvas.delete("all")

if __name__ == "__main__":
    # Asosiy oynani yaratish va dasturni ishga tushirish
    root = tk.Tk()
    app = SimpleDrawingApp(root)
    root.mainloop()