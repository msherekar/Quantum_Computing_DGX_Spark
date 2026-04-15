#!/usr/bin/env bash
set -euo pipefail

# Initializes a local git repo, creates README/.gitignore, and links to GitHub.
# Usage: ./scripts/setup_github_repo.sh "Quantum_Computing_DGX_Spark" "https://github.com/msherekar/Quantum_Computing_DGX_Spark.git" [--no-push]

REPO_NAME="${1:-Quantum_Computing_DGX_Spark}"
REMOTE_URL="${2:-https://github.com/msherekar/Quantum_Computing_DGX_Spark.git}"
PUSH_FLAG="${3:-}"
DEFAULT_BRANCH="main"

if [ ! -d .git ]; then
  git init
fi

if [ ! -f README.md ]; then
  echo "# ${REPO_NAME}" > README.md
elif ! rg -q "^# ${REPO_NAME}$" README.md; then
  echo "# ${REPO_NAME}" >> README.md
fi

if [ ! -f .gitignore ]; then
  cat <<'EOF' > .gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Jupyter
.ipynb_checkpoints/

# OS / Editor
.DS_Store
.vscode/

# Logs / Env
*.log
.env
EOF
fi

git add README.md .gitignore

if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git commit -m "first commit"
fi

git branch -M "${DEFAULT_BRANCH}"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "${REMOTE_URL}"
else
  git remote add origin "${REMOTE_URL}"
fi

echo "Remote origin is set to: $(git remote get-url origin)"

if [ "${PUSH_FLAG}" != "--no-push" ]; then
  git push -u origin "${DEFAULT_BRANCH}"
else
  echo "Skipping push. To push later, run: git push -u origin ${DEFAULT_BRANCH}"
fi
