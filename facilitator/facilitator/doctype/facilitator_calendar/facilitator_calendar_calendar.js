frappe.views.calendar["Facilitator Calendar"] = {
	field_map:{
		"start": "start_on",
		"end": "end_on",
		"id": "name",
		"allDay":false,
		"title": "title",
		"doctype":"doctype",
		"color":"color"
	},
	gantt: true,
	eventLimit: true,
 	 views: {
           month: {
             eventLimit: 6 // adjust to 6 only for agendaWeek/agendaDay
             }
         },
	filters: [
		{
			fieldtype: "Link",
			fieldname: "facilitator",
			options: "Facilitator",
			default: "Samah Shenouda",
			label: __("Facilitators")
		},
		{
			fieldtype: "Link",
			fieldname: "event",
			options: "Event",
			label: __("Alaa")
		},
		{
			"fieldtype": "Date",
			"fieldname": "start_on",
			"label": __("Start Date")
		}
	],

	get_events_method: "facilitator.facilitator.doctype.facilitator_calendar.facilitator_calendar.getData"
	

}

