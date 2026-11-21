# Populate the same fixed-output store path as the nix2container Skopeo patch.
# GitHub's commit.patch URL returns 503; its commit API serves the same patch.
let
  lock = builtins.fromJSON (builtins.readFile ../devenv.lock);
  root = lock.nodes.${lock.root}.inputs;
  nixpkgs = lock.nodes.${root.nixpkgs};
  source = builtins.fetchTree lock.nodes.${nixpkgs.inputs.nixpkgs-src}.locked;
  pkgs = import source {};
  revision = "21b053ac62f3137de42585611953e923577d0e10";
in
pkgs.fetchpatch2 {
  name = "${revision}.patch";
  url = "https://api.github.com/repos/nlewo/container-libs/commits/${revision}";
  curlOptsList = [ "--header" "Accept: application/vnd.github.patch" ];
  hash = "sha256-pfwQh7FKWHY/xVAGMSvnjMOmkpMo9NG2HFZqhqZ1VN0=";
  postFetch = ''
    sed -i -e '/^index /d' -e '/^similarity index /d' -e '/^dissimilarity index /d' "$out"
  '';
}
