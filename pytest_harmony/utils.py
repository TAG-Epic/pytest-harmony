import typing
import typing_extensions
import asyncio

P = typing_extensions.ParamSpec("P")
T = typing.TypeVar("T")


async def maybe_coro(coro: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """Execute a sync or async function
    Parameters
    ----------
    coro:
        The function to execute
    args:
        The arguments to pass to the function
    kwargs:
        The keyword arguments to pass to the function
    Returns
    -------
    :data:`typing.Any`
        The result of the function
    """
    result = coro(*args, **kwargs)

    if asyncio.iscoroutine(result):
        # coro was a async function
        return await result

    # Not a async function, just return the result
    return result
