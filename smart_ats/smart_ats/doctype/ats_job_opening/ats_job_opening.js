frappe.ui.form.on("ATS Job Opening", {
	refresh(frm) {
		const status = frm.doc.status || "Open";
		const color = {
			Open: "green",
			"On Hold": "orange",
			Closed: "red",
		}[status] || "blue";

		frm.dashboard.clear_headline();
		frm.dashboard.add_indicator(__(status), color);

		if (frm.doc.open_positions) {
			frm.dashboard.add_indicator(
				__("{0} Open Position(s)", [frm.doc.open_positions]),
				"blue"
			);
		}
	},
});

