// Copyright (c) 2016, Facilitators and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Quest Planning Report"] = {
	"filters": [

		{
			"fieldname":"client",
			"label": __("Client"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"sales_person",
			"label": __("Sales Person"),
			"fieldtype": "Link",
			"options": "Sales Person"
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "course_status",
			"label": __("Course Status"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				let status = ["Tentative", "Completed", "Postpond", "Canceled"]
				let options = []
				for (let option of status){
					options.push({
						"value": option,
						"description": ""
					})
				}
				return options
			}
		},
		{
			fieldname: "course_type",
			label: __("Course Type"),
			fieldtype: "Select",
			options: [
				{ "value": "Virtual", "label": __("Virtual") },
				{ "value": "Classroom", "label": __("Class Room") }
			],
		},
		{
			fieldname: "direct_indirect_",
			label: __("Direct Indirect"),
			fieldtype: "Select",
			options: [
				{ "value": "Direct", "label": __("Direct") },
				{ "value": "Indirect", "label": __("Indirect") },
				{ "value": "Retail", "label": __("Retail") },
				{ "value": "Whole Sale", "label": __("Whole Sale") }
			],
		},
		
	]
}
