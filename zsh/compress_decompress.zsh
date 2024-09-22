#!/bin/zsh

# Function to compress files
compress_files() {
  for file in "$@"; do
    if [[ -f "$file" ]]; then
      echo "Compressing $file"
      gzip "$file"
    else
      echo "Skipping $file (not a regular file)"
    fi
  done
}

# Function to decompress files
decompress_files() {
  for file in "$@"; do
    if [[ -f "$file" ]] && [[ "$file" == *.gz ]]; then
      echo "Decompressing $file"
      gunzip "$file"
    else
      echo "Skipping $file (not a .gz file)"
    fi
  done
}

# Check for arguments
if [[ $# -eq 0 ]]; then
  echo "Usage: $0 command [files...]"
  echo "Commands:"
  echo "  compress:   Compress the specified files"
  echo "  decompress: Decompress the specified .gz files"
  exit 1
fi

# Determine the operation based on the first argument
case "$1" in
  compress)
    shift
    compress_files "$@"
    ;;
  decompress)
    shift
    decompress_files "$@"
    ;;
  *)
    echo "Invalid command: $1"
    echo "Use 'compress' or 'decompress'"
    exit 2
    ;;
esac
