"""Shared utilities."""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from dryclean.constant import TEMPLATES_ROOT


@dataclass
class CommandOptions:
    """Options for run_command."""

    cwd: Path | None = None
    env: dict[str, str] | None = None
    input: str | None = None
    silent: bool = False
    skip_lines_containing: str | None = None
    stream: bool = False


_console = Console()
_stderr = Console(stderr=True)


def error(message: str) -> None:
    """Print an error message to stderr."""
    _stderr.print(f"[red]ERROR:[/red] {message}")


def header(title: str, bold: bool = True) -> None:
    """Print a centered header to stdout."""
    _console.print()
    _console.print(Rule(title, style="bold" if bold else "dim"))
    _console.print()


def info(message: str) -> None:
    """Print an informational message to stdout."""
    _console.print(message)


def panel(body: str, title: str, style: str = "green") -> None:
    """Print a bordered panel to stdout."""
    _console.print(Panel(body, title=title, border_style=style))


def warning(message: str) -> None:
    """Print a warning message to stderr."""
    _stderr.print(f"[yellow]WARNING:[/yellow] {message}")


def prompt_yes_no(question: str) -> bool:
    """Prompt the user with a yes/no question."""
    answer = input(f"{question} [y/n]: ").strip().lower()
    return answer.startswith("y")


def read_template(name: str) -> str:
    """Return the contents of a template file."""
    return (TEMPLATES_ROOT / name).read_text(encoding="utf-8")


def write_file(path: Path, content: str, overwrite: bool = False) -> None:
    """Write content to a file and create parent directories as needed."""
    if not overwrite and path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _run_streamed(
    command: list[str], options: CommandOptions
) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        command,
        cwd=options.cwd,
        env=options.env,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    assert options.skip_lines_containing is not None
    for line in process.stdout:
        if options.skip_lines_containing not in line:
            sys.stdout.write(line)
            sys.stdout.flush()
    process.wait()
    return subprocess.CompletedProcess(command, process.returncode)


def _run_default(
    command: list[str], options: CommandOptions
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        capture_output=not options.stream,
        cwd=options.cwd,
        env=options.env,
        input=options.input,
        text=True,
    )
    if (
        not options.silent
        and not options.stream
        and result.returncode != 0
        and result.stderr.strip()
    ):
        error(result.stderr.strip())
    return result


def run_command(
    command: list[str], options: CommandOptions = CommandOptions()
) -> subprocess.CompletedProcess[str]:
    """Run a command and optionally filter output or report errors."""
    if options.stream and options.skip_lines_containing:
        return _run_streamed(command, options)
    return _run_default(command, options)
