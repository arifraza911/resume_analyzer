
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class CandidateDetails(BaseModel):
    name: str = "Not found"
    current_role: str = "Not found"
    experience: str = "Not found"


class SkillMatch(BaseModel):
    skill: str
    evidence: str = Field(
        description="Brief evidence from the resume"
    )


class SkillGap(BaseModel):
    skill: str
    importance: Literal["high", "medium", "low"]


class ScoreBreakdown(BaseModel):
    skills: float = Field(ge=0, le=4)
    experience: float = Field(ge=0, le=2)
    projects: float = Field(ge=0, le=2)
    education: float = Field(ge=0, le=1)
    achievements: float = Field(ge=0, le=1)

    total_score: float = Field(ge=0, le=10)

    @model_validator(mode="after")
    def calculate_total(self):
        self.total_score = round(
            self.skills
            + self.experience
            + self.projects
            + self.education
            + self.achievements,
            1,
        )
        return self


class ResumeAnalysis(BaseModel):
    candidate: CandidateDetails

    match_score: ScoreBreakdown

    matched_skills: list[SkillMatch]
    partial_matches: list[SkillMatch]
    missing_skills: list[SkillGap]

    strengths: list[str] = Field(
        description="Up to 3 relevant strengths"
    )
    improvements: list[str] = Field(
        description="Up to 3 actionable resume improvements"
    )

    recommendation: Literal[
        "Strong match",
        "Potential match",
        "Low match",
    ]

    summary: str = Field(
        description="A concise, 2-3 sentence assessment"
    )
