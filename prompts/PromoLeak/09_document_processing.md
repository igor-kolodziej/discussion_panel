# Document Processing

## Objective
Design a simple, auditable workflow for storing, extracting, and linking evidence from pilot documents.

## Prerequisites
- A brand has shared documents under NDA or paid terms.
- Audit scope and document list are finalized.
- Confidentiality/document-handling rules exist.

## Inputs
- Shared document set.
- Document request list.
- Confidentiality rules.
- Audit scope.

## Instructions
1. Define folder structure for one pilot.
2. Define naming rules for raw files, extracted tables, and evidence snippets.
3. Specify OCR/PDF extraction steps.
4. Define core spreadsheet tables.
5. Add an evidence-linking method so every finding points back to source files.
6. Keep the workflow manual-first and explainable.

## Subagents
- Use subagents for parallel document extraction only after confidentiality rules permit it.
- Use one subagent to independently check whether source links support the findings.

## Output
Return:
- folder structure
- file naming rules
- extraction workflow
- spreadsheet table schema
- evidence-linking method
- quality-control checklist
