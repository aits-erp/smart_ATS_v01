frappe.ui.form.on("ATS Candidate", {
	refresh(frm) {
		const score = flt(frm.doc.ats_score);
		const status = frm.doc.candidate_status || "Applied";
		const color = status === "Rejected" ? "red" : score >= 75 ? "green" : score >= 45 ? "orange" : "red";

		frm.dashboard.clear_headline();
		frm.dashboard.add_indicator(__(status), color);
		frm.dashboard.add_indicator(__("ATS Score: {0}%", [score]), color);

		if (!frm.is_new() && frm.doc.resume_attachment) {
			frm.add_custom_button(__("Parse Resume"), () => {
				frappe.call({
					method: "smart_ats.smart_ats.doctype.ats_candidate.ats_candidate.parse_resume_now",
					args: { candidate_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Parsing resume..."),
					callback(r) {
						frappe.msgprint(r.message?.log || __("Resume parsed."));
						frm.reload_doc();
					},
				});
			});
		}
	},
});
