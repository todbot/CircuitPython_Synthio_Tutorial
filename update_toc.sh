#!/bin/sh
# needs https://github.com/ekalinin/github-markdown-toc
for f in README-*.md ; do
    echo $f
    gh-md-toc  --insert --no-backup --hide-footer $f
done
