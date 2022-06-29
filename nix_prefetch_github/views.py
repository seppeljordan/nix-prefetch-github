from sys import exit, stderr, stdout

from nix_prefetch_github.presenter import ViewModel


class CommandLineViewImpl:
    def render_view_model(self, model: ViewModel) -> None:
        for line in model.stderr_lines:
            print(line, file=stderr)
        for line in model.stdout_lines:
            print(line, file=stdout)
        exit(model.exit_code)
