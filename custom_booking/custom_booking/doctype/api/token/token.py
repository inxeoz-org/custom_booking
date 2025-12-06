import time

import frappe
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from typing_extensions import Dict

SECRET = frappe.conf.get("jwt_secret", "mysecretkey")


def jwt_token(info: Dict):
	# generate JWT
	payload = {
		"info": info,
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
			"info": payload.get("info"),
			"exp": payload.get("exp"),
			"iat": payload.get("iat"),
		}

	except ExpiredSignatureError:
		return {"ok": False, "error": "Token expired"}

	except InvalidTokenError:
		return {"ok": False, "error": "Invalid token"}


from functools import wraps


def token_auth(id_name):
	"""Decorator factory allowing:
	@token_auth("field_name")
	"""

	def decorator(fn):
		@wraps(fn)
		def wrapper(*args, **kwargs):
			# ----------------------------------
			# 1. Read raw token
			# ----------------------------------
			token = frappe.local.request.headers.get("Authorization")

			if not token:
				return {"error": "Missing Authorization token"}

			token = token.strip()
			data = decode_jwt(token)

			if not data["ok"]:
				frappe.throw("Invalid token", frappe.PermissionError)

			# save details
			id = data["info"][id_name]

			if not id:
				frappe.throw("id not found", frappe.DoesNotExistError)

			frappe.local.form_dict[id_name] = id

			return fn(*args, **kwargs)

		return wrapper

	return decorator
