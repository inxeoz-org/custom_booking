# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DarshanAppointment(Document):
	pass


@frappe.whitelist()
def insert_default_companion_from_customer_to_darshan_appointment(customer_id, darshan_appointment_id):
	if not customer_id or not darshan_appointment_id:
		frappe.throw("Invalid Customer or Darshan Appointment ID")

	# Fetch both documents
	customer = frappe.get_doc("Customer", customer_id)
	darshan_appointment = frappe.get_doc("Darshan Appointment", darshan_appointment_id)

	# Ensure field exists on customer
	if not hasattr(customer, "custom_companion"):
		frappe.throw("Customer does not have a field named 'custom_companion'")

	# COPY value (not move)
	copied_value = customer.custom_companion

	# Assign copy to appointment field
	darshan_appointment.companion = copied_value

	# Save updated appointment
	darshan_appointment.save(ignore_permissions=True)

	return f"Copied companion '{copied_value}' to Darshan Appointment {darshan_appointment_id}"
