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
		customer_name = frappe.db.get_value("Token Mapping", {"token": token}, "customer")

		if not customer_name:
			return {"error": "Invalid token"}

		# Attach resolved customer so endpoint can use it
		frappe.local.form_dict["customer_name"] = customer_name

		return fn(*args, **kwargs)

	return wrapper
