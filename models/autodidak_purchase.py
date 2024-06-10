from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class autodidak_purchase(models.Model):
    _name = 'autodidak.purchase'

    def funct_approved(self):
        if self.status == 'draft':
            if self.name == 'New':
                seq = self.env['ir.sequence'].next_by_code('autodidak.purchase') or 'New' #Sesuai Code yang ada di xml sequence | Jika Belum ada idnya maka 'New
                self.name = seq
            self.status = 'approve'

    def funct_set_to_done(self):
        if self.status == 'approve':
            self.status = 'done'

    name = fields.Char(string="Name", default="New")
    tanggal = fields.Date(string="Tanggal")
    status = fields.Selection([('draft','Draft'),('approve','Approve'),('done',"Done")],default='draft')

    # Field untuk One To Many
    autodidak_purchase_ids = fields.One2many('autodidak.purchase.line', 'autodidak_purchase_id',string='Autodidak Purchase Ids')
    # Field untuk Many To Many
    brand_ids = fields.Many2many('autodidak.brand', 'autodidak_purchase_brand_rel', 'autodidak_purchase_id', 'brand_id',string="Brand Ids" ) #membuat Tabel bantuan seperti jembatan atau bride (autodidak_purchase_brand_rel)


# Relasi One To Many
class autodidak_purchase_line(models.Model):
    _name = 'autodidak.purchase.line'

    @api.onchange('product_id')
    def funct_onchange_product_id(self): # DI odo setiap membuat function akan otomatis terdapat sefl di argument. self isinua adalah nama dari classnya
        if not self.product_id:
            return {}
        
        else:
            self.description = self.product_id.name
            return {}
        
    def _funct_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price
        
    
    # Ini adalah Field many to one 
    autodidak_purchase_id = fields.Many2one('autodidak.purchase', string="Autodidak Purchase Id")
    product_id = fields.Many2one('product.product', string="Product Id")
    quantity = fields.Integer(string="Quantity", default=0)
    uom_id = fields.Many2one('uom.uom', string="Satuan")
    description = fields.Char(string="Description")
    price = fields.Float(string="harga", default=0.0)
    subtotal = fields.Float(string="Sub Total", compute=_funct_subtotal)

# Relasi Many To Many
class autodidak_brand(models.Model):
    _name = 'autodidak.brand'

    name = fields.Char(string="name")


class autodidak_purchase_report_wizard(models.TransientModel):
    _name = 'autodidak.purchase.report.wizard'

    name = fields.Char(string='Name')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

