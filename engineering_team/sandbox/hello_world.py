from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

VOWELS: Final[frozenset[str]] = frozenset({"a", "e", "i", "o", "u"})

app = FastAPI(title="Vowel and Consonant Chatbot", version="1.0.0")


class AnalysisRequest(BaseModel):
    text: str = Field(..., description="User-provided text to analyze")

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if value is None:
            raise ValueError("text is required")
        if not value.strip():
            raise ValueError("text must not be blank")
        return value


class AnalysisResponse(BaseModel):
    text: str
    vowels: int
    consonants: int
    message: str


@dataclass(frozen=True)
class TextAnalysis:
    vowels: int
    consonants: int


def analyze_text(text: str) -> TextAnalysis:
    vowels = 0
    consonants = 0

    for char in text:
        if not char.isalpha():
            continue
        normalized = char.casefold()
        if normalized in VOWELS:
            vowels += 1
        else:
            consonants += 1

    return TextAnalysis(vowels=vowels, consonants=consonants)


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
    try:
        analysis = analyze_text(request.text)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=500, detail="Failed to analyze text") from exc

    return AnalysisResponse(
        text=request.text,
        vowels=analysis.vowels,
        consonants=analysis.consonants,
        message=(
            f"Analysis complete: vowels={analysis.vowels}, consonants={analysis.consonants}"
        ),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
