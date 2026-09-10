{
  description = "Python development environment with uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux"; 
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          python313
          uv
          zlib # Needed for CRC-32 and standard zlib support
        ];

        # Fixes native library loading on NixOS for uv/pip packages
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (with pkgs; [
          stdenv.cc.cc.lib
          zlib
        ]);

        shellHook = ''
          echo "=== Python + uv DevShell Active ==="
          # Create virtual environment automatically if it doesn't exist
          if [ ! -d ".venv" ]; then
            uv venv
          fi
          source .venv/bin/activate
        '';
      };
    };
}