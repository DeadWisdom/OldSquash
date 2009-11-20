from base import Response, Resource
from squash.util import serialize

class ProjectList(Resource):
    url = '*.[format]'
    
    def get(self, repo, request, format=None):    
        """List all projects."""
        return [o.details() for o in repo.get_projects()]

class Project(Resource):
    url = '[project].[format]'
    
    def get(self, repo, request, project=None):
        """Get the details of a project."""
        project = repo.get_project(project)
        if project:
            return project.details()
    
    def post(self, repo, request, project=None):
        """Post changes to a project."""
        project = repo.get_project(project)
        if project:
            return project.update(serialize.load(request.input, request.format))
    
    def put(self, repo, request, project=None):
        """Put a new project."""
        project = repo.create_project(project)
        return project.update(serialize.load(request.input, request.format))
    
    def delete(self, repo, request, project=None):
        """Delete the project."""
        project = repo.get_project(project)
        if project:
            repo.session.delete(project)
            return True
        
        