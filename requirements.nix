# generated using pypi2nix tool (version: 2.0.3)
# See more at: https://github.com/nix-community/pypi2nix
#
# COMMAND:
#   pypi2nix -r requirements.txt -s setuptools-scm -s pytest-runner -E 'openssl libffi'
#

{ pkgs ? import <nixpkgs> { }, overrides ? ({ pkgs, python }: self: super: { })
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
    import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
      inherit pkgs;
      inherit (pkgs) stdenv;
      python = pkgs.python3;
    };

  commonBuildInputs = with pkgs; [ openssl libffi ];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' [ "__unfix__" ];
      interpreterWithPackages = selectPkgsFn:
        pythonPackages.buildPythonPackage {
          name = "python3-interpreter";
          buildInputs = [ makeWrapper ] ++ (selectPkgsFn pkgs);
          buildCommand = ''
            mkdir -p $out/bin
            ln -s ${pythonPackages.python.interpreter} \
                $out/bin/${pythonPackages.python.executable}
            for dep in ${builtins.concatStringsSep " " (selectPkgsFn pkgs)}; do
              if [ -d "$dep/bin" ]; then
                for prog in "$dep/bin/"*; do
                  if [ -x "$prog" ] && [ -f "$prog" ]; then
                    ln -s $prog $out/bin/`basename $prog`
                  fi
                done
              fi
            done
            for prog in "$out/bin/"*; do
              wrapProgram "$prog" --prefix PYTHONPATH : "$PYTHONPATH"
            done
            pushd $out/bin
            ln -s ${pythonPackages.python.executable} python
            ln -s ${pythonPackages.python.executable} \
                python3
            popd
          '';
          passthru.interpreter = pythonPackages.python;
        };

      interpreter = interpreterWithPackages builtins.attrValues;
    in {
      __old = pythonPackages;
      inherit interpreter;
      inherit interpreterWithPackages;
      mkDerivation = args:
        pythonPackages.buildPythonPackage (args // {
          nativeBuildInputs = (args.nativeBuildInputs or [ ])
            ++ args.buildInputs;
        });
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage
        (drv.drvAttrs // f drv.drvAttrs // { meta = drv.meta; });
      withPackages = pkgs'': withPackages (pkgs // pkgs'');
    };

  python = withPackages { };

  generated = self: {
    "appdirs" = python.mkDerivation {
      name = "appdirs-1.4.3";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-1.4.3.tar.gz";
        sha256 =
          "9e5896d1372858f8dd3344faf4e5014d21849c756c8d5701f78f8a103b372d92";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/ActiveState/appdirs";
        license = licenses.mit;
        description =
          "A small Python module for determining appropriate platform-specific dirs, e.g. a "
          user data dir ".";
      };
    };

    "attrs" = python.mkDerivation {
      name = "attrs-19.3.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/98/c3/2c227e66b5e896e15ccdae2e00bbc69aa46e9a8ce8869cc5fa96310bf612/attrs-19.3.0.tar.gz";
        sha256 =
          "f7b7ce16570fe9965acd6d30101a28f62fb4a7f9e926b3bbc9b61f8b04247e72";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."setuptools" self."wheel" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };

    "black" = python.mkDerivation {
      name = "black-19.10b0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/b0/dc/ecd83b973fb7b82c34d828aad621a6e5865764d52375b8ac1d7a45e23c8d/black-19.10b0.tar.gz";
        sha256 =
          "c2edb73a08e9e0e6f65a0e6af18b059b8b1cdd5bef997d7a0b181df93dc81539";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [
        self."appdirs"
        self."attrs"
        self."click"
        self."pathspec"
        self."regex"
        self."toml"
        self."typed-ast"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/psf/black";
        license = licenses.mit;
        description = "The uncompromising code formatter.";
      };
    };

    "bleach" = python.mkDerivation {
      name = "bleach-3.1.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/78/5a/0df03e8735cd9c75167528299c738702437589b9c71a849489d00ffa82e8/bleach-3.1.0.tar.gz";
        sha256 =
          "3fdf7f77adcf649c9911387df51254b813185e32b2c6619f690b593a617e19fa";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."six" self."webencodings" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mozilla/bleach";
        license = licenses.asl20;
        description = "An easy safelist-based HTML-sanitizing tool.";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2019.11.28";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/41/bf/9d214a5af07debc6acf7f3f257265618f1db242a3f8e49a9b516f24523a6/certifi-2019.11.28.tar.gz";
        sha256 =
          "25b64c7da4cd7479594d035c08c2d809eb4aab3a26e5a990ea98cc450c320f1f";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://certifi.io/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };

    "cffi" = python.mkDerivation {
      name = "cffi-1.14.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/05/54/3324b0c46340c31b909fcec598696aaec7ddc8c18a63f2db352562d3354c/cffi-1.14.0.tar.gz";
        sha256 =
          "2d384f4a127a15ba701207f7639d94106693b6cd64173d6c8988e2c25f3ac2b6";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."pycparser" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://cffi.readthedocs.org";
        license = licenses.mit;
        description = "Foreign Function Interface for Python calling C code.";
      };
    };

    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz";
        sha256 =
          "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };

    "click" = python.mkDerivation {
      name = "click-7.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/f8/5c/f60e9d8a1e77005f664b76ff8aeaee5bc05d0a91798afd7f53fc998dbc47/Click-7.0.tar.gz";
        sha256 =
          "5b94b49521f6456670fdb30cd82a4eca9412788a93fa6dd6df72c94d5a8ff2d7";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/click/";
        license = licenses.bsdOriginal;
        description = "Composable command line interface toolkit";
      };
    };

    "coverage" = python.mkDerivation {
      name = "coverage-5.0.3";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/6d/1d/d44ed71d9a254453f4dd296cadf497957454995a35defcc7a7424caec89d/coverage-5.0.3.tar.gz";
        sha256 =
          "77afca04240c40450c331fa796b3eab6f1e15c5ecf8bf2b8bee9706cd5452fef";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/nedbat/coveragepy";
        license = licenses.asl20;
        description = "Code coverage measurement for Python";
      };
    };

    "cryptography" = python.mkDerivation {
      name = "cryptography-2.8";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/be/60/da377e1bed002716fb2d5d1d1cab720f298cb33ecff7bf7adea72788e4e4/cryptography-2.8.tar.gz";
        sha256 =
          "3cda1f0ed8747339bbdf71b9f38ca74c7b592f24f65cdb3ab3765e4b02871651";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."cffi" self."setuptools" self."wheel" ];
      propagatedBuildInputs = [ self."cffi" self."six" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pyca/cryptography";
        license = licenses.asl20;
        description =
          "cryptography is a package which provides cryptographic recipes and primitives to Python developers.";
      };
    };

    "docutils" = python.mkDerivation {
      name = "docutils-0.16";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/2f/e0/3d435b34abd2d62e8206171892f174b180cd37b09d57b924ca5c2ef2219d/docutils-0.16.tar.gz";
        sha256 =
          "c2de3a60e9e7d07be26b7f2b00ca0309c207e06c100f9cc2a94931fc75a478fc";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docutils.sourceforge.net/";
        license = licenses.publicDomain;
        description = "Docutils -- Python Documentation Utilities";
      };
    };

    "effect" = python.mkDerivation {
      name = "effect-1.1.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/31/7a/3c7a4568ed3a8fa463ffabbc70ed9471d82daad4e479b305d299bec72b49/effect-1.1.0.tar.gz";
        sha256 =
          "7affb603707c648b07b11781ebb793a4b9aee8acf1ac5764c3ed2112adf0c9ea";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."attrs" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/python-effect/effect/";
        license = licenses.mit;
        description = "pure effects for Python";
      };
    };

    "entrypoints" = python.mkDerivation {
      name = "entrypoints-0.3";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/b4/ef/063484f1f9ba3081e920ec9972c96664e2edb9fdc3d8669b0e3b8fc0ad7c/entrypoints-0.3.tar.gz";
        sha256 =
          "c70dd71abe5a8c85e55e12c19bd91ccfeec11a6e99044204511f9ed547d48451";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."flit" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/takluyver/entrypoints";
        license = licenses.mit;
        description = "Discover and load entry points from installed packages.";
      };
    };

    "flake8" = python.mkDerivation {
      name = "flake8-3.7.9";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/a5/bb/7e707d8001aca96f15f684b02176ecb0575786f041293f090b44ea04f2d0/flake8-3.7.9.tar.gz";
        sha256 =
          "45681a117ecc81e870cbf1262835ae4af5e7a8b08e40b944a8a6e6b895914cfb";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs =
        [ self."entrypoints" self."mccabe" self."pycodestyle" self."pyflakes" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://gitlab.com/pycqa/flake8";
        license = licenses.mit;
        description = "the modular source code checker: pep8, pyflakes and co";
      };
    };

    "flit" = python.mkDerivation {
      name = "flit-2.2.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/35/87/a92625dc5c81cf1608553b27b5c216bdc1e678ea6738a3a8a69ee2e5fb51/flit-2.2.0.tar.gz";
        sha256 =
          "a273dc2a5ab1f42f0e02878347d94f5462c42cbe232a5014b6778c9e5975327f";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."flit-core" ];
      propagatedBuildInputs =
        [ self."docutils" self."flit-core" self."pytoml" self."requests" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/takluyver/flit";
        license = licenses.bsdOriginal;
        description = "A simple packaging tool for simple packages.";
      };
    };

    "flit-core" = python.mkDerivation {
      name = "flit-core-2.2.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/77/72/5dda5dc417a4e702e0d7e4a77e9802792a0e4a2daec2aeed915ead7db477/flit_core-2.2.0.tar.gz";
        sha256 =
          "4efb8bffc1a04d8e550e877f0c9acf53109a021cc27c2a89b1b467715dc1d657";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."intreehooks" ];
      propagatedBuildInputs = [ self."pytoml" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/takluyver/flit";
        license = licenses.bsdOriginal;
        description =
          "Distribution-building parts of Flit. See flit package for more information";
      };
    };

    "idna" = python.mkDerivation {
      name = "idna-2.8";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/ad/13/eb56951b6f7950cadb579ca166e448ba77f9d24efc03edd7e55fa57d04b7/idna-2.8.tar.gz";
        sha256 =
          "c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };

    "importlib-metadata" = python.mkDerivation {
      name = "importlib-metadata-1.5.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/0d/e4/638f3bde506b86f62235c595073066e7b8472fc9ee2b8c6491347f31d726/importlib_metadata-1.5.0.tar.gz";
        sha256 =
          "06f5b3a99029c7134207dd882428a66992a9de2bef7c2b699b5641f9886c3302";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [ self."zipp" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://importlib-metadata.readthedocs.io/";
        license = licenses.asl20;
        description = "Read metadata from Python packages";
      };
    };

    "intreehooks" = python.mkDerivation {
      name = "intreehooks-1.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/f9/a5/5dacebf93232a847970921af2b020f9f2a8e0064e3a97727cd38efc77ba0/intreehooks-1.0.tar.gz";
        sha256 =
          "87e600d3b16b97ed219c078681260639e77ef5a17c0e0dbdd5a302f99b4e34e1";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."pytoml" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/takluyver/intreehooks";
        license = licenses.mit;
        description = "Load a PEP 517 backend from inside the source tree";
      };
    };

    "jeepney" = python.mkDerivation {
      name = "jeepney-0.4.2";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/47/ce/f32852260f93a5b25bbd30f013ce7df1f7df531ff2f4cbed54e726ce6c6f/jeepney-0.4.2.tar.gz";
        sha256 =
          "0ba6d8c597e9bef1ebd18aaec595f942a264e25c1a48f164d46120eacaa2e9bb";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."flit-core" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://gitlab.com/takluyver/jeepney";
        license = licenses.mit;
        description = "Low-level, pure Python DBus protocol wrapper.";
      };
    };

    "jinja2" = python.mkDerivation {
      name = "jinja2-2.11.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/d8/03/e491f423379ea14bb3a02a5238507f7d446de639b623187bccc111fbecdf/Jinja2-2.11.1.tar.gz";
        sha256 =
          "93187ffbc7808079673ef52771baa950426fd664d3aad1d0fa3e95644360e250";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."markupsafe" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/jinja/";
        license = licenses.bsdOriginal;
        description = "A very fast and expressive template engine.";
      };
    };

    "keyring" = python.mkDerivation {
      name = "keyring-21.1.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/7e/70/399b955e814380568c1f2e98145d37f0467b79531766b687bc27eb873a0a/keyring-21.1.0.tar.gz";
        sha256 =
          "1f393f7466314068961c7e1d508120c092bd71fa54e3d93b76180b526d4abc56";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs =
        [ self."importlib-metadata" self."jeepney" self."secretstorage" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jaraco/keyring";
        license = licenses.mit;
        description = "Store and access your passwords safely.";
      };
    };

    "markupsafe" = python.mkDerivation {
      name = "markupsafe-1.1.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/b9/2e/64db92e53b86efccfaea71321f597fa2e1b2bd3853d8ce658568f7a13094/MarkupSafe-1.1.1.tar.gz";
        sha256 =
          "29872e92839765e546828bb7754a68c418d927cd064fd4708fab9fe9c8bb116b";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/markupsafe/";
        license = licenses.bsdOriginal;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "mccabe" = python.mkDerivation {
      name = "mccabe-0.6.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/06/18/fa675aa501e11d6d6ca0ae73a101b2f3571a565e0f7d38e062eec18a91ee/mccabe-0.6.1.tar.gz";
        sha256 =
          "dd8d182285a0fe56bace7f45b5e7d1a6ebcbf524e8f3bd87eb0f125271b8831f";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pycqa/mccabe";
        license = licenses.mit;
        description = "McCabe checker, plugin for flake8";
      };
    };

    "more-itertools" = python.mkDerivation {
      name = "more-itertools-8.2.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/a0/47/6ff6d07d84c67e3462c50fa33bf649cda859a8773b53dc73842e84455c05/more-itertools-8.2.0.tar.gz";
        sha256 =
          "b1ddb932186d8a6ac451e1d95844b382f55e12686d51ca0c68b6f61f2ab7a507";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/erikrose/more-itertools";
        license = licenses.mit;
        description =
          "More routines for operating on iterables, beyond itertools";
      };
    };

    "mypy" = python.mkDerivation {
      name = "mypy-0.761";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/71/8a/9afc9f297d482a35cea32dc43fdbf11853eeeb93141738e81ea1b02f09f2/mypy-0.761.tar.gz";
        sha256 =
          "85baab8d74ec601e86134afe2bcccd87820f79d2f8d5798c889507d1088287bf";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs =
        [ self."mypy-extensions" self."typed-ast" self."typing-extensions" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://www.mypy-lang.org/";
        license = licenses.mit;
        description = "Optional static typing for Python";
      };
    };

    "mypy-extensions" = python.mkDerivation {
      name = "mypy-extensions-0.4.3";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/63/60/0582ce2eaced55f65a4406fc97beba256de4b7a95a0034c6576458c6519f/mypy_extensions-0.4.3.tar.gz";
        sha256 =
          "2d82818f5bb3e369420cb3c4060a7970edba416647068eb4c5343488a6c604a8";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/python/mypy_extensions";
        license = licenses.mit;
        description =
          "Experimental type system extensions for programs checked with the mypy typechecker.";
      };
    };

    "packaging" = python.mkDerivation {
      name = "packaging-20.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/7b/d5/199f982ae38231995276421377b72f4a25d8251f4fa56f6be7cfcd9bb022/packaging-20.1.tar.gz";
        sha256 =
          "e665345f9eef0c621aa0bf2f8d78cf6d21904eef16a93f020240b704a57f1334";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."pyparsing" self."six" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/packaging";
        license = licenses.asl20;
        description = "Core utilities for Python packages";
      };
    };

    "pathspec" = python.mkDerivation {
      name = "pathspec-0.7.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/ce/f2/d35c292da8fbff725625a17ae40f48f933070acd5ccddb03d8c09d81758d/pathspec-0.7.0.tar.gz";
        sha256 =
          "562aa70af2e0d434367d9790ad37aed893de47f1693e4201fd1d3dca15d19b96";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/cpburnz/python-path-specification";
        license = licenses.mpl20;
        description =
          "Utility library for gitignore style pattern matching of file paths.";
      };
    };

    "pkginfo" = python.mkDerivation {
      name = "pkginfo-1.5.0.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/6c/04/fd6683d24581894be8b25bc8c68ac7a0a73bf0c4d74b888ac5fe9a28e77f/pkginfo-1.5.0.1.tar.gz";
        sha256 =
          "7424f2c8511c186cd5424bbf31045b77435b37a8d604990b79d4e70d741148bb";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://code.launchpad.net/~tseaver/pkginfo/trunk";
        license = licenses.mit;
        description =
          "Query metadatdata from sdists / bdists / installed packages.";
      };
    };

    "pluggy" = python.mkDerivation {
      name = "pluggy-0.13.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/f8/04/7a8542bed4b16a65c2714bf76cf5a0b026157da7f75e87cc88774aa10b14/pluggy-0.13.1.tar.gz";
        sha256 =
          "15b2acde666561e1298d71b523007ed7364de07029219b604cf808bfa1c765b0";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [ self."importlib-metadata" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pluggy";
        license = licenses.mit;
        description = "plugin and hook calling mechanisms for python";
      };
    };

    "py" = python.mkDerivation {
      name = "py-1.8.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/bd/8f/169d08dcac7d6e311333c96b63cbe92e7947778475e1a619b674989ba1ed/py-1.8.1.tar.gz";
        sha256 =
          "5e27081401262157467ad6e7f851b7aa402c5852dbcb3dae06768434de5752aa";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = licenses.mit;
        description =
          "library with cross-python path, ini-parsing, io, code, log facilities";
      };
    };

    "pycodestyle" = python.mkDerivation {
      name = "pycodestyle-2.5.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/1c/d1/41294da5915f4cae7f4b388cea6c2cd0d6cd53039788635f6875dfe8c72f/pycodestyle-2.5.0.tar.gz";
        sha256 =
          "e40a936c9a450ad81df37f549d676d127b1b66000a6c500caa2b085bc0ca976c";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://pycodestyle.readthedocs.io/";
        license = licenses.mit;
        description = "Python style guide checker";
      };
    };

    "pycparser" = python.mkDerivation {
      name = "pycparser-2.19";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/68/9e/49196946aee219aead1290e00d1e7fdeab8567783e83e1b9ab5585e6206a/pycparser-2.19.tar.gz";
        sha256 =
          "a988718abfad80b6b157acce7bf130a30876d27603738ac39f140993246b25b3";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/eliben/pycparser";
        license = licenses.bsdOriginal;
        description = "C parser in Python";
      };
    };

    "pyflakes" = python.mkDerivation {
      name = "pyflakes-2.1.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/52/64/87303747635c2988fcaef18af54bfdec925b6ea3b80bcd28aaca5ba41c9e/pyflakes-2.1.1.tar.gz";
        sha256 =
          "d976835886f8c5b31d47970ed689944a0262b5f3afa00a5a7b4dc81e5449f8a2";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/PyCQA/pyflakes";
        license = licenses.mit;
        description = "passive checker of Python programs";
      };
    };

    "pygments" = python.mkDerivation {
      name = "pygments-2.5.2";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/cb/9f/27d4844ac5bf158a33900dbad7985951e2910397998e85712da03ce125f0/Pygments-2.5.2.tar.gz";
        sha256 =
          "98c8aa5a9f778fcd1026a17361ddaf7330d1b7c62ae97c3bb0ae73e0b9b6b0fe";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pygments.org/";
        license = licenses.bsdOriginal;
        description =
          "Pygments is a syntax highlighting package written in Python.";
      };
    };

    "pyparsing" = python.mkDerivation {
      name = "pyparsing-2.4.6";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/a2/56/0404c03c83cfcca229071d3c921d7d79ed385060bbe969fde3fd8f774ebd/pyparsing-2.4.6.tar.gz";
        sha256 =
          "4c830582a84fb022400b85429791bc551f1f4871c33f23e44f353119e92f969f";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pyparsing/pyparsing/";
        license = licenses.mit;
        description = "Python parsing module";
      };
    };

    "pytest" = python.mkDerivation {
      name = "pytest-5.3.5";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/f0/5f/41376614e41f7cdee02d22d1aec1ea028301b4c6c4523a5f7ef8e960fe0b/pytest-5.3.5.tar.gz";
        sha256 =
          "0d5fe9189a148acc3c3eb2ac8e1ac0742cb7618c084f3d228baaec0c254b318d";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [
        self."attrs"
        self."importlib-metadata"
        self."more-itertools"
        self."packaging"
        self."pluggy"
        self."py"
        self."wcwidth"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pytest.org/en/latest/";
        license = licenses.mit;
        description = "pytest: simple powerful testing with Python";
      };
    };

    "pytest-black" = python.mkDerivation {
      name = "pytest-black-0.3.8";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/3d/e9/2f3605f3922c1650cd43433be704a58773ee9baeb78731cc896822c2cc57/pytest-black-0.3.8.tar.gz";
        sha256 =
          "01a9a7acc69e618ebf3f834932a4d7a81909f6911051d0871b0ed4de3cbe9712";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."black" self."pytest" self."toml" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/shopkeep/pytest-black";
        license = licenses.mit;
        description = "A pytest plugin to enable format checking with black";
      };
    };

    "pytest-cov" = python.mkDerivation {
      name = "pytest-cov-2.8.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/13/8a/51f54b43a043c799bceca846594b9a310823a3e52df5ec27109cccba90f4/pytest-cov-2.8.1.tar.gz";
        sha256 =
          "cc6742d8bac45070217169f5f72ceee1e0e55b0221f54bcf24845972d3a47f2b";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."coverage" self."pytest" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-cov";
        license = licenses.bsdOriginal;
        description = "Pytest plugin for measuring coverage.";
      };
    };

    "pytest-runner" = python.mkDerivation {
      name = "pytest-runner-5.2";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/5b/82/1462f86e6c3600f2471d5f552fcc31e39f17717023df4bab712b4a9db1b3/pytest-runner-5.2.tar.gz";
        sha256 =
          "96c7e73ead7b93e388c5d614770d2bae6526efd997757d3543fe17b557a0942b";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-runner/";
        license = licenses.mit;
        description =
          "Invoke py.test as distutils command with dependency resolution";
      };
    };

    "pytoml" = python.mkDerivation {
      name = "pytoml-0.1.21";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/f4/ba/98ee2054a2d7b8bebd367d442e089489250b6dc2aee558b000e961467212/pytoml-0.1.21.tar.gz";
        sha256 =
          "8eecf7c8d0adcff3b375b09fe403407aa9b645c499e5ab8cac670ac4a35f61e7";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/avakar/pytoml";
        license = licenses.mit;
        description = "A parser for TOML-0.4.0";
      };
    };

    "readme-renderer" = python.mkDerivation {
      name = "readme-renderer-24.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/44/de/a567140b13a0fc8d3b04d85a510b5a7d9869b44b2939fa8ac07c5e421485/readme_renderer-24.0.tar.gz";
        sha256 =
          "bb16f55b259f27f75f640acf5e00cf897845a8b3e4731b5c1a436e4b8529202f";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs =
        [ self."bleach" self."docutils" self."pygments" self."six" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/readme_renderer";
        license = licenses.asl20;
        description = "readme_renderer is a library for rendering " readme
          " descriptions for Warehouse";
      };
    };

    "regex" = python.mkDerivation {
      name = "regex-2020.1.8";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/73/d9/b58289d885180b5d538aa6df07974b5fe6088547ac846c0f76f77259c304/regex-2020.1.8.tar.gz";
        sha256 =
          "d0f424328f9822b0323b3b6f2e4b9c90960b24743d220763c7f07071e0778351";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/mrabarnett/mrab-regex";
        license = licenses.psfl;
        description = "Alternative regular expression module, to replace re.";
      };
    };

    "requests" = python.mkDerivation {
      name = "requests-2.22.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/01/62/ddcf76d1d19885e8579acb1b1df26a852b03472c0e46d2b959a714c90608/requests-2.22.0.tar.gz";
        sha256 =
          "11e007a8a2aa0323f5a921e9e6a2d7e4e67d9877e85773fba9ba6419025cbeb4";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs =
        [ self."certifi" self."chardet" self."idna" self."urllib3" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-requests.org";
        license = licenses.asl20;
        description = "Python HTTP for Humans.";
      };
    };

    "requests-toolbelt" = python.mkDerivation {
      name = "requests-toolbelt-0.9.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/28/30/7bf7e5071081f761766d46820e52f4b16c8a08fef02d2eb4682ca7534310/requests-toolbelt-0.9.1.tar.gz";
        sha256 =
          "968089d4584ad4ad7c171454f0a5c6dac23971e9472521ea3b6d49d610aa6fc0";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ self."requests" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://toolbelt.readthedocs.org";
        license = licenses.asl20;
        description = "A utility belt for advanced users of python-requests";
      };
    };

    "secretstorage" = python.mkDerivation {
      name = "secretstorage-3.1.2";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/fd/9f/36197c75d9a09b1ab63f56cb985af6cd858ca3fc41fd9cd890ce69bae5b9/SecretStorage-3.1.2.tar.gz";
        sha256 =
          "15da8a989b65498e29be338b3b279965f1b8f09b9668bd8010da183024c8bff6";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."setuptools" self."wheel" ];
      propagatedBuildInputs = [ self."cryptography" self."jeepney" ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mitya57/secretstorage";
        license = licenses.bsdOriginal;
        description = "Python bindings to FreeDesktop.org Secret Service API";
      };
    };

    "setuptools" = python.mkDerivation {
      name = "setuptools-45.2.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/68/75/d1d7b7340b9eb6e0388bf95729e63c410b381eb71fe8875cdfd949d8f9ce/setuptools-45.2.0.zip";
        sha256 =
          "89c6e6011ec2f6d57d43a3f9296c4ef022c2cbf49bab26b407fe67992ae3397f";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools";
        license = licenses.mit;
        description =
          "Easily download, build, install, upgrade, and uninstall Python packages";
      };
    };

    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.5.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/b2/f7/60a645aae001a2e06cf4b8db2fba9d9f36b8fd378f10647e3e218b61b74b/setuptools_scm-3.5.0.tar.gz";
        sha256 =
          "5bdf21a05792903cafe7ae0c9501182ab52497614fa6b1750d9dbae7b60c1a87";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs ++ [ self."setuptools" self."wheel" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.14.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/21/9f/b251f7f8a76dec1d6651be194dfba8fb8d7781d10ab3987190de8391d08e/six-1.14.0.tar.gz";
        sha256 =
          "236bdbdce46e6e6a3d61a337c0f8b763ca1e8717c03b369e87a7ec7ce1319c0a";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "toml" = python.mkDerivation {
      name = "toml-0.10.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/b9/19/5cbd78eac8b1783671c40e34bb0fa83133a06d340a38b55c645076d40094/toml-0.10.0.tar.gz";
        sha256 =
          "229f81c57791a41d65e399fc06bf0848bab550a9dfd5ed66df18ce5f05e73d5c";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/uiri/toml";
        license = licenses.mit;
        description = "Python Library for Tom's Obvious, Minimal Language";
      };
    };

    "tqdm" = python.mkDerivation {
      name = "tqdm-4.42.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/f7/83/9dc2296d40020ba54cbc711160577157d7aa3c2bbdcf6b245c96a7ba6f67/tqdm-4.42.1.tar.gz";
        sha256 =
          "251ee8440dbda126b8dfa8a7c028eb3f13704898caaef7caa699b35e119301e2";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/tqdm/tqdm";
        license = licenses.mit;
        description = "Fast, Extensible Progress Meter";
      };
    };

    "twine" = python.mkDerivation {
      name = "twine-3.1.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/7e/2f/e2a91a8ab97e8c9830ce297132631aef5dcd599f076123d1ebb26f1941b6/twine-3.1.1.tar.gz";
        sha256 =
          "d561a5e511f70275e5a485a6275ff61851c16ffcb3a95a602189161112d9f160";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [
        self."importlib-metadata"
        self."keyring"
        self."pkginfo"
        self."readme-renderer"
        self."requests"
        self."requests-toolbelt"
        self."setuptools"
        self."tqdm"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://twine.readthedocs.io/";
        license = licenses.asl20;
        description = "Collection of utilities for publishing packages on PyPI";
      };
    };

    "typed-ast" = python.mkDerivation {
      name = "typed-ast-1.4.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/18/09/b6a6b14bb8c5ec4a24fe0cf0160aa0b784fd55a6fd7f8da602197c5c461e/typed_ast-1.4.1.tar.gz";
        sha256 =
          "8c8aaad94455178e3187ab22c8b01a3837f8ee50e09cf31f1ba129eb293ec30b";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/python/typed_ast";
        license = licenses.asl20;
        description =
          "a fork of Python 2 and 3 ast modules with type comment support";
      };
    };

    "typing-extensions" = python.mkDerivation {
      name = "typing-extensions-3.7.4.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/e7/dd/f1713bc6638cc3a6a23735eff6ee09393b44b96176d3296693ada272a80b/typing_extensions-3.7.4.1.tar.gz";
        sha256 =
          "091ecc894d5e908ac75209f10d5b4f118fbdb2eb1ede6a63544054bb1edb41f2";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage =
          "https://github.com/python/typing/blob/master/typing_extensions/README.rst";
        license = licenses.psfl;
        description = "Backported and Experimental Type Hints for Python 3.5+";
      };
    };

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.25.8";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/09/06/3bc5b100fe7e878d3dee8f807a4febff1a40c213d2783e3246edde1f3419/urllib3-1.25.8.tar.gz";
        sha256 =
          "87716c2d2a7121198ebcb7ce7cccf6ce5e9ba539041cfbaeecfb641dc0bf6acc";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://urllib3.readthedocs.io/";
        license = licenses.mit;
        description =
          "HTTP library with thread-safe connection pooling, file post, and more.";
      };
    };

    "wcwidth" = python.mkDerivation {
      name = "wcwidth-0.1.8";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/5e/33/92333eb80be0c96385dee338f30b53e24a8b415d5785e225d789b3f90feb/wcwidth-0.1.8.tar.gz";
        sha256 =
          "f28b3e8a6483e5d49e7f8949ac1a78314e740333ae305b4ba5defd3e74fb37a8";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jquast/wcwidth";
        license = licenses.mit;
        description =
          "Measures number of Terminal column cells of wide-character codes";
      };
    };

    "webencodings" = python.mkDerivation {
      name = "webencodings-0.5.1";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/0b/02/ae6ceac1baeda530866a85075641cec12989bd8d31af6d5ab4a3e8c92f47/webencodings-0.5.1.tar.gz";
        sha256 =
          "b36a1c245f2d304965eb4e0a82848379241dc04b865afcc4aab16748587e1923";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/SimonSapin/python-webencodings";
        license = licenses.bsdOriginal;
        description = "Character encoding aliases for legacy web content";
      };
    };

    "wheel" = python.mkDerivation {
      name = "wheel-0.34.2";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/75/28/521c6dc7fef23a68368efefdcd682f5b3d1d58c2b90b06dc1d0b805b51ae/wheel-0.34.2.tar.gz";
        sha256 =
          "8788e9155fe14f54164c1b9eb0a319d98ef02c160725587ad60f14ddc57b6f96";
      };
      doCheck = commonDoCheck;
      format = "setuptools";
      buildInputs = commonBuildInputs ++ [ self."setuptools" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/wheel";
        license = licenses.mit;
        description = "A built-package format for Python";
      };
    };

    "zipp" = python.mkDerivation {
      name = "zipp-2.2.0";
      src = pkgs.fetchurl {
        url =
          "https://files.pythonhosted.org/packages/60/85/668bca4a9ef474ca634c993e768f12bd99af1f06bb90bb2655bc538a967e/zipp-2.2.0.tar.gz";
        sha256 =
          "5c56e330306215cd3553342cfafc73dda2c60792384117893f3a83f8a1209f50";
      };
      doCheck = commonDoCheck;
      format = "pyproject";
      buildInputs = commonBuildInputs
        ++ [ self."setuptools" self."setuptools-scm" self."wheel" ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/jaraco/zipp";
        license = licenses.mit;
        description =
          "Backport of pathlib-compatible object wrapper for zip files";
      };
    };
  };
  localOverridesFile = ./requirements_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
    (let
      src = pkgs.fetchFromGitHub {
        owner = "nix-community";
        repo = "pypi2nix-overrides";
        rev = "fbbcadd9e5fedade659ba2585893d3a8cbba8e56";
        sha256 = "1fmqib6j08lswfw0agbgy1hdib3rfmrzx2x5zyzrqbkvc80a734b";
      };
    in import "${src}/overrides.nix" { inherit pkgs python; })
  ];
  paramOverrides = [ (overrides { inherit pkgs python; }) ];
  allOverrides = (if (builtins.pathExists localOverridesFile) then
    [ localOverrides ]
  else
    [ ]) ++ commonOverrides ++ paramOverrides;

in python.withPackages (fix' (pkgs.lib.fold extends generated allOverrides))
