import os
import subprocess
import argparse
from openai import OpenAI

# Rough pricing constants (adjust as needed):
PROMPT_COST_PER_1K_TOKENS = 0.03  # $0.03 per 1k prompt tokens for GPT-4 prompt
COMPLETION_COST_PER_1K_TOKENS = 0.06  # $0.06 per 1k completion tokens for GPT-4
APPROX_CHARS_PER_TOKEN = 4  # rough approximation

from dotenv import load_dotenv

load_dotenv()  # This will load variables from .env into the environment
api_key = os.getenv("OPENAI_API_KEY")
def estimate_cost(prompt, completion_length=500):
    """
    Estimate cost of the API call.
    This is a rough calculation and should be replaced with a token-counting method for accuracy.
    """
    # Approximate tokens in prompt
    prompt_tokens = len(prompt) / APPROX_CHARS_PER_TOKEN
    # Assume a small completion response (adjust as needed)
    completion_tokens = completion_length

    # Convert tokens to thousands
    prompt_thousands = prompt_tokens / 1000.0
    completion_thousands = completion_tokens / 1000.0

    # Calculate estimated cost
    estimated_prompt_cost = prompt_thousands * PROMPT_COST_PER_1K_TOKENS
    estimated_completion_cost = completion_thousands * COMPLETION_COST_PER_1K_TOKENS
    total_estimated_cost = estimated_prompt_cost + estimated_completion_cost

    return total_estimated_cost

def get_git_diff(repo_path, base_branch, compare_branch):
    """
    Get the git diff between two branches in the specified repository.
    Returns a string containing the diff or None if an error occurs.
    """
    # Use the `-C` option to specify the working directory for git commands
    try:
        diff = subprocess.check_output(
            ['git', '-C', repo_path, 'diff', f'{base_branch}...{compare_branch}'],
            text=True
        )
        return diff.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        return None

def analyze_with_openai(diff_content):
    """
    Analyze the given diff content using the OpenAI API.
    """
    if not api_key:
        print("OPENAI_API_KEY not set.")
        return None

    client = OpenAI(api_key=api_key)

    prompt = f"""Please analyze this git diff and provide:
1. Summary of key changes
2. Potential issues or risks
3. Code quality suggestions
4. Test coverage considerations

Diff content:
{diff_content}
"""

    # Estimate the cost before sending
    cost_estimate = estimate_cost(prompt)
    print(f"Estimated cost for this request: ~${cost_estimate:.4f}")

    # Ask for user confirmation
    confirmation = input("Do you want to proceed with the API call? (y/N): ").strip().lower()
    if confirmation != 'y':
        print("Request canceled.")
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful code review assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze a git diff using OpenAI.")
    parser.add_argument("--repo_path", required=True, help="The path to the git repository.")
    parser.add_argument("--base_branch", default="dev", help="The base branch to compare against (default: dev).")
    parser.add_argument("--compare_branch", required=True, help="The branch that contains the changes.")
    args = parser.parse_args()

    # Get the diff
    diff_content = get_git_diff(args.repo_path, args.base_branch, args.compare_branch)
    if diff_content is None:
        print("No diff content found or an error occurred.")
        return
    if not diff_content.strip():
        print("No differences detected between the given branches.")
        return

    # Get the analysis
    analysis = analyze_with_openai(diff_content)
    if analysis:
        print("\n=== PR Analysis ===")
        print(analysis)
    else:
        print("No analysis could be retrieved.")

if __name__ == "__main__":
    main()
