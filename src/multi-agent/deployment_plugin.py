import time
import tempfile
import os
from datetime import datetime
from zipfile import ZipFile

class DeploymentPlugin:
    """A Semantic Kernel plugin that simulates deployment of Python server code"""

    def package_code(self, pythoncode: str):
        print("zipping code...")
        artifacts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"artifacts")

        # save code to artifacts folder as temp file
        with tempfile.NamedTemporaryFile(mode="w+",dir=artifacts_path,delete=True) as temp_file:
            print("Temporary file name:", temp_file.name)
            temp_file.write(pythoncode)
        
            # zip temp file and name it  ddmmyy_code.zip and write it to artifacts folder
            zip_file_name = os.path.join(artifacts_path,f"{datetime.now().strftime("%d-%m-%s")}_code.zip")
            
            with ZipFile(zip_file_name, 'w') as zip_file:
                zip_file.write(temp_file.name,arcname=os.path.basename("code.py"))
                print(zip_file_name)
        
        return zip_file_name

    def deploy_code(self, code_package_file: str):
        # basic validation - does the file path exist

        if os.path.exists(code_package_file) == False:
            raise FileNotFoundError(f"{code_package_file} does not exist")
        ## get path to artifacts folder
        ## write code artifact
        print(f"deploying package {os.path.basename(code_package_file)}")
        time.sleep(5)
        print("package successfully deeployed!")

        