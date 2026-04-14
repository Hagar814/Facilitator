frappe.ui.form.on('Course', {
    refresh: function(frm) {
        // Only show for users with a specific role if needed
        if (!frappe.user.has_role('Course Attendance')) return;
        // Add custom "Reject" button
        frm.add_custom_button(__('Reject'), function() {
            frappe.prompt(
                [
                    {
                        fieldname: 'note',
                        fieldtype: 'Small Text',
                        label: __('Reason'),
                        reqd: 1
                    }
                ],
                function(values) {
                    const rejected_by = frappe.session.user_fullname;

                    frappe.call({
                        method: "facilitator.custom.python.course.notify_admin_about_event",
                        args: {
                            event_name: frm.doc.name,
                            note: values.note,
                            rejected_by: rejected_by
                        },
                        callback: function(r) {
                            frm.set_value('rejected', 1)
                            frm.set_value('rejection_reason', values.note);
                            frm.save();

                            frappe.show_alert({
                                message: __("Notification sent for {0}", [frm.doc.name]),
                                indicator: "orange"
                            });
                        }
                    });
                },
                __('Reject Event'),
                __('Send')
            );
        });
    },
        get_attendance: function(frm) {

        console.log("🚀 Button clicked for Course:", frm.doc.name);

        if (!frm.doc.name) {
            frappe.msgprint("Please save the Event first.");
            return;
        }

        // Clear existing rows
        frm.clear_table('course_attendance');

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Courses Attendance',  // fetch from this doctype
                filters: { event: frm.doc.event }, // match current Event
                fields: ['name', 'contact_name', 'attendance_date'] // make sure fieldnames match Course Attendance
            },
            callback: function(r) {


                if (r.message && r.message.length > 0) {
                    r.message.forEach(function(row, index) {

                        console.log(`➡ Processing row ${index + 1}:`, row);

                        let child = frm.add_child('course_attendance');

                        // Set the fields in the child table row
                        child.id = row.name;
                        child.contact_name = row.contact_name || "";
                        child.date = row.attendance_date || "";

                        console.log("📝 Added child row:", child);
                    });

                    frm.refresh_field('course_attendance');
                    frm.save()
          
                } else {

                    frappe.msgprint("No attendance records found for this Event.");
                }
            },
            error: function(err) {
                console.error("❌ frappe.call error:", err);
            }
        });
    },
    approve: function(frm) {
        console.log("custom_approve clicked");

        // select rows based on __checked property
        let selected_rows = frm.doc.course_attendance.filter(r => r.__checked);

        console.log("Selected rows via __checked:", selected_rows);

        if (!selected_rows || selected_rows.length === 0) {
            frappe.msgprint("Please select at least one attendance row to approve.");
            return;
        }

        // submit selected rows
        selected_rows.forEach(row => {
            console.log("Submitting row:", row.id);
            frappe.call({
                method: 'frappe.client.get',
                args: { doctype: 'Courses Attendance', name: row.id },
                callback: function(r) {
                    let doc = r.message;
                    if (doc.docstatus === 1) {
                        frappe.msgprint(`Document ${row.id} is already submitted ✅`);
                        return;
                    }

                    frappe.call({
                        method: 'frappe.client.submit',
                        args: { doc: doc },
                        callback: function(res) {
                            frappe.msgprint(`Document ${row.id} submitted successfully ✅`);
                            console.log("Submitted:", res);

                            // uncheck row after submission
                            row.__checked = 0;
                            frm.refresh_field('course_attendance');
                        }
                    });
                }
            });
        });
    }
});
