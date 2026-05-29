import re

# ====================================
# QUERY CATEGORIES
# ====================================

QUERY_CATEGORIES = {
    "finance": [
        "fee",
        "fees",
        "payment",
        "scholarship",
        "refund",
        "tuition"
    ],

    "academics": [
        "exam",
        "syllabus",
        "semester",
        "result",
        "marks",
        "attendance",
        "assignment"
    ],

    "hostel": [
        "hostel",
        "room",
        "mess",
        "canteen",
        "accommodation"
    ],

    "admissions": [
        "admission",
        "apply",
        "eligibility",
        "documents",
        "registration"
    ],

    "placements": [
        "placement",
        "internship",
        "company",
        "recruitment",
        "job"
    ]
}

# ====================================
# CLASSIFIER
# ====================================

def classify_query(question: str):

    question = question.lower()

    scores = {}

    # Count keyword matches
    for category, keywords in QUERY_CATEGORIES.items():

        score = 0

        for keyword in keywords:

            if re.search(rf"\b{keyword}\b", question):

                score += 1

        scores[category] = score

    # Best category
    best_category = max(scores, key=scores.get)

    # No matches fallback
    if scores[best_category] == 0:

        return {
            "category": "general",
            "confidence": 0.0
        }

    confidence = scores[best_category] / max(
        1,
        sum(scores.values())
    )

    return {
        "category": best_category,
        "confidence": round(confidence, 2)
    }