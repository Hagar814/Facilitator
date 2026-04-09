# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import copy
from frappe import _
from frappe.utils import flt, date_diff, getdate

def execute(filters=None):
	if not filters:
		return [], [], None, []

	validate_filters(filters)

	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	if not data:
		return [], [], None, []

	data, chart_data = prepare_data(data, filters)

	return columns, data, None, chart_data

def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	if not from_date and to_date:
		frappe.throw(_("From and To Dates are required."))
	elif date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and so.transaction_date between %(from_date)s and %(to_date)s"
		# conditions += " and si.posting_date between %(from_date)s and %(to_date)s"
	if filters.get("company"):
		conditions += " and so.company = %(company)s"

	if filters.get("sales_order"):
		conditions += " and so.name in %(sales_order)s"

	if filters.get("status"):
		conditions += " and so.status in %(status)s"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql("""
		SELECT
			so.transaction_date as date,
			soi.delivery_date as delivery_date,
			dn.posting_date as delivery_date_dn,
			so.name as sales_order,
			so.status, so.customer, soi.item_code,
			DATEDIFF(CURDATE(), soi.delivery_date) as delay_days,
			IF(so.status in ('Completed','To Bill'), 0, (SELECT delay_days)) as delay,
			soi.qty, soi.delivered_qty,
			(soi.qty - soi.delivered_qty) AS pending_qty,
   			soi.returned_qty,
			si.posting_date as invoice_date,
			si.name as invoice_name,
			dni.parent as delivery_name,
   			CASE WHEN (si.posting_date between %(from_date)s and %(to_date)s) THEN sii.base_amount ELSE 0 END as total_sales,
     		@temp3 := CASE WHEN (si.posting_date between %(from_date)s and %(to_date)s) and si.is_return THEN sii.base_amount ELSE 0 END as invoice_amount,
			IFNULL(SUM(sii.qty), 0) as billed_qty,
			@temp2 := sii.qty,
			soi.base_amount as amount,
			(soi.delivered_qty * soi.base_rate) as delivered_qty_amount,
			@temp1 := (soi.billed_amt * IFNULL(si.conversion_rate, 1))  as billed_amount,
   			(@temp2 * @temp1),
			(soi.base_amount - (soi.billed_amt * IFNULL(so.conversion_rate, 1))) as pending_amount,
			soi.warehouse as warehouse,
			ev.name as event_name, ev.course_status as event_status, ev.starts_on as event_start , ev.ends_on as event_end,
			so.company, soi.name
		FROM 
			`tabSales Order` so,
			`tabSales Order Item` soi

		LEFT JOIN `tabSales Invoice Item` sii
			ON sii.so_detail = soi.name
        LEFT JOIN `tabSales Invoice` si
			ON sii.parent = si.name
        LEFT JOIN `tabDelivery Note Item` dni
			ON dni.parent = sii.delivery_note
		LEFT JOIN `tabDelivery Note` dn
			ON dni.parent = dn.name
		LEFT JOIN `tabEvent` ev
			ON dn.name = ev.delivery_note

		WHERE
			soi.parent = so.name
			and so.status not in ('Stopped', 'Closed', 'On Hold')
			and so.docstatus = 1
			and si.status != 'Cancelled'
			{conditions}
		GROUP BY si.name
		ORDER BY si.posting_date , so.transaction_date ASC
	""".format(conditions=conditions), filters, as_dict=1)

	return data


def prepare_data(data, filters):
	completed, pending = 0, 0

	if filters.get("group_by_so"):
		sales_order_map = {}

	for row in data:
		# sum data for chart
		completed += row["billed_amount"]
		pending += row["pending_amount"]

		# prepare data for report view
		row["qty_to_bill"] = flt(row["qty"]) - flt(row["billed_qty"])

		row["delay"] = 0 if row["delay"] and row["delay"] < 0 else row["delay"]
		if filters.get("group_by_so"):
			so_name = row["sales_order"]

			if not so_name in sales_order_map:
				frappe.errprint(sales_order_map)
				# create an entry
				row_copy = copy.deepcopy(row)
				sales_order_map[so_name] = row_copy
			else:
				# update existing entry
				so_row = sales_order_map[so_name]
				so_row["required_date"] = max(getdate(so_row["delivery_date"]), getdate(row["delivery_date"]))
				so_row["delay"] = min(so_row["delay"], row["delay"])

				# sum numeric columns
				fields = ["qty", "delivered_qty", "pending_qty", "billed_qty", "qty_to_bill", "amount",
					"delivered_qty_amount", "billed_amount", "pending_amount"]
				for field in fields:
					so_row[field] = flt(row[field]) + flt(so_row[field])
			frappe.errprint(sales_order_map)

	chart_data = prepare_chart_data(pending, completed)

	if filters.get("group_by_so"):
		data = []
		for so in sales_order_map:
			data.append(sales_order_map[so])
		return data, chart_data

	return data, chart_data

def prepare_chart_data(pending, completed):
	labels = ["Amount to Bill", "Billed Amount"]

	return {
		"data" : {
			"labels": labels,
			"datasets": [
				{"values": [pending, completed]}
				]
		},
		"type": 'donut',
		"height": 300
	}

def get_columns(filters):
	columns = [
		{
			"label":_("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 90
		},
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 120
		},
		{
			"label":_("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 130
		}]

	if not filters.get("group_by_so"):
		columns.append({
			"label":_("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 130
		})

	columns.extend([
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty"
		},
		{
			"label": _("Delivered Qty"),
			"fieldname": "delivered_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "qty"
		},
  	{
			"label": _("Returned Qty"),
			"fieldname": "returned_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "qty"
		},
		{
			"label": _("Qty to Deliver"),
			"fieldname": "pending_qty",
			"fieldtype": "Float",
			"width": 130,
			"convertible": "qty"
		},
		{
			"label": _("Billed Qty"),
			"fieldname": "billed_qty",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty"
		},
		{
			"label": _("Qty to Bill"),
			"fieldname": "qty_to_bill",
			"fieldtype": "Float",
			"width": 100,
			"convertible": "qty"
		},
		{
			"label": _("Order Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 120,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
  		{
			"label": _("Delivered Amount"),
			"fieldname": "delivered_qty_amount",
			"fieldtype": "Currency",
			"width": 140,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
		{
			"label": _("Billed Amount"),
			"fieldname": "billed_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
  		{
			"label": _("Returned Amount"),
			"fieldname": "invoice_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
        {
			"label": _("Total Sales"),
			"fieldname": "total_sales",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},
		{
			"label": _("Pending Amount"),
			"fieldname": "pending_amount",
			"fieldtype": "Currency",
			"width": 130,
			"options": "Company:company:default_currency",
			"convertible": "rate"
		},

		{
			"label":_("Delivery Date (SO)"),
			"fieldname": "delivery_date",
			"fieldtype": "Date",
			"width": 140
		},
  		{
			"label":_("Acual Delivery Date"),
			"fieldname": "delivery_date_dn",
			"fieldtype": "Date",
			"width": 140
		},
  		{
			"label":_("Invoice Date"),
			"fieldname": "invoice_date",
			"fieldtype": "Date",
			"width": 120
		},
    
        {
			"label": _("Delivery Name"),
			"fieldname": "delivery_name",
			"fieldtype": "Link",
   			"options": "Delivery Note",	
			"width": 120,
		},
      {
			"label": _("Invoice Name"),
			"fieldname": "invoice_name",
			"fieldtype": "Link",
   			"options": "Sales Invoice",	
			"width": 120,
		},
  		{
			"label":_("Event Name"),
			"fieldname": "event_name",
   			"fieldtype": "Link",
			"options": "Event",
			"width": 100
		},
      	{
			"label":_("Event Start On"),
			"fieldname": "event_start",
			"fieldtype": "Datetime",
			"width": 120
		},
        {
			"label":_("Event End On"),
			"fieldname": "event_end",
			"fieldtype": "Datetime",
			"width": 120
		},
      	{
			"label":_("Event Status"),
			"fieldname": "event_status",
   			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Delay (in Days)"),
			"fieldname": "delay",
			"fieldtype": "Data",
			"width": 100
		}
	])
	if not filters.get("group_by_so"):
		columns.append({
			"label": _("Warehouse"),
			"fieldname": "warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 100
		})
	columns.append({
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100
		})


	return columns