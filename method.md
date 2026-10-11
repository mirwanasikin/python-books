# Progress Method — Python DevOps Book

To maintain integrity and deep understanding, follow this exact sequence for every day.

## 1. Study & Practice (2-3 hrs)
- Open the day's markdown file in `book/`.
- **Typing Rule:** Never copy-paste. Re-type every example manually into a temporary script or REPL.
- **Run:** Execute the snippets. If they fail, debug them manually.

## 2. Exercises & Projects (1-2 hrs)
- Complete the exercises at the bottom of the day's file.
- Implement any mini-scripts or projects requested.

## 3. Verification
- **Run Tests:** Every day must pass its automated test suite.
  ```bash
  source .venv/bin/activate
  pytest tests/dayNN/test_dayNN.py -v
  ```
- All tests must be green before proceeding.

## 4. Documentation
- Edit the day's markdown file.
- Mark all items in the `## Todo` section as completed: `[ ]` → `[x]`.

## 5. Machine Tracking
- Update the central progress tracker using the script:
  ```bash
  python3 scripts/check_progress.py NN
  ```
- This ensures other agents or scripts know your current level.

## 6. Version Control
- Commit your progress to keep a history of your journey.
  ```bash
  git add .
  git commit -m "feat: complete day NN"
  ```

*Note: If you skip steps or use AI to generate solutions, you bypass the cognitive friction necessary for retention.*
