# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from ..api.validation.validation import to_frappe_date


class VipDarshanSlot(Document):
	def autoname(self):
		# use your ID instead of naming series
		if self.slot_date:
			id = to_frappe_date(self.slot_date, format="%d-%m-%Y-1")
			self.name = id
		else:
			# fallback: use default pattern
			super().autoname()


def create_slot(slot_date):
	id = to_frappe_date(slot_date, format="%d-%m-%Y-1")

	# if exists → return directly
	if frappe.db.exists("Vip Darshan Slot", id):
		slot_date_doc = frappe.get_doc("Vip Darshan Slot", id)
		return slot_date_doc
	else:
		default_slot_info = frappe.get_doc("Vip Darshan Slot Info")
		slot_date_doc = frappe.new_doc("Vip Darshan Slot")
		slot_date_doc.slot_date = to_frappe_date(slot_date)
		slot_date_doc.slot_info = default_slot_info.slot_info
		slot_date_doc.insert(ignore_permissions=True)
		return slot_date_doc


@frappe.whitelist(allow_guest=True)
def get_vip_darshan_slots(slot_date):
	slot_date_doc = create_slot(slot_date)
	# filter fields
	selected_fields = [
		{"slot_name": row.slot_name, "current_capacity": row.current_capacity}
		for row in slot_date_doc.slot_info
	]

	return selected_fields
