import datetime
from fpdf import FPDF
import os
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class FilePlugin:
    """A Semantic Kernel plugin that simulates creation of text and pdf files"""

    @kernel_function(description="A function that creates a txt file given a response from LLM")
    def create_prompt_file(self, file_content: str):
        current_date = datetime.datetime.now()
        file_name = os.path.join(os.path.dirname(__file__),f"{current_date.strftime("%d%m%y")}_llm_output.txt")
        with open(file_name, "w+",newline="") as file:
            file.write(file_content)
        return file_name

    @kernel_function(description="A function that exports a text file into pdf format")
    def export_file_topdf(self, file_path: str):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        with open(file_path,"r") as file:
            for line in file:
                pdf.cell(0, 10, txt=line.strip(), ln=1, align='L')

        pdf.output(f"{os.path.splitext(os.path.basename(file_path))[0]}.pdf")
