{
  description = "KSP kRPC Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        
        # Build the missing kRPC package
        krpc-python = pkgs.python3Packages.buildPythonPackage rec {
          pname = "krpc";
          version = "0.5.4";
          format = "setuptools";

          src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            extension = "zip";
            # You'll need to update this hash or let it fail once to get the real one
            hash = "sha256-lbRRKggMktRaG2Drue/5KQxSY6Gf8avbNR4S/7UfthU=";
          };

          nativeBuildInputs = [ pkgs.unzip ];

          propagatedBuildInputs = with pkgs.python3Packages; [
            protobuf
            certifi
          ];

          doCheck = false;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            (pkgs.python3.withPackages (ps: [ 
              ps.ipython 
              krpc-python 
            ]))
          ];

          shellHook = ''
            echo "🚀 KSP kRPC Environment Loaded"
            export PS1="[kRPC] $PS1"
          '';
        };
      });
}
