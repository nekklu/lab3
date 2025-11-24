import datetime

class Task:
    """
    Класс, описывающий отдельную задачу.
    """
    def __init__(self, title: str, time: str):
        self.title = title
        self.time = time
        self.is_completed = False

    def __str__(self):
        return f"{self.time} - {self.title}"


class TaskManager:
    """
    Класс для управления списком задач.
    Реализует добавление, удаление и получение задач.
    """
    def __init__(self):
        self.tasks = []

    def add_task(self, title: str, time: str) -> None:
        """Добавляет новую задачу в список."""
        new_task = Task(title, time)
        self.tasks.append(new_task)
        # Сортировка по времени будет добавлена позже

    def get_all_tasks(self) -> list:
        """Возвращает список всех задач."""
        return self.tasks