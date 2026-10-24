from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    """Minimal schema for validating incoming user input."""

    message: str = Field(..., description="The user's prompt or message.")


class AIResponse(BaseModel):
    """Minimal schema for structured response output from the AI service layer."""

    content: str = Field(..., description="The generated response text or user-friendly error message.")
    success: bool = Field(True, description="Flag indicating if the operation succeeded.")
    error_message: str | None = Field(None, description="Detailed error description if success is False.")


class LookupArgs(BaseModel):
    """Validated arguments for the lookup_course tool."""

    model_config = ConfigDict(strict=True, extra="forbid")
    course_id: str = Field(min_length=2, max_length=20)
    activity: Literal["workshop", "project"]


class CourseObservation(BaseModel):
    """Result returned by the lookup_course tool."""

    model_config = ConfigDict(strict=True, extra="forbid")
    found: bool
    course_id: str
    activity: Literal["workshop", "project"]
    deadline: str | None = None


class SupportReply(BaseModel):
    """Structured final answer produced by the model."""

    model_config = ConfigDict(strict=True, extra="forbid", str_strip_whitespace=True)
    answer: str = Field(min_length=1, max_length=600)
    category: Literal["course", "account", "other"]
    needs_human: bool