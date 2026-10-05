# Personal Diary MCP Server

A personal diary server built with **FastMCP** and **python-docx**.

Write your thoughts naturally in Claude without worrying about formatting. Claude can structure the entry and call this MCP server to save it as a date-wise `.docx` diary file with:

- automatic date and time
- a title
- mood
- cleaned thoughts
- reflection
- key takeaways
- tags
- one Word document per day
- multiple entries appended to the same day's file

The server also exposes diary content through MCP tools and resources.

---

## How it works

```text
You
│
│  "Diary: today I finally understood MCP..."
│
▼
Claude
│
│  structures your raw thoughts
│
├── title
├── mood
├── thoughts
├── reflection
├── key takeaways
└── tags
│
▼
Personal Diary MCP
│
▼
DOCX file
│
└── diary/2026/10/2026-10-05.docx
```

Claude handles the language understanding and formatting.

The MCP server handles deterministic tasks such as:

- timestamps
- file creation
- date-wise folders
- appending entries
- reading stored diary entries

No LLM API key is required inside the MCP server when Claude Desktop is the MCP host.

---

## Features

### MCP Tools

Depending on the version of `main.py`, the server can expose tools such as:

```text
write_diary_entry
read_today_diary
read_diary_by_date
list_diary_entries
get_diary_file_path
```

### MCP Resources

The server can also expose resources such as:

```text
diary://today
diary://entries
diary://2026-10-05
```

The date resource is dynamic:

```text
diary://{date}
```

---

## Project structure

A typical project looks like this:

```text
personal-diary-mcp/
│
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
└── src/
    └── remote_server/
        ├── __init__.py
        ├── main.py
        └── diary/
            └── 2026/
                └── 10/
                    └── 2026-10-05.docx
```

> The `diary/` folder contains personal data and should normally **not** be committed to GitHub.

---

# Installation

## 1. Prerequisites

Install:

- Python 3.12+ recommended
- `uv`
- Claude Desktop

Verify Python:

```bash
python --version
```

Verify `uv`:

```bash
uv --version
```

---

## 2. Clone the repository

Replace the URL with the actual repository URL.

```bash
git clone https://github.com/YOUR_USERNAME/personal-diary-mcp.git
cd personal-diary-mcp
```

---

## 3. Install dependencies

If the repository contains `pyproject.toml` and `uv.lock`, run:

```bash
uv sync
```

If you are creating the project manually, the important packages are:

```bash
uv add fastmcp python-docx tzdata
```

`tzdata` is useful on Windows because Python's `zoneinfo` may otherwise be unable to resolve:

```python
ZoneInfo("Asia/Kolkata")
```

---

# Test the MCP server in your browser

FastMCP's Inspector is the easiest way to test tools and resources before connecting Claude Desktop.

From the repository root:

```bash
uv run fastmcp dev inspector src/remote_server/main.py:mcp
```

The browser Inspector should open automatically.

You should be able to inspect and test the MCP tools and resources.

For example, test:

```text
write_diary_entry
```

with values such as:

```text
title:
MCP Finally Clicked

mood:
Excited

thoughts:
Today I finally understood MCP properly.

reflection:
Building real tools made the concept easier to understand.
```

After running the tool, a Word file should be created under the diary folder.

---

# Connect to Claude Desktop

Claude Desktop can launch the server locally using **stdio**.

Even if `main.py` contains an HTTP startup block such as:

```python
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )
```

you can still use the FastMCP CLI from Claude Desktop:

```text
fastmcp run ...main.py:mcp
```

The CLI imports the `mcp` object and runs it for the MCP host, so Claude Desktop does not need to execute the HTTP `__main__` block.

---

## Claude Desktop config location

### Windows

The normal Claude Desktop configuration file is:

```text
%APPDATA%\Claude\claude_desktop_config.json
```

You can open the folder from PowerShell:

```powershell
explorer "$env:APPDATA\Claude"
```

Or open the config directly:

```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

### macOS

The normal config file is:

```text
~/Library/Application Support/Claude/claude_desktop_config.json
```

---

# Windows Claude Desktop configuration

After running:

```bash
uv sync
```

your project should have a virtual environment containing FastMCP.

Use the **absolute path** to `fastmcp.exe`.

Example project:

```text
D:\GenAI\MCP\personal-diary-mcp
```

Then the config could be:

```json
{
  "mcpServers": {
    "personal-diary": {
      "command": "D:\\GenAI\\MCP\\personal-diary-mcp\\.venv\\Scripts\\fastmcp.exe",
      "args": [
        "run",
        "D:\\GenAI\\MCP\\personal-diary-mcp\\src\\remote_server\\main.py:mcp"
      ]
    }
  }
}
```

### Important

Replace:

```text
D:\GenAI\MCP\personal-diary-mcp
```

with the actual absolute path where **you cloned the repository**.

Windows JSON paths require escaped backslashes:

```text
\\
```

So:

```text
D:\Projects\Diary
```

must appear in JSON as:

```text
D:\\Projects\\Diary
```

---

# If you already have other MCP servers

Do **not** create a second `"mcpServers"` object.

For example, if you already have:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "..."
    }
  }
}
```

add Personal Diary **inside the existing object**:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "..."
    },

    "personal-diary": {
      "command": "D:\\ABSOLUTE\\PATH\\TO\\personal-diary-mcp\\.venv\\Scripts\\fastmcp.exe",
      "args": [
        "run",
        "D:\\ABSOLUTE\\PATH\\TO\\personal-diary-mcp\\src\\remote_server\\main.py:mcp"
      ]
    }
  }
}
```

There must be only one top-level:

```json
"mcpServers"
```

object.

---

# macOS Claude Desktop configuration

After running:

```bash
uv sync
```

the FastMCP executable will normally be inside:

```text
/path/to/personal-diary-mcp/.venv/bin/fastmcp
```

Example:

```json
{
  "mcpServers": {
    "personal-diary": {
      "command": "/Users/YOUR_NAME/Projects/personal-diary-mcp/.venv/bin/fastmcp",
      "args": [
        "run",
        "/Users/YOUR_NAME/Projects/personal-diary-mcp/src/remote_server/main.py:mcp"
      ]
    }
  }
}
```

Replace the example paths with your own absolute paths.

---

# Restart Claude Desktop

After editing `claude_desktop_config.json`:

1. Save the file.
2. Fully quit Claude Desktop.
3. Make sure Claude is no longer running in the background.
4. Reopen Claude Desktop.
5. Open the MCP / connector settings.
6. Confirm that `personal-diary` appears.

Claude Desktop reads the config when it starts, so simply closing the window may not be enough.

---

# Try it in Claude

Once connected, you do not need to write structured diary content manually.

For example:

```text
Diary: Today was a little tiring but I finally understood MCP.
Building the expense tracker and diary server made everything
click. I think I can now use MCP in much larger projects.
```

Claude can transform that into structured arguments for:

```text
write_diary_entry
```

and your MCP server can save it in a Word document.

You can also try:

```text
Write this in my diary:
I was very productive in the morning but lost focus later.
Still, I completed something I had been avoiding for days.
```

Or:

```text
Read today's diary.
```

Or:

```text
What did I write on 2026-10-05?
```

---

# Diary file organization

Entries are stored date-wise:

```text
diary/
├── 2026/
│   ├── 10/
│   │   ├── 2026-10-05.docx
│   │   ├── 2026-10-06.docx
│   │   └── 2026-10-07.docx
│   │
│   └── 11/
│       └── ...
│
└── 2027/
    └── ...
```

If you write multiple times on the same date, new entries are appended to the same `.docx` file.

---

# Recommended `.gitignore`

Your diary may contain highly personal information.

Do not accidentally push diary entries to a public GitHub repository.

Add this to `.gitignore`:

```gitignore
# Virtual environment
.venv/

# Python
__pycache__/
*.py[cod]

# Personal diary data
src/remote_server/diary/

# Optional: ignore all Word documents
*.docx

# Environment variables
.env
.env.*
```

If you want to include a demo Word file in the repository, remove:

```gitignore
*.docx
```

and only ignore the real diary folder.

---

# Run as an HTTP MCP server

The project can also be run over HTTP.

Example `main.py` startup:

```python
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )
```

Start it with:

```bash
uv run python src/remote_server/main.py
```

The MCP endpoint will normally be:

```text
http://localhost:8000/mcp
```

`localhost` is still local to your computer.

To make the server genuinely remote, deploy it to a server or cloud platform and expose it over HTTPS.

---

# Local vs remote mode

```text
Claude Desktop + config JSON
        │
        │ stdio
        ▼
fastmcp run main.py:mcp
        │
        ▼
Personal Diary MCP
```

For remote deployment:

```text
MCP Client
    │
    │ HTTPS
    ▼
Remote FastMCP server
    │
    ▼
Personal Diary MCP
```

The same `mcp` object can be used in both cases.

---

# Troubleshooting

## Claude Desktop does not show the server

Check:

1. `claude_desktop_config.json` is valid JSON.
2. Paths are absolute.
3. Windows paths use `\\`.
4. `.venv` exists.
5. `fastmcp.exe` exists.
6. `main.py` exists at the configured location.
7. Claude Desktop was fully restarted.

Test the FastMCP executable manually:

```powershell
& "D:\ABSOLUTE\PATH\TO\personal-diary-mcp\.venv\Scripts\fastmcp.exe" run "D:\ABSOLUTE\PATH\TO\personal-diary-mcp\src\remote_server\main.py:mcp"
```

---

## `ZoneInfoNotFoundError: Asia/Kolkata`

Install timezone data:

```bash
uv add tzdata
```

Then run:

```bash
uv sync
```

---

## `ModuleNotFoundError: docx`

Install `python-docx`:

```bash
uv add python-docx
```

---

## `Expected a Python module at src\remote_server\__init__.py`

Make sure this file exists:

```text
src/remote_server/__init__.py
```

It may be empty.

On Windows PowerShell:

```powershell
New-Item -ItemType File -Force src\remote_server\__init__.py
```

---

## Config JSON is invalid

You can validate a Windows Claude config from PowerShell:

```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" -Raw | ConvertFrom-Json
```

If PowerShell returns the parsed object without a red error, the JSON syntax is valid.

---

# Privacy and security

This project is designed for personal diary data.

Keep in mind:

- Diary files are stored on the machine where the MCP server runs.
- Do not commit real diary files to a public repository.
- Do not put API keys or secrets directly in GitHub.
- Keep `.env` files out of source control.
- Review what an MCP client can access before enabling it.
- If you deploy the HTTP server publicly, add authentication before storing private diary content on it.

A public unauthenticated diary MCP endpoint is **not recommended**.

---

# Development

Run the browser Inspector:

```bash
uv run fastmcp dev inspector src/remote_server/main.py:mcp
```

Run the HTTP server:

```bash
uv run python src/remote_server/main.py
```

Synchronize dependencies:

```bash
uv sync
```

---

# Example Claude workflow

```text
User:
"Diary: I felt really motivated today. I struggled with a bug
for a while, but when I finally solved it I understood the
concept much better."

Claude:
    ↓ interprets the thought
    ↓ prepares structured fields
    ↓ calls write_diary_entry

MCP Server:
    ↓ adds date/time
    ↓ opens or creates today's DOCX
    ↓ appends the entry
    ↓ saves the document

Result:
src/remote_server/diary/2026/10/2026-10-05.docx
```

---

# Built with

- Python
- FastMCP
- Model Context Protocol (MCP)
- python-docx
- uv
- Claude Desktop

---

## Contributions

Issues, suggestions, and pull requests are welcome.

If you add a new feature, please avoid committing personal diary files or credentials in examples.
