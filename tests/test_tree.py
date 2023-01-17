from pytest_harmony import TreeTests
import typing

tree = TreeTests()
test_tree = tree.create_pytest()

@tree.append()
def first_link(state: typing.Dict[str, int]):
  state["counter"] = 1
  
@first_link.cleanup()
def cleanup_tree_test_start(state: typing.Dict[str, int]):
  state["counter"] -= 1
  assert state["counter"] == 0

@first_link.append()
def second_link(state: typing.Dict[str, int]):
  state["counter"] += 1

@second_link.cleanup()
def cleanup_second_link(state: typing.Dict[str, int]):
  state["counter"] -= 1
