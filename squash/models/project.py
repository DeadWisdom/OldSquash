from squash.util import schema
import mutable

class Project(mutable.Mutable):
    def __init__(self, slug, name, description):
        self.slug = slug
        self.name = name
        self.description = description
    
    def __repr__(self):
        return self.slug
        
    def _update(self, details):
        return {
            'slug': schema.slug,
            'name': str,
            'description': str
        }

    def _details(self):
        yield {
            'pk': self.slug,
            'slug': self.slug,
            'name': self.name,
            'description': self.description
        }
    
    def yaml(self):
        return "\n".join([
            "%-9s%s" % ("slug:", self.slug),
            "%-9s%s" % ("name:", self.name),
            "description: ",
            "  " + self.description,
        ])
    
    def create_ticket(self):
        from ticket import Ticket
        ticket = Ticket(self)
        self.session.add(ticket)
        return ticket
    
    def get_ticket(self, id):
        from ticket import Ticket
        return self.session.query(Ticket).filter_by(project=self).filter_by(slug=id).first()
    
    def get_tickets(self):
        from ticket import Ticket
        return self.session.query(Ticket)
    
    @property
    def settings(self):
        return {
            'state_default': 'open',
            'state_closed': 'closed',
            'states': [
                'open',
                'invalid',
                'wontfix',
                'closed',
            ],
            'type_default': 'story',
            'types': [
                'story',
                'task',
                'bug',
                'chore'
            ],
        }

# Mapping
from tables import projects_table, mapper
mapper(Project, projects_table)