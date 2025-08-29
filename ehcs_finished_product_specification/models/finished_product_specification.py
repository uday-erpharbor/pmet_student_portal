from odoo import models, fields, api, _
from datetime import datetime,date

product_variants = [
        ('breath_drops_boxed', 'Breath Drops (Boxed)'),
        ('breath_drops_no_box', 'Breath Drops (No Box)'),
        ('breath_spray_boxed', 'Breath Spray (Boxed)'),
        ('breath_spray_no_box', 'Breath Spray (No Box)'),
        ('concentrated_mouthwash_boxed', 'Concentrated Mouthwash (Boxed)'),
        ('concentrated_mouthwash_no_box', 'Concentrated Mouthwash (No Box)'),
        ('dental_vitamins_jar', 'Dental Vitamins (Jar)'),
        ('dental_vitamins_pouch', 'Dental Vitamins (Pouch)'),
        ('dental_vitamins_tin', 'Dental Vitamins (Tin)'),
        ('foaming_mouthwash_boxed', 'Foaming Mouthwash (Boxed)'),
        ('foaming_mouthwash_no_box', 'Foaming Mouthwash (No Box)'),
        ('lip_balm_boxed', 'Lip Balm (Boxed)'),
        ('lip_gloss_boxed', 'Lip Gloss (Boxed)'),
        ('mints_jar', 'Mints (Jar)'),
        ('mints_pouch', 'Mints (Pouch)'),
        ('mints_tin', 'Mints (Tin)'),
        ('mouthwash_boxed', 'Mouthwash (Boxed)'),
        ('mouthwash_no_box', 'Mouthwash (No Box)'),
        ('mouthwash_tablets_jar', 'Mouthwash Tablets (Jar)'),
        ('mouthwash_tablets_pouch', 'Mouthwash Tablets (Pouch)'),
        ('mouthwash_tablets_tin', 'Mouthwash Tablets (Tin)'),
        ('powder_jar_boxed', 'Powder (Jar) (Boxed)'),
        ('powder_jar_no_box', 'Powder (Jar) (No Box)'),
        ('teeth_whitening_gel_pap_bulk_packed', 'Teeth Whitening Gel (PAP) (Bulk Packed)'),
        ('teeth_whitening_gel_pap_kit', 'Teeth Whitening Gel (PAP) (Kit)'),
        ('teeth_whitening_gel_pap_topup', 'Teeth Whitening Gel (PAP) (Top-Up)'),
        ('teeth_whitening_gel_peroxide_bulk_packed', 'Teeth Whitening Gel (Peroxide) (Bulk Packed)'),
        ('teeth_whitening_gel_peroxide_kit', 'Teeth Whitening Gel (Peroxide) (Kit)'),
        ('teeth_whitening_gel_peroxide_topup', 'Teeth Whitening Gel (Peroxide) (Top-Up)'),
        ('teeth_whitening_pen_boxed', 'Teeth Whitening Pen (PAP) (Boxed)'),
        ('teeth_whitening_pen_no_box', 'Teeth Whitening Pen (PAP) (No Box)'),
        ('toothpaste_boxed', 'Toothpaste (Boxed)'),
        ('toothpaste_bulk_packed', 'Toothpaste (Bulk Packed)'),
        ('toothpaste_tablets_jar_boxed', 'Toothpaste Tablets (Jar) (Boxed)'),
        ('toothpaste_tablets_jar_no_box', 'Toothpaste Tablets (Jar) (No Box)'),
        ('toothpaste_tablets_pouch_boxed', 'Toothpaste Tablets (Pouch) (Boxed)'),
        ('toothpaste_tablets_pouch_no_box', 'Toothpaste Tablets (Pouch) (No Box)'),
        ('toothpaste_tablets_tin_boxed', 'Toothpaste Tablets (Tin) (Boxed)'),
        ('toothpaste_tablets_tin_no_box', 'Toothpaste Tablets (Tin) (No Box)'),
        ('tongue_drops_boxed', 'Tongue Drops (Boxed)'),
        ('tongue_drops_no_box', 'Tongue Drops (No Box)'),
        ('whitening_strips_pap', 'Whitening Strips (PAP)'),
        ('whitening_strips_peroxide', 'Whitening Strips (Peroxide)'),
        ]

class FinishedProductSpecification(models.Model):
    _name = 'finished.product.specification'
    _description = 'Finished Product Specification'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char("Name", required=True,copy=False,readonly=True,default=lambda self: ('New'))
    date = fields.Date('Date Deposit Paid',default = datetime.now())
    product_status = fields.Selection([("draft",'Draft'), ('approved','Approved'), ('discontinued','Discontinued')], string='Product Status', default='draft')
    fps_version_number = fields.Char('Finished Product Specification Version Number')
    product_id = fields.Many2one('product.template',string='Product')
    finished_goods_number = fields.Char('Finished Goods Number')
    customer_id = fields.Many2one('res.partner', string='Company Name')
    bom_id = fields.Many2one('mrp.bom', string='Bulk Bill of Material')
    product_being_packed = fields.Selection(
        selection=product_variants,
        string="Product Type",
    )
    formula_version_number = fields.Char('Formula Version Number')
    lot_location = fields.Char('Lot Location')
    file = fields.Binary(string='Upload Artwork with Example Lot Location')
    shelf_life = fields.Selection([('pao', 'PAO'), ('bbe', 'BBE / EXP (Expiry)')], string='Shelf-Life')
    pao_months = fields.Char('PAO Months')
    bbe_months = fields.Char('BBE / EXP (Expiry)')
    primary_packing_component = fields.Selection([
                                ('tube', 'Tube'),
                                ('bottle','Bottle'),
                                ('breath_spray','Breath Spray'),
                                ('jar_tin','Jar / Tin'),
                                ('pouch','Pouch'),
                                ('syringe','Syringe'),
                                ('pen','Pen'),
                                ('dropper_bottel','Dropper Bottle')], string='Primary Packaging (e.g. Tube) Component')
    secondary_packaging = fields.Char('Secondary Packaging (e.g. Box)')
    not_applicable = fields.Boolean('Not Applicable')
    component_id = fields.Many2one('product.template','Component')
    unit_per_sc_packging = fields.Char('Units per Secondary Packaging')
    notes = fields.Char('Notes')
    supplied_by = fields.Selection([('cosmolab', 'Cosmolab'), ('customer', 'Customer')], string='Supplied By')
    artwork = fields.Binary(string='Artwork')
    
    tp_component = fields.Many2one('product.template', 'Tertiary Package (e.g. SRT) Component')
    tp_unit_per_packging = fields.Char('Units per Tertiary Packaging')
    tp_notes = fields.Char('Notes')
    tp_supplied_by = fields.Selection([('cosmolab', 'Cosmolab'), ('customer', 'Customer')], string='Supplied By')
    tp_package_label = fields.Selection([('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')], string='Tertiary Package Label')
    tp_app_details = fields.Char('Label Application Details')
    tp_artwork = fields.Binary(string='Artwork')
    
    pri_component_id = fields.Many2one('product.template','Primary Shipping Carton Component')
    psc_package_label = fields.Selection([('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')], string='Secondary Shipping Carton')
    no_unit_per_shipp_cartoon = fields.Char('No. Units per Primary Shipping Carton')
    psc_notes = fields.Char('Notes')
    psc_supplied_by = fields.Selection([('cosmolab', 'Cosmolab'), ('customer', 'Customer'), ('re_use_supplier','Re-Use Supplier Packaging')], string='Supplied By')
    psc_label_app_details = fields.Char('Label Application Details')
    psc_artwork = fields.Binary(string='Artwork')

    ssc_shipping_carton = fields.Selection([('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')], string='Secondary Shipping Carton')
    ssc_component_id = fields.Many2one('product.template','Component')
    no_psc_per_ssc_shipp_cartoon = fields.Char('No. Primary Shipping Cartons per Secondary Shipping Carton')
    no_unit_per_ssc_shipp_cartoon = fields.Char('No. Units per Secondary Shipping Carton')
    ssc_notes = fields.Char('Notes')
    ssc_supplied_by = fields.Selection([('cosmolab', 'Cosmolab'), ('customer', 'Customer'), ('re_use_supplier','Re-Use Supplier Packaging')], string='Supplied By')
    ssc_artwork = fields.Binary(string='Artwork')
    ssc_package_label = fields.Selection([('applicable', 'Applicable'), ('not_applicable', 'Not Applicable')], string='Secondary Shipping Carton Label')
    sc_app_details = fields.Char('Label Application Details')
    sc_artwork = fields.Binary(string='Artwork')

    additional_components = fields.Char('Additional Components (e.g. Leaflet)')
    add_not_applicable = fields.Boolean('Not Applicable')
    add_components = fields.Selection([
                    ('tray_case','Tray Case'),
                    ('leaflet','Leaflet'),
                    ('other','Other'),
                    ], string='Component')
    add_notes = fields.Char('Notes')
    add_supplied_by = fields.Selection([('cosmolab', 'Cosmolab'), ('customer', 'Customer')], string='Supplied By')
    add_artwork = fields.Binary(string='Artwork')
    formula_id = fields.Many2one('')


    #Tube
    tube_type = fields.Selection([('pe','PE'), ('laminate','Laminate'), ('aluminium',('Aluminium'))], string='Aluminium')
    tube_type_addi_info = fields.Char('Tube Type Additional Info')
    tube_fill_size = fields.Char('Fill Size')
    tube_diameter_mm = fields.Char('Tube Diameter (mm)')
    tube_height_mm = fields.Char('Tube Height (mm)')
    tube_color = fields.Char('Tube Colour', help='If the tube is coloured, advise if it is a white tube with ink printed on top to colour it or if the tube is made from coloured plastic.')
    tube_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss')
                        ], string='Tube Finish')
    tube_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    tube_tamper_evidence = fields.Selection([
                        ('foil_seal_office','Foil Seal on Orifice'), ('plastic_wrap_cap', 'Plastic Warp on Cap')
                        ], string='Tamper Evidence')
    tube_orifice_size_mm = fields.Char('Orifice Size (mm)')
    tube_cap_type = fields.Selection([
                        ('flip_cap_so','Flip Cap (Screw On)'),
                        ('flip_cap_po', 'Flip Cap (Push On)'),
                        ('screw_cap', 'Screw Cap')
                        ], string='Cap Type')
    tube_oriented_cap = fields.Char('Oriented Cap')
    tube_cap_shape = fields.Binary('Cap Shape')
    tube_cap_colour = fields.Char('Cap Colour')
    tube_cap_finish = fields.Selection([('matt', 'Matt'), ('gloss', 'Gloss')], string='Cap Finish')
    supplied_by = fields.Selection([('cosmolab', 'Cosmolab'), ('customer', 'Customer')], string='Supplied By')
    supplier = fields.Many2one('res.partner', 'Supplier')
    tube_artwork = fields.Binary('Artwork')
    add_info = fields.Text('Additional Info')

    #Bottle
    bottle_material = fields.Char('Bottle Material')
    bottle_diameter_mm = fields.Char('Bottle Diameter (mm)')
    bottle_height_mm = fields.Char('Bottle Height (mm)')
    bottle_colour = fields.Char('Bottle Colour')
    bottle_decoration_type = fields.Selection([('label','Label'), ('printed', 'Printed')], string='Decoration Type')
    bottle_label_option = fields.Selection([('13','13'),('14','14'),('15','15'),('16','16'),('17','17')], string='Options')
    bottle_print_option = fields.Selection([('120','120'),('121','121'),('122','122')], string='Options')
    bottle_app_type = fields.Selection([('front_back','Front & Back'), ('wrap','Wrap Around')], 'Label Application Type')
    bottle_label_supplier = fields.Many2one('res.partner', 'Supplier')
    bottle_label_size = fields.Char('Label Size')
    bottle_label_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Label Print Finish')
    bottle_label_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    bottle_label_artwork = fields.Binary('Label Artwork')

    bottle_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Bottle Print Finish')
    bottle_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    bottle_artwork = fields.Binary('Printed Artwork')
    bottle_cap_material = fields.Char('Cap Material')
    bottle_cap_colour = fields.Char('Cap Colour')
    bottle_tamper_evidence = fields.Char('Tamper Evidence')

    #Breath Spray
    bs_spray_bottle_material = fields.Char('Spray Bottle Material')
    bs_spray_bottle_diameter = fields.Char('Spray Bottle Diameter (mm)')
    bs_spray_bottle_height = fields.Char('Spray Spray Bottle Height (mm) (inc. cap)')
    bs_spray_bottle_colour = fields.Char('Spray Bottle Colour')
    bs_decoration_type = fields.Selection([('label','Label'), ('printed', 'Printed')], string='Decoration Type')
    bs_label_option = fields.Selection([('142','142'),('143','143'),('144','144'),('145','145'), ('146','146'), ('147','147')], string='Options')
    bs_print_option = fields.Selection([('149','149'),('150','150'),('151','151')], string='Options')
    bs_app_type = fields.Selection([('front_back','Front & Back'), ('wrap','Wrap Around')], 'Label Application Type')
    bs_label_supplier = fields.Many2one('res.partner', 'Supplier')
    bs_size = fields.Char('Label Size')
    bs_label_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Label Print Finish')
    bs_label_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    bs_label_artwork = fields.Binary('Label Artwork')
    bs_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Spray Bottle Print Finish')
    bs_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    bs_artwork = fields.Binary('Printed Artwork')
    cap_if_app = fields.Char('Cap (if applicable)')
    cap_mat_if_app = fields.Char('Cap Material (if applicable)')
    cap_col_if_app = fields.Char('Cap Colour (if applicable)')
    tamper_evidence = fields.Char('Tamper Evidence')

    #Jar / Tin
    jt_fill_size_gram = fields.Integer('Fill Size (grams or no. units)')
    jt_diameter_mm = fields.Float('Jar/Tin Diameter (mm)')
    jt_height_mm = fields.Float('Jar/Tin Height (mm)')
    jt_colour = fields.Char('Jar/Tin Colour')
    jt_finish = fields.Char('Jar/Tin Finish')
    jt_decoration_type = fields.Selection([('label','Label'), ('printed', 'Printed')], string='Decoration Type')
    jt_label_option = fields.Selection([('170','170'),('171','171'),('172','172'),('173','173'), ('174','174'), ('175','175')], string='Options')
    jt_print_option = fields.Selection([('177','177'),('178','178'),('179','179')], string='Options')
    jt_app_type = fields.Selection([('front_back','Front & Back'), ('wrap','Wrap Around')], 'Label Application Type')
    jt_label_supplier = fields.Many2one('res.partner', 'Supplier')
    jt_label_size = fields.Char('Label Size')
    jt_label_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Label Print Finish')
    jt_label_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    jt_label_artwork = fields.Binary('Label Artwork')
    jt_print_finish = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Jar/Tin Print Finish')
    jt_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    jt_artwork = fields.Binary('Printed Artwork')
    dessicant_required = fields.Selection([('yes','Yes'), ('no','No')], string='Dessicant Required')

    #Pouch
    pouch_fillsize = fields.Integer('Fill Size (grams or no. units)')
    pouch_type = fields.Selection([
                ('resealable','Resealable (Doypack - Stand-Up Pouch / Non-Resealable (Pillow Pack)'),
                ('not_resealable','Non-Resealable (3 Side Sealed Pillow Pack) (On a Roll)')], string='Pouch Type')
    pouch_height = fields.Char('Pouch Height (mm)')
    pouch_width = fields.Char('Pouch Width (mm)')
    pouch_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Pouch Finish')
    pouch_material = fields.Selection([('aluminium','Aluminium'), ('pe','PE'), ('kp','Kraft Paper + PLA + NK')], string='Pouch Material')
    pouch_decoration_type = fields.Selection([('label','Label'), ('printed', 'Printed')], string='Decoration Type')
    pouch_label_option = fields.Selection([('170','170'),('171','171'),('172','172'),('173','173'), ('174','174'), ('175','175')], string='Options')
    pouch_print_option = fields.Selection([('177','177'),('178','178'),('179','179')], string='Options')
    pouch_app_type = fields.Selection([('front_back','Front & Back'), ('wrap','Wrap Around')], 'Pouch Label Application Type')
    pouch_label_supplier = fields.Many2one('res.partner', 'Pouch Label Supplier')
    pouch_label_size = fields.Char('Pouch Label Size')
    pouch_label_artwork = fields.Binary('Pouch Label Artwork')
    pouch_print_finish = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Pouch Print Finish')
    pouch_special_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    pouch_artwork = fields.Binary('Printed Artwork')

    #Syringe
    sr_fillsize = fields.Integer('Fill Size (ml)')
    sr_barrel_colour = fields.Char('Barrel Colour')
    sr_plunger_colour = fields.Char('Plunger Colour')
    sr_decoration_type = fields.Selection([('label','Label'), ('printed', 'Printed')], string='Decoration Type')
    sr_label_option = fields.Selection([('203','203'),('204','204'),('205','205'),('206','206'), ('207','207')], string='Options')
    sr_print_option = fields.Selection([('209','209'),('210','210')], string='Options')
    sr_label_supplier = fields.Many2one('res.partner', 'Label Supplier')
    sr_label_size = fields.Char('Label Size')
    sr_print_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Label Print Finish')
    sr_spec_print = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    sr_label_artwork = fields.Binary('Label Artwork')
    sr_spec_printing = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    sr_print_syr_artwork = fields.Binary('Printed Syringe Artwork')

    #Pen
    pen_fillsize = fields.Integer('Fill Size (ml)')
    pen_barrel_colour = fields.Char('Barrel Colour')
    pen_lid_colour = fields.Char('Lid Colour')
    pen_tip_type = fields.Char('Tip Type')
    pen_spec_print = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    pen_artwork = fields.Binary('Artwork')

    #Dropper Bottle
    db_bottel_material = fields.Char('Droper Bottle Material')
    db_diameter_mm = fields.Char('Droper Bottle Diameter (mm)')
    db_height_mm = fields.Char('Droper Bottle Height (mm)')
    db_bottle_colour = fields.Char('Droper Bottle Colour')
    db_decoration_type = fields.Selection([('label','Label'), ('printed', 'Printed')], string='Decoration Type')
    db_label_option = fields.Selection([('255','255'), ('256','256'), ('257','257'), ('258','258'), ('259','259'), ('260','260')], string='Options')
    db_print_option = fields.Selection([('262','262'), ('263','263'), ('264','264')], string='Options')
    db_app_type = fields.Selection([('front_back','Front & Back'), ('wrap','Wrap Around')], 'Droper Bottle Label Application Type')
    db_label_supplier = fields.Many2one('res.partner', 'Droper Bottle Label Supplier')
    db_label_size = fields.Char('Droper Bottle Label Size')
    db_bl_print_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Droper Bottle Label Print Finish')
    db_b_spec_print = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    db_b_label_artwork = fields.Binary('Droper Bottle Label Artwork')
    db_print_finish = fields.Selection([
                        ('matt','Matt'), ('gloss', 'Gloss'), ('uncoated','Uncoated')
                        ], string='Droper Bottle Print Finish')
    db_spec_print = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    db_label_artwork = fields.Binary('Droper Bottle Printed Artwork')
    db_cap_material = fields.Char('Droper Bottle Cap Material')
    db_cap_colour = fields.Char('Droper Bottle Cap Colour')
    db_tamper_evidence = fields.Char('Tamper Evidence')

    #Tray Case
    tc_colour = fields.Char('Tray Case Colour')
    tc_logo_colour = fields.Char('Tray Case Logo Colour')
    tc_spec_print = fields.Selection([
                        ('non','None'),
                        ('hotfoil', 'Hot Foil'),
                        ('spotuv', 'Spot UV')
                        ], string='Special Printing')
    tc_material = fields.Char('Material')
    tc_size = fields.Char('Size')
    tc_artwork = fields.Binary('Artwork')

    #Leaflet
    leaflet_details = fields.Char('Leaflet')
    leaflet_artwork = fields.Binary('Artwork')

    #Component Type
    component_type = fields.Char('Component Type')

    # Pallet Configurator
    pallet_type = fields.Selection([('standard', 'Standard'), ('euro', 'Euro')], string='Pallet Type')
    cartons_per_row = fields.Char('Cartons Per Row')
    number_of_rows = fields.Char('Number Of Rows')
    max_pallet_height_cm = fields.Char('Max Pallet Height (cm)')
    corners = fields.Selection([('yes','Yes'), ('no','No')], string='Corners')
    wrapping_colour = fields.Selection([('clear','Clear'), ('black','Black')], string='Wrapping Colour')
    upload_pallet_configurator_pdf = fields.Binary('Upload Pallet Configurator PDF')

    @api.onchange('bom_id')
    def _onchange_formula_version_number(self):
        for rec in self:
            if rec.bom_id:
                rec.formula_version_number = rec.bom_id.code

    @api.onchange('product_id')
    def _onchange_finished_goods_number(self):
        for rec in self:
            if rec.product_id:
                rec.finished_goods_number = rec.product_id.default_code

    @api.model
    def create(self,vals):
        if vals.get('name',_('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('finished.product.specification') or _('ref')
        res = super(FinishedProductSpecification, self).create(vals)
        return res
