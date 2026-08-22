{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  buildInputs = [
    pkgs.file
    pkgs.python3
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.file.out}/lib:$LD_LIBRARY_PATH"
  '';
}
