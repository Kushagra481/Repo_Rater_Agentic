{
  description = "RepoAgent Lite - Multi-agent GitHub repository reviewer";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          pip
          virtualenv
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            pythonEnv
            pkgs.git
            pkgs.git-lfs
            pkgs.just
          ];

          shellHook = ''
            echo "🚀 RepoAgent Lite Nix Shell"
            echo "Run:"
            echo "  python -m venv .venv"
            echo "  source .venv/bin/activate"
            echo "  pip install -r requirements.txt"
            echo "  streamlit run app.py"
          '';
        };
      });
}