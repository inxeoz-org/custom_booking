import frappe
from frappe.utils import random_string

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

	return customer
	# print(str(customer.custom_aadhar))
	# return {
	# 	"devoteee_name": customer.customer_name,
	# 	"is_kyc_complete": customer.custom_aadhar and len(str(customer.custom_aadhar)) > 0,
	# }
