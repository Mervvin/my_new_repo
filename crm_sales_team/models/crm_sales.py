from odoo import models, api

class CrmSales(models.Model):
    _inherit = 'crm.lead'

    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):

        # Get the teams associated with the current user
        teams = self._get_user_teams()

        # Update the domain based on user permissions
        domain = self._update_domain(domain, teams)

        return super(CrmSales, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)

    def _get_user_teams(self):
        """Get the teams associated with the current user."""
        return self.env['crm.team'].search([('user_id', '=', self.env.user.id)]).mapped('member_ids')

    def _update_domain(self, domain, teams):
        """Update the domain based on user permissions."""
        if self.env.user.has_group('sales_team.group_sale_manager'):
            domain = ['|', ('user_id', 'in', teams.ids), ('user_id', '=', self.env.user.id)] + (domain or [])
        return domain
