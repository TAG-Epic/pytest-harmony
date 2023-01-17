from __future__ import annotations
import typing
import typing_extensions
import pytest
from .utils import maybe_coro

HANDLER: typing_extensions.TypeAlias = typing.Callable[[typing.Dict[str, typing.Any]], typing.Any]
STATE: typing_extensions.TypeAlias = typing.Dict[str, typing.Any]

class TreeTests:
    """A tree of tests

    A stack like test runner, primarily made for pytest

    **Example usage**

    .. code-block:: python3
        from pytest_harmony import TreeTests

        tree = TreeTests()
        test_tree = tree.create_pytest()

        @tree.append()
        async def first_link(state):
            print("Called first")
            state["counter"] = 1
        @first_link.cleanup(state)
        async def cleanup_first_link(state):
            print("Called fourth")
            state["counter"] -= 1
            assert state["counter"] != 0

        @first_link.append()
        async def second_link(state)
            print("Called second")
            state["counter"] += 1

        @second_link.cleanup()
        async def cleanup_second_link(state):
            print("Called third")
            state["counter"] -= 1

    **Visualized**
    - Test 1 runs
      - Test 2 runs
      - Test 2 cleanup gets called
    - Test 1 cleanup gets called
    """
    def __init__(self) -> None:
        self._sub_trees: list[TreeTests] = []
        self._run_handler: HANDLER | None = None
        self._cleanup_handler: HANDLER | None = None

    def append(self) -> typing.Callable[[HANDLER], TreeTests]:
        """Register a sub-tree

        .. code-block:: python3
            from pytest_harmony import TreeTests

            tree = TreeTests()

            @tree.append()
            async def sub_tree(state):
                state["oh"] = "shiny"
        """
        def capture_run_handler(handler: HANDLER) -> TreeTests:
            tree = self._from_run_handler(handler)
            self._sub_trees.append(tree)

            return tree
        return capture_run_handler

    @classmethod
    def _from_run_handler(cls, handler: HANDLER) -> TreeTests:
        instance = cls()
        instance._run_handler = handler

        return instance

    def cleanup(self) -> typing.Callable[[HANDLER], None]:
        """Register a cleanup handler

        .. code-block:: python3
            from pytest_harmony import TreeTests

            tree = TreeTests()

            @tree.cleanup()
            async def on_cleanup(state):
                print(state)
        """
        def capture_run_handler(handler: HANDLER) -> None:
            self._cleanup_handler = handler

        return capture_run_handler

    async def run_tests(self, *, state: STATE | None = None) -> None:
        """Manually run tests.

        .. hint::
            If you are using pytest use :meth:`create_pytest`

        **Example usage**
        .. code-block:: python3
            from pytest_harmony import TreeTests
            import asyncio

            tree = TreeTests()
            asyncio.run(tree.run_tests())

        """
        if state is None:
            state = {}
        
        if self._run_handler is not None:
            await maybe_coro(self._run_handler, state)

        for tree in self._sub_trees:
            await tree.run_tests(state=state)

        if self._cleanup_handler is not None:
            await maybe_coro(self._cleanup_handler, state)

    def create_pytest(self) -> typing.Callable[[], typing.Awaitable[None]]:
        """Creates a test compatible with pytest

        **Example usage**
        .. code-block:: python3
            from pytest_harmony import TreeTests

            tree = TreeTests()
            test_tree = tree.create_pytest()
        """
        @pytest.mark.asyncio
        async def test_tree() -> None:
            await self.run_tests()
        return test_tree
