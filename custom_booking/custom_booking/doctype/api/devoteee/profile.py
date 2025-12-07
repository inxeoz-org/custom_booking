# from typing import Dict

# import frappe
# from frappe.utils import random_string

# from ..sms.sms import send_email_otp, send_sms_otp, verify_email_otp, verify_sms_otp
# from ..token.token import token_auth


# @frappe.whitelist(allow_guest=True)
# @token_auth
# def profile():
# 	customer_id = frappe.local.form_dict["customer_id"]

# 	if not customer_id:
# 		frappe.throw("customer_id is required")

# 	frappe.set_user("Administrator")
# 	customer = frappe.get_doc("Customer", customer_id)

# 	# return customer
# 	print(str(customer.custom_aadhar))

# 	return {
# 		"devoteee_name": customer.customer_name,
# 		"email": customer.custom_email,
# 		"gender": customer.gender,
# 		"dob": customer.custom_dob,
# 		"aadhar": customer.custom_aadhar,
# 		"location": customer.custom_location,
# 		"companion": customer.custom_companion,
# 		"phone": customer.custom_phone,
# 	}


# @frappe.whitelist(allow_guest=True)
# @token_auth
# def update_profile(
# 	devoteee_name: str | None = None,
# 	gender: str | None = None,
# 	dob: str | None = None,
# 	aadhar: str | None = None,
# 	location: str | None = None,
# 	companion: Dict | None = None,
# ):
# 	customer_id = frappe.local.form_dict.get("customer_id")

# 	if not customer_id:
# 		frappe.throw("customer_id is required")

# 	frappe.set_user("Administrator")
# 	customer = frappe.get_doc("Customer", customer_id)

# 	if devoteee_name:
# 		customer.customer_name = devoteee_name.lower()
# 	if gender:
# 		customer.gender = gender.lower()
# 	if dob:
# 		customer.custom_dob = dob
# 	if aadhar:
# 		customer.custom_aadhar = aadhar
# 	if location:
# 		customer.custom_location = location.lower()

# 	customer.save()
# 	return profile()


# @frappe.whitelist(allow_guest=True)
# @token_auth
# def update_cred(
# 	phone: str | None = None,
# 	otp_phone: str | None = None,
# 	email: str | None = None,
# 	otp_email: str | None = None,
# 	email2: str | None = None,
# 	otp_email2: str | None = None,
# ):
# 	customer_id = frappe.local.form_dict.get("customer_id")

# 	if not customer_id:
# 		frappe.throw("customer_id is required")

# 	frappe.set_user("Administrator")
# 	customer = frappe.get_doc("Customer", customer_id)

# 	if email and (customer.custom_email != email):
# 		if otp_email is None:
# 			status = send_email_otp(email)
# 			return status["message"]
# 		else:
# 			verification_status = verify_email_otp(email=email, otp=otp_email)
# 			if verification_status["VERIFIED"]:
# 				customer.custom_email = email
# 			else:
# 				return verification_status["message"]

# 	if phone and (customer.custom_phone != phone):
# 		if otp_phone is None:
# 			status = send_sms_otp(phone)
# 			return status["message"]
# 		else:
# 			verification_status = verify_sms_otp(phone=phone, otp=otp_phone)
# 			if verification_status["VERIFIED"]:
# 				customer.custom_phone = phone
# 			else:
# 				return verification_status["message"]

# 	if email2 and (customer.email2 != email2):
# 		if otp_email2 is None:
# 			status = send_email_otp(email2)
# 			return status["message"]
# 		else:
# 			verification_status = verify_email_otp(email=email2, otp=otp_email2)
# 			if verification_status["VERIFIED"]:
# 				customer.custom_email2 = email2
# 			else:
# 				return verification_status["message"]

# 	customer.save()
# 	return profile()
