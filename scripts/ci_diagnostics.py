
import os
from pathlib import Path

log_file = Path("ci-error.log")

if not log_file.exists():
    print("No CI error log was supplied.")
    raise SystemExit(0)

log = log_file.read_text(encoding="utf-8", errors="replace").lower()

checks = [
    (
        ["unauthorized", "authentication required", "denied: requested access"],
        "Docker Hub authentication issue",
        "Check the Docker Hub username and repository access token stored in GitHub Actions secrets."
    ),
    (
        ["npm err!", "npm error", "could not resolve dependency"],
        "Frontend dependency installation issue",
        "Review package.json, package-lock.json and dependency compatibility."
    ),
    (
        ["no module named", "modulenotfounderror", "pip install"],
        "Backend dependency issue",
        "Check backend requirements and ensure all required Python packages are installed."
    ),
    (
        ["failed to solve", "dockerfile", "failed to calculate checksum"],
        "Docker build issue",
        "Review Dockerfile instructions, build context and COPY paths."
    ),
    (
        ["connection refused", "could not connect", "connection timed out"],
        "Service connectivity issue",
        "Check service availability, ports, networking and database health."
    )
]

matches = []

for keywords, category, recommendation in checks:
    if any(keyword in log for keyword in keywords):
        matches.append((category, recommendation))

summary_path = os.getenv("GITHUB_STEP_SUMMARY")

if summary_path:
    with open(summary_path, "a", encoding="utf-8") as summary:
        summary.write("## CI Failure Diagnostic Report\n\n")

        if matches:
            for category, recommendation in matches:
                summary.write(f"### {category}\n")
                summary.write(f"- Suggested investigation: {recommendation}\n\n")
        else:
            summary.write(
                "No known error pattern matched. "
                "Review the failed GitHub Actions step logs manually.\n"
            )

print("CI diagnostic analysis completed.")

for category, recommendation in matches:
    print(f"{category}: {recommendation}")
