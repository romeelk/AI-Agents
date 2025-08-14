import os, zipfile, tempfile
from semantic_kernel.functions import kernel_function

class CodePackagingPlugin:
    @kernel_function(description="Package python code into a ZIP file")
    def generate_zip(self, python_code: str) -> str:
        tmp_dir = tempfile.mkdtemp()
        script_path = os.path.join(tmp_dir, "script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(python_code)
        zip_path = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + ".zip")
        with zipfile.ZipFile(zip_path, "w") as z:
            z.write(script_path, arcname="script.py")
        return zip_path

    @kernel_function(description="Deploy a ZIP package")
    def deploy_zip(self, zip_path: str) -> str:
        # Replace with actual deployment logic
        return f"✅ Deployed: {os.path.basename(zip_path)}"
