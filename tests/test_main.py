import json
import subprocess

from nix_prefetch_github.__main__ import main

from .markers import network, requires_nix_build


@network
@requires_nix_build
def test_main_script_outputs_valid_json(capsys):
    main.callback(owner="seppeljordan", repo="nix-prefetch-github", nix=False)
    captured = capsys.readouterr()
    json.loads(captured.out)


@network
@requires_nix_build
def test_main_script_outputs_valid_nix(capsys):
    main.callback(owner="seppeljordan", repo="nix-prefetch-github", nix=True)
    captured = capsys.readouterr()
    subprocess.run(["nix-instantiate", "--expr", captured.out])
