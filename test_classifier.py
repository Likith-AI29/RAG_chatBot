from router.classifier import classify_query

queries = [
    "What is hostel fee?",
    "When are exams?",
    "How can I apply for admission?",
    "Which companies visit placements?"
]

for q in queries:

    result = classify_query(q)

    print(q)
    print(result)
    print("-" * 40)