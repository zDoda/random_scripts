class SoftwareEngineer:
    def __init__(self, name, experience, skills):
        self.name = name
        self.experience = experience
        self.skills = skills

    def display_info(self):
        print(f"Name: {self.name}, Experience: {self.experience} years")
        print("Skills:")
        for skill in self.skills:
            print(skill)

se = SoftwareEngineer("John Doe", 5, ["Python", "Java", "SQL"])
se.display_info()
