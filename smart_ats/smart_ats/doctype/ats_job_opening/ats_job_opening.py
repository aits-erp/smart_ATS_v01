import frappe
from frappe.model.document import Document


class ATSJobOpening(Document):
	def validate(self):
		if not self.status:
			self.status = "Open"

		if self.open_positions is not None and self.open_positions < 0:
			frappe.throw("Open positions cannot be negative.")

