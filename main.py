# Rescue Route

from data_loader import (
    load_donations,
    load_recipients,
    load_volunteers
)

def main():

    # loading data from CSV
    donations = load_donations()
    recipients = load_recipients()
    volunteers = load_volunteers()

    # display loaded data just for testing
    print("\nDONATIONS:")
    for donation in donations:
        print(donation)

    print("\nRECIPIENTS:")
    for recipient in recipients:
        print(recipient)

    print("\nVOLUNTEERS:")
    for volunteer in volunteers:
        print(volunteer)

if __name__ == "__main__":
    main()
