from fpdf import FPDF
from fpdf.enums import Align, WrapMode
from csv import DictReader


class PDF(FPDF):
    @classmethod
    def create_puzzle_sales_pdf(cls):
        sale_puzzles_pdf = PDF()
        sale_puzzles_pdf.add_page(orientation="L")
        with open("list_of_puzzles.csv", "r") as file:
            reader = DictReader(file)

            sale_puzzles_pdf.create_table(reader)
        sale_puzzles_pdf.output("sale_puzzles.pdf")
    
    def create_table(self, reader):
        self.set_unicode_font()

        with self.table() as table:
            for _ in range(1):
                row = table.row()
                for field in reader.fieldnames:
                    row.cell(field)
            
            for i, puzzle_dict in enumerate(reader):
                row = table.row()
                for j, key in enumerate(puzzle_dict):
                    if j == 1 and i >= 0:
                        row.cell(img=puzzle_dict[key])
                    elif j == 2 and i >=0:
                        row.cell("Link to puzzle", link=puzzle_dict[key])
                    else:
                        row.cell(puzzle_dict[key])
    
    def set_unicode_font(self):
        self.add_font("dejavu-sans", style='', fname="/Users/reneetoscan/Library/Fonts/DejaVuSans.ttf")
        self.add_font("dejavu-sans", style='b', fname="/Users/reneetoscan/Library/Fonts/DejaVuSans.ttf")
        self.set_font("dejavu-sans", size=12)

    
        

