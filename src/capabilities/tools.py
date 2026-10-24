"""
Optional project capability: Tools & External API Integration.

Implement this module only if this capability is relevant to your application's
user problem. Remove the file if the capability is not used.

Conceptual Overview:
-------------------
Tools allow the AI application to perform operations beyond text generation,
such as fetching live data from external APIs, performing calculations, or
executing internal application functions.

Key concepts when implementing tools:
1. Tool Definition: Defining function schemas (names, descriptions, parameters)
   that describe what each tool does.
2. Model Tool Calling: Providing tool schemas to the model so it can request tool execution
   when needed.
3. Execution & Response: Parsing tool call requests, executing the corresponding
   Python function or API call, and passing the results back to the model or user.

Note:
-----
Tools should be deterministic, safe, and scoped to the user problem.
"""

from src.schemas.responses import CourseObservation, LookupArgs

# Implement custom tool functions and schema definitions below if selected.

COURSE_RECORDS = {
    "SAMPLE-AI": {
        "workshop": "2026-10-15T10:00:00+03:00",
        "project": "2026-10-30T16:00:00+02:00",
    }
}


def lookup_course(course_id: str, activity: str) -> CourseObservation:
    """Read the workshop or project deadline for a fictional course record."""
    args = LookupArgs(course_id=course_id, activity=activity)
    deadline = COURSE_RECORDS.get(args.course_id, {}).get(args.activity)
    return CourseObservation(
        found=deadline is not None,
        course_id=args.course_id,
        activity=args.activity,
        deadline=deadline,
    )