from app.rag.index_document import index_document

documents = [
"docs/hr/leave_policy.md",
"docs/hr/remote_work_policy.md",
"docs/hr/working_hours_policy.md",
]

for document in documents:
    index_document(document)

