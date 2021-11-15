import typing

ParentT = typing.TypeVar("ParentT")
ChildT = typing.TypeVar("ChildT")


class Node(typing.Generic[ParentT, ChildT]):
    def __init__(
        self,
        *,
        content: ParentT,
        parent: typing.Optional["Node[ParentT, typing.Any]"] = None,
    ) -> None:
        self.parent = parent
        self.content = content
        self.children = set()  # type: typing.Set[Node[ChildT, typing.Any]]

    def addchild(self, child: "Node[ChildT, typing.Any]"):
        self.children.add(child)

    def from_content(self, content: ParentT):
        node = Node(content=content)
        self.addchild(node)
        return node


class RootNode(Node[ParentT, ChildT]):
    def __init__(
        self,
    ) -> None:
        super().__init__(content=None, parent=None)  # type: ignore
