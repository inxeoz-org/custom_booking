from datetime import datetime

import frappe

from ..token.token import token_auth


@frappe.whitelist(allow_guest=True)
@token_auth
def create_appointment(appointment_datetime):
	customer_id = frappe.local.form_dict.get("customer_id")

	print("@" * 20, customer_id)

	if not customer_id:
		frappe.throw("Customer ID is required")

	if not appointment_datetime:
		frappe.throw("Scheduled time must be in the future")

	# Convert input "DD-MM-YYYY HH:MM:SS" to MySQL format
	try:
		scheduled_dt = datetime.strptime(appointment_datetime, "%d-%m-%Y %H:%M:%S")
		appointment_datetime = scheduled_dt.strftime("%Y-%m-%d %H:%M:%S")
	except ValueError:
		frappe.throw("Invalid datetime format. Use DD-MM-YYYY HH:MM:SS")

	# frappe.set_user("Administrator")

	appointment = frappe.new_doc("Darshan Appointment")
	appointment.appointment_datetime = appointment_datetime
	appointment.customer = customer_id

	appointment.save()
	return "Ok"


@frappe.whitelist(allow_guest=True)
@token_auth
def appointment_list():
	customer_id = frappe.local.form_dict.get("customer_id")

	# frappe.set_user("Administrator")
	if not customer_id:
		frappe.throw("Customer ID is required")

	appointments = frappe.get_all(
		"Darshan Appointment",
		filters={"customer": customer_id},
		fields=["name", "appointment_datetime", "workflow_state"],
	)

	return appointments


@frappe.whitelist(allow_guest=True)
@token_auth
def appointment_details(appointment_id):
	customer_id = frappe.local.form_dict.get("customer_id")
	if not customer_id:
		frappe.throw("Customer ID is required")

	frappe.set_user("Administrator")
	appointment = frappe.get_list(
		"Darshan Appointment", filters={"name": appointment_id, "customer": customer_id}, fields=["companion"]
	)

	if not appointment:
		frappe.throw("Appointment not found")

	first_appointment = frappe.get_doc("Darshan Appointment", appointment[0].name)

	return first_appointment
