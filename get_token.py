
import os
from getpass import getpass
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

email = input("Enter manager email: ")
password = getpass("Enter manager password: ")

result = client.auth.sign_in_with_password({
    "email": email,
    "password": password
})

print("\nLogin successful!")
print("Access token:")
print(result.session.access_token)
