import tkinter as tk
from tkinter import messagebox
import sys
from logic import TaskManager
from interface import DailyPlannerGUI

def main():
    try:
        root = tk.Tk()
        
        manager = TaskManager()
        
        app = DailyPlannerGUI(root, manager)
        
        root.mainloop()

    except Exception as e:
        # Глобальная обработка исключений, чтобы приложение не "падало" молча
        try:
            messagebox.showerror("Критическая ошибка", f"Произошла ошибка:\n{e}")
        except:
            # Если даже GUI не может запуститься, пишем в консоль
            print(f"Critical error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()