## Summary

<!-- What changes on the site, and why. Link the issue: "Closes #123". -->

## Checklist

- [ ] `black --check .`, `ruff check .` and `mypy` pass
- [ ] `python build.py` succeeds and `lychee --offline --root-dir "$PWD/_site" _site` finds no broken links
- [ ] I looked at the changed pages in light and dark mode, and at phone width
- [ ] Code samples run with `lbd run`, and their comments show what they really print
