import click
import frappe
from frappe.utils.fixtures import export_fixtures
from frappe.commands import pass_context


@click.command("prepare-user-fixtures")
@pass_context
def prepare_user_fixtures(context):
	"""Prepare User records before exporting fixtures"""
	emails = ["devoteee@example.com", "approver@example.com", "attender@example.com"]

	for site in context.sites:
		try:
			frappe.init(site=site)
			frappe.connect()
			frappe.db.set_value(
				"User", {"email": ["in", emails]}, "send_welcome_email", 0, update_modified=False
			)
			frappe.db.commit()
		finally:
			frappe.destroy()
	if not context.sites:
		from frappe.exceptions import SiteNotSpecifiedError

		raise SiteNotSpecifiedError


@click.command("export-prepared-fixtures")
@pass_context
def export_prepared_fixtures(context):
	"""Prepare data and export fixtures"""
	for site in context.sites:
		try:
			frappe.init(site=site)
			frappe.connect()
			emails = ["devoteee@example.com", "approver@example.com", "attender@example.com"]
			frappe.db.set_value(
				"User", {"email": ["in", emails]}, "send_welcome_email", 0, update_modified=False
			)
			frappe.db.commit()
			export_fixtures()
		finally:
			frappe.destroy()
	if not context.sites:
		from frappe.exceptions import SiteNotSpecifiedError

		raise SiteNotSpecifiedError
