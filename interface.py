import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic import TaskManager

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.configure(bg="white")
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
    
        self.scrollable_content = tk.Frame(self.canvas, bg="white")
        
        # Обновляем область прокрутки при добавлении виджетов
        self.scrollable_content.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Размещаем фрейм внутри окна холста
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")

        # Растягиваем фрейм по ширине холста при ресайзе окна
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width)
        )

        # Связываем скроллбар обратно с холстом
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Упаковка элементов
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Привязка прокрутки колесиком мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class DailyPlannerGUI:
    #  Основной класс графического интерфейса приложения
    def __init__(self, root: tk.Tk, manager: TaskManager):
        self.root = root
        self.manager = manager
        
        self._setup_main_window()
        self._create_menu()
        self._create_widgets()
        
        # Загрузка данных и настройка выхода
        self._load_initial_data()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_window)

    def _setup_main_window(self):
        self.root.title("Планировщик дня")
        self.root.geometry("500x600")
        
        self.root.resizable(True, True)
        self.root.minsize(400, 500)

        style = ttk.Style()
        style.theme_use('clam')

        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabelframe", background=bg_color)
        style.configure("TLabelframe.Label", background=bg_color, font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background=bg_color, font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 9), padding=6)
        
        style.configure("Task.TCheckbutton", 
                        font=("Segoe UI", 11), 
                        background="white")
        
        style.configure("Done.Task.TCheckbutton", 
                        font=("Segoe UI", 11, "overstrike"), 
                        foreground="gray",
                        background="white")

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)
        
        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Сохранить", command=self.manager.save_to_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._on_close_window)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню "Вид" (Демонстрация работы с размерами окна)
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Сбросить размер", command=lambda: self.root.geometry("500x600"))
        view_menu.add_command(label="Компактный вид", command=lambda: self.root.geometry("400x500"))
        menu_bar.add_cascade(label="Вид", menu=view_menu)

        # Меню "Справка"
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Инфо", command=self._show_info)
        menu_bar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menu_bar)

    def _create_widgets(self):
        
        input_frame = ttk.LabelFrame(self.root, text="Новая задача", padding=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(input_frame, text="Время:").grid(row=0, column=0, sticky="w")
        self.time_entry = ttk.Entry(input_frame, width=10, font=("Segoe UI", 10))
        self.time_entry.grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=35, font=("Segoe UI", 10))
        self.title_entry.grid(row=1, column=1, padx=5, sticky="ew")
        
        add_btn = ttk.Button(input_frame, text="Добавить задачу", command=self._add_task_handler)
        add_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        # Растягиваем вторую колонку
        input_frame.columnconfigure(1, weight=1)

        list_container = ttk.LabelFrame(self.root, text="Список дел", padding=5)
        list_container.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tasks_frame = ScrollableFrame(list_container)
        self.tasks_frame.pack(fill="both", expand=True)

    def _add_task_handler(self):
        #Обработка нажатия кнопки 'Добавить'.
        time_val = self.time_entry.get().strip()
        title_val = self.title_entry.get().strip()
        
        if not time_val or not title_val:
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return
        
        try:
            self.manager.add_task(title_val, time_val)
            self._update_task_list()
            self.time_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
        except ValueError as ve:
            # Ловим ошибки формата времени
            messagebox.showerror("Ошибка формата", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка", f"{e}")

    def _update_task_list(self):
        for widget in self.tasks_frame.scrollable_content.winfo_children():
            widget.destroy()
        
        tasks = self.manager.get_all_tasks()
        
        if not tasks:
            # Если задач нет, показываем заглушку
            lbl = tk.Label(self.tasks_frame.scrollable_content, 
                           text="Список пуст", 
                           fg="gray", bg="white", font=("Segoe UI", 10))
            lbl.pack(pady=20)
            return
        
        for task in tasks:
            self._render_task_row(task)

    def _render_task_row(self, task: object):
        row_frame = tk.Frame(self.tasks_frame.scrollable_content, bg="white")
        row_frame.pack(fill="x", pady=2, padx=5)

        var = tk.BooleanVar(value=task.is_completed)
        style_name = "Done.Task.TCheckbutton" if task.is_completed else "Task.TCheckbutton"

        chk = ttk.Checkbutton(
            row_frame, 
            text=f"[{task.time}] {task.title}", 
            variable=var,
            style=style_name,
            command=lambda t=task: self._toggle_task(t)
        )
        chk.pack(side="left", fill="x", expand=True)

        del_btn = ttk.Button(
            row_frame, 
            text="✖", 
            width=3,
            command=lambda t=task: self._delete_task_handler(t)
        )
        del_btn.pack(side="right")


    def _toggle_task(self, task):
        self.manager.toggle_task_status(task)
        self._update_task_list() 

    def _delete_task_handler(self, task):
        try:
            self.manager.delete_task(task)
            self._update_task_list()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _load_initial_data(self):
        #Безопасная загрузка данных при старте.
        try:
            self.manager.load_from_file()
            self._update_task_list()
        except Exception:
            pass # Игнорируем ошибки при первом запуске

    def _on_close_window(self):
        self.manager.save_to_file()
        self.root.destroy()
        
    def _show_info(self):
        messagebox.showinfo("О программе", "Планировщик дня")