import keyauth
from twilio.rest import Client

# KeyAuth credentials
keyauth_id = "YOUR_KEYAUTH_ID"
keyauth_secret = "YOUR_KEYAUTH_SECRET"

# Instantiate keyauthapp using the keyauth_id and keyauth_secret
keyauthapp = keyauth.Client(keyauth_id, keyauth_secret)

# Verify the license
if not keyauthapp.verify():
    print("Invalid license. Please obtain a valid license to use this software.")
    exit()

# Read Twilio variables from KeyAuth application variables
twilio_account_sid = keyauthapp.var("twilio_account_sid")
twilio_auth_token = keyauthapp.var("twilio_auth_token")
twilio_phone_number = keyauthapp.var("twilio_phone_number")

# Read limit from KeyAuth variable
limit = int(keyauthapp.var("limit"))

# Initialize Twilio client
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Function to send a single SMS
def send_single_sms(phone_number, message):
    nonlocal limit

    if limit > 0:
        twilio_client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f"SMS sent to {phone_number}")

        # Update limit variable after sending each single SMS
        limit -= 1
        keyauthapp.setvar("limit", str(limit))

        if limit == 0:
            print("Limit is finished!")
            return
    else:
        print("Limit is finished!")

# Function to send bulk SMS
def send_bulk_sms(phone_numbers_file, message):
    with open(phone_numbers_file, 'r') as file:
        phone_numbers = [line.strip() for line in file]

    for phone_number in phone_numbers:
        if limit > 0:
            twilio_client.messages.create(
                body=message,
                from_=twilio_phone_number,
                to=phone_number
            )
            print(f"SMS sent to {phone_number}")

            # Update limit variable after sending each SMS
            limit -= 1
            keyauthapp.setvar("limit", str(limit))

            if limit == 0:
                print("Limit is finished!")
                break  # Stop further SMS sending
        else:
            print("Limit is finished!")
            break  # Stop further SMS sending

# Main function
def main():
    print("Welcome to LeadsSender!")

    while True:
        print("\nSelect an option:")
        print("1. Single SMS mode")
        print("2. Bulk SMS mode")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            phone_number = input("Enter the recipient's phone number: ")
            message = input("Enter the message: ")
            send_single_sms(phone_number, message)
        elif choice == "2":
            phone_numbers_file = input("Enter the path to the phone numbers text file: ")
            message = input("Enter the message: ")
            send_bulk_sms(phone_numbers_file, message)
        elif choice == "0":
            print("Thank you for using LeadsSender. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
