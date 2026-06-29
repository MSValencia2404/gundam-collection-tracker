# Gundam information file

# Create class for Gundam

class Gundam:
    STATUS_CHOICES = [
        "Unbuilt",
        "WIP",
        "Built",
        "Panel lined",
        "Painted"
    ]

    GRADE_CHOICES = [
        "EG",
        "HG",
        "RG",
        "MG",
        "MGEX",
        "PG",
        "SD",
        "FM",
        "PGU"
    ]
    
    #initiate self name
    def __init__(self, id, name, grade, series, status):
        self.id = id
        self.name = name
        self.grade = grade
        self.series = series
        self.status = status

    #For dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'series': self.series,
            'status': self.status
        }

    def display_info(self):
        print("\n==== GUNDAM INFORMATION ====")
        print("ID: " + self.id)
        print("Name: " + self.name)
        print("Grade: " + self.grade)
        print("Series: " + self.series)
        print("Status: " + self.status)

    def update(self, name=None, grade=None, series=None, status=None):
        if name:
            self.name = name
        if grade:
            self.grade = grade
        if series:
            self.series = series
        if status:
            self.status = status
