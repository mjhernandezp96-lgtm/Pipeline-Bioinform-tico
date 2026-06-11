class Protein:
    def __init__(self, uniprot_id: str):
        self._uniprot_id = uniprot_id
        self._sequence: str = ""
        self._description: str = ""
        self._pfam_family: str = ""
        self._pfam_accession: str = ""
        self._score: float = 0.0
        self._evalue: float = 0.0

    # --- Getters ---
    @property
    def uniprot_id(self) -> str:
        return self._uniprot_id

    @property
    def sequence(self) -> str:
        return self._sequence

    @property
    def description(self) -> str:
        return self._description

    @property
    def pfam_family(self) -> str:
        return self._pfam_family

    @property
    def pfam_accession(self) -> str:
        return self._pfam_accession

    @property
    def score(self) -> float:
        return self._score

    @property
    def evalue(self) -> float:
        return self._evalue

    # --- Setters ---
    @uniprot_id.setter
    def uniprot_id(self, value: str):
        self._uniprot_id = value

    @sequence.setter
    def sequence(self, value: str):
        self._sequence = value

    @description.setter
    def description(self, value: str):
        self._description = value

    @pfam_family.setter
    def pfam_family(self, value: str):
        self._pfam_family = value

    @pfam_accession.setter
    def pfam_accession(self, value: str):
        self._pfam_accession = value

    @score.setter
    def score(self, value: float):
        self._score = value

    @evalue.setter
    def evalue(self, value: float):
        self._evalue = value

    # --- Methods ---
    def set_family(self, family: str):
        self._pfam_family = family

    def to_dict(self) -> dict:
        return {
            "uniprot_id": self._uniprot_id,
            "description": self._description[:120] if self._description else "",
            "sequence_length": len(self._sequence),
            "pfam_family": self._pfam_family if self._pfam_family else "No hit",
            "pfam_accession": self._pfam_accession,
            "score": self._score,
            "evalue": self._evalue,
        }

    def __str__(self) -> str:
        return (
            f"Protein(uniprot_id='{self._uniprot_id}', "
            f"pfam_family='{self._pfam_family}', "
            f"score={self._score:.2f})"
        )


class PfamResult:
    def __init__(self, family: str, accession: str, score: float, evalue: float):
        self._family = family
        self._accession = accession
        self._score = score
        self._evalue = evalue

    @property
    def family(self) -> str:
        return self._family

    @property
    def accession(self) -> str:
        return self._accession

    @property
    def score(self) -> float:
        return self._score

    @property
    def evalue(self) -> float:
        return self._evalue

    def __str__(self) -> str:
        return (
            f"PfamResult(family='{self._family}', "
            f"accession='{self._accession}', "
            f"score={self._score:.2f}, "
            f"evalue={self._evalue:.2e})"
        )
