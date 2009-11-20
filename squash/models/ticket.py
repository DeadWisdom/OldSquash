from squash.util import schema
from project import Project
import mutable

class Ticket(mutable.Mutable):
    def __init__(self, project):
        self.project = project
        self.slug = ''
        self.status = project.settings['state_default']
        self.name = ''
        self.type = project.settings['type_default']
        self.owner = ''
        self.reporter = ''
        self.description = ''
    
    def __repr__(self):
        return self.slug
        
    def _update(self, details):
        if not self.slug and not details.get('slug') and details.get('name'):
            details['slug'] = schema.slug(details['name'])
        
        return {
            'slug': str,
            'name': str,
            'status': str,
            'description': str,
            'reporter': str,
            'owner': str,
            'type': str,
            'project_id': str,
        }
    
    def _details(self):
        yield {
            'pk': self.id,
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'status': self.status,
            'description': self.description,
            'reporter': self.reporter,
            'owner': self.owner,
            'type': self.type,
            'project': self.project.id,
        }
    
    def yaml(self):
        return "\n".join([
            "# %s ticket %s" % (self.project.name, self.id),
            "%-11s%s" % ("slug:", self.slug),
            "%-11s%s" % ("name:", self.name),
            "%-11s%s" % ("type:", self.type),
            "%-11s%s" % ("status:", self.status),
            "%-11s%s" % ("owner:", self.owner),
            "%-11s%s" % ("reporter:", self.reporter),
            "description: ",
            "    %s" % self.description,
        ])

# Mapping
from tables import tickets_table, mapper, relation

mapper(Ticket, tickets_table, properties={
    'project': relation(Project, backref='tickets')
})