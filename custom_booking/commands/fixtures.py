import click
import frappe
from frappe.commands import pass_context
from frappe.utils.fixtures import export_fixtures


@click.command("prepare-user-fixtures")
@pass_context
def prepare_user_fixtures(context):
	"""Prepare User records before exporting fixtures"""

	emails = [
		"devoteee@example.com",
		"approver@example.com",
		"attender@example.com",
	]

	if not context.sites:
		from frappe.exceptions import SiteNotSpecifiedError

		raise SiteNotSpecifiedError

	for site in context.sites:
		try:
			frappe.init(site=site)
			frappe.connect()

			# IMPORTANT:
			# Never mutate core doctypes without update_modified=False
			frappe.db.set_value(
				"User",
				{"email": ["in", emails]},
				"send_welcome_email",
				0,
				update_modified=False,
			)

			frappe.db.commit()

		finally:
			frappe.destroy()


@click.command("export-prepared-fixtures")
@pass_context
def export_prepared_fixtures(context):
	"""Export fixtures after preparing data safely"""

	emails = [
		"devoteee@example.com",
		"approver@example.com",
		"attender@example.com",
	]

	if not context.sites:
		from frappe.exceptions import SiteNotSpecifiedError

		raise SiteNotSpecifiedError

	for site in context.sites:
		try:
			frappe.init(site=site)
			frappe.connect()

			# Idempotent + safe
			frappe.db.set_value(
				"User",
				{"email": ["in", emails]},
				"send_welcome_email",
				0,
				update_modified=False,
			)

			frappe.db.commit()

			# Export fixtures only AFTER safe mutation
			export_fixtures()

		finally:
			frappe.destroy()
