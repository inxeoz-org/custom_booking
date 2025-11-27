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
	# TODO: replace with real external verification
	token = random_string(16)

	if token is None:
		return "invalid credentials"

	frappe.set_user("Administrator")

	# Get customer by mobile number
	customer_name = frappe.db.get_value("Customer", {"mobile_no": phone})
	if not customer_name:
		return "Customer not found"

	customer = frappe.get_doc("Customer", customer_name)

	# Add session info to child table
	customer.append("custom_session_info", {"token": token, "login_time": frappe.utils.now()})

	customer.save(ignore_permissions=True)

	return token
