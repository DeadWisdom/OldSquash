from base import Action

class Ticket(Action):
    help = 'Ticket manipulation.'
    
    def run(self, repo, args):
        if args.project:
            project = repo.get_project(args.project)
        else:
            project = repo.get_working_project()
                    
        if args.add:
            ticket = project.create_ticket()
            args.name = args.id
        else:
            ticket = project.get_ticket(args.id)
            if ticket is None:
                self.log("# Cannot find ticket: %s\n", args.id)
                return
        
        if args.delete:
            if not args.noinput:
                if not raw_input("Enter 'delete' to confirm deleting the ticket '%s': " % ticket.name) == 'delete':
                    self.log("\n# Aborted.")
                    return
                self.log('\n')
            
            repo.session.delete(ticket)
            self.log("# Ticket deleted: %s\n" % ticket.name)
            return
        
        ticket.update(dict((k, v) for k, v in args.__dict__.items() if v is not None))
        repo.session.flush()
        self.log("%s\n", ticket.yaml())

Ticket.add_argument('id', type=str,
                           help='slug, id, or name of the ticket')
                               
Ticket.add_argument('-a', '--add', help='add a new ticket', action='store_true')
Ticket.add_argument('-x', '--delete', help='delete the ticket (you might want change its status instead)', action='store_true')
Ticket.add_argument('-d', '--description', help='set the description', type=str, nargs='?')
Ticket.add_argument('-s', '--slug', help='set the slug', type=str, nargs='?')
Ticket.add_argument('-n', '--name', help='set the name', type=str, nargs='?')
Ticket.add_argument('-t', '--status', help='set the status', type=str, nargs='?')
Ticket.add_argument('-p', '--project', help='specify the project, otherwise squash will use the working project', type=str, nargs='?')


class List(Action):
    help = 'List tickets in the project.'
    
    def run(self, repo, args):
        if args.project:
            project = repo.get_project(args.project)
        else:
            project = repo.get_working_project()
        
        if args.open:
            args.status = 'open'
        
        if args.status:
            tickets = project.get_tickets().filter_by(status=args.status)
        else:
            tickets = project.get_tickets()
        
        if (tickets.count() == 0):
            self.log("No tickets found.")
            return
        
        sz = max(len(t.slug) for t in tickets)
        if sz < 10:
            sz = 10
        line = "%%-%ds  %%s\n" % sz
        
        for t in tickets:
            self.log(line, t.slug, t.name)

List.add_argument('-p', '--project', help='specify the project, otherwise squash will use the working project', type=str, nargs='?')
List.add_argument('-t', '--status', help='only list tickets with this status', type=str, nargs='?')
List.add_argument('-o', '--open', help='only list open tickets', action='store_true')

