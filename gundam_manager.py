# Gundam manager for collection

# Import Gundam file
from gundam import Gundam
from utils.file_handler import save_data, load_data, clear_data
from tabulate import tabulate
from datetime import datetime
import csv
import math


# Initiate class for manager
class GundamManager:
    def __init__(self):
        self.collection = []
        self.next_id = 1

    def initialize_next_id(self):

        if not self.collection:
            self.next_id = 1
            return
        self.next_id = (
                max(
                    int(g.id.replace("GDM", ""))
                    for g in self.collection
                ) + 1
        )

    def generate_id(self):
        gundam_id = f"GDM{self.next_id:03d}"
        self.next_id += 1
        return gundam_id

    def get_status(self):
        while True:
            print("What is the status of the Gundam?")

            for i, status in enumerate(Gundam.STATUS_CHOICES, start=1):
                print(f"{i}. {status}")

            choice = input("Enter your choice (Default: Unbuilt): ")

            if not choice:
                return Gundam.STATUS_CHOICES[0]

            if choice.isdigit():
                choice = int(choice)

                if 1 <= choice <= len(Gundam.STATUS_CHOICES):
                    return Gundam.STATUS_CHOICES[choice - 1]

            print("Invalid choice. Please try again.")


    # GRADE check
    def get_grade(self):
        while True:
            print("Grade of the Gundam:")

            for i, grade in enumerate(Gundam.GRADE_CHOICES, start=1):
                print(f"{i}. {grade}")

            choice = input("Enter your choice (Default: HG): ")

            if not choice:
                return Gundam.GRADE_CHOICES[0]

            if choice.isdigit():
                choice = int(choice)

                if 1 <= choice <= len(Gundam.GRADE_CHOICES):
                    return Gundam.GRADE_CHOICES[choice - 1]

            print("Invalid choice. Please try again.")

    def save_collection(self):
        save_data("./data/gundams.json", self.collection)

    # Add Gundam to data
    def add_gundam(self):
        gundam_id = self.generate_id()
        name = input("Enter the Gundam: ")
        grade = self.get_grade()
        series = input("Enter the Gundam Series: ")
        status = self.get_status()
        new_gundam = Gundam(gundam_id,name,grade,series,status)
        self.collection.append(new_gundam)
        self.save_collection()
        print(f"{name} added successfully!")

    # View Gundam collection
    def view_collection(self):

        if not self.collection:
            print("No Gundam in collection")
            return

        # Pagination
        page = 0
        page_size = 5
        total_items = len(self.collection)
        total_pages = math.ceil(len(self.collection) / page_size)

        while True:
            start = page * page_size
            end = start + page_size

            showing_from = start + 1
            showing_to = min(end, total_items)

            page_data = self.collection[start:end]

            table = []

            for gundam in page_data:
                table.append([
                    gundam.id,
                    gundam.name,
                    gundam.grade,
                    gundam.series,
                    gundam.status
                ])
            print(f"\n==== MY GUNDAM COLLECTION ====\n")

            print(tabulate(
                table,
                headers=["ID", "Name", "Grade", "Series", "Status"],
                tablefmt="fancy_grid"
            ))
            print(f"\nShowing {showing_from} to {showing_to} of {total_items} Gundams")
            print(f"Page {page + 1} of {total_pages}\n")

            print("[N] Next Page | [P] Previous Page | [B] Back")
            choice = input("Select option: ").upper()

            if choice == "N":
                if page < total_pages - 1:
                    page += 1
                else:
                    print("⚠️ You are already on the last page.")
            elif choice == "P":
                if page > 0:
                    page -= 1
                else:
                    print("⚠️ You are already on the first page.")
            elif choice == "B":
                break
            else:
                print("❌ Invalid option.")

    #Search Gundam ID
    def search_gundam(self, gundam_id):
        for gundam in self.collection:
            if gundam_id == gundam.id:
                table = [[
                    gundam.id,
                    gundam.name,
                    gundam.grade,
                    gundam.series,
                    gundam.status
                ]]

                print(tabulate(
                    table, headers=["ID", "Name", "Grade", "Series","Status"],
                    tablefmt="fancy_grid"
                ))
                return gundam
        print("Gundam not in collection")
        return None

    # Update Gundam
    def update_gundam(self):
        gundam_id = input("Enter the Gundam ID: ").strip().upper()
        result = self.search_gundam(gundam_id)
        if not result:
            print("❌ Gundam not found.")
            return

        print("\nCurrent Details")
        print(f"Name: {result.name}")
        print(f"Grade: {result.grade}")
        print(f"Series: {result.series}")
        print(f"Status: {result.status}")

        name = result.name
        name = input("New Name: ") or name
        grade = result.grade
        for i, grade in enumerate(Gundam.GRADE_CHOICES, start=1):
            print(f"{i}. {grade}")

        grade_choice = input("New Grade: (Enter to keep current grade): ")


        if grade_choice:
            try:
                grade = Gundam.GRADE_CHOICES[int(grade_choice) - 1]
            except (ValueError, IndexError):
                print("❌ Invalid grade selection.")
                return
        series = result.series
        series = input("New Series: ") or series
        status = result.status
        for i, status in enumerate(Gundam.STATUS_CHOICES, start=1):
            print(f"{i}. {status}")

        status_choice = input("Current Status: (Enter to keep current status): ")


        if status_choice:
            try:
                status = Gundam.STATUS_CHOICES[int(status_choice) - 1]
            except (ValueError, IndexError):
                print("❌ Invalid status selection.")
                return

        result.update(
            name=name,
            grade=grade,
            series=series,
            status=status
        )

        self.save_collection()
        print("Gundam Updated")

    # Delete Gundam
    def delete_gundam(self):
        gundam_id = input("Enter the Gundam ID: ").strip().upper()
        result = self.search_gundam(gundam_id)

        if not result:
            print("❌ Gundam not found.")
            return

        confirm = input(f"Are you sure you want to delete {result.name}? [Y/N] ").upper()

        if confirm == "Y":
            self.collection.remove(result)
            self.save_collection()
            print("Gundam deleted successfully!")
            return True

        print("Gundam not deleted")
        return False

    # Collection Statistics
    def stats_gundam(self):
        if not self.collection:
            print("No Gundams in collection.")
            return

        total = len(self.collection)

        grades = {}
        statuses = {}
        series = {}

        for gundam in self.collection:
            grades[gundam.grade] = grades.get(gundam.grade, 0) + 1

            statuses[gundam.status] = statuses.get(gundam.status, 0) + 1

            series[gundam.series] = series.get(gundam.series, 0) + 1

        print("\n===== GUNDAM COLLECTION STATISTICS =====")

        print(f"Total Gundams: {total}")

        print("\nBy Grade")

        for grade, count in grades.items():
            print(f"{grade}: {count}")

        print("\nBy Status")

        for status, count in statuses.items():
            print(f"{status}: {count}")

        print("\nBy Series")

        for show, count in series.items():
            print(f"{show}: {count}")


    def show_dashboard(self):
        if not self.collection:
            print("\n📊 DASHBOARD")
            print("No Gundams in collection")
            return

        total = len(self.collection)
        grades = {}
        statuses = {}
        series = {}

        for gundam in self.collection:
            grades[gundam.grade] = grades.get(gundam.grade, 0) + 1
            statuses[gundam.status] = statuses.get(gundam.status, 0) + 1
            series[gundam.series] = series.get(gundam.series, 0) + 1

        built = statuses.get("Built", 0)
        backlog = statuses.get("Unbuilt", 0)

        completion_rate = (built / total) * 100

        most_collected_grade = (
            max(grades, key=grades.get)
            if grades
            else "N/A"
        )

        most_collected_series = (
            max(series, key=series.get)
            if series
            else "N/A"
        )

        print("\n" + "=" * 50)
        print("📊 GUNDAM COLLECTION DASHBOARD")
        print("=" * 50)
        print(f"Total Kits           : {total}")
        print(f"Built Kits           : {built}")
        print(f"Backlog Kits         : {backlog}")
        print(f"Completion Rate      : {completion_rate:.2f}%")
        print(f"Most Collected Grade : {most_collected_grade}")
        print(f"Favorite Series      : {most_collected_series}")

        print("=" * 50)

#Filter Gundam by Grade
    def filter_gundam_grade(self):
        grade = input("Enter the Gundam Grade: ").upper()

        filtered = [
            gundam for gundam in self.collection
            if gundam.grade.upper() == grade
        ]

        if not filtered:
            print(f"No Gundam found for {grade}")
            return

        print(f"\n=== {grade} Gundams ===")
        for gundam in filtered:
            print(f"{gundam.id} - {gundam.name} ({gundam.series})")

# Filter Gundam by Series
    def filter_gundam_series(self):
        series = input("Enter the Gundam Series: ")
        filtered = [
            gundam for gundam in self.collection
            if gundam.series == series
        ]

        if not filtered:
            print(f"No Gundam found for {series}")
            return

        print(f"\n=== {series}  ===")
        for gundam in filtered:
            print(f"{gundam.id} - {gundam.name} ({gundam.grade}")


# Export to CSV
    def export_csv(self):
        if not self.collection:
            print("No Gundams in collection")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"./data/gundam_collection_{timestamp}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Header
            writer.writerow([
                "ID",
                "Name",
                "Grade",
                "Series",
                "Status"
            ])

            # Data for the CSV
            for gundam in self.collection:
                writer.writerow([
                    gundam.id,
                    gundam.name,
                    gundam.grade,
                    gundam.series,
                    gundam.status
                ])

        print(f"✅ Collection exported successfully!")
        print(f"📁 File: {filename}")