from treelib import Tree

flatten = lambda l: [item for sublist in l for item in sublist]


def get_team_hierarchy_tree(all_teams):
    team_list = []
    for team in all_teams:
        team_list.append({'team': team, 'children': team.sub_teams()})

    return TeamHierarchy(team_list).tree


def find_children(team_list):
    return flatten([team['children'] for team in team_list])


def find_roots(team_list):
    children = find_children(team_list)
    teams = [team['team'] for team in team_list]

    root_ids = list(set([team.Id for team in teams]) - set([team.Id for team in children]))

    return [team for team in teams if team.Id in root_ids]


class TeamHierarchy:
    def __init__(self, all_teams):
        self.all_teams = all_teams
        self.tree = Tree()
        self.tree.create_node('root', 'root')

        roots = find_roots(self.all_teams)
        self._add_node('root', roots)

    def _add_node(self, root_id, children):
        for child in children:
            self.tree.create_node(child.Name, child.Name, root_id, child)

            team = next(x for x in self.all_teams if x['team'].Id == child.Id)

            children_of_children = flatten([x['children'] for x in self.all_teams if x['team'].Id in [child.Id for child in team['children']]  ])
            direct_children = list(set(team['children']) - set(children_of_children))

            self._add_node(child.Name, direct_children)
