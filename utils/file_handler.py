#JSON for Gundam collection
import json

from gundam import Gundam


#Save to JSON file
def save_data(filename, collection):
    data = [gundam.to_dict() for gundam in collection]

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

#Load Data JSON
def load_data(filename, collection):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

            for item in data:
                gundam = Gundam(
                    item['id'],
                    item['name'],
                    item.get("grade", "HG"),
                    item['series'],
                    item.get("status", "Unbuilt")
                )

                gundam.id = item['id']
                collection.append(gundam)

                if collection:
                    max_id = max(
                        int(g.id.replace("GDM", ""))
                        for g in collection
                    )
                    Gundam.next_id = max_id + 1
            return collection

    except FileNotFoundError:
            print("File not found")
            return []

def clear_data(filename):
    with open(filename, "w") as file:
        json.dump([], file, indent=4)
    print("Collection reset successfully")