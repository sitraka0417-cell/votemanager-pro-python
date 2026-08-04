"""Modeles de donnees pour VoteManager Pro."""
from dataclasses import dataclass, field
import uuid


def new_id():
    return uuid.uuid4().hex[:8]


@dataclass
class Candidate:
    id: str = field(default_factory=new_id)
    name: str = ""
    score: int = 0

    def to_dict(self):
        return {"id": self.id, "name": self.name, "score": self.score}

    @staticmethod
    def from_dict(d):
        c = Candidate(id=d.get("id", new_id()))
        c.name = d.get("name", "")
        c.score = int(d.get("score", 0))
        return c


@dataclass
class Section:
    id: str = field(default_factory=new_id)
    title: str = ""
    threshold: int = 3
    candidates: list = field(default_factory=list)

    def total(self):
        return sum(c.score for c in self.candidates)

    def ranked(self):
        return sorted(self.candidates, key=lambda c: c.score, reverse=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "threshold": self.threshold,
            "candidates": [c.to_dict() for c in self.candidates],
        }

    @staticmethod
    def from_dict(d):
        s = Section(id=d.get("id", new_id()))
        s.title = d.get("title", "")
        s.threshold = int(d.get("threshold", 3))
        s.candidates = [Candidate.from_dict(c) for c in d.get("candidates", [])]
        return s


@dataclass
class Project:
    name: str = "Mon Projet"
    sections: list = field(default_factory=list)

    def to_dict(self):
        return {"name": self.name, "sections": [s.to_dict() for s in self.sections]}

    @staticmethod
    def from_dict(d):
        p = Project(name=d.get("name", "Mon Projet"))
        p.sections = [Section.from_dict(s) for s in d.get("sections", [])]
        return p
