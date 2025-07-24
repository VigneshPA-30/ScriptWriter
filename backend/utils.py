from agents.lifecycle import RunHooksBase # or AssistantAgent, depending on your setup
import asyncio, random, functools, time
from openai import RateLimitError
from typing import Iterable, Optional

# If your agents SDK exposes a base Hook class, inherit from it.
try:
    from agents import Hook               # >= v0.7.0
except ImportError:                        # older SDKs use a plain object
    class Hook:                            # fallback shim
        pass

class DelayHook(RunHooksBase):
    """
    Insert a fixed pause *before* every tool‑call item that matches `only_for`.

    Args:
        seconds (float): how long to wait (default 3 s).
        only_for (Iterable[str] | None): list of tool‑names to delay.
            If None, **all** tools are delayed.
    """

    

    async def on_agent_start(self, context, agent ):
        tool_call_count = 0
        return

    async def on_tool_start(self, context, agent,tool) -> int:
        """
        Fired once, right before the first turn of the run.
        We don’t need to delay here, so it’s just a no‑op [does nothing].
        """
        self.tool_call_count += 1
        return self.tool_call_count
    # -------- Runner hook entry‑points --------
    # The Runner fires `on_run_item` *just before* the item is executed.

    async def on_agent_prompt(self, agent, prompt, run_context):
           return (
            f"""{prompt}\n\nIMPORTANT :You have already used tools {self.tool_call_count} times """
        )


        
complete_automatic = True
user_niche = "Best AI Startups"



# utils/backoff.py


def async_backoff(retries: int = 6, base_delay: float = 2.0, max_delay: float = 60.0):
    """
    Exponential back‑off with jitter [small random wiggle] for async funcs.
    """
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(retries):
                try:
                    return await fn(*args, **kwargs)
                except RateLimitError as e:
                    if attempt == retries - 1:
                        raise                       # exhausted
                    jitter = delay * 0.25 * random.random()
                    await asyncio.sleep(min(delay + jitter, max_delay))
                    delay *= 2                     # exponential
            # Shouldn’t reach here
        return wrapper
    return decorator



# utils/cache.py  – new file


def async_ttl_cache(maxsize: int = 1000, ttl_seconds: float = 86_400):
    """
    Very small async‑safe cache decorator.
    Drops the oldest entry when over `maxsize`.
    """
    cache: dict[str, tuple[float, any]] = {}
    lock = asyncio.Lock()

    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(url: str, *args, **kwargs):
            async with lock:
                ts_val = cache.get(url)
                if ts_val and (time.time() - ts_val[0]) < ttl_seconds:
                    return ts_val[1]                 # ← HIT

            result = await fn(url, *args, **kwargs)   # ← MISS
            async with lock:
                if len(cache) >= maxsize:
                    cache.pop(next(iter(cache)))       # drop oldest
                cache[url] = (time.time(), result)
            return result

        return wrapper
    return decorator



# utils/throttle.py  – drop this next to backend/utils.py


def rate_limited(min_interval_sec: float = 3.0):
    """
    Decorator that ensures at most one call passes every `min_interval_sec`.
    """
    lock = asyncio.Lock()
    last_call = 0.0

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                nonlocal last_call
                async with lock:
                    wait = min_interval_sec - (time.time() - last_call)
                    if wait > 0:
                        await asyncio.sleep(wait)
                    result = await func(*args, **kwargs)
                    last_call = time.time()
                    return result
            return wrapper
        else:  # sync fallback
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal last_call
                wait = min_interval_sec - (time.time() - last_call)
                if wait > 0:
                    time.sleep(wait)
                result = func(*args, **kwargs)
                last_call = time.time()
                return result
            return wrapper
    return decorator
