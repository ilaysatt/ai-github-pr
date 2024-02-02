# GitHub PR Comment Generator

This tool generates clear, concise, and actionable pull request (PR) comments for GitHub repositories based on OpenAI's language model, GPT-3.5-turbo. The generated comments provide constructive feedback to developers and suggest specific, practical, and easy-to-implement changes to improve the code.

## Usage

### Prerequisites

Before using the tool, make sure you have the following:

- OpenAI API key
- GitHub token with access to the repositories you want to analyze

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:ilaysatt/ai-github-pr.git
   ```

2. Navigate to the project directory:

   ```bash
   cd ai-github-pr
   ```

3. Install using pip:

   ```bash
   pip install .
   ```

### Configuration

Configure environment variables OPENAI_API_KEY and GITHUB_TOKEN with your OpenAI API key and GitHub token respectively.
If you don't want to add environment variables ,create a `.env` file in the project directory with the following format:

```plaintext
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
```

Replace `your_openai_api_key` and `your_github_token` with your actual API key and GitHub token.

### Running the Tool

Use the following command to run the tool:

```bash
ai-github-pr [-u] [-r REPO] [-e ENV] [-pr PULL_REQUEST_ID] [-q]
```

#### Options:

- `-u` or `--upload`: Upload generated comments to GitHub.
- `-r REPO` or `--repo REPO`: Specify the repository to check (format: `repo_owner/repo_name`). If not provided, the tool will use the repository associated with the current directory.
- `-e ENV` or `--env ENV`: Path to the `.env` file to use.
- `-pr PULL_REQUEST_ID` or `--pull-requests-id PULL_REQUEST_ID`: ID of the specific pull request to check. If not provided, all pull requests in the repository will be analyzed.
- `-q` or `--quite`: Suppress printing generated comments and suggestions to the command line.

### Example Usage

```bash
ai-github-pr -u -r yourusername/your-repo -e path/to/.env -pr 123 -q
```

This command will generate comments and suggestions for pull request #123 in the specified repository, suppress printing to the command line, and upload the comments to GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.