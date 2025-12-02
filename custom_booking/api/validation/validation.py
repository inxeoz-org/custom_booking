import re


# as frappe originally uses data type for phone number
def valid_phone(phone: str):
	return re.match(r"^\d{10}$", phone)


def valid_email(email: str):
	return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)


def valid_name(name: str):
	return re.match(r"^[a-zA-Z\s]+$", name)


def valid_aadhar(aadhar: str):
	return re.match(r"^\d{12}$", str(aadhar))


def valid_gender(gender: str):
	return gender.lower() in ["male", "female", "other"]


def valid_dob(dob: str):
	return re.match(r"^\d{2}-\d{2}-\d{4}$", dob)


def valid_location(location: str):
	return re.match(r"^[a-zA-Z\s]+$", location)


def valid_date(date: str):
	return re.match(r"^\d{2}-\d{2}-\d{4}$", date)


def valid_24hrtime(time: str):
	return re.match(r"^\d{2}:\d{2}$", time)


def valid_12hrtime(time: str):
	return re.match(r"^\d{1,2}:\d{2} [APap][Mm]$", time)


def valid_otp(otp: str):
	return len(f"{otp}") == 6
