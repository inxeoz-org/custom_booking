import frappe
from frappe.utils import random_string


@frappe.whitelist(allow_guest=True)
def login(name):
	return "You got logged in! " + name


@frappe.whitelist(allow_guest=True)
def create_customer(phone):
	exists = frappe.db.exists("Customer", {"custom_phone": phone})

	if exists:
		frappe.throw("Devoteee Exists", frappe.ValidationError)

	new_customer = frappe.get_doc(
		{
			"doctype": "Customer",
			"customer_name": f"{phone}",
			"customer_type": "Individual",
			"custom_phone": phone,
		}
	)

	new_customer.insert(ignore_permissions=True)
	frappe.db.commit()

	return new_customer


@frappe.whitelist(allow_guest=True)
def customer_login(phone, password):
	# TODO: replace with real external verification
	token = random_string(16)
	# token = None

	if token is None:
		frappe.throw("Invalid credentials", frappe.ValidationError)
		# return "invalid credentials"

	frappe.set_user("Administrator")

	# Get customer by mobile number
	customer_name = frappe.db.get_value("Customer", {"custom_phone": phone})
	if not customer_name:
		frappe.throw("Customer not found")
		# return "Customer not found"

	customer = frappe.get_doc("Customer", customer_name)

	new_token_map_record = frappe.get_doc({"doctype": "Token Mapping", "token": token, "custom_phone": phone})

	new_token_map_record.insert(ignore_permissions=True)

	# Add session info to child table

	customer.append("custom_session_info", {"token": token, "login_time": frappe.utils.now()})

	customer.save(ignore_permissions=True)

	return token


import frappe
from google.auth.transport import requests
from google.oauth2 import id_token


@frappe.whitelist(allow_guest=True)
def google_login(token):
	try:
		# Verify ID token
		idinfo = id_token.verify_oauth2_token(
			token,
			requests.Request(),
			"877753772904-78b39tu876jt75f2he4t7nluuvlk7fi8.apps.googleusercontent.com",
		)

		email = idinfo["email"]
		name = idinfo.get("name")
		picture = idinfo.get("picture")

		# Find or create user
		user = frappe.db.get_value("User", {"email": email})

		if not user:
			user = frappe.get_doc(
				{"doctype": "User", "email": email, "first_name": name, "enabled": 1, "send_welcome_email": 0}
			)
			user.insert(ignore_permissions=True)

		frappe.local.login_manager.user = email
		frappe.local.login_manager.post_login()

		return {"status": "ok", "email": email}

	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "Google Login Failed")
		return {"error": str(e)}
