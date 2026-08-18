from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


documents_db = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_document",
    description="Read a document",
)
def read_document(
    document_id: str = Field(description="The ID of the document to read"),
) -> str:
    if document_id not in documents_db:
        raise ValueError(f"Document {document_id} not found")

    return documents_db[document_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document",
)
def edit_document(
    document_id: str = Field(description="The ID of the document to edit"),
    old_content: str = Field(description="The old text to replace in the document"),
    new_content: str = Field(description="The new text to insert into the document"),
) -> None:
    if document_id not in documents_db:
        raise ValueError(f"Document {document_id} not found")

    documents_db[document_id] = new_content


@mcp.resource(
    uri="docs://documents",
    description="A list of all document IDs",
    mime_type="application/json",
)
def list_document_ids() -> list[str]:
    return list[str](documents_db.keys())


@mcp.resource(
    uri="docs://documents/{document_id}",
    description="The contents of a particular document",
    mime_type="text/plain",
)
def get_document_content(document_id: str) -> str:
    if document_id not in documents_db:
        raise ValueError(f"Document {document_id} not found")

    return documents_db[document_id]


# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
