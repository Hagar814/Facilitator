# -*- coding: utf-8 -*-
# Copyright (c) 2018, Facilitators and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.utils import add_days,format_datetime
from frappe import _



@frappe.whitelist()
def getData(start,end,filters=None):
	event_obj=[]
	available_facilitators=0
	fil = []
	selected_facilitator = None
	selected_event = None
	if filters:
		fil=json.loads(filters)
		for fil_cond in fil:
			if fil_cond[1]=="available_facilitators":
				available_facilitators = fil_cond[3]

			if fil_cond[1]=="facilitator":
				selected_facilitator = fil_cond[3]

			if fil_cond[1]=="event":
				selected_event = fil_cond[3]
	if available_facilitators == 1:
		available_faci=getAvailableFacilitator(start,end,event_obj,selected_facilitator)
		return available_faci

	event=frappe.db.sql("""select ev.name,ev.starts_on,ev.ends_on,ev.course_name,ft.facilitator,ev.color,ev.client,ft.status from  `tabFacilitator Table` as ft  inner join `tabEvent` as ev on ev.name=ft.parent WHERE
				(date(ev.starts_on) BETWEEN date(%s) AND date(%s))
				OR (date(ev.ends_on) BETWEEN date(%s) AND date(%s))""",(start, end, start, end))
	for row in event:
		if selected_facilitator:
			if not row[4] == selected_facilitator:
				continue
		if selected_event:
			if not row[0] == selected_event:
				continue
		title_temp=''
		if not row[6]==None:
			if not row[4]==None:
				title_temp=row[4]+('\n')+str(row[3])+('\n')+row[6] if not row[3]==None else row[4]+('\n')+row[6]
			else:
				title_temp=row[3]+('\n')+row[6] if not row[3]==None else row[6]
		else:
			if not row[4]==None:
				title_temp=row[4]+('\n')+row[3] if not row[3]==None else row[4]
			else:
				title_temp=row[3] if not row[3]==None else 'No Info'

		item={}
		item["start_on"]=row[1] if not row[2]==None else add_days(row[1],0)
		item["end_on"]=row[2] if not row[2]==None else add_days(row[1],0)
		item["name"]=row[0]
		item["title"]=title_temp
		item["doctype"]="Event"
		item["color"]=getColor(row[7] if not row[7]==None else 'Default')
		event_obj.append(item)
	
	leave=frappe.db.sql('''select name,start_on,end_on,facilitator from `tabFacilitator Holiday` WHERE
				(date(`tabFacilitator Holiday`.start_on) BETWEEN date(%s) AND date(%s))
				OR (date(`tabFacilitator Holiday`.end_on) BETWEEN date(%s) AND date(%s))''',(start, end, start, end))
	for row1 in leave:
		if selected_facilitator:
			if not row1[3] == selected_facilitator:
				continue
		leave_item={}
		leave_item["name"]=row1[0]
		leave_item["start_on"]=row1[1]
		leave_item["end_on"]=row1[2]
		leave_item["title"]='Holiday -'+'\n'+str(row1[3])
		leave_item["doctype"]="Facilitator Holiday"
		leave_item["color"]="#808080"
		event_obj.append(leave_item)
	return event_obj

@frappe.whitelist()
def getColor(status):
	data=frappe.db.sql("""select color from `tabFacilitator Status Color` where status=%s limit 1""",status)
	if data:
		return data[0][0]
	else:
		return '#07f2c7'

@frappe.whitelist()
def getAvailableFacilitator(start,end,event_obj,faci_cond=None):
	facilitator=frappe.db.sql("""select name from `tabFacilitator`""", as_list = 1)
	start_date=add_days(format_datetime(start,'YYYY-MM-dd'),1)
	end_date=format_datetime(end,'YYYY-MM-dd')
	facilitator_list = []
	if faci_cond==None:
		while start_date<end_date:
			existing_facilitator_list = []
			existing_facilitator_list.extend(frappe.db.sql("""select ft.facilitator from `tabEvent` as ev inner join `tabFacilitator Table` as ft on ev.name=ft.parent where %s between ev.starts_on and ev.ends_on""",(start_date), as_list = 1))
			existing_facilitator_list.extend(frappe.db.sql("""select facilitator from `tabFacilitator Holiday` where %s between start_on and end_on""",(start_date), as_list = 1))
			facilitator_list.extend([[start_date, row] if row not in existing_facilitator_list else None for row in facilitator])
			start_date=add_days(start_date,1)
		for row in facilitator_list:
			if row:
				faci_item={}
				faci_item["name"]=row[1]
				faci_item["start_on"]=row[0]
				faci_item["end_on"]=row[0]
				faci_item["title"]=row[1]
				faci_item["doctype"]="Facilitator"
				faci_item["color"]="#FFA500"	
				event_obj.append(faci_item)
	else:
		while start_date<end_date:
			faci_item={}
			event=frappe.db.sql("""select ev.name,ev.starts_on,ev.ends_on,ft.facilitator from `tabEvent` as ev inner join `tabFacilitator Table` as ft on ev.name=ft.parent where %s between ev.starts_on and ev.ends_on and ft.facilitator=%s""",(start_date,faci_cond))
			if event:
				start_date=add_days(start_date,1)
				continue
			holiday=frappe.db.sql("""select name,start_on,end_on,facilitator from `tabFacilitator Holiday` where %s between start_on and end_on and facilitator=%s""",(start_date,faci_cond))
			if holiday:
				start_date=add_days(start_date,1)
				continue
			faci_item["name"]=faci_cond
			faci_item["start_on"]=start_date
			faci_item["end_on"]=start_date
			faci_item["title"]=faci_cond
			faci_item["doctype"]="Facilitator"
			faci_item["color"]="#FFA500"	
			event_obj.append(faci_item)
			start_date=add_days(start_date,1)
		

	return event_obj