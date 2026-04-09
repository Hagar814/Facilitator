frappe.ui.form.on('Delivery Note', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1 ) {
			frm.add_custom_button(__('Schedule'), function() {
				frappe.model.open_mapped_doc({
					method: "facilitator.custom.python.delivery_note.make_event",
					frm: cur_frm,
				})
			}, __('Create'));
			frm.page.set_inner_btn_group_as_primary(__('Create'));
		}}})