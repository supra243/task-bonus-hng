# the required librairies
from hashlib import sha256
import csv
import json

# the hashing function transforms and gives the sha256 of the json file
def hashing(file):
    hashed = sha256()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hashed.update(byte_block)
            return hashed.hexdigest()


# This function creates a csv file
def new_csv(file, fields):
    with open(file, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()


# the put_in_csv_file add the data in a csv file
def put_in_csv_file(file, data):
    with open(file, mode="a") as csv_file:
        writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(data)


# the main reads a csv file, creates a json file for each entry
def main():
    FILE = "HNGi9-CSV-FILE.csv"

    with open(FILE) as csv_file:
        print("Wait...")
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        json_format = {"format": "CHIP-0007"}

        for row in csv_reader:

            if line_count == 0:
                column_names = [*row]
                fields = [*column_names, "sha256"]
                csv_file = "HNGi9-CSV-FILE.output.csv"
                new_csv(csv_file, fields)
            else:
                if not row[0].isnumeric():
                    continue

                file = row[1]
                entry_dict = json_format.copy()

                for j in range(len(column_names)):
                    entry_dict[f"{column_names[j]}"] = row[j]
                json_object = json.dumps(entry_dict, indent=4)

                try:
                    json_file = f"./{file}.json"
                    with open(json_file, "w") as outfile:
                        outfile.write(json_object)

                    sha256 = hashing(json_file)

                    data = [*row, sha256]
                    put_in_csv_file(csv_file, data)
                except Exception as error:
                    print("Shomething wrong !")
                    print(error)

            line_count += 1

        print("The operation was successful")


if __name__ == "__main__":
    main()
