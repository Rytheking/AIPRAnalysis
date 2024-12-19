# PR Analysis Tool
## Overview
This project, **PR Analysis Tool**, provides a simple and efficient way to analyze Git pull request (PR) code changes using OpenAI's GPT models. It generates helpful insights, including:
1. A summary of key changes.
2. Identification of potential risks or issues.
3. Suggestions for code quality improvements.
4. Test coverage considerations.

The tool uses the OpenAI API for analysis and estimates potential costs before making any API calls.
## Prerequisites
To use this project, ensure you have the following installed and set up:
- Python 3.7 or higher
- `pip` for managing Python packages
- Git installed on your system (to access `git diff` commands)
- An OpenAI API key with access to GPT-4 or GPT-3.5

## Features
- Command-line interface for easy usage.
- Cost estimation of OpenAI API calls based on token usage.
- User confirmation before invoking the OpenAI API.
- Customizable Git branch comparisons for `git diff`.

## Setup Instructions
### Step 1: Clone the Repository
``` bash
git clone https://github.com/Rytheking/AIPRAnalysis
cd AIPRAnalysis


```
### Step 2: Install Python Dependencies
It is recommended to use a virtual environment:
``` bash
# Create and activate a virtual environment (optional, but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required Python libraries
pip install python-dotenv openai
```
### Step 3: Configure Environment Variables
Create a `.env` file in the project directory, and set your OpenAI API key:
``` dotenv
# .env
OPENAI_API_KEY=your_openai_api_key_here
```
This `.env` file will be automatically loaded by the application. Ensure it is **ignored in Git** (already configured in `.gitignore`).
### Step 4: Run the Tool
To analyze a pull request, use the following command:
``` bash
python PR_Analysis.py --repo_path <path-to-git-repo> --base_branch <base-branch> --compare_branch <feature-branch>
```
- `repo_path`: Path to your Git repository (required).
- `base_branch`: The branch to compare against. Defaults to `dev` if not specified.
- `compare_branch`: The branch containing your changes (required).

For example:
``` bash
python PR_Analysis.py --repo_path /path/to/repo --compare_branch feature-branch
```
### Step 5: Review and Confirm API Call
Before making an API call, the tool will estimate the cost based on token usage and wait for confirmation:
``` plaintext
Estimated cost for this request: ~$0.0100
Do you want to proceed with the API call? (y/N):
```
Type `y` to proceed. The tool will then output the PR analysis.
## Project Structure
The repository contains the following key files:
- **PR_Analysis.py**: Main Python script with all functionality.
- **.env**: Stores sensitive environment variables (ignored by Git).
- **.gitignore**: Ensures `.env` and temporary files are ignored by Git.

## Dependencies
This project uses the following Python libraries:
- `openai`: For interacting with the OpenAI API.
- `python-dotenv`: For managing environment variables.
- `subprocess` (standard library): For invoking Git commands.

## Notes
- Make sure you have sufficient API credits on your OpenAI account before using the tool.
- The `estimate_cost` method provides an approximation of the OpenAI API cost. It is not exact and should be used as a guideline.

## Contribution Guidelines
If you'd like to contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a detailed description.

Enjoy automated and insightful PR analysis with this tool! If you encounter issues or have suggestions, feel free to raise them via the project's GitHub Issues
