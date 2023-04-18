#!/bin/bash

find . -name "*.out" -delete
find . -name "*.class" -delete

find . -path ./node_modules -prune -o -name "*.md" -exec sed -i "" 'N;/^\n/D' {} \;
