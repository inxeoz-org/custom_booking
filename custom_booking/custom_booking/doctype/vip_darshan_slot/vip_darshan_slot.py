# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from ..api.validation.validation import to_frappe_date


class VipDarshanSlot(Document):
	pass


# def get_vip_darshan_slots(slot_date):


@frappe.whitelist(allow_guest=True)
def slot_date_to_id(slot_date):
	id = to_frappe_date(slot_date, format="%d-%m-%Y-1")
	return id
