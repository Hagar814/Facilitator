# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
import frappe.defaults
from erpnext.controllers.selling_controller import SellingController
from erpnext.stock.doctype.batch.batch import set_batch_nos
from erpnext.stock.doctype.serial_no.serial_no import get_delivery_note_serial_no
from frappe import _
from frappe.contacts.doctype.address.address import get_company_address
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from frappe.model.utils import get_fetch_values
from frappe.utils import cint, flt
from erpnext.controllers.accounts_controller import get_taxes_and_charges


@frappe.whitelist()
def make_event(source_name, target_doc=None):
	# def set_missing_values(source, target):
	# 	target.client = customer_name	

	doc = get_mapped_doc("Delivery Note", source_name, {
		"Delivery Note": {
			"doctype": "Event",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map":{
				"customer_name" : "client",
			}
		},
		"Delivery Note Item": {
			"doctype": "Event So Item",
			"field_map": {
				"rate": "rate",
				"delivery_date": "delivery_date",
				}
			},
		"Sales Team": {
			"doctype": "Sales Team",
			"add_if_empty": True
		}
	}, target_doc)

	return doc
