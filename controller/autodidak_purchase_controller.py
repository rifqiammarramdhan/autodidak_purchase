from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter
import datetime

class ReportExcelAutodidakPurchaseController(http.Controller):
    @http.route(['/autodidak_purchase/autodidak_purchase_report_excel/<model("autodidak.purchase"):data>',],type="http", auth="user",csrf="False")
    def get_autodidak_purchase_excel_report(self, data=None, **args):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Autodidak Purchase Report'+'.xlsx'))
            ]
        )

        # Create Object From library xlsxwriter
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory': True})

        #Setting Syle 
        top_style = workbook.add_format({'font_name':'Times', 'bold':True, 'align':'left'})
        top_isi_style = workbook.add_format({'font_name':'Times', 'bold':False, 'align':'left'})
        header_style = workbook.add_format({'font_name':'Times', 'bold':True, 'left':1, 'bottom':1, 'top':1, 'right':1, 'align':'center' })
        text_style = workbook.add_format({'font_name':'Times', 'bold':False, 'left':1, 'bottom':1, 'top':1, 'right':1, 'align':'left' })        

        # Looping data yang mau dipilih
        for top in data:
            # worksheet / tab per user
            sheet = workbook.add_worksheet(top.name)

            # Set Orientasi Landscape
            sheet.set_landscape()

            # set ukuran / size kertas A4 dengan angka 9
            sheet.set_paper(9)

            # set margin (Satuan Inci)
            sheet.set_margins(0.5,0.5,0.5,0.5)

            # atur lebar kolom 
            sheet.set_column('A:A', 5)
            sheet.set_column('B:B', 50)
            sheet.set_column('C:C', 50)
            sheet.set_column('D:D', 10)
            sheet.set_column('E:E', 10)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 25)

            # Atur Judul | Header
            sheet.merge_range('A1:B1', 'Name', top_style)
            sheet.merge_range('A2:B2', 'Tanggal', top_style)

            # Index XLSX dimnulai dari 0, 0 = kolom 1

            #  Atur Isi Judul
            tanggal = top.tanggal 
            sheet.write(0, 2, top.name, top_isi_style)
            sheet.write(1, 2, tanggal.strftime("%d/%m/%Y"), top_isi_style)

            # Atur Judul kolom  
            sheet.write(3, 0, 'No', header_style)
            sheet.write(3, 1, 'Product', header_style)
            sheet.write(3, 2, 'Description', header_style)
            sheet.write(3, 3, 'Qty', header_style)
            sheet.write(3, 4, 'Satuan', header_style)
            sheet.write(3, 5, 'Harga', header_style)
            sheet.write(3, 6, 'Subtotal', header_style)

            row = 4
            number = 1

            # Cari record dari autodidak purchase line yang akan kita tampilkan
            record_line = request.env['autodidak.purchase.line'].search([('autodidak_purchase_id', '=', top.id)])
            for record in record_line:
                # Isi Dari Table
                        #    row, kolom, value (record)
                sheet.write(row, 0, number, text_style)
                sheet.write(row, 1, record.product_id.name, text_style)
                sheet.write(row, 2, record.description, text_style)
                sheet.write(row, 3, record.quantity, text_style)
                sheet.write(row, 4, record.uom_id.name, text_style)
                sheet.write(row, 5, record.price, text_style)
                sheet.write(row, 6, record.subtotal, text_style)

                row += 1
                number += 1


            #  File Excel yang sudah di generate ke dalam response
            workbook.close()
            output.seek(0)
            response.stream.write(output.read())
            output.close()

            return response 