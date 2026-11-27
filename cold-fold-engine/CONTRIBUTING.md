# Contributing to cold_fold_engine

Thanks for your interest in this project.

## Reporting bugs and asking questions
Open an issue at https://github.com/Hydrogenesi/Phoenix-2.0-Apex-Edition/issues.
Please include your Python version, your operating system, the exact command you ran, and the output you got.
Questions about how to use the engine are welcome as issues too.

## Contributing code
1. Fork the repository and create a branch.
2. Set up a development install: `pip install -e ".[test]"`
3. Add tests for any change in behaviour. Plates must stay pure, with no randomness, clock, or I/O inside `apply`.
4. Run `python -m pytest tests -q`. The determinism digest test must still pass. If you change the trace digest on purpose, explain why in the pull request.
5. Open a pull request describing what you changed and why.

## Code of conduct
This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
