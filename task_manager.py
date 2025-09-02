import threading

class TaskManager:
    def __init__(self):
        self.tasks: list[object] = []

    def add_task(self, **kwargs):
        task = threading.Thread(**kwargs).start()
        self.tasks.append(task)