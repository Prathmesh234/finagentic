from semantic_kernel.functions.kernel_function_decorator import kernel_function
from typing_extensions import Annotated
from fpdf import FPDF
import textwrap
import os

class MyPDF(FPDF):
    """Custom FPDF class to add header and footer for a cleaner layout."""

    def header(self):
        # Set up a custom header
        self.set_font("Arial", "B", 12)
        # Draw a cell with the title.
        self.cell(0, 10, "Trade Prospectus", 0, 0, "C")
        # Line break
        self.ln(10)
        # Draw a horizontal line
        self.set_line_width(0.3)
        self.line(10, 25, 200, 25)
        # Line break for spacing after the line
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font("Arial", "I", 8)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", 0, 0, "C")

class ProspectusPlugin:
    """Plugin for the Web Surfer agent."""

    @kernel_function(description="Given the details creates a prospectus for the trade specific to the user")
    def create_prospectus(
        self,
        data: Annotated[str, "Data from all other agents organized by the Orchestrator"],
        user_query: Annotated[str, "Initial User Query"], 
        final_answer: Annotated[str, "Final Answer from the Orchestrator"]
    ) -> Annotated[str, "Gives an indepth prospectus"]:
        """
        Generates a professionally formatted PDF 'prospectus.pdf' file from the provided data.
        Uses <End of Paragraph> as a custom delimiter to separate paragraphs.
        Appends any PNG charts at the bottom of the PDF. The user query is displayed 
        beside 'Prospectus' in the PDF’s main title or heading.
        """
        print(final_answer)

        # -----------------------------
        # 1. Initialize the PDF
        # -----------------------------
        pdf = MyPDF()
        pdf.alias_nb_pages()            # Enables page numbers in the footer
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # -----------------------------
        # 2. Title + User Query
        # -----------------------------
        pdf.set_font("Arial", "B", 16)
        # We can manually write a sub-title containing the user query, right under our custom header
        pdf.cell(0, 10, f"Prospectus - {user_query}", ln=True, align="C")
        pdf.ln(5)

        # -----------------------------
        # 3. Parse and Format 'data'
        # -----------------------------
        paragraphs = data.split("<EndofParagraph>")
        pdf.set_font("Arial", "", 12)

        # For justified text, we’ll store each paragraph in full, 
        # then multi_cell in “J” alignment. Increase line height for readability.
        line_height = 7
        max_width = 180  # Adjust if you want narrower text columns

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Use multi_cell with "J" alignment for justification
                pdf.multi_cell(max_width, line_height, paragraph, 0, "J")
                pdf.ln(5)
            else:
                # If paragraph is empty, just add some vertical space
                pdf.ln(5)

        # -----------------------------
        # 4. Insert Charts
        # -----------------------------
        chart_files = ["chart1.png", "chart2.png"]  # Example chart files

        for chart_file in chart_files:
            if os.path.exists(chart_file):
                # Estimate space required for the chart
                needed_space_mm = 80
                current_y_position = pdf.get_y()
                bottom_margin = 15
                page_height = pdf.h - bottom_margin

                if (current_y_position + needed_space_mm) > page_height:
                    pdf.add_page()

                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Chart: {chart_file}", ln=True, align="L")

                # Insert the image (width = 160 mm, suitable for an A4 page)
                pdf.image(chart_file, x=None, y=None, w=160)
                pdf.ln(10)
            else:
                pdf.ln(5)
                pdf.set_font("Arial", "I", 10)
                pdf.multi_cell(0, 10, f"Chart file not found: {chart_file}")
                pdf.ln(5)

        # -----------------------------
        # 5. Save the PDF
        # -----------------------------
        output_filename = "prospectus.pdf"
        pdf.output(output_filename)

        # -----------------------------
        # 6. Return a success message
        # -----------------------------
        return f"Prospectus created successfully and saved as '{output_filename}'."
