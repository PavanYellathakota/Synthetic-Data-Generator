# utils/faker_utils.py

def generate_pii_value(fake, subtype: str):
    if subtype == "name":
        return fake.name()
    elif subtype == "email":
        return fake.email()
    elif subtype == "phone":
        return fake.phone_number()
    elif subtype == "address":
        return fake.address().replace("\n", ", ")
    else:
        return "Unknown"
