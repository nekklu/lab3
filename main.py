import tkinter as tk
from tkinter import messagebox
import sys
from logic import TaskManager
from interface import DailyPlannerGUI

def main():
    """
    Главная функция запуска приложения.
    """
    try:
        # Инициализация корневого окна
        root = tk.Tk()
        
        # Инициализация логики
        manager = TaskManager()
        
        # Инициализация интерфейса
        app = DailyPlannerGUI(root, manager)
        
        # Запуск основного цикла
        root.mainloop()

    except Exception as e:
        # Глобальная обработка исключений, чтобы приложение не "падало" молча
        # В реальном GUI лучше показывать окно ошибки
        try:
            messagebox.showerror("Критическая ошибка", f"Произошла ошибка:\n{e}")
        except:
            # Если даже GUI не может запуститься, пишем в консоль
            print(f"Critical error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()