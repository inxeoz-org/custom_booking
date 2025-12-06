# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from ..api.validation.validation import to_frappe_date


class VipDarshanSlot(Document):
	pass


@frappe.whitelist(allow_guest=True)
def get_vip_darshan_slots(slot_date):
	id = to_frappe_date(slot_date, format="%d-%m-%Y-1")
	slot_date_doc = frappe.get_doc("Vip Darshan Slot", id)
	selected_fields = [
		{"slot_name": row.slot_name, "current_capacity": row.current_capacity}
		for row in slot_date_doc.slot_info
	]

	return selected_fields
