"""Configure GitHub repository settings interactively."""

import json

import yaml

from dryclean.constant import CLAUDE_MD_PATH, WORKFLOW_PATH
from dryclean.util import (
    CommandOptions,
    info,
    panel,
    prompt_yes_no,
    read_template,
    run_command,
)

_CI_COMMIT_MESSAGE = "ci: configure dryclean"
_CI_JOB_KEY = "quality"
_CI_TEMPLATE = "dryclean.yml.tmpl"
_DEFAULT_BRANCH = "main"
_INIT_COMMIT_MESSAGE = "init: project scaffold"
_SECRET_NAME = "CLAUDE_CODE_OAUTH_TOKEN"


def _push_to_origin() -> bool:
    has_commits = (
        run_command(
            ["git", "rev-parse", "HEAD"], CommandOptions(silent=True)
        ).returncode
        == 0
    )
    message = _CI_COMMIT_MESSAGE if has_commits else _INIT_COMMIT_MESSAGE

    if (
        run_command(["git", "add", str(CLAUDE_MD_PATH), str(WORKFLOW_PATH)]).returncode
        != 0
    ):
        return False
    if run_command(["git", "commit", "--no-verify", "-m", message]).returncode != 0:
        return False
    return run_command(["git", "push", "-u", "origin", _DEFAULT_BRANCH]).returncode == 0


def _find_missing_remote_files(owner: str, repo: str) -> list[str]:
    api = f"repos/{owner}/{repo}/contents"
    missing = []
    for path in [CLAUDE_MD_PATH, WORKFLOW_PATH]:
        result = run_command(
            ["gh", "api", f"{api}/{path}?ref={_DEFAULT_BRANCH}"],
            CommandOptions(silent=True),
        )
        if result.returncode != 0:
            missing.append(str(path))
    return missing


def _ensure_remote_ready(owner: str, repo: str) -> bool:
    missing = _find_missing_remote_files(owner, repo)
    if not missing:
        return True
    files = " and ".join(missing)

    panel(
        f"\ndryclean will:\n"
        f"  1. Commit {files} to '{_DEFAULT_BRANCH}' (--no-verify)\n"
        f"  2. Push to origin/{_DEFAULT_BRANCH}\n"
        f"  3. Then configure branch protection and OAuth token\n\n"
        f"[red]Without this push, branch protection will lock you out.[/red]",
        title=f"< {files} not found on origin/{_DEFAULT_BRANCH} >",
        style="yellow",
    )

    if not prompt_yes_no("Proceed?"):
        info("Push manually, then run dryclean init again for GitHub setup.")
        return False

    return _push_to_origin()


def _get_status_check_context() -> str:
    workflow = yaml.safe_load(read_template(_CI_TEMPLATE))
    context: str = workflow["jobs"][_CI_JOB_KEY].get("name", _CI_JOB_KEY)
    return context


def _apply_branch_protection(owner: str, repo: str, payload: str) -> bool:
    endpoint = f"repos/{owner}/{repo}/branches/{_DEFAULT_BRANCH}/protection"
    return (
        run_command(
            ["gh", "api", endpoint, "-X", "PUT", "--input", "-"],
            CommandOptions(input=payload),
        ).returncode
        == 0
    )


def _configure_branch_protection(owner: str, repo: str) -> None:
    payload = json.dumps(
        {
            "required_pull_request_reviews": {},
            "required_status_checks": {
                "contexts": [_get_status_check_context()],
                "strict": True,
            },
            "required_conversation_resolution": True,
            "enforce_admins": True,
            "restrictions": None,
        }
    )
    if not _apply_branch_protection(owner, repo, payload):
        return
    panel(
        "\n- Require a pull request before merging\n"
        "- Require status checks to pass before merging\n"
        "- Require branches to be up to date before merging\n"
        "- Require conversation resolution before merging\n"
        "- Do not allow bypassing the above settings",
        title=f"< Branch protection applied to '{_DEFAULT_BRANCH}' >",
    )


def _setup_oauth_token() -> None:
    token = input("Paste Claude Code OAuth token (run: claude setup-token): ").strip()
    if not token or not token.startswith("sk-ant-"):
        panel(
            "\nPR review and PR description will not work without it.\n"
            f"Add {_SECRET_NAME} in your repo's GitHub Actions secrets.",
            title="[red]< Claude Code OAuth token not set >[/red]",
            style="yellow",
        )
        return

    if (
        run_command(
            ["gh", "secret", "set", _SECRET_NAME], CommandOptions(input=token)
        ).returncode
        == 0
    ):
        info(f"{_SECRET_NAME} set.")


def setup_github() -> None:
    """Configure GitHub repository settings."""
    try:
        result = run_command(
            ["gh", "repo", "view", "--json", "owner,name"],
            CommandOptions(silent=True),
        )
    except FileNotFoundError:
        info("Install gh from: https://cli.github.com. Skipping GitHub setup.")
        return

    if result.returncode != 0:
        info("Not a GitHub repository. Skipping GitHub setup.")
        return

    data = json.loads(result.stdout)
    owner, repo = data["owner"]["login"], data["name"]

    if not _ensure_remote_ready(owner, repo):
        return

    if prompt_yes_no(f"Apply protection rules to '{_DEFAULT_BRANCH}'?"):
        _configure_branch_protection(owner, repo)

    _setup_oauth_token()
