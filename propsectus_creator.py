from semantic_kernel.functions.kernel_function_decorator import kernel_function
from typing_extensions import Annotated
from fpdf import FPDF
import textwrap
import os

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
        beside 'Prospectus' in the title.
        """
        print(final_answer)

        # -----------------------------
        # 1. Initialize the PDF
        # -----------------------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)  # Auto flow to new pages

        # -----------------------------
        # 2. Title + User Query
        # -----------------------------
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Prospectus - {user_query}", ln=True, align="C")
        pdf.ln(5)

        # -----------------------------
        # 3. Parse and Format 'data'
        # -----------------------------
        # Use <End of Paragraph> as your custom delimiter
        paragraphs = data.split("<End of Paragraph>")
        pdf.set_font("Arial", "", 12)
        max_char_in_line = 90  # Adjust to suit desired width

        for paragraph in paragraphs:
            # Strip leading/trailing whitespace
            paragraph = paragraph.strip()
            # Wrap the paragraph to fit the PDF width
            lines = textwrap.wrap(paragraph, width=max_char_in_line)

            if lines:
                for line in lines:
                    pdf.multi_cell(0, 8, line)
                # Add a blank line after each paragraph for spacing
                pdf.ln(5)
            else:
                # If paragraph is empty, just add a newline for spacing
                pdf.ln(5)

        # -----------------------------
        # 4. Insert Charts
        # -----------------------------
        # Example list of charts:
        chart_files = ["chart1.png", "chart2.png"]  # Adjust as needed

        for chart_file in chart_files:
            if os.path.exists(chart_file):
                # Estimate space required for the chart
                needed_space_mm = 80
                current_y_position = pdf.get_y()
                bottom_margin = 15
                page_height = pdf.h - bottom_margin

                # If there's not enough space on the current page, add a new page
                if (current_y_position + needed_space_mm) > page_height:
                    pdf.add_page()

                # Label the chart
                pdf.ln(5)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"Chart: {chart_file}", ln=True, align="L")

                # Insert the image (width = 160 mm, suitable for an A4 page)
                pdf.image(chart_file, x=None, y=None, w=160)
                pdf.ln(5)
            else:
                # Chart file doesn't exist; note that in the PDF if desired
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
