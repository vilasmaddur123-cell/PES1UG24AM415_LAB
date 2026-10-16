"""Course enrollment system with safer calculations and file handling."""

import hashlib
import secrets
from pathlib import Path
from typing import Any

COURSES: dict[str, dict[str, Any]] = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

TOTAL_TUITION = {"amount": 0.0}


def enroll_student(
    course_id: str,
    student_name: str,
    credits_registered: int = 3,
    audit_trail: list[str] | None = None,
) -> bool:
    """Enroll a student if the course exists and has available seats."""
    if audit_trail is None:
        audit_trail = []

    course = COURSES.get(course_id)
    if course is None or course["is_closed"] or course["seats"] <= 0:
        return False

    course["seats"] -= 1
    if course["seats"] == 0:
        course["is_closed"] = True

    TOTAL_TUITION["amount"] += course["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id: str) -> bool:
    """Reopen a course and restore one seat when the course exists."""
    course = COURSES.get(course_id)
    if course is None:
        return False

    course["seats"] += 1
    course["is_closed"] = False
    return True


def check_course_status(course_id: str) -> bool:
    """Return whether a course exists and is open for enrollment."""
    course = COURSES.get(course_id)
    return course is not None and not course["is_closed"]


def calculate_scholarship_tuition(
    course_id: str,
    discount_rate: float,
) -> float:
    """Calculate tuition after a discount rate between 0 and 1."""
    course = COURSES.get(course_id)
    if course is None:
        raise ValueError(f"Unknown course ID: {course_id}")
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0 and 1.")

    return round(course["fee"] * (1.0 - discount_rate), 2)


def generate_student_hash(roll_no: str) -> str:
    """Return a SHA-256 digest for a student identifier."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp() -> str:
    """Generate a cryptographically secure four-digit enrollment OTP."""
    return f"{secrets.randbelow(9000) + 1000:04d}"


def export_course_roster(filename: str = "course_roster.txt") -> None:
    """Write the current course catalog to a UTF-8 text file."""
    roster_path = Path(filename)
    roster_path.write_text(str(COURSES), encoding="utf-8")
    print(f"Course roster exported to: {roster_path}")


def get_open_courses_summary(
    course_catalog: dict[str, dict[str, Any]],
) -> int:
    """Count courses that are currently open."""
    return sum(
        1
        for details in course_catalog.values()
        if not details["is_closed"]
    )


def main() -> None:
    """Run a small demonstration of the course enrollment system."""
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", 0.25),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))


if __name__ == "__main__":
    main()
