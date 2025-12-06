import frappe

from custom_booking.api.token.token import token_auth


@frappe.whitelist(allow_guest=True)
@token_auth
def create_donor():
	customer_id = frappe.local.form_dict.get("customer_id")
	frappe.set_user("Administrator")
	customer = frappe.get_doc("Customer", customer_id)
	new_donor = frappe.new_doc("Donor")
	new_donor.donor_name = customer.customer_name
	new_donor.email = customer.custom_email
	new_donor.donor_type = "Individual"
	new_donor.save()
	return new_donor
