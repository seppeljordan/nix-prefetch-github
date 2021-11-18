import json
import subprocess

from nix_prefetch_github.__main__ import main

from .markers import network, requires_nix_build


@network
@requires_nix_build
def test_main_script_outputs_valid_json(capsys):
    main(["seppeljordan", "nix-prefetch-github"])
    captured = capsys.readouterr()
    json.loads(captured.out)


@network
@requires_nix_build
def test_main_script_outputs_valid_nix(capsys):
    main(["seppeljordan", "nix-prefetch-github"])
    captured = capsys.readouterr()
    subprocess.run(["nix-instantiate", "--expr", captured.out])
