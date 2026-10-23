
# terminology.py

# Initial demonstration mappings for the prototype.
# These are illustrative examples, not clinically validated equivalences.
# Replace or verify them against reliable medical terminology sources.

TERMINOLOGY_DATA = [
    {
        "concept": "diabetes",
        "terms": {
            "allopathy": [
                "Diabetes mellitus"
            ],
            "ayurveda": [
                "Madhumeha"
            ],
            "homeopathy": []
        },
        "relationship": "needs_verification",
        "source": None
    }
]


def find_equivalent_terms(source_system, source_term):
    search_term = source_term.strip().casefold()
    results = []

    for entry in TERMINOLOGY_DATA:
        terms = entry["terms"]

        source_terms = terms.get(source_system, [])

        all_terms = [
            term.casefold()
            for system_terms in terms.values()
            for term in system_terms
        ]

        if search_term == entry["concept"].casefold() or any(
            search_term == term.casefold()
            for term in source_terms
        ):
            matches = {}

            for system, system_terms in terms.items():
                if system != source_system:
                    matches[system] = system_terms

            results.append({
                "concept": entry["concept"],
                "matches": matches,
                "relationship": entry["relationship"],
                "source": entry["source"]
            })

    return results
