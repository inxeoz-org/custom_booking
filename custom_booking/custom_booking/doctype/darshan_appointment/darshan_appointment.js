// Copyright (c) 2025, inxeoz and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Darshan Appointment", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Darshan Appointment", {
	fetch_default_companion(frm) {
		call_companion_api(frm);
	},
});

function call_companion_api(frm) {
	frappe.call({
		method: "custom_booking.custom_booking.doctype.darshan_appointment.darshan_appointment.insert_default_companion_from_customer_to_darshan_appointment",
		args: {
			customer_id: frm.doc.customer,
			darshan_appointment_id: frm.doc.name,
		},
		callback(r) {
			frappe.msgprint(r.message);
			frm.reload_doc();
		},
	});
}
