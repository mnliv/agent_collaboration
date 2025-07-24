## Setup Python Virtual Environment with `uv`

1. **Install `uv` (if not already installed):**
    ```bash
    pip install uv
    ```

2. **Create a new virtual environment:**
    ```bash
    uv venv .venv
    ```

3. **Activate the virtual environment:**
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```

4. **Install dependencies (if you have a `requirements.txt`):**
    ```bash
    uv pip install -r requirements.txt
    ```