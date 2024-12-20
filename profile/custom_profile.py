class UserProfile:
    def __init__(self, id, name=None, age=None):
        self.id = id
        self.name = name
        self.age = age

    def set_profile_name(self, name):
        self.name = name

    def set_profile_age(self, age):
        self.age = age

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}"