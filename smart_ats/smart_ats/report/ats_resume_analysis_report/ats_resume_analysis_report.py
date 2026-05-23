import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})
	conditions = []
	values = {}

	if filters.applied_job:
		conditions.append("applied_job = %(applied_job)s")
		values["applied_job"] = filters.applied_job

	if filters.candidate_status:
		conditions.append("candidate_status = %(candidate_status)s")
		values["candidate_status"] = filters.candidate_status

	if filters.min_score:
		conditions.append("ats_score >= %(min_score)s")
		values["min_score"] = filters.min_score

	where = "where " + " and ".join(conditions) if conditions else ""

	data = frappe.db.sql(
		f"""
		select
			name as candidate,
			candidate_name,
			applied_job,
			candidate_status,
			ats_score,
			parsed_skills,
			matching_skills,
			missing_skills,
			source,
			resume_parse_status
		from `tabATS Candidate`
		{where}
		order by ats_score desc, modified desc
		""",
		values,
		as_dict=True,
	)

	return get_columns(), data


def get_columns():
	return [
		{"label": "Candidate", "fieldname": "candidate", "fieldtype": "Link", "options": "ATS Candidate", "width": 140},
		{"label": "Name", "fieldname": "candidate_name", "fieldtype": "Data", "width": 170},
		{"label": "Applied Job", "fieldname": "applied_job", "fieldtype": "Link", "options": "ATS Job Opening", "width": 180},
		{"label": "Status", "fieldname": "candidate_status", "fieldtype": "Data", "width": 110},
		{"label": "ATS Score", "fieldname": "ats_score", "fieldtype": "Percent", "width": 100},
		{"label": "Parsed Skills", "fieldname": "parsed_skills", "fieldtype": "Small Text", "width": 220},
		{"label": "Matching Skills", "fieldname": "matching_skills", "fieldtype": "Small Text", "width": 220},
		{"label": "Missing Skills", "fieldname": "missing_skills", "fieldtype": "Small Text", "width": 220},
		{"label": "Source", "fieldname": "source", "fieldtype": "Data", "width": 100},
		{"label": "Parse Status", "fieldname": "resume_parse_status", "fieldtype": "Data", "width": 120},
	]

