# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

# from asyncore import file_wrapper

import frappe
from frappe.model.document import Document


class VipDarshanSlotInfo(Document):
	pass


@frappe.whitelist(allow_guest=True)
def get_default_slot_info():
	slot_info_doc = frappe.get_doc("Vip Darshan Slot Info")
	return [
		{"slot_name": row.slot_name, "current_capacity": row.current_capacity}
		for row in slot_info_doc.slot_info
	]
