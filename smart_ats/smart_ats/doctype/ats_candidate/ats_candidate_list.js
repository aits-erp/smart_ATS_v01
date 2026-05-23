frappe.listview_settings["ATS Candidate"] = {
	add_fields: ["ats_score", "candidate_status", "applied_job"],

	get_indicator(doc) {
		if (doc.candidate_status === "Rejected") {
			return [__("Rejected"), "red", "candidate_status,=,Rejected"];
		}

		const score = flt(doc.ats_score);
		if (score >= 75) {
			return [__("High Match"), "green", "ats_score,>=,75"];
		}
		if (score >= 45) {
			return [__("Medium Match"), "orange", "ats_score,>=,45"];
		}
		return [__("Low Match"), "red", "ats_score,<,45"];
	},
};

