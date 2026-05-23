import re

import frappe
from frappe.model.document import Document


class ATSCandidate(Document):
	def validate(self):
		self.set_ats_score()
		self.set_ai_summary()

	def set_ats_score(self):
		job_skills = self.get_job_skills()
		candidate_skills = self.get_candidate_skills()

		if not job_skills:
			self.ats_score = 0
			self.matching_skills = ""
			self.missing_skills = ""
			return

		matched = sorted(job_skills.intersection(candidate_skills))
		missing = sorted(job_skills.difference(candidate_skills))

		self.ats_score = round((len(matched) / len(job_skills)) * 100, 2)
		self.matching_skills = ", ".join(matched)
		self.missing_skills = ", ".join(missing)

	def get_job_skills(self):
		if not self.applied_job:
			return set()

		required_skills = frappe.db.get_value(
			"ATS Job Opening", self.applied_job, "required_skills"
		)
		return normalize_skills(required_skills)

	def get_candidate_skills(self):
		skills = normalize_skills(self.skills)

		for row in self.get("candidate_skills") or []:
			skills.update(normalize_skills(row.skill))

		return skills

	def set_ai_summary(self):
		score = self.ats_score or 0
		status = "strong" if score >= 75 else "moderate" if score >= 45 else "low"
		role = frappe.db.get_value("ATS Job Opening", self.applied_job, "job_title") or "the role"

		self.ai_summary = (
			f"{self.candidate_name or 'Candidate'} is a {status} match for {role} "
			f"with an ATS score of {score}%. Matching skills: "
			f"{self.matching_skills or 'none listed'}. Missing skills: "
			f"{self.missing_skills or 'none'}. Recruiter should review experience, "
			"salary expectation, notice period, and interview rating before next action."
		)


def normalize_skills(value):
	if not value:
		return set()

	parts = re.split(r"[,;\n|/]+", value)
	return {part.strip().lower() for part in parts if part.strip()}

