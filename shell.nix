{
  pkgs ? import <nixpkgs> {
    config = {
      allowUnfree = true;
    };
  },
}:

pkgs.mkShell {
  buildInputs = [
    pkgs.file
    pkgs.python3
    pkgs.ngrok
  ];

  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.file.out}/lib:$LD_LIBRARY_PATH"
  '';
}
