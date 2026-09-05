# Knowledge Sync README

This project uses `sync_knowledge.py` as the single command to keep the website knowledge base, approved aviation sources, and local PDF page indexes synchronized.

## Project Folder

```text
C:\Users\bhigh\OneDrive\02. PROJECTS\04. CODING\2026_CFI_Syllabus_Lessons
```

## Activate the Virtual Environment

Open Command Prompt and change to the project folder:

```cmd
cd "C:\Users\bhigh\OneDrive\02. PROJECTS\04. CODING\2026_CFI_Syllabus_Lessons"
```

If needed, first add the Anaconda DLL folder to `PATH`:

```cmd
set "PATH=C:\Users\bhigh\anaconda3\Library\bin;%PATH%"
```

Activate the virtual environment:

```cmd
.venv\Scripts\activate
```

When activated, the command prompt should begin with:

```text
(.venv)
```

## Run the Knowledge Sync

```cmd
python sync_knowledge.py
```

## What `sync_knowledge.py` Does

### Site Content

The script scans:

```text
content/**/lesson.md
```

and synchronizes those lesson files to the OpenAI `SITE_CONTENT` vector store.

It detects:

- New lessons
- Changed lessons
- Deleted lessons
- Unchanged lessons

### Approved Aviation Sources

The script recursively scans:

```text
knowledge/approved/**/*.pdf
```

The original PDF files are synchronized to the OpenAI `APPROVED_AVIATION_SOURCES` vector store.

The original PDF is retained so the source document, including diagrams and other visual content, remains available.

### Local PDF Page Index

For every approved PDF, the script creates a local page-aware text index under:

```text
knowledge/index/
```

Example:

```text
knowledge/approved/Pilots_Handbook_of_Aeronautical_Knowledge.pdf
```

creates:

```text
knowledge/index/Pilots_Handbook_of_Aeronautical_Knowledge.pdf.txt
```

The generated text contains physical PDF page markers:

```text
<<<PDF_PAGE:143>>>
```

The Flask chatbot can use this index to map text retrieved by OpenAI File Search back to the physical PDF viewer page.

This allows a reference such as:

```text
Pilots Handbook of Aeronautical Knowledge — PDF p. 143
```

to link directly to:

```text
/knowledge/Pilots_Handbook_of_Aeronautical_Knowledge.pdf#page=143
```

The `.pdf.txt` files are local lookup files only.

They are NOT uploaded to the OpenAI approved vector store.

### Approved PDF Changes

If an approved PDF is changed:

1. Its local page index is rebuilt.
2. The updated original PDF is uploaded and indexed by OpenAI.
3. The previous OpenAI version is removed after the replacement successfully indexes.

### Deleted Approved PDFs

If an approved PDF is removed from:

```text
knowledge/approved/
```

the sync removes:

- The corresponding OpenAI vector-store file
- The manifest record
- The corresponding local `.pdf.txt` page index
- Empty index folders left behind

## Normal Workflow for Adding an Approved Document

Copy the PDF anywhere under:

```text
knowledge/approved/
```

Then run:

```cmd
python sync_knowledge.py
```

The sync automatically handles:

```text
Approved PDF
    │
    ├── Original PDF → OpenAI APPROVED_AVIATION_SOURCES
    │
    └── Page-aware text → knowledge/index/
```

## Typical Full Command Sequence

```cmd
cd "C:\Users\bhigh\OneDrive\02. PROJECTS\04. CODING\2026_CFI_Syllabus_Lessons"
set "PATH=C:\Users\bhigh\anaconda3\Library\bin;%PATH%"
.venv\Scripts\activate
python sync_knowledge.py
```

## Run the Flask Website

With the virtual environment activated:

```cmd
python flask_app\app.py
```

## Environment Variables

The `.env` file contains the OpenAI configuration used by the application and sync process, including:

```text
OPENAI_API_KEY
OPENAI_SITE_VECTOR_STORE_ID
OPENAI_APPROVED_VECTOR_STORE_ID
```

Do not commit `.env` to source control.

## Important Files and Folders

```text
sync_knowledge.py
knowledge_manifest.db

content/

knowledge/
├── approved/
└── index/

flask_app/
├── app.py
├── templates/
└── static/

.env
```

## Knowledge Maintenance

`sync_knowledge.py` is the single knowledge-maintenance command.

A separate `build_knowledge_index.py` script is no longer required because PDF page-index generation is handled directly by `sync_knowledge.py`.

Normal maintenance is therefore:

```cmd
.venv\Scripts\activate
python sync_knowledge.py
```



## Lesson creation prompt:
✅ **COMPLETED:** Private Lesson 4 — Airspace, Local Operations and Pre-Solo Regulations

- Full lesson.md generated (GROUND + FLIGHT, Developing)
- Touch-and-go flight reinforcement (Lesson 3 procedures in Class D environment)
- Kneeboard formatted per house style (Lesson 3 rail layout)
- PNG image reference removed (embedded VFR minimums text instead)
- Ready for your review