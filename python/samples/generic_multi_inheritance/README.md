Generic + Multiple Inheritance (Python)

What this shows
- Multiple inheritance: combine behavior from a "context" base and a generic "component" base.
- Generics: type-safe configuration object via Component[TConfig].
- Practical pattern: build featureful, reusable components that still carry domain-specific context.

Files
- component.py: Generic Component[TConfig] base.
- context_base.py: ChatCompletionContext base for message history.
- unbounded_context.py: UnboundedChatCompletionContext(ChatCompletionContext, Component[Config]).
- main.py: Small runnable demo.

Why this is useful
- Separation of concerns: context manages chat history; component manages lifecycle/config.
- Type safety: the config is strongly typed (e.g., UnboundedChatCompletionContextConfig), improving IDE help and mypy/pyright checks.
- Composition via inheritance: order matters (left wins if methods collide). You get a single object that is both a context and a component.
- Reuse: create more contexts that re-use the same generic component infra with different config types.

Run
1) From repo root, ensure Python env is active (see repository guidelines).
2) Run the sample (module mode so package imports work):
   - python -m python.samples.generic_multi_inheritance.main

Notes
- This sample keeps code minimal and type-hinted. See docstrings for quick guidance.
