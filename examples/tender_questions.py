from licitpy import Licitpy

licitpy = Licitpy()

tender = licitpy.tenders.from_code("750301-54-L124")

questions = tender.questions

for question in questions:
    print(f"Question: {question.text}")
    print(f"Answer: {question.answer.text}")
