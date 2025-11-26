import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic import TaskManager

class DailyPlannerGUI:
    """
    Класс графического интерфейса приложения.
    """
    def __init__(self, root: tk.Tk, manager: TaskManager):
        self.root = root
        self.manager = manager
        
        self._setup_main_window()
        self._create_menu()
        self._create_widgets()
        
        # --- НОВОЕ: Загрузка и настройка выхода ---
        self._load_initial_data()
        
        # Перехватываем нажатие на крестик окна
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_window)

    def _setup_main_window(self):
        self.root.title("Планировщик дня")
        self.root.geometry("450x550")
        self.root.minsize(400, 500)
        style = ttk.Style()
        style.configure("TButton", padding=6)

    def _create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        # Кнопка "Выход" теперь тоже должна вызывать наш метод закрытия
        file_menu.add_command(label="Выход", command=self._on_close_window) 
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Инфо", command=self._show_info)
        menu_bar.add_cascade(label="Справка", menu=help_menu)
        self.root.config(menu=menu_bar)

    def _create_widgets(self):
        # (Этот код остается тем же, что и раньше)
        input_frame = ttk.LabelFrame(self.root, text="Новая задача", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame, text="Время (ЧЧ:ММ):").grid(row=0, column=0, sticky="w")
        self.time_entry = ttk.Entry(input_frame, width=10)
        self.time_entry.grid(row=0, column=1, padx=5, sticky="w")

        ttk.Label(input_frame, text="Задача:").grid(row=1, column=0, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=40)
        self.title_entry.grid(row=1, column=1, padx=5, sticky="ew")

        add_btn = ttk.Button(input_frame, text="Добавить", command=self._add_task_handler)
        add_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        list_frame = ttk.LabelFrame(self.root, text="Список дел", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.task_listbox = tk.Listbox(list_frame, font=("Arial", 10), selectmode=tk.SINGLE)
        self.task_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(fill="x")
        del_btn = ttk.Button(bottom_frame, text="Удалить выбранное", command=self._delete_task_handler)
        del_btn.pack(fill="x")

    def _add_task_handler(self):
        # (Код тот же)
        time_val = self.time_entry.get().strip()
        title_val = self.title_entry.get().strip()
        if not time_val or not title_val:
            messagebox.showwarning("Внимание", "Все поля должны быть заполнены!")
            return
        try:
            self.manager.add_task(title_val, time_val)
            self._update_task_list()
            self.time_entry.delete(0, tk.END)
            self.title_entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("Ошибка формата", str(ve))
        except Exception as e:
            messagebox.showerror("Критическая ошибка", f"Что-то пошло не так:\n{e}")

    def _delete_task_handler(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showinfo("Внимание", "Выберите задачу для удаления.")
            return
        try:
            index = selection[0]
            self.manager.delete_task_by_index(index)
            self._update_task_list()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить задачу:\n{e}")

    def _update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.manager.get_all_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, str(task))

    def _show_info(self):
        messagebox.showinfo("О программе", "Планировщик дня v1.1\nСохранение данных")

    # --- НОВЫЕ МЕТОДЫ ИНТЕРФЕЙСА ---

    def _load_initial_data(self):
        """Загрузка данных при старте."""
        self.manager.load_from_file()
        self._update_task_list()

    def _on_close_window(self):
        """Действия при закрытии окна."""
        # Можно спросить подтверждение, но обычно автосохранение удобнее
        # if messagebox.askokcancel("Выход", "Вы уверены?"):
        self.manager.save_to_file()
        self.root.destroy()