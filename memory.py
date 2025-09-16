class Memory:
    def __init__(self):
        self.log = []

    def add(self, agent, message):
        self.log.append(f"{agent}: {message}")

    def get_log(self):
        return self.log
