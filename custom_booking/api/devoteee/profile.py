import frappe
from frappe.utils import random_string

from ..token.token import token_auth


@frappe.whitelist(allow_guest=True)
@token_auth
def profile():
	customer_id = frappe.local.form_dict["customer_id"]

	if not customer_id:
		frappe.throw("customer_id is required")

	frappe.set_user("Administrator")
	customer = frappe.get_doc("Customer", customer_id)

	# return customer
	print(str(customer.custom_aadhar))

	return {
		"devoteee_name": customer.customer_name,
		"email": customer.custom_email,
		"gender": customer.gender,
		"dob": customer.custom_dob,
		"aadhar": customer.custom_aadhar,
		"location": customer.custom_location,
		"companion": customer.custom_companion,
	}


@frappe.whitelist(allow_guest=True)
@token_auth
def update_profile(devoteee_name: str, email: str, gender: str, dob: str, aadhar: str, location: str):
	customer_id = frappe.local.form_dict.get("customer_id")

	if not customer_id:
		frappe.throw("customer_id is required")

	frappe.set_user("Administrator")
	customer = frappe.get_doc("Customer", customer_id)

	if devoteee_name:
		customer.customer_name = devoteee_name
	if email:
		customer.custom_email = email
	if gender:
		customer.gender = gender
	if dob:
		customer.custom_dob = dob
	if aadhar:
		customer.custom_aadhar = aadhar
	if location:
		customer.custom_location = location

	customer.save()

	return "Profile Updated"
