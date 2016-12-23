from nose.tools import eq_, assert_true

from litmos.team_hierarchy import TeamHierarchy,\
    find_children,\
    find_roots,\
    get_team_hierarchy_tree


class Team(object):
    pass

    def sub_teams(self):
        return self.children


class TestTeamHierarchy:
    def setUp(self):
        self.team_list = []

        self.team1 = Team()
        self.team1.Name = 'team1'
        self.team1.Id = 'team1'

        self.team4 = Team()
        self.team4.Name = 'team4'
        self.team4.Id = 'team4'

        self.team2 = Team()
        self.team2.Name = 'team2'
        self.team2.Id = 'team2'

        self.team3 = Team()
        self.team3.Name = 'team3'
        self.team3.Id = 'team3'

        self.team5 = Team()
        self.team5.Name = 'team5'
        self.team5.Id = 'team5'

        self.team_list.append({'team': self.team3, 'children': [self.team2, self.team1, self.team4]})
        self.team_list.append({'team': self.team2, 'children': [self.team1, self.team4]})
        self.team_list.append({'team': self.team1, 'children': []})
        self.team_list.append({'team': self.team4, 'children': [self.team5]})
        self.team_list.append({'team': self.team5, 'children': []})

        self.team3.children = [self.team2, self.team1, self.team4]
        self.team2.children = [self.team1, self.team4]
        self.team1.children = []
        self.team4.children = [self.team5]
        self.team5.children = []

    def test__find_children(self):
        children = find_children(self.team_list)

        expected_result = [self.team2, self.team1, self.team4, self.team1, self.team4, self.team5]

        eq_(len(children), len(expected_result))
        assert_true(all(x in children for x in expected_result))

    def test__find_roots(self):
        children = find_roots(self.team_list)

        expected_result = [self.team3]

        eq_(len(children), len(expected_result))
        assert_true(all(x in children for x in expected_result))

    def test_create_tree(self):
        hierarchy = TeamHierarchy(self.team_list)

        tree = hierarchy.tree

        expected_result = [['root', 'team3', 'team2', 'team4', 'team5'], ['root', 'team3', 'team2', 'team1']]
        tree_paths = tree.paths_to_leaves()

        eq_(len(tree_paths), len(expected_result))
        assert_true(all(x in tree_paths for x in expected_result))

    def test_get_team_hierarchy_tree(self):
        tree = get_team_hierarchy_tree([self.team1, self.team2, self.team3, self.team4, self.team5])

        expected_result = [['root', 'team3', 'team2', 'team4', 'team5'], ['root', 'team3', 'team2', 'team1']]
        tree_paths = tree.paths_to_leaves()

        eq_(len(tree_paths), len(expected_result))
        assert_true(all(x in tree_paths for x in expected_result))
