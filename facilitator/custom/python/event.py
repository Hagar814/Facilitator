import json
import frappe
import frappe, json
from frappe import utils
import json
import datetime
from datetime import timezone, datetime, timedelta
from frappe.utils import (getdate, cint, add_months, date_diff, add_days,
	nowdate, get_datetime_str, cstr, get_datetime, now_datetime, format_datetime)
from frappe import _
from frappe.utils import flt
from frappe.model.document import Document


@frappe.whitelist()
def update_course_status():
	events = frappe.get_list("Event", filters={"status": "Open"}, fields=["name", "ends_on", "course_status"])
	now = now_datetime()
	for event in events:
		if (event.ends_on and getdate(event.ends_on) < getdate(nowdate())) and (event.course_status not in ('Canceled','Postpond')):
			frappe.db.set_value("Event", event.name, "course_status", "Completed")
@frappe.whitelist()	
def update_facilitator_status():
	events = frappe.get_list("Event", filters={"course_status": "Completed"}, fields=["name"])
	for event in events:
		facilitator_table = frappe.get_list('Facilitator Table', {'parent': event['name']})
		for row in facilitator_table:
			frappe.db.set_value('Facilitator Table', {'name': row['name']}, 'status', 'Delivered')
			frappe.db.commit()




def create_course_from_event(doc, method):
    try:
        # Safety check
        if not doc.facilitator:
            return

        for row in doc.facilitator:
            if not row.facilitator:
                continue

            # Get facilitator email
            facilitator_email = frappe.db.get_value(
                "Facilitator",
                row.facilitator,
                "email"
            )

            # Create Course
            course = frappe.new_doc("Course")

            course.client = doc.client
            course.course_name = doc.course_name
            course.course_status = doc.course_status
            course.facilitator = row.facilitator
            course.facilitator_email = facilitator_email
            course.starts_on = doc.starts_on
            course.ends_on = doc.ends_on
            course.company = doc.company
            course.language = doc.language_1
            course.event = doc.name

            # Optional
            if hasattr(doc, "location"):
                course.address = doc.location

            course.insert(ignore_permissions=True)

            frappe.logger().info(
                f"[COURSE CREATED] Event: {doc.name} → Course: {course.name}"
            )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Create Course Failed for Event {doc.name}"
        )


def sync_courses_from_event(doc, method):
    try:
        # -------------------------
        # Prepare Data
        # -------------------------
        event_facilitators = set()
        if doc.facilitator:
            for row in doc.facilitator:
                if row.facilitator:
                    event_facilitators.add(row.facilitator)

        existing_courses = frappe.get_all(
            "Course",
            filters={"event": doc.name},
            fields=["name", "facilitator"]
        )

        existing_map = {c.facilitator: c.name for c in existing_courses}

        # =====================================================
        # 🟢 CREATE SECTION (new facilitators)
        # =====================================================
        new_facilitators = event_facilitators - set(existing_map.keys())

        for facilitator in new_facilitators:
            facilitator_email = frappe.db.get_value(
                "Facilitator",
                facilitator,
                "email"
            )

            course = frappe.new_doc("Course")

            course.client = doc.client
            course.course_name = doc.course_name
            course.course_status = doc.course_status
            course.facilitator = facilitator
            course.facilitator_email = facilitator_email
            course.starts_on = doc.starts_on
            course.ends_on = doc.ends_on
            course.language = doc.language_1
            course.event = doc.name

            if hasattr(doc, "location"):
                course.address = doc.location

            course.insert(ignore_permissions=True)

        # =====================================================
        # 🟡 UPDATE SECTION (existing facilitators)
        # =====================================================
        common_facilitators = event_facilitators & set(existing_map.keys())

        for facilitator in common_facilitators:
            course = frappe.get_doc("Course", existing_map[facilitator])

            facilitator_email = frappe.db.get_value(
                "Facilitator",
                facilitator,
                "email"
            )

            course.client = doc.client
            course.course_name = doc.course_name
            course.course_status = doc.course_status
            course.starts_on = doc.starts_on
            course.ends_on = doc.ends_on
            course.language = doc.language_1
            course.facilitator_email = facilitator_email

            if hasattr(doc, "location"):
                course.address = doc.location

            course.save(ignore_permissions=True)

        # =====================================================
        # 🔴 DELETE SECTION (removed facilitators)
        # =====================================================
        removed_facilitators = set(existing_map.keys()) - event_facilitators

        for facilitator in removed_facilitators:
            frappe.delete_doc("Course", existing_map[facilitator], force=True)

        # -------------------------
        # Log
        # -------------------------
        frappe.logger().info(
            f"[SYNC] Event {doc.name} | "
            f"Created: {len(new_facilitators)} | "
            f"Updated: {len(common_facilitators)} | "
            f"Deleted: {len(removed_facilitators)}"
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Course Sync Failed for Event {doc.name}"
        )

# @frappe.whitelist()
# def update_course_status(event=None):
#         now = now_datetime()
#         event = frappe.get_doc('Event', event)
#         for doc in event:
#             facilitator = doc.facilitator
#         for d in doc.facilitator:
#             if doc.ends_on != None and endtime < now and doc.course_status not in ('Canceled','Postpond'):
#                 doc.course_status = "Completed"
#                 d.status = "Delivered"
#         frappe.db.commit()
#         # doc.save()
#         print(doc.course_status, doc.name)
      

   # print("hi")

    # newnote = frappe.get_doc({"doctype": "Note", "title": "Some note"})
    # newnote.insert()
    # frappe.db.commit()
    # doc = frappe.get_doc("Event", "EV27755")
    # events = frappe.get_list("Event", filters={"status": "Open"}, fields=["name"])