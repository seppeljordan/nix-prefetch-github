# generated using pypi2nix tool (version: 2.0.0)
# See more at: https://github.com/garbas/pypi2nix
#
# COMMAND:
#   pypi2nix -V 3 --default-overrides -r requirements.txt -s setuptool-scm -e readme_renderer -e ./.#egg=nix-prefetch-github
#

{ pkgs ? import <nixpkgs> {},
  overrides ? ({ pkgs, python }: self: super: {})
}:

let

  inherit (pkgs) makeWrapper;
  inherit (pkgs.stdenv.lib) fix' extends inNixShell;

  pythonPackages =
  import "${toString pkgs.path}/pkgs/top-level/python-packages.nix" {
    inherit pkgs;
    inherit (pkgs) stdenv;
    python = pkgs.python3;
    # patching pip so it does not try to remove files when running nix-shell
    overrides =
      self: super: {
        bootstrapped-pip = super.bootstrapped-pip.overrideDerivation (old: {
          patchPhase = old.patchPhase + ''
            if [ -e $out/${pkgs.python3.sitePackages}/pip/req/req_install.py ]; then
              sed -i \
                -e "s|paths_to_remove.remove(auto_confirm)|#paths_to_remove.remove(auto_confirm)|"  \
                -e "s|self.uninstalled = paths_to_remove|#self.uninstalled = paths_to_remove|"  \
                $out/${pkgs.python3.sitePackages}/pip/req/req_install.py
            fi
          '';
        });
      };
  };

  commonBuildInputs = [];
  commonDoCheck = false;

  withPackages = pkgs':
    let
      pkgs = builtins.removeAttrs pkgs' ["__unfix__"];
      interpreterWithPackages = selectPkgsFn: pythonPackages.buildPythonPackage {
        name = "python3-interpreter";
        buildInputs = [ makeWrapper ] ++ (selectPkgsFn pkgs);
        buildCommand = ''
          mkdir -p $out/bin
          ln -s ${pythonPackages.python.interpreter} \
              $out/bin/${pythonPackages.python.executable}
          for dep in ${builtins.concatStringsSep " "
              (selectPkgsFn pkgs)}; do
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
      mkDerivation = pythonPackages.buildPythonPackage;
      packages = pkgs;
      overrideDerivation = drv: f:
        pythonPackages.buildPythonPackage (
          drv.drvAttrs // f drv.drvAttrs // { meta = drv.meta; }
        );
      withPackages = pkgs'':
        withPackages (pkgs // pkgs'');
    };

  python = withPackages {};

  generated = self: {
    "Click" = python.mkDerivation {
      name = "Click-7.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f8/5c/f60e9d8a1e77005f664b76ff8aeaee5bc05d0a91798afd7f53fc998dbc47/Click-7.0.tar.gz";
        sha256 = "5b94b49521f6456670fdb30cd82a4eca9412788a93fa6dd6df72c94d5a8ff2d7";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://palletsprojects.com/p/click/";
        license = licenses.bsdOriginal;
        description = "Composable command line interface toolkit";
      };
    };

    "Jinja2" = python.mkDerivation {
      name = "Jinja2-2.10";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/56/e6/332789f295cf22308386cf5bbd1f4e00ed11484299c5d7383378cf48ba47/Jinja2-2.10.tar.gz";
        sha256 = "f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."MarkupSafe"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://jinja.pocoo.org/";
        license = licenses.bsdOriginal;
        description = "A small but fast and easy to use stand-alone template engine written in pure python.";
      };
    };

    "MarkupSafe" = python.mkDerivation {
      name = "MarkupSafe-1.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ac/7e/1b4c2e05809a4414ebce0892fe1e32c14ace86ca7d50c70f00979ca9b3a3/MarkupSafe-1.1.0.tar.gz";
        sha256 = "4e97332c9ce444b0c2c38dd22ddc61c743eb208d916e4265a2a3b575bdccb1d3";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.palletsprojects.com/p/markupsafe/";
        license = licenses.bsdOriginal;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "Pygments" = python.mkDerivation {
      name = "Pygments-2.3.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/64/69/413708eaf3a64a6abb8972644e0f20891a55e621c6759e2c3f3891e05d63/Pygments-2.3.1.tar.gz";
        sha256 = "5ffada19f6203563680669ee7f53b64dabbeb100eb51b61996085e99c03b284a";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pygments.org/";
        license = licenses.bsdOriginal;
        description = "Pygments is a syntax highlighting package written in Python.";
      };
    };

    "atomicwrites" = python.mkDerivation {
      name = "atomicwrites-1.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ec/0f/cd484ac8820fed363b374af30049adc8fd13065720fd4f4c6be8a2309da7/atomicwrites-1.3.0.tar.gz";
        sha256 = "75a9445bac02d8d058d5e1fe689654ba5a6556a1dfd8ce6ec55a0ed79866cfa6";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/untitaker/python-atomicwrites";
        license = licenses.mit;
        description = "Atomic file writes.";
      };
    };

    "attrs" = python.mkDerivation {
      name = "attrs-18.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0f/9e/26b1d194aab960063b266170e53c39f73ea0d0d3f5ce23313e0ec8ee9bdf/attrs-18.2.0.tar.gz";
        sha256 = "10cbf6e27dbce8c30807caf056c8eb50917e0eaafe86347671b57254006c3e69";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };

    "bleach" = python.mkDerivation {
      name = "bleach-3.1.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/78/5a/0df03e8735cd9c75167528299c738702437589b9c71a849489d00ffa82e8/bleach-3.1.0.tar.gz";
        sha256 = "3fdf7f77adcf649c9911387df51254b813185e32b2c6619f690b593a617e19fa";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."six"
        self."webencodings"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mozilla/bleach";
        license = "Apache Software License";
        description = "An easy safelist-based HTML-sanitizing tool.";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2018.11.29";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/55/54/3ce77783acba5979ce16674fc98b1920d00b01d337cfaaf5db22543505ed/certifi-2018.11.29.tar.gz";
        sha256 = "47f9c83ef4c0c621eaef743f133f09fa8a74a9b75f037e8624f83bd1b6626cb7";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://certifi.io/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };

    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz";
        sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl3;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };

    "coverage" = python.mkDerivation {
      name = "coverage-4.5.2";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/fb/af/ce7b0fe063ee0142786ee53ad6197979491ce0785567b6d8be751d2069e8/coverage-4.5.2.tar.gz";
        sha256 = "ab235d9fe64833f12d1334d29b558aacedfbca2356dfb9691f2d0d38a8a7bfb4";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/ned/coveragepy";
        license = licenses.asl20;
        description = "Code coverage measurement for Python";
      };
    };

    "docutils" = python.mkDerivation {
      name = "docutils-0.14";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/84/f4/5771e41fdf52aabebbadecc9381d11dea0fa34e4759b4071244fa094804c/docutils-0.14.tar.gz";
        sha256 = "51e64ef2ebfb29cae1faa133b3710143496eca21c530f3f71424d77687764274";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docutils.sourceforge.net/";
        license = "public domain, Python, 2-Clause BSD, GPL 3 (see COPYING.txt)";
        description = "Docutils -- Python Documentation Utilities";
      };
    };

    "effect" = python.mkDerivation {
      name = "effect-0.12.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e0/48/9b8f44c0ce230cb88abf1addc3efb266c2df02a325c8bf453c7a0de0b374/effect-0.12.0.tar.gz";
        sha256 = "f43322b269b2dca0c15856f090b9167d8499bf474ec64696c80a508299d51f69";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."attrs"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/python-effect/effect/";
        license = licenses.mit;
        description = "pure effects for Python";
      };
    };

    "idna" = python.mkDerivation {
      name = "idna-2.8";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/ad/13/eb56951b6f7950cadb579ca166e448ba77f9d24efc03edd7e55fa57d04b7/idna-2.8.tar.gz";
        sha256 = "c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };

    "more-itertools" = python.mkDerivation {
      name = "more-itertools-6.0.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/dd/f4/cdfbb6f07f767e0cd8a11b16adfecc735b6eb87dbebda026ce8898e1cc22/more-itertools-6.0.0.tar.gz";
        sha256 = "590044e3942351a1bdb1de960b739ff4ce277960f2425ad4509446dbace8d9d1";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/erikrose/more-itertools";
        license = licenses.mit;
        description = "More routines for operating on iterables, beyond itertools";
      };
    };

    "nix-prefetch-github" = python.mkDerivation {
      name = "nix-prefetch-github-2.0";
      src = pkgs.lib.cleanSource ./.;
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."Click"
        self."Jinja2"
        self."attrs"
        self."effect"
        self."requests"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/seppeljordan/nix-prefetch-github";
        license = "GPL3";
        description = "Prefetch source code from github for nix build tool";
      };
    };

    "pkginfo" = python.mkDerivation {
      name = "pkginfo-1.5.0.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/6c/04/fd6683d24581894be8b25bc8c68ac7a0a73bf0c4d74b888ac5fe9a28e77f/pkginfo-1.5.0.1.tar.gz";
        sha256 = "7424f2c8511c186cd5424bbf31045b77435b37a8d604990b79d4e70d741148bb";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."coverage"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://code.launchpad.net/~tseaver/pkginfo/trunk";
        license = licenses.mit;
        description = "Query metadatdata from sdists / bdists / installed packages.";
      };
    };

    "pluggy" = python.mkDerivation {
      name = "pluggy-0.8.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/38/e1/83b10c17688af7b2998fa5342fec58ecbd2a5a7499f31e606ae6640b71ac/pluggy-0.8.1.tar.gz";
        sha256 = "8ddc32f03971bfdf900a81961a48ccf2fb677cf7715108f85295c67405798616";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pluggy";
        license = "MIT license";
        description = "plugin and hook calling mechanisms for python";
      };
    };

    "py" = python.mkDerivation {
      name = "py-1.8.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/f1/5a/87ca5909f400a2de1561f1648883af74345fe96349f34f737cdfc94eba8c/py-1.8.0.tar.gz";
        sha256 = "dc639b046a6e2cff5bbe40194ad65936d6ba360b52b3c3fe1d08a82dd50b5e53";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [
        self."setuptools-scm"
      ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = "MIT license";
        description = "library with cross-python path, ini-parsing, io, code, log facilities";
      };
    };

    "pytest" = python.mkDerivation {
      name = "pytest-4.3.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/7c/02/b35c0a322e332544716a0c598f8208ba3474fa94706183c26465d833b283/pytest-4.3.0.tar.gz";
        sha256 = "067a1d4bf827ffdd56ad21bd46674703fce77c5957f6c1eef731f6146bfcef1c";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."atomicwrites"
        self."attrs"
        self."more-itertools"
        self."pluggy"
        self."py"
        self."requests"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://docs.pytest.org/en/latest/";
        license = "MIT license";
        description = "pytest: simple powerful testing with Python";
      };
    };

    "pytest-cov" = python.mkDerivation {
      name = "pytest-cov-2.6.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/54/16/4229c5514d12b25c3555ca775c7c3cade9a63da99b52fd5fc45962fa3d29/pytest-cov-2.6.1.tar.gz";
        sha256 = "0ab664b25c6aa9716cbf203b17ddb301932383046082c081b9848a0edf5add33";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."coverage"
        self."pytest"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-cov";
        license = licenses.mit;
        description = "Pytest plugin for measuring coverage.";
      };
    };

    "readme-renderer" = python.mkDerivation {
      name = "readme-renderer-24.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/44/de/a567140b13a0fc8d3b04d85a510b5a7d9869b44b2939fa8ac07c5e421485/readme_renderer-24.0.tar.gz";
        sha256 = "bb16f55b259f27f75f640acf5e00cf897845a8b3e4731b5c1a436e4b8529202f";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."Pygments"
        self."bleach"
        self."docutils"
        self."six"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/readme_renderer";
        license = licenses.asl20;
        description = "readme_renderer is a library for rendering \"readme\" descriptions for Warehouse";
      };
    };

    "requests" = python.mkDerivation {
      name = "requests-2.21.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/52/2c/514e4ac25da2b08ca5a464c50463682126385c4272c18193876e91f4bc38/requests-2.21.0.tar.gz";
        sha256 = "502a824f31acdacb3a35b6690b5fbf0bc41d63a24a45c4004352b0242707598e";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."certifi"
        self."chardet"
        self."idna"
        self."urllib3"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://python-requests.org";
        license = licenses.asl20;
        description = "Python HTTP for Humans.";
      };
    };

    "requests-toolbelt" = python.mkDerivation {
      name = "requests-toolbelt-0.9.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/28/30/7bf7e5071081f761766d46820e52f4b16c8a08fef02d2eb4682ca7534310/requests-toolbelt-0.9.1.tar.gz";
        sha256 = "968089d4584ad4ad7c171454f0a5c6dac23971e9472521ea3b6d49d610aa6fc0";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."requests"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://toolbelt.readthedocs.org";
        license = licenses.asl20;
        description = "A utility belt for advanced users of python-requests";
      };
    };

    "setuptools-scm" = python.mkDerivation {
      name = "setuptools-scm-3.2.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/54/85/514ba3ca2a022bddd68819f187ae826986051d130ec5b972076e4f58a9f3/setuptools_scm-3.2.0.tar.gz";
        sha256 = "52ab47715fa0fc7d8e6cd15168d1a69ba995feb1505131c3e814eb7087b57358";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz";
        sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "tqdm" = python.mkDerivation {
      name = "tqdm-4.31.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/80/9b/f3036a9a11c250eb51d38acf94d1d7c33a0d4da8a8931bfdf15e12d505b1/tqdm-4.31.1.tar.gz";
        sha256 = "e22977e3ebe961f72362f6ddfb9197cc531c9737aaf5f607ef09740c849ecd05";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/tqdm/tqdm";
        license = "MPLv2.0, MIT Licences";
        description = "Fast, Extensible Progress Meter";
      };
    };

    "twine" = python.mkDerivation {
      name = "twine-1.13.0";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/e1/af/4f5bfaa8e9c0ddce229b058a4ebdc11a6e05e9c2e51b854d1d0e8f764d09/twine-1.13.0.tar.gz";
        sha256 = "d6c29c933ecfc74e9b1d9fa13aa1f87c5d5770e119f5a4ce032092f0ff5b14dc";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."pkginfo"
        self."readme-renderer"
        self."requests"
        self."requests-toolbelt"
        self."tqdm"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://twine.readthedocs.io/";
        license = licenses.asl20;
        description = "Collection of utilities for publishing packages on PyPI";
      };
    };

    "urllib3" = python.mkDerivation {
      name = "urllib3-1.24.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/b1/53/37d82ab391393565f2f831b8eedbffd57db5a718216f82f1a8b4d381a1c1/urllib3-1.24.1.tar.gz";
        sha256 = "de9529817c93f27c8ccbfead6985011db27bd0ddfcdb2d86f3f663385c6a9c22";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [
        self."certifi"
        self."idna"
      ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://urllib3.readthedocs.io/";
        license = licenses.mit;
        description = "HTTP library with thread-safe connection pooling, file post, and more.";
      };
    };

    "webencodings" = python.mkDerivation {
      name = "webencodings-0.5.1";
      src = pkgs.fetchurl {
        url = "https://files.pythonhosted.org/packages/0b/02/ae6ceac1baeda530866a85075641cec12989bd8d31af6d5ab4a3e8c92f47/webencodings-0.5.1.tar.gz";
        sha256 = "b36a1c245f2d304965eb4e0a82848379241dc04b865afcc4aab16748587e1923";
      };
      doCheck = commonDoCheck;
      buildInputs = commonBuildInputs ++ [ ];
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/SimonSapin/python-webencodings";
        license = licenses.bsdOriginal;
        description = "Character encoding aliases for legacy web content";
      };
    };
  };
  localOverridesFile = ./requirements_override.nix;
  localOverrides = import localOverridesFile { inherit pkgs python; };
  commonOverrides = [
        (let src = pkgs.fetchFromGitHub { owner = "garbas"; repo = "nixpkgs-python"; rev = "403bb1d312b1cfd82663208d7e9ae48c8ff2614a"; sha256 = "0v4gxikwh4362s40an68kj7dyiib1bcq5bn9m5j7h93yniz3zkd3"; } ; in import "${src}/overrides.nix" { inherit pkgs python; })
  ];
  paramOverrides = [
    (overrides { inherit pkgs python; })
  ];
  allOverrides =
    (if (builtins.pathExists localOverridesFile)
     then [localOverrides] else [] ) ++ commonOverrides ++ paramOverrides;

in python.withPackages
   (fix' (pkgs.lib.fold
            extends
            generated
            allOverrides
         )
   )