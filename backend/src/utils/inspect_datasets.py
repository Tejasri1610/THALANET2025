import pandas as pd

# Load datasets
donors = pd.read_csv("data/donors.csv")
patients = pd.read_csv("data/patients.csv")
requests = pd.read_csv("data/emergency_requests.csv")
historical = pd.read_csv("data/historical_donations.csv")

# Quick glance at first 5 rows
print("=== DONORS ===")
print(donors.head(), "\n")

print("=== PATIENTS ===")
print(patients.head(), "\n")

print("=== EMERGENCY REQUESTS ===")
print(requests.head(), "\n")

print("=== HISTORICAL DONATIONS ===")
print(historical.head(), "\n")

# Summary stats
print("=== DONORS SUMMARY ===")
print(donors.describe(include='all'), "\n")
print(donors['blood_type'].value_counts(), "\n")
print(donors['availability_status'].value_counts(), "\n")

print("=== PATIENTS SUMMARY ===")
print(patients.describe(include='all'), "\n")
print(patients['blood_type_required'].value_counts(), "\n")
print(patients['urgency_level'].value_counts(), "\n")

print("=== EMERGENCY REQUESTS SUMMARY ===")
print(requests.describe(include='all'), "\n")
print(requests['blood_type_needed'].value_counts(), "\n")
print(requests['urgency_level'].value_counts(), "\n")

print("=== HISTORICAL DONATIONS SUMMARY ===")
print(historical.describe(include='all'), "\n")
print(historical['blood_type'].value_counts(), "\n")
