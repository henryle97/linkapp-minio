find . -name "*.py" -not -path "" | xargs black --line-length 88
find . -name "*.py" -not -path "" | xargs isort