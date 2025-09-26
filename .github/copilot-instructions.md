# Copilot Instructions for AI Coding Agents

## Project Overview
Prism is a multi-platform GUI tool for splitting and reconstructing secrets using Shamir's Secret Sharing. The main logic resides in `prism.py`. The project is designed for simplicity and cross-platform compatibility.

## Architecture & Key Files
- `prism.py`: Main application file. Contains core logic for secret splitting/reconstruction and GUI handling.
- `README.md`: Project summary and usage context.
- `requirements.txt` / `pyproject.toml`: Python dependencies (GUI toolkit, cryptography, etc.).
- `Makefile`: Defines build and packaging commands (if present).
- `prism.spec`: PyInstaller spec for building standalone executables.

## Developer Workflows
- **Run the app:**
  ```bash
  python prism.py
  ```
- **Build executable:**
  ```bash
  make build
  # or
  pyinstaller prism.spec
  ```
- **Dependencies:**
  Use Poetry or pip to manage dependencies. Check both `requirements.txt` and `pyproject.toml`.
- **Testing:**
  No explicit test suite detected. If adding tests, follow the structure and conventions in `prism.py`.

## Patterns & Conventions
- All logic is centralized in a single file (`prism.py`).
- GUI and cryptographic logic are tightly coupled for simplicity.
- Use clear, user-facing error messages for secret operations.
- Cross-platform compatibility is a priority (avoid OS-specific code unless necessary).

## Integration Points
- Uses external libraries for GUI and Shamir's Secret Sharing (see dependencies).
- Packaging via PyInstaller (`prism.spec`).

## Examples
- To split a secret, follow the function pattern in `prism.py`:
  ```python
  # ...existing code...
  shares = split_secret(secret, threshold, num_shares)
  # ...existing code...
  ```
- To reconstruct:
  ```python
  # ...existing code...
  secret = reconstruct_secret(shares)
  # ...existing code...
  ```

## Recommendations for AI Agents
- Focus on `prism.py` for all logic changes.
- When adding features, maintain the single-file structure unless refactoring is required.
- Reference `prism.spec` for packaging logic.
- Document any new developer workflows in this file and in the README.

---

*Please review and suggest improvements or clarify any unclear sections.*
