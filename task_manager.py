import threading

class TaskManager:
    def __init__(self):
        self.tasks: list[threading.Thread] = []

    def add_task(self, **kwargs):
        self.tasks.append(threading.Thread(**kwargs))

    def run_tasks(self):
        for task in self.tasks:
            task.start()