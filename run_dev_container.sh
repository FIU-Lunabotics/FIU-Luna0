#!/usr/bin/env bash

echo "opening luna in code dev container"

# check if installed
if ! command -v code &>/dev/null; then
  echo "missing dep: vscode and remote containers extension"
  exit 1
fi

code .

echo "accept 'Open in Dev Container' prompt"
