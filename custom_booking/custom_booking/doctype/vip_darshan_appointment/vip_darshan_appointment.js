// Copyright (c) 2025, inxeoz and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Vip Darshan Appointment", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Vip Darshan Appointment", {
	fetch_default_companion(frm) {
		call_companion_api(frm);
	},
});

function call_companion_api(frm) {
	frappe.call({
		method: "custom_booking.custom_booking.doctype.devoteee.profile.companion",
		args: {
			devoteee_id: frm.doc.devoteee_id,
		},
		callback(r) {
			frappe.msgprint(r.message);
			frm.reload_doc();
		},
	});
}
