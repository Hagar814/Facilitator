
# Copyright (c) 2013, Facilitators and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from collections.abc import Set


def execute(filters=None):
    columns, data = [], []
    columns = get_column()
    data = get_data(filters)
    return columns, data


def get_column():
    columns = [
        {
            "label": "Event ID",
            "fieldname": "event_id",
            "fieldtype": "Link",
            "options": "Event",
            "width": 150
        },
        {
            "label": "Sales Person",
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 150
        },
        {
            "label": "Course Name",
            "fieldname": "course_name",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "SO Reference",
            "fieldname": "so_reference",
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 150
        },
        {
            "label": "Client",
            "fieldname": "client",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "label": "Facilitator(s)",
            "fieldname": "facilitator",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Product Line",
            "fieldname": "project",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Course Status",
            "fieldname": "course_status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Amount",
            "fieldname": "so_amount",
            "fieldtype": "Data",
            "width": 160
        },
        {
            "label": "Amount EGP",
            "fieldname": "base_amount",
            "fieldtype": "Currency",
            "width": 160
        },
        {
            "label": "Duration",
            "fieldname": "duration",
            "fieldtype": "Int",
            "width": 100
        }
    ]
    return columns


def get_data(filters):
    final_data = []
    data = frappe.db.sql("""SELECT e.name as event_id,
	e.course_name,
	e.so_reference,
	e.client,
	e.ends_on,
	e.starts_on,
    i.project,
	f.facilitator,
	e.course_status,
	so.rate as so_amount,
	i.amount,
	i.base_amount,
	t.sales_person,
	e.course_type,
	e.direct_indirect_,
	TIMESTAMPDIFF(DAY, e.starts_on, e.ends_on) as duration
	FROM `tabEvent` e
	CROSS JOIN `tabFacilitator Table` f
	ON f.`parent` = e.`name`
	CROSS JOIN `tabSales Team` t
	ON t.`parent` = e.`name`
	CROSS JOIN `tabSales Order Item` so
	ON so.`parent` = e.`so_reference`
	CROSS JOIN `tabEvent So Item` i
	ON i.`parent` = e.`name`
	where so.item_code = i.item_code
	group by e.name , f.facilitator, i.amount
	order by e.name desc""", as_dict=1)

    for i in range(0, len(data)):
        if data[i]['facilitator']:
            facilitators = {data[i]['facilitator']}
        else:
            facilitators = set()
        for j in range(0, len(data)):
            if data[i]['so_reference'] == data[j]['so_reference'] and data[i]['event_id'] == data[j]['event_id'] and data[i]['course_name'] == data[j]['course_name'] and data[i]['client'] == data[j]['client']\
                and not data[i]['facilitator'] == data[j]['facilitator'] and data[i]['course_status'] == data[j]['course_status']\
                    and data[i]['amount'] == data[j]['amount'] and data[i]['duration'] == data[j]['duration']:
                if isinstance(data[j]['facilitator'], Set):
                    facilitators = facilitators | data[j]['facilitator']
                else:
                    facilitator = data[j]['facilitator']
                    facilitators.add(facilitator)
        data[i]['facilitator'] = facilitators
    for d in data:
        if filters.get('client'):
            if not filters.get('client') == d['client']:
                continue
        if filters.get('course_status'):
            if not d['course_status'] in filters.get('course_status'):
                continue
        if filters.get('course_type'):
            if not filters.get('course_type') == d['course_type']:
                continue
        if filters.get('direct_indirect_'):
            if not filters.get('direct_indirect_') == d['direct_indirect_']:
                continue
        if filters.get('sales_person'):
            if not filters.get('sales_person') == d['sales_person']:
                continue
        if filters.get('from_date') and filters.get('to_date'):
            if not d['starts_on']:
                continue
            # frappe.errprint(d['starts_on'])
            date = str(d['ends_on']).split(" ")[0]
            date = str(d['starts_on']).split(" ")[0]
            if not (date >= filters.get('from_date') and date <= filters.get('to_date')):
                continue
        if d.get('facilitator'):
            d['facilitator'] = ','.join(sorted(d['facilitator']))
            if not d in final_data:
                final_data.append(d)
    return final_data
