import frappe


def execute():
	if not frappe.db.exists("DocType", "ATS Candidate"):
		return

	jobs = [
		{
			"job_title": "Senior Python Developer",
			"required_skills": "Python, Frappe, ERPNext, REST API, MariaDB",
			"experience_required": "4+ years",
			"open_positions": 2,
		},
		{
			"job_title": "HR Recruiter",
			"required_skills": "Recruitment, Screening, Interviewing, HRMS, Communication",
			"experience_required": "2+ years",
			"open_positions": 1,
		},
	]

	job_names = {}
	for row in jobs:
		name = frappe.db.exists("ATS Job Opening", {"job_title": row["job_title"]})
		if not name:
			doc = frappe.get_doc({"doctype": "ATS Job Opening", "status": "Open", **row})
			doc.insert(ignore_permissions=True)
			name = doc.name
		job_names[row["job_title"]] = name

	candidates = [
		{
			"candidate_name": "Aarav Mehta",
			"email": "aarav.demo@example.com",
			"applied_job": job_names["Senior Python Developer"],
			"candidate_status": "Shortlisted",
			"skills": "Python, Frappe, ERPNext, MariaDB",
			"experience": "5 years",
			"source": "LinkedIn",
			"candidate_skills": [
				{"skill": "Python", "experience": "5 years", "rating": 5},
				{"skill": "Frappe", "experience": "3 years", "rating": 4},
				{"skill": "ERPNext", "experience": "3 years", "rating": 4},
			],
		},
		{
			"candidate_name": "Priya Nair",
			"email": "priya.demo@example.com",
			"applied_job": job_names["Senior Python Developer"],
			"candidate_status": "Screening",
			"skills": "Python, Django, PostgreSQL",
			"experience": "3 years",
			"source": "Referral",
			"candidate_skills": [
				{"skill": "Python", "experience": "3 years", "rating": 4},
				{"skill": "Django", "experience": "2 years", "rating": 4},
			],
		},
		{
			"candidate_name": "Rahul Shah",
			"email": "rahul.demo@example.com",
			"applied_job": job_names["HR Recruiter"],
			"candidate_status": "Interview",
			"skills": "Recruitment, Screening, Interviewing, Communication",
			"experience": "4 years",
			"source": "Website",
			"candidate_skills": [
				{"skill": "Recruitment", "experience": "4 years", "rating": 5},
				{"skill": "Screening", "experience": "4 years", "rating": 5},
				{"skill": "Communication", "experience": "4 years", "rating": 4},
			],
		},
	]

	for row in candidates:
		if frappe.db.exists("ATS Candidate", {"email": row["email"]}):
			continue

		doc = frappe.get_doc({"doctype": "ATS Candidate", **row})
		doc.insert(ignore_permissions=True)

