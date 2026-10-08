# reads CSV files

import csv

def load_csv(filename):
    records = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    return records

def load_donations():
    return load_csv("data/donations.csv")

def load_recipients():
    return load_csv("data/recipients.csv")

def load_volunteers():
    return load_csv("data/volunteers.csv")