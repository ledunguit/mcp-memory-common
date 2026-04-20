from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ToolKind(str, Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    ORCHESTRATOR = "orchestrator"
    JUDGE = "judge"


class LeakSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class LeakConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class InvestigationVerdict(str, Enum):
    CONFIRMED_LEAK = "confirmed_leak"
    LIKELY_LEAK = "likely_leak"
    INCONCLUSIVE = "inconclusive"
    FALSE_POSITIVE = "false_positive"


class LeakLocation(BaseModel):
    file: str | None = None
    line: int | None = None
    column: int | None = None
    function: str | None = None
    code_snippet: str | None = None


class ArtifactRef(BaseModel):
    name: str
    path: str | None = None
    uri: str | None = None
    mime_type: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class LeakPath(BaseModel):
    kind: str
    frames: list[LeakLocation] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class LeakEvidence(BaseModel):
    tool: str
    tool_kind: ToolKind
    kind: str
    message: str
    confidence: LeakConfidence = LeakConfidence.MEDIUM
    severity: LeakSeverity = LeakSeverity.MEDIUM
    location: LeakLocation | None = None
    allocation_site: LeakLocation | None = None
    missing_free_site: LeakLocation | None = None
    call_path: LeakPath | None = None
    stack: list[LeakLocation] = Field(default_factory=list)
    artifacts: list[ArtifactRef] = Field(default_factory=list)
    raw_evidence: dict[str, Any] = Field(default_factory=dict)


class LeakCandidate(BaseModel):
    candidate_id: str
    signature: str
    summary: str
    primary_tool: str
    confidence: LeakConfidence = LeakConfidence.MEDIUM
    severity: LeakSeverity = LeakSeverity.MEDIUM
    repo_path: str | None = None
    file: str | None = None
    line: int | None = None
    function: str | None = None
    allocation_site: LeakLocation | None = None
    missing_free_site: LeakLocation | None = None
    escape_path: LeakPath | None = None
    path_constraints: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    evidence: list[LeakEvidence] = Field(default_factory=list)


class LeakSuggestion(BaseModel):
    summary: str
    rationale: str
    code_change_hint: str | None = None
    target_location: LeakLocation | None = None
    before_snippet: str | None = None
    after_snippet: str | None = None
    unified_diff: str | None = None
    before_start_line: int | None = None
    after_start_line: int | None = None


class VerdictResult(BaseModel):
    candidate_id: str
    verdict: InvestigationVerdict
    confidence: LeakConfidence = LeakConfidence.MEDIUM
    why: str
    supporting_evidence_ids: list[int] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    human_explanation: str | None = None
    fix_suggestions: list[LeakSuggestion] = Field(default_factory=list)


class LeakBundle(BaseModel):
    bundle_id: str
    repo_path: str | None = None
    candidate: LeakCandidate
    related_candidates: list[str] = Field(default_factory=list)
    orchestrator_notes: list[str] = Field(default_factory=list)
    verdict: VerdictResult | None = None
