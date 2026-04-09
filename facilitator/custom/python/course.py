import frappe
import qrcode
import io
from frappe.utils.file_manager import save_file
from frappe.utils import get_url, nowdate
from frappe import _
from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification


@frappe.whitelist()
def create_attendance_web_form(docname):
    try:
        # Get Event
        event_doc = frappe.get_doc("Course", docname)
        count = frappe.db.count("Web Form", {
    "title": ["like", f"Attendance - {event_doc.name}%"]
})

        form_name = f"Attendance - {event_doc.name} - {count + 1}"
        company_logo = ""
        if event_doc.company:
            company_doc = frappe.get_doc("Company", event_doc.company)
            company_logo = company_doc.logo or ""
        
        web_form = frappe.get_doc({
    "doctype": "Web Form",
    "title": form_name,
    "route": frappe.scrub(form_name),
    "doc_type": "Courses Attendance",
    "published": 1,
    "custom_css": """
                /* Hides the entire top navigation bar */
                .navbar {
                    display: none !important;
                }

                /* Adjusts padding so the content doesn't feel cut off at the top */
                body {
                    padding-top: 0 !important;
                }
            """,
    "introduction_text": f"""
    <div style="text-align:center; margin-bottom:20px;">
        <img src="{company_logo}" style="max-height:100px;">
    </div>
""",
    "web_form_fields": [
                

                {
                    "fieldname": "contact_name",
                    "label": "Name",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "fieldname": "email",
                    "label": "Email",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "fieldname": "mobile_number",
                    "label": "Mobile Number",
                    "fieldtype": "Int",
                    "reqd": 1
                },
                {
                    "fieldname": "course_attendance_status",
                    "label": "Course Attendance Status",
                    "fieldtype": "Link",
                    "options":"Course Attendance Status",
                    "reqd": 0
                },
                {
                    "fieldname": "comment",
                    "label": "Comment",
                    "fieldtype": "Small Text",
                    "reqd": 0
                },
 
                {
                    "fieldname": "company",
                    "label": "Company",
                    "fieldtype": "Data",
                    "default": str(event_doc.company),
                    "read_only": 1
                },
                 {
                    "fieldname": "client",
                    "label": "Customer",
                    "fieldtype": "Data",
                    "default": str(event_doc.client),
                    "read_only": 1
                },
                {
                    "fieldname": "facilitator",
                    "label": "Facilitator",
                    "fieldtype": "Data",
                    "default": str(event_doc.facilitator),
                    "read_only": 1
                },
                {
                    "fieldname": "event",
                    "label": "Event",
                    "fieldtype": "Link",
                    "options": "Event",
                    "default": event_doc.event,
                    "read_only": 1
                },
                {
                    "fieldname": "course_name",
                    "label": "Course",
                    "fieldtype": "Data",
                    "default": str(event_doc.course_name),
                    "read_only": 1
                },
                {
                    "fieldname": "language",
                    "label": "Language",
                    "fieldtype": "Data",
                    "default": str(event_doc.language),
                    "read_only": 1
                },
                {
                    "fieldname": "starts_on",
                    "label": "Starts ON",
                    "fieldtype": "Datetime",
                    "default": str(event_doc.starts_on),
                    "read_only": 1
                },
               {
                    "fieldname": "ends_on",
                    "label": "Ends ON",
                    "fieldtype": "Datetime",
                    "default": str(event_doc.ends_on),
                    "read_only": 1
                },
                {
                    "fieldname": "attendance_date",
                    "label": "Date",
                    "fieldtype": "Date",
                    "default": nowdate(),
                    "read_only": 1
                }
            ]
        })

        web_form.insert(ignore_permissions=True)
        frappe.db.commit()

        # Generate QR
        form_url = f"{get_url()}/{web_form.route}"

        qr = qrcode.make(form_url)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")

        # Save QR to Event
        file_doc = save_file(
            fname=f"{form_name}.png",
            content=buffer.getvalue(),
            dt="Event",
            dn=docname,
            is_private=0
        )

        event_doc.custom_qr_code = file_doc.file_url
        event_doc.save(ignore_permissions=True)

        return file_doc.file_url

    except Exception:
        frappe.log_error(
            title="Attendance Web Form ERROR",
            message=frappe.get_traceback()
        )
        frappe.throw("Failed to create Attendance Web Form.")


@frappe.whitelist()
def notify_admin_about_event(event_name, note=None, rejected_by=None):
    # 1. Handle defaults for your new parameters
    rejected_by = rejected_by or frappe.session.user_fullname
    note_text = f"\nNote: {note}" if note else ""
    
    # 2. Create the Notification Log (This is what triggers the 'Bell' icon)
    notification = frappe.get_doc({
        "doctype": "Notification Log",
        "subject": f"Event {event_name} was rejected by {rejected_by}.{note_text}",
        "for_user": "Administrator",
        "type": "Alert", # Use 'Alert' for the orange badge or 'Notification' for blue
        "document_type": "Event",
        "document_name": event_name,
        "email_content": f"Event Rejected: {event_name}"
    })
    
    notification.insert(ignore_permissions=True)

    # 3. IMPORTANT: Commit the record so the background worker can see it
    frappe.db.commit()

    # 4. Push to real-time (Socketio) and Email
    frappe.enqueue(
        method="frappe.desk.doctype.notification_log.notification_log.send_notification",
        queue="default",
        doc=notification
    )

    return "Notification sent"



@frappe.whitelist()
def get_facilitator_stats():
    user = frappe.session.user

    facilitator = frappe.db.get_value(
        "Facilitator",
        {"email": user},
        "name"
    )

    if not facilitator:
        return {"value": 0, "fieldtype": "Int"}

    count = frappe.db.count("Courses Attendance", {
        "facilitator": facilitator
    })

    return {
        "value": count,
        "fieldtype": "Int"
    }

@frappe.whitelist()
def get_attendee_stats():
    """Counts total attendees for the logged-in facilitator"""
    user = frappe.session.user
    # frappe.db.count runs as System by default (no permission check)
    count = frappe.db.count("Courses Attendance", {"facilitator": user})
    
    return {
        "value": count,
        "fieldtype": "Int"
    }

@frappe.whitelist()
def get_course_stats():
    # 1. Get the email of the currently logged-in user
    user_email = frappe.session.user
    
    # 2. Count records where the 'facilitator' field matches that email
    # Ensure 'facilitator' matches the actual field name in your Course Doctype
    course_count = frappe.db.count("Course", {
        "facilitator_email": user_email
    })
    
    # 3. Return the dictionary format required by the Number Card
    return {
        "value": course_count,
        "fieldtype": "Int"
    }

