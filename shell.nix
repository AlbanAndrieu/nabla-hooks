{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.05") {} }:

pkgs.mkShellNoCC {
  packages = with pkgs; [
    poetry
    python3
    virtualenv
    nodejs
    git
    cowsay
  ];

  shellHook = ''
    echo "Welcome to the Shell! May your pipelines be green." | cowsay -f dragon
  '';
}
