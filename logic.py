import datetime
import csv
import os

class Task:
    def __init__(self, title: str, time: str, is_completed: bool = False):
        self.title = title
        self.time = time
        self.is_completed = is_completed

    def __str__(self):
        status = "[x]" if self.is_completed else "[ ]"
        return f"{status} {self.time} - {self.title}"


class TaskManager:
    # Отвечает за добавление, удаление, сортировку задач и работу с файловой системой.
    def __init__(self):
        self.tasks = []
        self.file_name = "tasks_db.csv" 

    def _normalize_time_input(self, time_str: str) -> str:
        # Превращает '1020', '10-20' в '10:20', '10:20'
        for sep in ['-', '.', ' ', ',', ';']:
            time_str = time_str.replace(sep, ':')
        
        # Если разделителей нет, пытаемся понять логику по длине строки
        if ':' not in time_str and time_str.isdigit():
            if len(time_str) == 4:    # "1020" -> "10:20"
                time_str = f"{time_str[:2]}:{time_str[2:]}"
            elif len(time_str) == 3:  # "930" -> "09:30"
                time_str = f"0{time_str[0]}:{time_str[1:]}"
            elif len(time_str) in (1, 2): # "9" -> "09:00"
                time_str = f"{time_str.zfill(2)}:00"
        return time_str



    def add_task(self, title: str, time: str) -> None:
        # Создает новую задачу и добавляет её в список.
        # Выбрасывает ValueError, если время указано некорректно.
        normalized_input = self._normalize_time_input(time)
        
        try:
            # Парсим время для проверки валидности (часы 0-23, минуты 0-59)
            dt = datetime.datetime.strptime(normalized_input, "%H:%M")
            formatted_time = dt.strftime("%H:%M")
        except ValueError:
            raise ValueError(f"Не удалось распознать время: '{time}'. Используйте формат ЧЧ:ММ.")

        new_task = Task(title, formatted_time)
        self.tasks.append(new_task)
        
        # Автоматическая сортировка списка по времени
        self.tasks.sort(key=lambda x: x.time)

    def delete_task(self, task: Task) -> None:
        if task in self.tasks:
            self.tasks.remove(task)

    def toggle_task_status(self, task: Task) -> None:
        task.is_completed = not task.is_completed

    def get_all_tasks(self) -> list:
        return self.tasks

    def save_to_file(self) -> None:
        try:
            with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                for task in self.tasks:
                    # Сериализуем объект в строку CSV
                    writer.writerow([task.title, task.time, str(task.is_completed)])
        except Exception as e:
            print(f"Ошибка сохранения базы данных: {e}")

    def load_from_file(self) -> None:
        if not os.path.exists(self.file_name):
            return  # Файла нет — начинаем с чистого листа

        try:
            self.tasks = []
            with open(self.file_name, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        title = row[0]
                        time = row[1]
                        # Восстанавливаем булево значение из строки
                        is_completed = (row[2] == 'True') if len(row) > 2 else False
                        
                        new_task = Task(title, time, is_completed)
                        self.tasks.append(new_task)
            
            # Сортируем после загрузки, на случай если файл редактировали вручную
            self.tasks.sort(key=lambda x: x.time)
        except Exception as e:
            print(f"Ошибка загрузки базы данных: {e}")