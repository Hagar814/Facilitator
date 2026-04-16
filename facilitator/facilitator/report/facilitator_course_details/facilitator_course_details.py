import frappe
from frappe.utils import getdate

def execute(filters=None):
    filters = filters or {}

    conditions = []
    values = {}

    # Facilitator filter (default from session)
    if filters.get("facilitator"):
        conditions.append("c.facilitator_email = %(facilitator)s")
        values["facilitator"] = filters.get("facilitator")

    # Course filter
    if filters.get("course"):
        conditions.append("c.name = %(course)s")
        values["course"] = filters.get("course")

    # Course Name filter
    if filters.get("course_name"):
        conditions.append("c.course_name LIKE %(course_name)s")
        values["course_name"] = f"%{filters.get('course_name')}%"

    # Course Status filter
    if filters.get("course_status"):
        conditions.append("c.course_status = %(course_status)s")
        values["course_status"] = filters.get("course_status")

    # Starts On filter
    if filters.get("starts_on"):
        conditions.append("DATE(c.starts_on) >= %(starts_on)s")
        values["starts_on"] = getdate(filters.get("starts_on"))

    # Ends On filter
    if filters.get("ends_on"):
        conditions.append("DATE(c.ends_on) <= %(ends_on)s")
        values["ends_on"] = getdate(filters.get("ends_on"))

    conditions_sql = " AND ".join(conditions)
    if conditions_sql:
        conditions_sql = "WHERE " + conditions_sql

    data = frappe.db.sql(f"""
        SELECT
            c.name AS course,
            c.client,
            c.course_name,
            c.course_status,
            c.language,
            c.starts_on,
            c.ends_on,
            c.facilitator,
            c.facilitator_email,
            COUNT(ca.name) AS attendance_count
        FROM `tabCourse` c
        LEFT JOIN `tabCourse Attendance` ca
            ON ca.parent = c.name
        {conditions_sql}
        GROUP BY c.name
        ORDER BY c.starts_on DESC
    """, values, as_dict=True)

    columns = [
        {"label": "Course", "fieldname": "course", "fieldtype": "Link", "options": "Course", "width": 150},
        {"label": "Client", "fieldname": "client", "fieldtype": "Data", "width": 150},
        {"label": "Course Name", "fieldname": "course_name", "fieldtype": "Data", "width": 200},
        {"label": "Language", "fieldname": "language", "fieldtype": "Data", "width": 120},
        {"label": "Status", "fieldname": "course_status", "fieldtype": "Data", "width": 120},
        {"label": "Start Date", "fieldname": "starts_on", "fieldtype": "Datetime", "width": 150},
        {"label": "End Date", "fieldname": "ends_on", "fieldtype": "Datetime", "width": 150},
        {"label": "Attendance Count", "fieldname": "attendance_count", "fieldtype": "Int", "width": 150},
    ]

    return columns, data