// Copyright (c) 2026, Facilitators and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Facilitator Course Details"] = {
    filters: [
        {
            fieldname: "facilitator",
            label: "Facilitator Email",
            fieldtype: "Data",
            default: frappe.session.user,
            read_only: 1
        },
		{
			fieldname: "course_name",
			label: "Course Name",
			fieldtype: "Link",
			options: "Item"
		},
        {
            fieldname: "course_status",
            label: "Course Status",
            fieldtype: "Select",
            options: "\nTentative\nCompleted\nCanceled\nPostpond\nConfirmed"
        },
        {
            fieldname: "starts_on",
            label: "Starts On",
            fieldtype: "Date"
        },
        {
            fieldname: "ends_on",
            label: "Ends On",
            fieldtype: "Date"
        }
    ]
};
