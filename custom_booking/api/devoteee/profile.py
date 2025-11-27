import frappe
from frappe.utils import random_string
from typing_extensions import Dict

from ..token2customer import token2customer


@frappe.whitelist(allow_guest=True)
@token2customer
def profile():
	customer_id = frappe.local.form_dict["customer_id"]

	if not customer_id:
		frappe.throw("customer_id is required")

	frappe.set_user("Administrator")
	customer = frappe.get_doc("Customer", customer_id)

	# return customer
	print(str(customer.custom_aadhar))

	is_kyc_complete = bool(customer.custom_aadhar) and len(str(customer.custom_aadhar)) > 0

	return {
		"devoteee_name": customer.customer_name,
		"is_kyc_complete": is_kyc_complete,
	}


@frappe.whitelist(allow_guest=True)
@token2customer
def update_profile(devoteee_name: str, email: str, gender: str, dob: str, aadhar: str, location: str):
	customer_id = frappe.local.form_dict.get("customer_id")

	if not customer_id:
		frappe.throw("customer_id is required")

	frappe.set_user("Administrator")
	customer = frappe.get_doc("Customer", customer_id)

	if devoteee_name:
		customer.customer_name = devoteee_name
	if email:
		customer.email = email
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
