from random import random

import frappe
from frappe.utils import random_string


@frappe.whitelist(allow_guest=True)
def login(name):
	return "You got logged in! " + name


@frappe.whitelist(allow_guest=True)
def create_customer(phone):
	exists = frappe.db.exists("Customer", {"mobile_no": phone})

	if exists:
		return "Devoteee Exists"

	new_customer = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": f"{phone}",
			"customer_type": "Individual",
			"mobile_no": phone,
		}
	)

	new_customer.insert(ignore_permissions=True)
	frappe.db.commit()

	return new_customer


@frappe.whitelist(allow_guest=True)
def customer_login(phone, password):
	# verify using external service
	# token = verify_customer(phone, password)
	token = random_string(16)

	return token
