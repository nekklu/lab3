import tkinter as tk
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

    def _setup_main_window(self):
        """Настройка основного окна приложения."""
        self.root.title("Планировщик дня")
        self.root.geometry("400x500")
        self.root.minsize(300, 400)  # Возможность изменения размеров, но не меньше этого

    def _create_menu(self):
        """Создание меню приложения (Файл, Справка)."""
        menu_bar = tk.Menu(self.root)
        
        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню "О программе"
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Инфо", command=self._show_info)
        menu_bar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _create_widgets(self):
        """Создание базовых виджетов (заглушка для первого коммита)."""
        self.label = tk.Label(self.root, text="Список задач пуст", font=("Arial", 12))
        self.label.pack(pady=20)

    def _show_info(self):
        """Отображение информации о программе."""
        messagebox.showinfo("О программе", "Планировщик дня v0.1\nЛабораторная работа")