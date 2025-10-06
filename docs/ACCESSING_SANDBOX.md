# Accessing the Codex Sandbox Repository Snapshot

This project was bootstrapped inside the hosted “sandbox” environment that ships with the coding assistant. The sandbox is an ephemeral Linux container that behaves like a normal Git workspace, so you can inspect files, run tests, and prepare commits—but it does **not** have direct access to your personal GitHub account.

To bring the work product from the sandbox onto your own machine (and then to GitHub), follow these steps:

1. **Create a portable bundle inside the sandbox**
   ```bash
   cd /workspace/rai-toolkit
   git bundle create /workspace/rai-toolkit.bundle --all
   ```
   The `git bundle` command packages every branch and commit into a single file that you can safely move out of the sandbox.

2. **Encode the bundle so it is easy to copy**
   ```bash
   base64 /workspace/rai-toolkit.bundle > /workspace/rai-toolkit.bundle.b64
   ```
   Run `cat /workspace/rai-toolkit.bundle.b64` to print the Base64 text, then copy the full output into a new file on your local machine (for example, `rai-toolkit.bundle.b64`).

   > **Copying tip:** Chat-based terminals sometimes truncate extremely long outputs and display an ellipsis (`...`). If that happens, split the Base64 file into smaller chunks before copying:
   > ```bash
   > split -b 50000 /workspace/rai-toolkit.bundle.b64 rai-toolkit.b64.part-
   > ```
   > This produces numbered files (for example, `rai-toolkit.b64.part-aa`, `rai-toolkit.b64.part-ab`). Run `cat rai-toolkit.b64.part-aa` (and the rest in order) to copy each segment without truncation, then concatenate them locally: `cat rai-toolkit.b64.part-* > rai-toolkit.bundle.b64`.

   > **Alternative:** If you prefer a direct download, start a one-off HTTP server inside the sandbox and fetch the bundle from your local machine:
   > ```bash
   > python -m http.server --directory /workspace 8000
   > ```
   > Leave the command running, then browse to `http://<sandbox-host>:8000/rai-toolkit.bundle` or use `curl`/`wget` from your workstation. When the download completes, stop the server with `Ctrl+C`.

   *Optional integrity check:* if you want extra assurance that the bundle arrived intact, record the SHA-256 hash before you leave the sandbox:
   ```bash
   sha256sum /workspace/rai-toolkit.bundle
   ```
   After decoding locally, rerun `sha256sum rai-toolkit.bundle` and confirm the values match.

3. **Re-create the repository on your local workstation**
   Decode the Base64 file and clone the bundle:
   ```bash
   base64 --decode rai-toolkit.bundle.b64 > rai-toolkit.bundle
   git clone rai-toolkit.bundle rai-toolkit
   cd rai-toolkit
   ```
   You now have a local Git repository with the same commit history as the sandbox.

4. **Attach your GitHub remote and push**
   ```bash
   git remote add origin https://github.com/<your-username>/rai-toolkit.git
   git push -u origin main  # push your default branch
   git push -u origin work  # push additional branches, if present
   ```

5. **Continue working locally**
   From here you can install dependencies, run Streamlit, or open pull requests just like any other project. Future updates can be pushed with a simple `git push`.

> **Note:** The sandbox is temporary. If the environment shuts down before you export the bundle, you will need to rebuild the work. Export your bundle and push it to GitHub regularly to avoid losing progress.

