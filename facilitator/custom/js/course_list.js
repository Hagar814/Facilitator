let current_filter_mode = "default"; // ✅ global

frappe.listview_settings['Course'] = {
    
    add_fields: ["status", "course_name", "client"],

    onload: function(listview) {
        if (frappe.session.user === "Administrator") return;
         setTimeout(() => {
                // Hide the whole standard filter section
                listview.page.wrapper
                    .find('.standard-filter-section')
                    .hide();

                // OPTIONAL: also hide filter button (if you want fully restricted UI)
                listview.page.wrapper
                    .find('.filter-selector')
                    .hide();

            }, 200);
current_filter_mode = "default"; 
        if (frappe.user.has_role('Course Attendance')) {
    const current_user = frappe.session.user;
            listview.filter_area.add([
                ['Course', 'facilitator_email', '=', current_user],
['Course', 'course_status', 'in', ['Tentative', 'Confirmed', 'Postpond', 'Canceled']]  ,
['Course', 'rejected', '=', 0]   
          ]);
        }
listview.page.add_inner_button("Completed", function() {
            listview.filter_area.clear();
    const current_user = frappe.session.user;
current_filter_mode = "completed"; 
    listview.filter_area.add([
        ['Course', 'facilitator_email', '=', current_user],
['Course', 'course_status', 'in', ['Completed']]   ,
['Course', 'rejected', '=', 0]   
    ]);
});
listview.page.add_inner_button("Rejected", function() {
            listview.filter_area.clear();
    const current_user = frappe.session.user;
current_filter_mode = "completed"; 
    listview.filter_area.add([
        ['Course', 'facilitator_email', '=', current_user],
['Course', 'rejected', '=', 1]   
    ]);
});
  listview.page.add_inner_button("Tentative", function() {
            listview.filter_area.clear();
    const current_user = frappe.session.user;

    listview.filter_area.add([
        ['Course', 'facilitator_email', '=', current_user],
['Course', 'course_status', 'in', ['Tentative', 'Confirmed', 'Postpond']]   ,
['Course', 'rejected', '=', 0]   
    ]);
});
    
    },

    refresh: function(listview) {
        if (frappe.session.user === "Administrator") return;
                    console.log(current_filter_mode);

if (current_filter_mode === "completed") return;
            listview.filter_area.clear();

        if (frappe.user.has_role('Course Attendance')) {

    const current_user = frappe.session.user;

            listview.filter_area.add([
                    ['Course', 'facilitator_email', '=', current_user],
               ['Course', 'course_status', 'in', ['Tentative', 'Confirmed', 'Postpond']]  
          ]);
            
        }

    },



    // Dropdown Button: Appears as a menu next to the primary button

    button: {
    show: function(doc) {
        console.log("Checking Generate Attendance button for:", doc.name, "Course Status:", doc.course_status);
        return true;  // <-- was doc.status
    },
    get_label: function(doc) {
        return __("QR");
    },
    get_description: function(doc) {
        return __("Generate Attendance Web Form & QR code for {0}", [doc.name]);
    },
    action: function(doc) {
        frappe.confirm(
            __('Generate Attendance Web Form for {0}?', [doc.name]),
            () => {
                frappe.call({
                    method: "facilitator.custom.python.course.create_attendance_web_form",
                    args: { docname: doc.name },
                    callback: function(r) {
                        if(r.message) {
                            let img_html = `<div style="text-align:center;">
                                                <img src="${r.message}" style="max-width:300px;"/>
                                            </div>`;
                            frappe.msgprint({
                                title: __('Attendance QR Code for {0}', [doc.name]),
                                message: img_html,
                                wide: 1
                            });
                            frappe.show_alert({ message: __("Attendance Form Generated"), indicator: 'green' });
                        }
                    }
                });
            }
        );
    }
}
};