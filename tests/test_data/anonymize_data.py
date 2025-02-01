import json
from faker import Faker

# Initialize Faker
fake = Faker()

# Load the JSON data
with open("tests/test_data/res.json", "r") as file:
    data = json.load(file)

# Dictionary to store the mapping of original names to fake names
name_mapping = {}


# Function to get a fake name for a given original name
def get_fake_name(original_name):
    if original_name not in name_mapping:
        fake_name = fake.name()
        name_mapping[original_name] = fake_name
    return name_mapping[original_name]


# Anonymize the data
def anonymize_data(data):
    for room in data:
        for booking in room["bookings"]:
            if booking["band"] is not None:
                if booking["band"]["name"] is not None:
                    booking["band"]["name"] = get_fake_name(booking["band"]["name"])
                    booking["band"]["short_name"] = booking["band"]["name"][:10]


anonymize_data(data)

# Save the anonymized data back to the JSON file
with open("tests/test_data/res_anonymized.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data anonymized and saved to tests/test_data/res_anonymized.json")
