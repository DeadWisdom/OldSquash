from base import Action

class Project(Action):
    name = 'project'
    help = 'Project manipulation.'
    
    def run(self, repo, args):
        if args.create:
            project = repo.create_project(args.id)
        elif args.id:
            project = repo.get_project(args.id)
        else:
            project = repo.get_working_project()
            if project is None:
                self.log('# No project found.\n')
                return
        
        if args.delete:
            if not args.noinput:
                if not raw_input("Enter 'delete' to confirm deleting the project '%s': " % project.name) == 'delete':
                    self.log("\n# Aborted.")
                    return
                self.log('\n')
            
            repo.session.delete(project)
            self.log("# Project deleted: %s\n" % project.name)
            return
        
        project.update(dict((k, v) for k, v in args.__dict__.items() if v is not None))

        if (args.create):
            self.log("# New project created: %s\n" % project.name)
            repo.set_working_project(project)
            
        self.log("\n%s\n", project.yaml())

Project.add_argument('id', type=str, 
                           nargs='?',
                           help='name or slug of the project'
                                '(you can ommit this if there is only one project)' )
                               
Project.add_argument('-c', '--create', help='create a new project', action='store_true')
Project.add_argument('-x', '--delete', help='delete the project', action='store_true')
Project.add_argument('-d', '--description', help='set the description', type=str, nargs='?')
Project.add_argument('-s', '--slug', help='set the slug', type=str, nargs='?')
Project.add_argument('-n', '--name', help='set the name', type=str, nargs='?')


class ProjectList(Action):
    name = 'projects'
    help = 'Lists projects.'
    
    def run(self, repo, args):
        one = False
        projects = repo.get_projects()
        if not projects.count():
            self.log("No projects found.\n")
        else:
            for project in projects:
                self.log(project.slug)
                self.log('\n')


class Switch(Action):
    help = 'Sets the working project.'
    
    def run(self, repo, args):
        project = repo.set_working_project(args.id)
        self.log("# Working project set to: %s\n", project.slug)
        
Switch.add_argument('id', type=str,
                           help='name or slug of the project')
                               