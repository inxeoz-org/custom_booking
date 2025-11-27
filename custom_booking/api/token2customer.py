from functools import wraps

import frappe


def token2customer(fn):
	"""
	Token-only authentication decorator.
	Reads raw token from Authorization header.
	Maps token -> customer using Token Mapping doctype.
	"""

	@wraps(fn)
	def wrapper(*args, **kwargs):
		# ----------------------------------
		# 1. Read raw token from Authorization header
		# ----------------------------------
		token = frappe.local.request.headers.get("Authorization")

		if not token:
			return {"error": "Missing Authorization token"}

		token = token.strip()

		# ----------------------------------
		# 2. Resolve customer from token
		# ----------------------------------
		custom_phone = frappe.db.get_value("Token Mapping", {"token": token}, "custom_phone")
		customer_name = frappe.db.get_value("Customer", {"custom_phone": custom_phone}, "customer_name")

		if not customer_name:
			frappe.throw("Invalid token")

		# Attach resolved customer so endpoint can use it
		#
		print("#" * 20 + customer_name)
		frappe.local.form_dict["customer_name"] = customer_name

		return fn(*args, **kwargs)

	return wrapper
