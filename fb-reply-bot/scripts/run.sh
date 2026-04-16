#!/usr/bin/env bash
# Wrapper for launchd — ensures correct working directory and captures output.
cd "$(dirname "$0")/.." || exit 1
exec /opt/homebrew/bin/node src/index.js
