import frappe
from frappe.utils import random_string
from typing_extensions import Dict

from ..token2customer import token2customer


@frappe.whitelist(allow_guest=True)
@token2customer
def get_customer_profile():
	customer = frappe.local.form_dict["customer_name"]
	return {"customer": customer}


@frappe.whitelist(allow_guest=True)
@token2customer
def profile():
	customer_name = frappe.local.form_dict["customer_name"]

	customer = frappe.get_doc("Customer", customer_name)

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
	customer_name = frappe.local.form_dict.get("customer_name")

	if not customer_name:
		frappe.throw("customer_name is required")

	customer = frappe.get_doc("Customer", customer_name)

	frappe.set_user("Administrator")
	customer.customer_name = devoteee_name
	customer.email = email
	customer.gender = gender
	customer.custom_dob = dob
	customer.custom_aadhar = aadhar
	customer.custom_location = location

	customer.save()

	return "Profile Updated"
