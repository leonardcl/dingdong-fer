class User():
    def __init__(self, username=None, password=None, email=None, classes=None, user_id=None, role=None):
        self.username = username
        self.password = password
        self.email = email
        self.classes = classes
        self.user_id = user_id
        self.role = role
    
    def get_classes(self):
        pass
    
    def clear_data(self):
        self.username = None
        self.password = None
        self.email = None
        self.classes = None
        self.user_id = None
        self.role = None