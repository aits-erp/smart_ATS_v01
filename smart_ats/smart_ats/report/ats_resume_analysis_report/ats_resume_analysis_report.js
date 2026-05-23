frappe.query_reports["ATS Resume Analysis Report"] = {
	filters: [
		{
			fieldname: "applied_job",
			label: __("Applied Job"),
			fieldtype: "Link",
			options: "ATS Job Opening",
		},
		{
			fieldname: "candidate_status",
			label: __("Candidate Status"),
			fieldtype: "Select",
			options: "\nApplied\nScreening\nShortlisted\nInterview\nOffered\nHired\nRejected",
		},
		{
			fieldname: "min_score",
			label: __("Minimum ATS Score"),
			fieldtype: "Percent",
			default: 0,
		},
	],
};

