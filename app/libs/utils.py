# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/14.
"""

__author__ = 'Allen7D'


class TreeNode(object):
    def __init__(self, id, parent_id):
        self.id = id
        self.parent_id = parent_id
        self.children = []

    def add_sub_node(self, tree_node):
        self.children.append(tree_node)

    def rm_sub_node(self, sub_node_id):
        for tree_node in self.children:
            if tree_node.id == sub_node_id:
                self.children.remove(tree_node)

    def keys(self):
        return 'id', 'parent_id', 'children'

    def __getitem__(self, item):
        return getattr(self, item)


class Tree(object):
    def __init__(self, root=None, nodeType=TreeNode):
        self.root = root
        self.nodeType = nodeType

    def generate_by_list(self, tree_list: list):
        """
            :param tree_list: 节点元素不含有children
        """
        # 建立id-route映射表
        id2node_dir = {}
        for line in tree_list:
            node = self.nodeType(**line)
            id2node_dir[node.id] = node
        # 遍历映射表, 将当前节点添加至父节点的children中
        for dir_node in id2node_dir.values():
            if not (dir_node.parent_id == 0 and dir_node.id == 0):
                id2node_dir[
                    dir_node.parent_id
                ].add_sub_node(dir_node)

        self.root = id2node_dir[0] if id2node_dir != {} else self.nodeType(id=0, parent_id=0)

    def generate_by_dir(self, tree_dir: dir):
        """
            :param tree_dir: 节点元素不含有parent
        """
        def create_node(cur_node_dir):
            node = self.nodeType(**cur_node_dir)
            if 'children' in cur_node_dir and \
                    len(cur_node_dir['children']) != 0:
                for child_node_dir in cur_node_dir['children']:
                    node.add_sub_node(create_node(child_node_dir))
            else:
                pass
            return node

        self.root = create_node(tree_dir)

    def serialize(self) -> dir:
        def serialize_node(tree_node):
            result = dict(tree_node)
            result['meta'] = {
                'icon': result['icon'],
                'title': result['title']
            }
            result.pop('icon')
            result.pop('title')
            result['children'] = [serialize_node(sub_node) for sub_node in tree_node.children]
            return result

        return serialize_node(self.root)

    def deserialize(self) -> list:
        tree_list = []

        def deserialize_node(cur_node, parent_id):
            result = dict(cur_node)
            result['parent_id'] = parent_id if parent_id else 0
            tree_list.append(result)
            for child_node in cur_node.children:
                deserialize_node(child_node, cur_node.id)

        deserialize_node(self.root, self.root.parent_id)
        return tree_list
