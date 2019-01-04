# generated using pypi2nix tool (version: 1.8.1)
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
    "Jinja2" = python.mkDerivation {
      name = "Jinja2-2.10";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/56/e6/332789f295cf22308386cf5bbd1f4e00ed11484299c5d7383378cf48ba47/Jinja2-2.10.tar.gz"; sha256 = "f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ac/7e/1b4c2e05809a4414ebce0892fe1e32c14ace86ca7d50c70f00979ca9b3a3/MarkupSafe-1.1.0.tar.gz"; sha256 = "4e97332c9ce444b0c2c38dd22ddc61c743eb208d916e4265a2a3b575bdccb1d3"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.palletsprojects.com/p/markupsafe/";
        license = licenses.bsdOriginal;
        description = "Safely add untrusted strings to HTML/XML markup.";
      };
    };

    "Pygments" = python.mkDerivation {
      name = "Pygments-2.3.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/64/69/413708eaf3a64a6abb8972644e0f20891a55e621c6759e2c3f3891e05d63/Pygments-2.3.1.tar.gz"; sha256 = "5ffada19f6203563680669ee7f53b64dabbeb100eb51b61996085e99c03b284a"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://pygments.org/";
        license = licenses.bsdOriginal;
        description = "Pygments is a syntax highlighting package written in Python.";
      };
    };

    "atomicwrites" = python.mkDerivation {
      name = "atomicwrites-1.2.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ac/ed/a311712ef6b4355035489f665e63e1a73f9eb371929e3c98e5efd451069e/atomicwrites-1.2.1.tar.gz"; sha256 = "ec9ae8adaae229e4f8446952d204a3e4b5fdd2d099f9be3aaf556120135fb3ee"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/untitaker/python-atomicwrites";
        license = licenses.mit;
        description = "Atomic file writes.";
      };
    };

    "attrs" = python.mkDerivation {
      name = "attrs-18.2.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/0f/9e/26b1d194aab960063b266170e53c39f73ea0d0d3f5ce23313e0ec8ee9bdf/attrs-18.2.0.tar.gz"; sha256 = "10cbf6e27dbce8c30807caf056c8eb50917e0eaafe86347671b57254006c3e69"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
      self."pytest"
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://www.attrs.org/";
        license = licenses.mit;
        description = "Classes Without Boilerplate";
      };
    };

    "bleach" = python.mkDerivation {
      name = "bleach-3.0.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ae/31/680afc7d44040004296a2d8f0584983c2f2386448cd9d0964197e6c1160e/bleach-3.0.2.tar.gz"; sha256 = "48d39675b80a75f6d1c3bdbffec791cf0bbbab665cf01e20da701c77de278718"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
      self."webencodings"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/mozilla/bleach";
        license = "License :: OSI Approved :: Apache Software License";
        description = "An easy safelist-based HTML-sanitizing tool.";
      };
    };

    "certifi" = python.mkDerivation {
      name = "certifi-2018.11.29";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/55/54/3ce77783acba5979ce16674fc98b1920d00b01d337cfaaf5db22543505ed/certifi-2018.11.29.tar.gz"; sha256 = "47f9c83ef4c0c621eaef743f133f09fa8a74a9b75f037e8624f83bd1b6626cb7"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://certifi.io/";
        license = licenses.mpl20;
        description = "Python package for providing Mozilla's CA Bundle.";
      };
    };

    "chardet" = python.mkDerivation {
      name = "chardet-3.0.4";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"; sha256 = "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/chardet/chardet";
        license = licenses.lgpl2;
        description = "Universal encoding detector for Python 2 and 3";
      };
    };

    "click" = python.mkDerivation {
      name = "click-6.7";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/95/d9/c3336b6b5711c3ab9d1d3a80f1a3e2afeb9d8c02a7166462f6cc96570897/click-6.7.tar.gz"; sha256 = "f15516df478d5a56180fbf80e68f206010e6d160fc39fa508b65e035fd75130b"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://github.com/mitsuhiko/click";
        license = licenses.bsdOriginal;
        description = "A simple wrapper around optparse for powerful command line utilities.";
      };
    };

    "coverage" = python.mkDerivation {
      name = "coverage-4.5.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/fb/af/ce7b0fe063ee0142786ee53ad6197979491ce0785567b6d8be751d2069e8/coverage-4.5.2.tar.gz"; sha256 = "ab235d9fe64833f12d1334d29b558aacedfbca2356dfb9691f2d0d38a8a7bfb4"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://bitbucket.org/ned/coveragepy";
        license = licenses.asl20;
        description = "Code coverage measurement for Python";
      };
    };

    "docutils" = python.mkDerivation {
      name = "docutils-0.14";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/84/f4/5771e41fdf52aabebbadecc9381d11dea0fa34e4759b4071244fa094804c/docutils-0.14.tar.gz"; sha256 = "51e64ef2ebfb29cae1faa133b3710143496eca21c530f3f71424d77687764274"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://docutils.sourceforge.net/";
        license = licenses.publicDomain;
        description = "Docutils -- Python Documentation Utilities";
      };
    };

    "effect" = python.mkDerivation {
      name = "effect-0.12.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/e0/48/9b8f44c0ce230cb88abf1addc3efb266c2df02a325c8bf453c7a0de0b374/effect-0.12.0.tar.gz"; sha256 = "f43322b269b2dca0c15856f090b9167d8499bf474ec64696c80a508299d51f69"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/ad/13/eb56951b6f7950cadb579ca166e448ba77f9d24efc03edd7e55fa57d04b7/idna-2.8.tar.gz"; sha256 = "c357b3f628cf53ae2c4c05627ecc484553142ca23264e593d327bcde5e9c3407"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/kjd/idna";
        license = licenses.bsdOriginal;
        description = "Internationalized Domain Names in Applications (IDNA)";
      };
    };

    "more-itertools" = python.mkDerivation {
      name = "more-itertools-5.0.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/dd/26/30fc0d541d9fdf55faf5ba4b0fd68f81d5bd2447579224820ad525934178/more-itertools-5.0.0.tar.gz"; sha256 = "38a936c0a6d98a38bcc2d03fdaaedaba9f412879461dd2ceff8d37564d6522e4"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."six"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/erikrose/more-itertools";
        license = licenses.mit;
        description = "More routines for operating on iterables, beyond itertools";
      };
    };

    "nix-prefetch-github" = python.mkDerivation {
      name = "nix-prefetch-github-1.3";
      src = pkgs.lib.cleanSource ./.;
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."Jinja2"
      self."attrs"
      self."click"
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
      name = "pkginfo-1.4.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/39/c9/111ececbeed8e69cd1b6bec79a32a0b0f6074038a4244e58e285ad278248/pkginfo-1.4.2.tar.gz"; sha256 = "5878d542a4b3f237e359926384f1dde4e099c9f5525d236b1840cf704fa8d474"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      name = "pluggy-0.8.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/65/25/81d0de17cd00f8ca994a4e74e3c4baf7cd25072c0b831dad5c7d9d6138f8/pluggy-0.8.0.tar.gz"; sha256 = "447ba94990e8014ee25ec853339faf7b0fc8050cdc3289d4d71f7f410fb90095"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pluggy";
        license = licenses.mit;
        description = "plugin and hook calling mechanisms for python";
      };
    };

    "py" = python.mkDerivation {
      name = "py-1.7.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/c7/fa/eb6dd513d9eb13436e110aaeef9a1703437a8efa466ce6bb2ff1d9217ac7/py-1.7.0.tar.gz"; sha256 = "bf92637198836372b520efcba9e020c330123be8ce527e535d185ed4b6f45694"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "http://py.readthedocs.io/";
        license = licenses.mit;
        description = "library with cross-python path, ini-parsing, io, code, log facilities";
      };
    };

    "pytest" = python.mkDerivation {
      name = "pytest-4.0.2";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/9d/a9/3688b67467527c25e7a4d02c3b22565f15158a0a5d681870bfda8af210c6/pytest-4.0.2.tar.gz"; sha256 = "f689bf2fc18c4585403348dd56f47d87780bf217c53ed9ae7a3e2d7faa45f8e9"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
        license = licenses.mit;
        description = "pytest: simple powerful testing with Python";
      };
    };

    "pytest-cov" = python.mkDerivation {
      name = "pytest-cov-2.6.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/d9/e2/58f90a316fbd94dd50bf5c826a23f3f5d079fb3cc448c1e9f0e3c33a3d2a/pytest-cov-2.6.0.tar.gz"; sha256 = "e360f048b7dae3f2f2a9a4d067b2dd6b6a015d384d1577c994a43f3f7cbad762"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."coverage"
      self."pytest"
    ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pytest-dev/pytest-cov";
        license = licenses.bsdOriginal;
        description = "Pytest plugin for measuring coverage.";
      };
    };

    "readme-renderer" = python.mkDerivation {
      name = "readme-renderer-24.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/44/de/a567140b13a0fc8d3b04d85a510b5a7d9869b44b2939fa8ac07c5e421485/readme_renderer-24.0.tar.gz"; sha256 = "bb16f55b259f27f75f640acf5e00cf897845a8b3e4731b5c1a436e4b8529202f"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/52/2c/514e4ac25da2b08ca5a464c50463682126385c4272c18193876e91f4bc38/requests-2.21.0.tar.gz"; sha256 = "502a824f31acdacb3a35b6690b5fbf0bc41d63a24a45c4004352b0242707598e"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      name = "requests-toolbelt-0.8.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/86/f9/e80fa23edca6c554f1994040064760c12b51daff54b55f9e379e899cd3d4/requests-toolbelt-0.8.0.tar.gz"; sha256 = "f6a531936c6fa4c6cfce1b9c10d5c4f498d16528d2a54a22ca00011205a187b5"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      name = "setuptools-scm-3.1.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/09/b4/d148a70543b42ff3d81d57381f33104f32b91f970ad7873f463e75bf7453/setuptools_scm-3.1.0.tar.gz"; sha256 = "1191f2a136b5e86f7ca8ab00a97ef7aef997131f1f6d4971be69a1ef387d8b40"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/pypa/setuptools_scm/";
        license = licenses.mit;
        description = "the blessed package to manage your versions by scm tags";
      };
    };

    "six" = python.mkDerivation {
      name = "six-1.12.0";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/dd/bf/4138e7bfb757de47d1f4b6994648ec67a51efe58fa907c1e11e350cddfca/six-1.12.0.tar.gz"; sha256 = "d16a0141ec1a18405cd4ce8b4613101da75da0e9a7aec5bdd4fa804d0e0eba73"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/benjaminp/six";
        license = licenses.mit;
        description = "Python 2 and 3 compatibility utilities";
      };
    };

    "tqdm" = python.mkDerivation {
      name = "tqdm-4.28.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/b0/9b/0b2f9dd0e42da42e17c79883021b21cda31dd3216aa2538205ccdd10cc7a/tqdm-4.28.1.tar.gz"; sha256 = "5b4d5549984503050883bc126280b386f5f4ca87e6c023c5d015655ad75bdebb"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [ ];
      meta = with pkgs.stdenv.lib; {
        homepage = "https://github.com/tqdm/tqdm";
        license = licenses.mit;
        description = "Fast, Extensible Progress Meter";
      };
    };

    "twine" = python.mkDerivation {
      name = "twine-1.12.1";
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/29/4d/801bbad5968e674c1ca047118025243a475f986a6f5b3ca36e5afece0f9f/twine-1.12.1.tar.gz"; sha256 = "7d89bc6acafb31d124e6e5b295ef26ac77030bf098960c2a4c4e058335827c5c"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
      propagatedBuildInputs = [
      self."pkginfo"
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/b1/53/37d82ab391393565f2f831b8eedbffd57db5a718216f82f1a8b4d381a1c1/urllib3-1.24.1.tar.gz"; sha256 = "de9529817c93f27c8ccbfead6985011db27bd0ddfcdb2d86f3f663385c6a9c22"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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
      src = pkgs.fetchurl { url = "https://files.pythonhosted.org/packages/0b/02/ae6ceac1baeda530866a85075641cec12989bd8d31af6d5ab4a3e8c92f47/webencodings-0.5.1.tar.gz"; sha256 = "b36a1c245f2d304965eb4e0a82848379241dc04b865afcc4aab16748587e1923"; };
      doCheck = commonDoCheck;
      checkPhase = "";
      installCheckPhase = "";
      buildInputs = commonBuildInputs;
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