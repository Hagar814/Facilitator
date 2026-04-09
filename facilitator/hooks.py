# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "facilitator"
app_title = "Facilitator"
app_publisher = "Facilitators"
app_description = "facilitator"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "maheshwaribhavesh95863@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/facilitator/css/facilitator.css"
#app_include_js = "/assets/facilitator/js/facilitator.js"

# include js, css files in header of web template
# web_include_css = "/assets/facilitator/css/facilitator.css"
# web_include_js = "/assets/facilitator/js/facilitator.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}
app_include_js = [
    "/assets/facilitator/custom/js/chart_sources.js"
]
#app_include_css = "/assets/facilitator/custom/css/facilitator.css"
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_list_js = {
    "Course": "custom/js/course_list.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {    "Course": "custom/js/course_calender.js"
}
calendars = ["Facilitator Calendar"]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "facilitator.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "facilitator.install.before_install"
# after_install = "facilitator.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "facilitator.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "Delivery Note": {
        # "validate": "e_invoice.custom.python.sales_invoice.validate_invoice",
        # "before_save": "e_invoice.custom.python.sales_invoice.before_save",
        # "onload": "facilitator.custom.python.delivery_note.make_event"
    },
    "Event": {
         "after_insert": "facilitator.custom.python.event.create_course_from_event"
        # "validate": "facilitator.custom.python.event.update_course_status",
        # "before_save": "e_invoice.custom.python.sales_invoice.before_save",
        # "onload": "facilitator.custom.python.delivery_note.make_event"
    },
    
}
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            ["name", "in", [
                "Delivery Note Item-language",
                "Sales Order Item-language",
                "Event-merucri_account_manager",
                "Event-leadership_account_manager",
                "Event-mercuri_client_relations",
                "Event-leadership_client_relations",
                "Delivery Note-merucri_account_manager",
                "Delivery Note-mercuri_client_relations",
                "Delivery Note-leadership_account_manager",
                "Delivery Note-leadership_client_relations",
                "Customer-merucri_account_manager",
                "Customer-mercuri_client_relations",
                "Salary Structure Assignment-mercuri_compensation_shared_services",
                "Facilitator Table-cost_center",
                "Salary Slip-calculated_tax",
                "Salary Slip-gross_salary_x",
                "Salary Structure Assignment-mercuri_incentive",
                "Salary Structure Assignment-board_incentive",
                "Salary Structure Assignment-normal_incentive",
                "Company Deviation-purchase_order",
                "Company Deviation-purchase_request",
                "Company Deviation-delivery_note",
                "Technical Deviation-column_break_ywp3l",
                "Technical Deviation-column_break_gpfkk",
                "Technical Deviation-dayes_before_delivery",
                "Purchase Receipt Item-business_unit",
                "Technical Deviation-time_",
                "Technical Deviation-column_break_bymdg",
                "Technical Deviation-column_break_dielv",
                "Technical Deviation-time",
                "Technical Deviation-delivered_to_planning",
                "Technical Deviation-technical_deviation_comment",
                "Delivery Note Item-number_of_days_",
                "Sales Order Item-number_of_days_",
                "Quotation Item-probability_value_per_item",
                "Technical Deviation-planningleadtime",
                "Technical Deviation-catigory",
                "Salary Structure Assignment-income_tax",
                "Quotation-probability__value",
                "Opportunity-probability_value_",
                "Lead-probability_value",
                "Quotation-stage_",
                "Quotation-probability",
                "Salary Structure Assignment-gross_salary",
                "Salary Structure Assignment-gross_income",
                "Salary Structure Assignment-صندوق_الشهداء",
                "Salary Structure Assignment-social_employee_share",
                "Salary Structure Assignment-personal_exemption",
                "Salary Structure Assignment-ksa_managment",
                "Salary Structure Assignment-mercuri",
                "Salary Structure Assignment-representation_allowance",
                "Salary Structure Assignment-car_allowance",
                "Salary Structure Assignment-mobile_allowance",
                "Salary Structure Assignment-insured_salary",
                "Lead-currency",
                "Lead-column_break",
                "Lead-lead_amount",
                "Lead-amount",
                "Technical Deviation-subsidiary",
                "Technical Deviation-planning_deviation",
                "Technical Deviation-column_break_27cug",
                "Technical Deviation-column_break_g1wbq",
                "Technical Deviation-column_break_uwgp9",
                "Technical Deviation-creation_date",
                "Technical Deviation-s_a_lead_time_",
                "Technical Deviation-ass_lead_time_",
                "Technical Deviation-ass_deviation_",
                "Technical Deviation-sadeviation_",
                "Technical Deviation-assembly_duration_",
                "Technical Deviation-sa_duration_",
                "Technical Deviation-ass_deviation",
                "Technical Deviation-sa_duration",
                "Technical Deviation-column_break_szffe",
                "Technical Deviation-section_break_y4lmh",
                "Technical Deviation-comments",
                "Technical Deviation-section_break_vd0hn",
                "Technical Deviation-column_break_mscee",
                "Technical Deviation-column_break_o9c9q",
                "Technical Deviation-column_break_pqy9e",
                "Technical Deviation-column_break_tcpry",
                "Technical Deviation-column_break_8q0gj",
                "Technical Deviation-column_break_cbtht",
                "Technical Deviation-column_break_rhjd0",
                "Technical Deviation-column_break_ripvh",
                "Technical Deviation-column_break_6xtu6",
                "Technical Deviation-section_break_cqvbn",
                "Technical Deviation-column_break_zaelf",
                "Technical Deviation-course_name",
                "Technical Deviation-column_break_djujp",
                "Technical Deviation-delivered_to__planning",
                "Technical Deviation-ass__accountability",
                "Technical Deviation-lead_time",
                "Technical Deviation-received_on",
                "Technical Deviation-accountability",
                "Technical Deviation-column_break_awrfq",
                "Technical Deviation-section_break_uxg7j",
                "Technical Deviation-program_type",
                "Technical Deviation-client_name",
                "Technical Deviation-starts_on",
                "Technical Deviation-ends_on",
                "Technical Deviation-s_a_lead_time",
                "Technical Deviation-event",
                "Technical Deviation-sadeviation",
                "Technical Deviation-assembly_duration",
                "Technical Deviation-solution_assembler_stage",
                "Deviation-solution_architect_deviation",
                "Deviation-section_break_tikte",
                "Deviation-column_break_c6pho",
                "Deviation-column_break_v16ts",
                "Deviation-column_break_grszx",
                "Deviation-solution_assembler_stage",
                "Deviation-section_break_cviwv",
                "Deviation-s_a_lead_time",
                "Deviation-facilitator",
                "Deviation-client_name",
                "Deviation-program_type",
                "Opportunity-probability_",
                "Deviation-column_break_ye3bs",
                "Deviation-sa_duration",
                "Deviation-assembly_duration",
                "Deviation-sadeviation",
                "Deviation-ends_on",
                "Deviation-starts_on",
                "Deviation-event",
                "Deviation-testsss",
                "Event So Item-number_of_days",
                "Event-client_relation_user",
                "Delivery Note-client_relation_user",
                "Event So Item-audience_level",
                "Event-attachments_",
                "Event-proposal_program_and_participants_information_attachments",
                "Event-section_break_mjuz1",
                "Delivery Note-attachments_",
                "Delivery Note-proposal_program_and_participants_information_attachments",
                "Delivery Note-section_break_nfg5m",
                "Event-audience_level",
                "Purchase Order Item-payment_currency",
                "Material Request Item-payment_currency",
                "Material Request-currencies",
                "Purchase Order-comment_section_",
                "Facilitator Table-rate_percentage",
                "Sales Order Item-audience_level",
                "Opportunity-project",
                "Customer-status_",
                "Customer-client_relation_user",
                "Facilitator Table-duration_",
                "Facilitator Table-column_break_acmqg",
                "Facilitator-rate",
                "Sales Order Item-royalty_to",
                "Sales Order Item-direct_indirect",
                "Purchase Receipt-user_remark_",
                "Purchase Receipt-comment_section_",
                "Material Request Item-column_break_jrfwi",
                "Purchase Order-user_remark",
                "Purchase Order-column_break_nluvi",
                "Purchase Order-section_break_npm14",
                "Material Request-user_remark_",
                "Material Request-column_break_esxjw",
                "Material Request-comment_section_",
                "Material Request-section_break_nukvd",
                "Opportunity-custom_stage",
                "Sales Order-attachments_",
                "Sales Order-proposal_program_and_participants_information_attachments",
                "Quotation-attachment",
                "Quotation-attachments",
                "Opportunity-attachment",
                "Opportunity-attachments",
                "Lead-attachment",
                "Lead-attachments_",
                "Quotation Item-project",
                "Sales Invoice-table",
                "Lead-project",
                "Sales Invoice-e_invoice_item",
                "Sales Invoice-section_break_5uxl1",
                "Lead-lost_reason",
                "Lead-custom_status",
                "Lead-reason",
                "Lead-stage",
                "Quotation Item-column_break_12m8e",
                "Quotation Item-cost_center",
                "Quotation Item-accounting_dimensions",
                "Quotation Item-number_of_days",
                "Quotation Item-commission_status",
                "Quotation Item-column_break_cxg6p",
                "Quotation Item-program_type",
                "Quotation Item-section_break_o5izc",
                "Quotation-program_type",
                "Quotation-delivery_date",
                "Event-finance_deviation",
                "Event So Item-royalty_to",
                "Event So Item-direct_indirect",
                "Delivery Note Item-royalty_to",
                "Delivery Note Item-direct_indirect",
                "Leave Application-workflow_state",
                "Employee-direct_manager_",
                "Employee-user_number",
                "Employee-social_insurance_number",
                "Sales Invoice-swift_code",
                "Bank Account-swift_code",
                "Event-notes_to_finance",
                "Event-notes_to_planning",
                "Event-column_break_mfnve",
                "Event-notes_to_technical",
                "Event-notes_to_client_relations",
                "Event-notes_section_",
                "Event-notes",
                "Delivery Note-notes_to_finance",
                "Delivery Note-notes_to_planning",
                "Delivery Note-column_break_uqms3",
                "Delivery Note-notes_to_technical",
                "Delivery Note-notes_to_client_relations",
                "Delivery Note-notes_section",
                "Delivery Note-notes",
                "Sales Order-notes_to_finance",
                "Sales Order-notes_to_planning",
                "Sales Order-column_break_ombtx",
                "Sales Order-notes_to_technical",
                "Sales Order-notes_to_client_relations",
                "Sales Order-comment_section_",
                "Sales Order-comments_info",
                "Event-pos_or_loa",
                "Event-course_address",
                "Stock Entry Detail-column_break_sl1sz",
                "Stock Entry Detail-customer",
                "Stock Entry Detail-course_name",
                "Stock Entry Detail-facilitator",
                "Event-commercial_deviations_comments",
                "Event-client_relations_comments",
                "Purchase Receipt-workflow_state",
                "Material Request Item-total_",
                "Material Request Item-budget_price_",
                "Delivery Note-address",
                "Sales Invoice-invoiced_name",
                "Sales Order Item-stage",
                "Delivery Note Item-stage",
                "Delivery Note Item-sales_stage",
                "Event-participants_info",
                "Event-comments_info",
                "Event-facilitators_info",
                "Delivery Note-section_break_xlqja",
                "Delivery Note-section_break_sgmoo",
                "Delivery Note-commercial_comment",
                "Delivery Note-section_break_nej1o",
                "Delivery Note-section_break_wwrkr",
                "Sales Order-section_break_frvx6",
                "Sales Order-section_break_rbhj9",
                "Material Request Item-course_name",
                "Material Request Item-customername",
                "Material Request Item-category_",
                "Sales Invoice Item-tax_amount",
                "Sales Invoice Item-discount_after",
                "Sales Invoice Item-tax_rate",
                "Sales Invoice Item-type",
                "Sales Invoice Item-total_amount",
                "Sales Invoice Item-discount_before",
                "Sales Invoice-e_invoice_process_status",
                "Sales Invoice-is_valid",
                "Sales Invoice-submission_id",
                "Sales Invoice-column_break_33",
                "Sales Invoice-cduuid",
                "Sales Invoice-uuid",
                "Sales Invoice-e_invoice",
                "Sales Invoice Item-tax_uom",
                "Sales Invoice-tn_id",
                "Customer-e_invoice_info_1",
                "Customer-country_code",
                "Customer-country",
                "Customer-region_city",
                "Item-code",
                "Sales Invoice-customer_types",
                "Customer-building_number",
                "Sales Invoice Item-item_type",
                "Customer-street",
                "Sales Invoice Item-code",
                "Customer-customer_types",
                "Item-item_type",
                "Customer-e_invoice_info",
                "Item Tax Template-tax_rate",
                "Item Tax Template-type",
                "Delivery Note-column_break_nwyr2",
                "Delivery Note-course_info",
                "Web Form-currency",
                "Web Form-amount",
                "Web Form-amount_field",
                "Web Form-amount_based_on_field",
                "Web Form-payments_cb",
                "Web Form-payment_button_help",
                "Web Form-payment_button_label",
                "Web Form-payment_gateway",
                "Web Form-accept_payment",
                "Web Form-payments_tab",
                "Loan Repayment-payroll_payable_account",
                "Loan Repayment-repay_from_salary",
                "Loan-repay_from_salary",
                "Terms and Conditions-hr",
                "Timesheet-salary_slip",
                "Task-total_expense_claim",
                "Project-total_expense_claim",
                "Designation-skills",
                "Designation-required_skills_section",
                "Designation-appraisal_template",
                "Department-expense_approvers",
                "Department-leave_approvers",
                "Department-shift_request_approver",
                "Department-approvers",
                "Department-leave_block_list",
                "Department-column_break_9",
                "Department-payroll_cost_center",
                "Department-section_break_4",
                "Company-default_payroll_payable_account",
                "Company-column_break_10",
                "Company-default_employee_advance_account",
                "Company-default_expense_claim_payable_account",
                "Company-hr_settings_section",
                "Employee-payroll_cost_center",
                "Employee-salary_cb",
                "Employee-shift_request_approver",
                "Employee-column_break_45",
                "Employee-leave_approver",
                "Employee-expense_approver",
                "Employee-approvers_section",
                "Employee-health_insurance_no",
                "Employee-health_insurance_provider",
                "Employee-health_insurance_section",
                "Employee-default_shift",
                "Employee-grade",
                "Employee-job_applicant",
                "Employee-employment_type",
                "Event-product_line",
                "Sales Order-program_type",
                "Event-evaluation_form_",
                "Event-column_break_36",
                "Event-references_",
                "Event-program",
                "Event-comments",
                "Event-comment_section",
                "Event-column_break_77",
                "Sales Order-comments",
                "Event So Item-column_break_3",
                "Event So Item-program_type",
                "Delivery Note Item-program_type",
                "Sales Order Item-column_break_13",
                "Sales Order Item-program_type",
                "Event-technical_deviation_comment",
                "Event-supply_chain_deviation_comment",
                "Sales Invoice-c_r_submission_id",
                "Event So Item-project",
                "Event-section_break_32",
                "Event-column_break_21",
                "Sales Order Item-project",
                "Sales Order Item-column_break_92",
                "Sales Order Item-cost_center",
                "Sales Order Item-accounting_dimensions",
                "Sales Invoice-vendor_number",
                "Sales Invoice-customer_data",
                "Sales Invoice-column_break_9",
                "Sales Invoice-column_break_16",
                "Sales Invoice-invoice_data",
                "Sales Invoice-country_code",
                "Sales Invoice-country",
                "Item Tax Template-subtype",
                "Item Tax Template-column_break_4",
                "Item Tax Template-rate",
                "Item-tax_uom",
                "Sales Invoice-cr_number",
                "Customer-cr_number",
                "Customer-city",
                "Delivery Note-delivered_on_",
                "Sales Invoice-gr_number",
                "Event-section_break_15",
                "Delivery Note-comment",
                "Delivery Note-section_break_52",
                "Sales Order-comments_section",
                "Sales Invoice-p_terms",
                "Sales Invoice-swift_number",
                "Sales Invoice-iban",
                "Sales Invoice-bank",
                "Sales Invoice-bank_account_no",
                "Sales Invoice-bank_account",
                "Event-course_type",
                "Event-facilitator",
                "Print Settings-print_uom_after_quantity",
                "Sales Invoice-e_invoice_item_wise_tax_details",
                "Sales Invoice-custom_tax_listing",
                "Sales Invoice-update_tax",
                "Sales Invoice-tax_template",
                "Sales Invoice-tax_item",
                "Sales Invoice-section_break",
                "Delivery Note-no_of_virtual_sessions",
                "Delivery Note-course_type",
                "Event-planning_comment",
                "Sales Invoice-total_item_discount",
                "Sales Invoice-total_amount",
                "Sales Invoice-total_discount",
                "Sales Invoice Item-subtype",
                "Sales Invoice-region_city",
                "Sales Invoice-building_number",
                "Sales Invoice-street",
                "Facilitator Table-cohost_status",
                "Facilitator Table-cohost_rate_percentage",
                "Facilitator Table-cohost_rate_category",
                "Facilitator Table-cohost_rate",
                "Facilitator Table-cohost",
                "Address-is_your_company_address",
                "Sales Order Item-net_value",
                "Sales Order Item-commission_status",
                "Sales Order Item-requested_by_client",
                "Sales Order Item-number_of_days",
                "Sales Order Item-sales_stage",
                "Sales Team-email",
                "Sales Person-emp_name",
                "Sales Person-email",
                "Delivery Note Item-requested_by_client",
                "Delivery Note-so_reference",
                "Delivery Note Item-commission_status",
                "Contact-is_billing_contact",
                "Delivery Note-event",
                "Event-delivery_note",
                "Delivery Note-workflow_state",
                "Event-language_1",
                "Delivery Note-course_address",
                "Delivery Note-facilitator_category",
                "Delivery Note-no_of_facilitators",
                "Delivery Note-language_1",
                "Delivery Note-comments",
                "Delivery Note-commission_status",
                "Delivery Note-royalty_to",
                "Delivery Note-direct_indirect_",
                "Delivery Note-subsidiary",
                "Delivery Note-section_break_106",
                "Delivery Note-facilitator",
                "Event-section_break_56",
                "Delivery Note-city",
                "Delivery Note-country",
                "Delivery Note-no_of_participants",
                "Delivery Note-number_of_days",
                "Delivery Note-requested_by_client",
                "Delivery Note-ends_on",
                "Delivery Note-starts_on",
                "Delivery Note-program_type",
                "Delivery Note-program_commercial_name",
                "Delivery Note-yes_or_no",
                "Delivery Note-po_number",
                "Delivery Note-pos_or_loa",
                "Delivery Note-course_status",
                "Delivery Note-course_name",
                "Delivery Note-course_family",
                "Event So Item-delivery_date",
                "Facilitator Table-add_other",
                "Facilitator Table-rate_category",
                "Event-number_of_days",
                "Event-yes_or_no",
                "Event-no_of_participants",
                "Event-so_reference",
                "Sales Order-workflow_state",
                "Event-program_account_manger",
                "Event-account_managers",
                "Delivery Note Item-delivery_date",
                "Delivery Note Item-number_of_days",
                "Sales Order Item-section_break_17",
                "Event-po_number",
                "Event-primary_address",
                "Event-title",
                "Customer-title",
                "Event-client_primary_contact",
                "Event-requested_by_client",
                "Event-facilitator_category",
                "Event-no_of_facilitators",
                "Event-program_commercial_name",
                "Event-program_type",
                "Event-workflow_state",
                "Event-email",
                "Event-mobile",
                "Event-column_break_43",
                "Deleted Document-gcalendar_sync_id",
                "Sales Invoice-comment",
                "Address-tax_category",
                "Quotation-direct_manager",
                "Designation-department",
                "Deleted Document-github_sync_id",
                "Task-github_sync_id",
                "Project-github_sync_id",
                "Sales Order Item-stages",
                "Quotation Item-delivery_date",
                "Quotation-pc_name",
                "Opportunity-pc_name",
                "Event-royalty_to",
                "Event-direct_indirect_",
                "Event-subsidiary",
                "Quotation Item-stage",
                "Quotation Item-planned",
                "Quotation Item-net",
                "Facilitator Table-rate",
                "Event-course_status",
                "Event-kanban_column",
                "Event-city",
                "Event-country",
                "Event-customer_information",
                "Event-facilitators_information",
                "Event-course_information",
                "Deleted Document-hub_sync_id",
                "Lead-hub_sync_id",
                "Item-hub_sync_id",
                "Company-hub_sync_id",
                "Print Settings-print_taxes_with_zero_amount",
                "Event-client",
                "Purchase Order Item-project_update",
                "Event-course_name",
                "Print Settings-compact_item_print",
                "Event-course_family"
            ]]
        ]
    }
]

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# }
# }

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "facilitator.custom.python.event.update_course_status",
        "facilitator.custom.python.event.update_facilitator_status"
    ],
    "cron": {
        "* 2 * * *": [
            # "facilitator.custom.python.event.update_course_status"
        ]

    }
}
# scheduler_events = {
# 	"all": [
# 		"facilitator.tasks.all"
# 	],
# 	"daily": [
# 		"facilitator.tasks.daily"
# 	],
# 	"hourly": [
# 		"facilitator.tasks.hourly"
# 	],
# 	"weekly": [
# 		"facilitator.tasks.weekly"
# 	]
# 	"monthly": [
# 		"facilitator.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "facilitator.install.before_tests"
# fixtures = ['Report', 'Role Profile', 'Role', 'Custom Field', 'Custom Script', 'Property Setter', 'Workflow', 'Workflow State', 'Workflow Action']
# fixtures = [{
# 	"doctype": "Event",
# 	# "filters": {
# 	# 	"name": ["in", "E-invoice"]
# 	# }
# 	},
# 	{
# 	"doctype": "Sales Order",
# 	# "filters": {
# 	# 	"role": ["in", "E-invoice"]
# 	# }
# 	}

# 	]
# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "facilitator.event.get_events"
# }
doctype_js = {"Delivery Note": "custom/js/delivery_note.js",
              "Sales Order": "custom/js/sales_order.js",
              "Course" : "custom/js/course.js"}
