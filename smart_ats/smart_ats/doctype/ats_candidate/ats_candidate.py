import os
import re

import frappe
from frappe.model.document import Document

DEMO_SKILLS = {
	"communication",
	"django",
	"erpnext",
	"excel",
	"flask",
	"frappe",
	"git",
	"hrms",
	"interviewing",
	"javascript",
	"mariadb",
	"mysql",
	"node",
	"payroll",
	"postgresql",
	"python",
	"react",
	"recruitment",
	"rest api",
	"screening",
	"sql",
}


class ATSCandidate(Document):
	def validate(self):
		if self.resume_attachment and (
			self.resume_parse_status != "Parsed" or self.has_value_changed("resume_attachment")
		):
			self.parse_resume()

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
		skills.update(normalize_skills(self.parsed_skills))

		for row in self.get("candidate_skills") or []:
			skills.update(normalize_skills(row.skill))

		return skills

	def parse_resume(self):
		try:
			text = extract_resume_text(self.resume_attachment)
			self.parsed_resume_text = text[:30000]
			self.parsed_email = extract_email(text)
			self.parsed_phone = extract_phone(text)
			self.parsed_skills = ", ".join(find_skills(text))
			self.resume_parse_status = "Parsed"
			self.resume_parse_log = "Resume parsed successfully."

			if self.parsed_email and not self.email:
				self.email = self.parsed_email
			if self.parsed_phone and not self.phone:
				self.phone = self.parsed_phone
			if self.parsed_skills:
				self.skills = merge_skill_text(self.skills, self.parsed_skills)
		except Exception as exc:
			self.resume_parse_status = "Failed"
			self.resume_parse_log = frappe.scrub(str(exc)).replace("_", " ")[:250]

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


def extract_resume_text(file_url):
	path = get_file_path(file_url)
	ext = os.path.splitext(path)[1].lower()

	if ext == ".txt":
		with open(path, encoding="utf-8", errors="ignore") as resume:
			return resume.read()

	if ext == ".pdf":
		reader = get_pdf_reader(path)
		return "\n".join(page.extract_text() or "" for page in reader.pages)

	if ext in {".png", ".jpg", ".jpeg", ".webp"}:
		raise frappe.ValidationError("Image OCR not available in lightweight demo.")

	raise frappe.ValidationError("Only PDF and TXT resume parsing is available in this demo.")


def get_file_path(file_url):
	if file_url.startswith("/private/files/"):
		return frappe.get_site_path("private", "files", file_url.rsplit("/", 1)[-1])
	if file_url.startswith("/files/"):
		return frappe.get_site_path("public", "files", file_url.rsplit("/", 1)[-1])

	file_name = frappe.db.get_value("File", {"file_url": file_url}, "name")
	if not file_name:
		raise frappe.ValidationError("Attached file record was not found.")

	file_doc = frappe.get_doc("File", file_name)
	return file_doc.get_full_path()


def get_pdf_reader(path):
	try:
		from pypdf import PdfReader
	except ImportError:
		try:
			from PyPDF2 import PdfReader
		except ImportError:
			raise frappe.ValidationError("PDF parser not installed. Install pypdf for PDF parsing.")

	return PdfReader(path)


def extract_email(text):
	match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text or "")
	return match.group(0) if match else ""


def extract_phone(text):
	match = re.search(r"(?:\+?\d[\s-]?){10,15}", text or "")
	return match.group(0).strip() if match else ""


def find_skills(text):
	normalized = (text or "").lower()
	return sorted(skill for skill in DEMO_SKILLS if re.search(rf"\b{re.escape(skill)}\b", normalized))


def merge_skill_text(existing, parsed):
	skills = normalize_skills(existing)
	skills.update(normalize_skills(parsed))
	return ", ".join(sorted(skills))


@frappe.whitelist()
def parse_resume_now(candidate_name):
	doc = frappe.get_doc("ATS Candidate", candidate_name)
	if not doc.resume_attachment:
		frappe.throw("Attach a resume first.")

	doc.parse_resume()
	doc.set_ats_score()
	doc.set_ai_summary()
	doc.save(ignore_permissions=True)
	return {"status": doc.resume_parse_status, "log": doc.resume_parse_log}
