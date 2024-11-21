import sys
def main():
    # provided file
    if len(sys.argv) != 2:
        print("Error: An operations file must be provided as a command-line argument.")
        sys.exit(1)

    operations_file = sys.argv[1]

    try:
        with open(operations_file, 'r') as file:
            operations = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{operations_file}' could not be opened.")
        sys.exit(1)

    demographics_data = load_demographics_data()
    print(f"Number of entries: {len(demographics_data)}")

    for operation in operations:
        process_operation(operation.strip(), demographics_data)

    print("All operations completed.")


def load_demographics_data() -> list:

    # Placeholder: Replace with actual data loading logic
    return [{"name": "John Doe", "age": 30}, {"name": "Jane Smith", "age": 25}]


def process_operation(operation: str, data: list):


    if __name__ == "__main__":
        main()


from typing import List, Dict

# allowed field
"Education.Bachelor's Degree or Higher", "Education.High School or Higher",
"Ethnicities.American Indian and Alaska Native Alone", "Ethnicities.Asian Alone",
"Ethnicities.Black Alone", "Ethnicities.Hispanic or Latino",
"Ethnicities.Native Hawaiian and Other Pacific Islander Alone",
"Ethnicities.Two or More Races", "Ethnicities.White Alone",
"Ethnicities.White Alone, not Hispanic or Latino", "Income.Persons Below Poverty Level"


def main():
    # Check command-line argument
    if len(sys.argv) != 2:
        print("Error: An operations file must be provided as a command-line argument.")
        sys.exit(1)

    operations_file = sys.argv[1]

    try:
        # Open and read the operations file
        with open(operations_file, 'r') as file:
            operations = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{operations_file}' could not be opened.")
        sys.exit(1)

   # load data
    demographics_data = load_demographics_data()
    print(f"Number of entries: {len(demographics_data)}")

    for i, operation in enumerate(operations, start=1):
        try:
            process_operation(operation.strip(), demographics_data)
        except ValueError as e:
            print(f"Error on line {i}: {e}")
            continue

    print("All operations completed.")


def load_demographics_data() -> List[Dict]:
    # Placeholder: Replace with actual data loading logic
    return [
        {"County": "Example County", "State": "EX", "Population": 1000,
         "Education.Bachelor's Degree or Higher": 25.0},
        {"County": "Another County", "State": "AN", "Population": 2000,
         "Education.Bachelor's Degree or Higher": 60.0}
    ]


def process_operation(operation: str, data: List[Dict]):
    if not operation:
        return  # Skip empty lines

    parts = operation.split(":")
    command = parts[0]

    if command == "display":
        display_data(data)
    elif command == "filter-state" and len(parts) == 2:
        filter_state(parts[1], data)
    elif command == "filter-gt" and len(parts) == 3:
        filter_gt(parts[1], float(parts[2]), data)
    elif command == "filter-lt" and len(parts) == 3:
        filter_lt(parts[1], float(parts[2]), data)
    elif command == "population-total":
        population_total(data)
    elif command == "population" and len(parts) == 2:
        population_field(parts[1], data)
    elif command == "percent" and len(parts) == 2:
        percent_field(parts[1], data)
    else:
        raise ValueError("Malformed operation.")


def display_data(data: List[Dict]):
    for entry in data:
        print(f"County: {entry['County']}, State: {entry['State']}, Population: {entry['Population']}")


def filter_state(state: str, data: List[Dict]):
    original_count = len(data)
    data[:] = [entry for entry in data if entry["State"] == state]
    print(f"Filter: state == {state} ({len(data)} entries)")


def filter_gt(field: str, number: float, data: List[Dict]):
    validate_field(field)
    original_count = len(data)
    data[:] = [entry for entry in data if entry.get(field, 0) > number]
    print(f"Filter: {field} gt {number} ({len(data)} entries)")


def filter_lt(field: str, number: float, data: List[Dict]):
    validate_field(field)
    original_count = len(data)
    data[:] = [entry for entry in data if entry.get(field, 0) < number]
    print(f"Filter: {field} lt {number} ({len(data)} entries)")


def population_total(data: List[Dict]):
    total_population = sum(entry["Population"] for entry in data)
    print(f"2014 population: {total_population}")


def population_field(field: str, data: List[Dict]):
    validate_field(field)
    total = sum(entry["Population"] * (entry.get(field, 0) / 100) for entry in data)
    print(f"2014 {field} population: {total}")


def percent_field(field: str, data: List[Dict]):
    validate_field(field)
    total_population = sum(entry["Population"] for entry in data)
    sub_population = sum(entry["Population"] * (entry.get(field, 0) / 100) for entry in data)
    percentage = (sub_population / total_population) * 100 if total_population > 0 else 0
    print(f"2014 {field} percentage: {percentage}")


def validate_field(field: str):
    if field not in ALLOWED_FIELDS:
        raise ValueError(f"Invalid field: {field}")


if __name__ == "__main__":
    main()
