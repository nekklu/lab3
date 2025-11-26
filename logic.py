import datetime
import csv  # Модуль для работы с файлами
import os   # Модуль для проверки существования файла

class Task:
    """
    Класс, описывающий отдельную задачу.
    """
    def __init__(self, title: str, time: str):
        self.title = title
        self.time = time
        self.is_completed = False

    def __str__(self):
        return f"[{self.time}]  {self.title}"


class TaskManager:
    """
    Класс для управления списком задач (Model).
    """
    def __init__(self):
        self.tasks = []
        self.file_name = "tasks_db.csv" # Имя файла для сохранения

    def _normalize_time_input(self, time_str: str) -> str:
        """Приведение времени к формату ЧЧ:ММ."""
        for sep in ['-', '.', ' ', ',', ';']:
            time_str = time_str.replace(sep, ':')
        
        if ':' not in time_str and time_str.isdigit():
            if len(time_str) == 4:
                time_str = f"{time_str[:2]}:{time_str[2:]}"
            elif len(time_str) == 3:
                time_str = f"0{time_str[0]}:{time_str[1:]}"
            elif len(time_str) in (1, 2):
                time_str = f"{time_str.zfill(2)}:00"
        return time_str

    def add_task(self, title: str, time: str) -> None:
        """Добавляет задачу с валидацией."""
        normalized_input = self._normalize_time_input(time)
        try:
            dt = datetime.datetime.strptime(normalized_input, "%H:%M")
            formatted_time = dt.strftime("%H:%M")
        except ValueError:
            raise ValueError(f"Не удалось распознать время: '{time}'")

        new_task = Task(title, formatted_time)
        self.tasks.append(new_task)
        self.tasks.sort(key=lambda x: x.time)

    def delete_task_by_index(self, index: int) -> None:
        """Удаляет задачу по индексу."""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def get_all_tasks(self) -> list:
        """Возвращает список задач."""
        return self.tasks

    # --- НОВЫЕ МЕТОДЫ ДЛЯ СОХРАНЕНИЯ ---

    def save_to_file(self) -> None:
        """Сохраняет все задачи в CSV файл."""
        try:
            # encoding='utf-8' важен для поддержки русского языка
            with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                for task in self.tasks:
                    # Записываем: Название, Время, Выполнено ли
                    writer.writerow([task.title, task.time])
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load_from_file(self) -> None:
        """Загружает задачи из CSV файла при старте."""
        if not os.path.exists(self.file_name):
            return  # Если файла нет (первый запуск), ничего не делаем

        try:
            self.tasks = [] # Очищаем список перед загрузкой
            with open(self.file_name, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        title, time = row[0], row[1]
                        # Создаем задачу напрямую, минуя проверки (мы доверяем своему файлу)
                        new_task = Task(title, time)
                        self.tasks.append(new_task)
            
            # Сортируем после загрузки
            self.tasks.sort(key=lambda x: x.time)
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")