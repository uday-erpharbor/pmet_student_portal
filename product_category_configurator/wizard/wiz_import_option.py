# -*- coding: utf-8 -*-
import base64
import logging

from io import BytesIO

from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import openpyxl
except ImportError:
    _logger.debug('Cannot `import openpyxl`.')


class WizardImportOption(models.TransientModel):
    _name = 'wiz.import.option'
    _description = 'Import Option Data'

    file_name = fields.Binary(string='File', help="Upload only the .xlsc file")

    def get_sheet_record(self, sheet):
        """get rows and columns sheet"""
        records = sheet.iter_rows(
            min_row=2, max_row=None, min_col=None, max_col=None,
            values_only=True)
        return records

    def import_data(self):
        """Import xlsx file records"""
        if not self.file_name:
            raise UserError(_('Please upload the file.'))

        FIELD = self.env['item.generate.field']
        FIELD_OPTION = self.env['item.generate.field.selection']
        try:
            categery_id = self._context.get('active_id')
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file_name)), read_only=True)
            sheets = wb.worksheets
            ## Options Sheet
            for sheet in sheets:
                _logger.info(f"Importing {sheet.title} Sheet")
                for record in self.get_sheet_record(sheet):
                    if record[0]:
                        # Search if the dynamic selection field exist else create new field
                        field_id = FIELD.search([
                            ('product_categery_id', '=', categery_id),
                            ('field_type', '=', 'option'), 
                            ('name', '=', record[0])
                        ], limit=1, order="id desc")
                        if not field_id and record[0]:
                            field_id = FIELD.create({
                                'name': record[0] or '',
                                'field_type': 'option',
                                'product_categery_id': categery_id
                            })
                        ## Selection Field Option
                        if field_id and record[1]:
                            option_id = FIELD_OPTION.search([
                                ('item_id', '=', field_id.id),
                                ('name', '=', record[1])
                            ], limit=1, order="id desc")
                            if not option_id:
                                option_id = FIELD_OPTION.create({
                                    'name': record[1] or '',
                                    'item_id': field_id.id,
                                })
                            # Commit created records
                            self._cr.commit()
            _logger.info("\n\tData Imported Successfully")
        except Exception as e:
            raise UserError(_('Please insert a valid file:\n"%s"') % (e))
