

# facilitator/facilitator/dashboard_chart_source/my_course_status/my_course_status.py
import frappe

# facilitator/facilitator/dashboard_chart_source/my_course_status/my_course_status.py
import frappe

@frappe.whitelist()
def get_data(chart_name=None, filters=None):
    user = frappe.session.user
    
    # Define the statuses you want to track
    statuses = ["Postponed", "Canceled", "Confirmed", "Tentative", "Completed"]
    
    # Initialize a dictionary with 0 for every status
    stats_map = {status: 0 for status in statuses}
    
    # Query the database
    data = frappe.db.get_all("Course",
        filters={"facilitator_email": user},
        fields=["course_status", "count(name) as count"],
        group_by="course_status"
    )

    # Fill the map with actual data from the query
    for d in data:
        if d.course_status in stats_map:
            stats_map[d.course_status] = d.count

    return {
        "labels": statuses,
        "datasets": [
            {
                "name": "Courses",
                "values": [stats_map[s] for s in statuses]
            }
        ]
    }
    user = frappe.session.user
    
    # 1. Define your statuses and their specific colors
    status_map = {
        "Confirmed": "#28a745",  # Green
        "Tentative": "#ffc107",  # Yellow
        "Postponed": "#fd7e14",  # Orange
        "Canceled": "#dc3545"    # Red
    }
    
    # 2. Fetch the actual counts from the database
    counts = frappe.db.sql("""
        SELECT course_status, COUNT(name) as count
        FROM `tabCourse`
        WHERE facilitator_email = %s
        GROUP BY course_status
    """, (user,), as_dict=True)
    
    # Create a lookup for the results
    results = {row.course_status: row.count for row in counts}
    
    # 3. Build the labels, values, and colors in a fixed order
    labels = []
    values = []
    colors = []
    
    for status, color in status_map.items():
        labels.append(status)
        values.append(results.get(status, 0)) # Default to 0 if status doesn't exist yet
        colors.append(color)

    return {
        "labels": labels,
        "datasets": [
            {
                "name": "Courses",
                "values": values
            }
        ],
        "colors": colors
    }
    # This captures the email of the person currently viewing the dashboard
    user = frappe.session.user
    
    # We query the Course doctype for statuses belonging only to this user
    data = frappe.db.get_all("Course",
        filters={"facilitator_email": user},
        fields=["course_status", "count(name) as count"],
        group_by="course_status"
    )

    if not data:
        return {
            "labels": [],
            "datasets": [{"values": []}]
        }

    return {
        "labels": [d.course_status or "No Status" for d in data],
        "datasets": [
            {
                "name": "Courses",
                "values": [d.count for d in data]
            }
        ]
    }