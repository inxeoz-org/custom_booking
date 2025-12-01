import time

import frappe
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from typing_extensions import Dict

SECRET = frappe.conf.get("jwt_secret", "mysecretkey")


def jwt_token(details: Dict):
	# generate JWT
	payload = {
		"details": details,
		"exp": int(time.time()) + 86400,  # token valid 24 hours
		"iat": int(time.time()),
	}

	token = jwt.encode(payload, SECRET, algorithm="HS256")

	return token


def decode_jwt(token: str):
	"""
	Decode JWT token and return payload.
	Raises appropriate errors for invalid/expired tokens.
	"""

	try:
		payload = jwt.decode(token, SECRET, algorithms=["HS256"])
		return {
			"ok": True,
			"details": payload.get("details"),
			"exp": payload.get("exp"),
			"iat": payload.get("iat"),
		}

	except ExpiredSignatureError:
		return {"ok": False, "error": "Token expired"}

	except InvalidTokenError:
		return {"ok": False, "error": "Invalid token"}


from functools import wraps

import frappe


def token_auth(fn):
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

		data = decode_jwt(token)

		if not data["ok"]:
			frappe.throw("Invalid token", frappe.PermissionError)

		frappe.local.form_dict["devotee_details"] = data["details"]
		frappe.local.form_dict["customer_id"] = data["details"]["id"]

		print("@" * 30, data["details"]["id"])

		return fn(*args, **kwargs)

	return wrapper
