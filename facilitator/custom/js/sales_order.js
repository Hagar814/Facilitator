frappe.ui.form.on('Sales Order', {
refresh: function(frm) {
    if(frm.doc.docstatus === 1 && frm.doc.status !== 'Closed'
         && flt(frm.doc.per_billed, 6) < 100) {
        frm.add_custom_button(__('Update Items'), () => {
            erpnext.utils.update_child_items({
                frm: frm,
                child_docname: "items",
                child_doctype: "Sales Order Detail",
                cannot_add_row: false,
            })
        });
    }
},
})