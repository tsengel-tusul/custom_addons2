from odoo import api, fields, models

class HospitalPatientt(models.Model):
    _name='hospital.appointment'
    _description='Hospital Appointment'
    _inherit = ['mail.thread']
    _rec_name='patient_id'
   # _rec_names_search=['reference','patient_id']

    reference=fields.Char(string="Reference", default='New')
    patient_id=fields.Many2one("hospital.patient2", string="Patient")
    date_appointment=fields.Date(string="Date")
    note=fields.Text(string="Note") 
    state=fields.Selection([('draft','Draft'),('confirmed','Confirmed'), ('ongoing','Ongoing'),('done','Done'),('cancel','Cancelled')])
    appointment_line_ids=fields.One2many('hospital.appointment.line','appointment_id', string="Lines") 
    total_qty=fields.Float(compute='_compute_total_qty', string="Total Quantity", store=True)
    date_of_birth=fields.Date(string="DOB",related='patient_id.date_of_birth')

    
    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
           # total_qty=0
           #print(rec.appointment_line_ids)
           # for line in rec.appointment_line_ids:
           #     total_qty=total_qty+line.qty
           # rec.total_qty=total_qty

           rec.total_qty=sum(rec.appointment_line_ids.mapped('qty'))
    #compute display name
    def _compute_display_name(self):
        for rec in self:
            print("values is", f"[{rec.reference}] {rec.patient_id.name}")
            rec.display_name=f"[{rec.reference}] {rec.patient_id.name}"
    @api.model_create_multi
    def create(self, vals_list):
        print("odoo mates", vals_list)
        for vals in vals_list:
            if not vals.get('reference')or vals['reference']=='New':
                vals['reference']=self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)
    def action_confirm(self):
        for rec in self:
            print("reference button is clicked", self.reference)


class HospitalAppointmentLine(models.Model):
    _name='hospital.appointment.line'
    _description='Hospital Appointment Lines'

    appointment_id=fields.Many2one('hospital.appointment',string="Appointment")
    product_id=fields.Many2one('product.product',string='Product', required=True)
    qty=fields.Float(string="Quantity")
    