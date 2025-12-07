# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VipProtocol(Document):
	pass


@frappe.whitelist(allow_guest=True)
def protocol_info(protocol_name):
	try:
		data = frappe.db.get_value(
			"Vip Protocol", protocol_name, ["protocol_name", "description", "protocol_level"], as_dict=True
		)

		if not data:
			frappe.throw("Protocol not found")

		return data
	except Exception as e:
		frappe.throw(str(e))


@frappe.whitelist(allow_guest=True)
def protocol_list():
	return frappe.get_all("Vip Protocol", fields=["name", "protocol_name", "description", "protocol_level"])
