# Main Menu Python file for Gundam Collection

# Import Gundam, Gundam Manager, and File Handler
from gundam import Gundam
from gundam_manager import GundamManager
from utils.file_handler import save_data, load_data, clear_data


manager = GundamManager()
manager.collection = load_data("./data/gundams.json", manager.collection)
manager.initialize_next_id()
while True:
    def display_menu():

        print("""

    ==================================================
               🤖 GUNDAM COLLECTION TRACKER
    ==================================================
    [1] Dashboard
    [2] Add Gundam
    [3] Gundam Collection
    [4] Search Gundam
    [5] Filter Gundam
    [6] Update Gundam
    [7] Delete Gundam
    [8] Statistics
    [9] Export CSV
    [0] Exit
    
    ===================================================
    """)


    def display_filter_menu():

        print("""

    ==================================================
                    FILTER GUNDAM
    ==================================================
    [1] Filter by Grade
    [2] Filter by Series
    [0] Back 

    ===================================================
    """)
    display_menu()
    choice = input("Select an option: ")

    if choice == "1":
        manager.show_dashboard()
    elif choice == "2":
        manager.add_gundam()
    elif choice == "3":
        manager.view_collection()
    elif choice == "4":
        gundam_id = input("Enter the Gundam ID: ").strip().upper()
        result = manager.search_gundam(gundam_id)
        if not result:
            print("❌ Gundam not found.")
    elif choice == "5":
        while True:
            display_filter_menu()
            choice2 = input("Select a filter option: ")
            if choice2 == "1":
                manager.filter_gundam_grade()
            elif choice2 == "2":
                manager.filter_gundam_series()
            elif choice2 == "0":
                break
            else:
                print("Please enter a valid option")
    elif choice == "6":
        manager.update_gundam()
    elif choice == "7":
        manager.delete_gundam()
    elif choice == "8":
        manager.stats_gundam()
    elif choice == "9":
        manager.export_csv()
    elif choice == "0":
        print("Thank you for using Gundam Tracker!")
        break
    else:
        print("Please enter a valid choice")

