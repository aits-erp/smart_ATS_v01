frappe.ui.form.on("ATS Candidate", {
	refresh(frm) {
		const score = flt(frm.doc.ats_score);
		const status = frm.doc.candidate_status || "Applied";
		const color = status === "Rejected" ? "red" : score >= 75 ? "green" : score >= 45 ? "orange" : "red";

		frm.dashboard.clear_headline();
		frm.dashboard.add_indicator(__(status), color);
		frm.dashboard.add_indicator(__("ATS Score: {0}%", [score]), color);
	},
});

