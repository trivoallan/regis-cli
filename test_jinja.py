import jinja2

env_default = jinja2.Environment()
try:
    print("Default:", env_default.from_string("{{ request.metadata.user | default('Unknown') }}").render(request={}))
except Exception as e:
    print("Default Error:", type(e), e)

try:
    env_chain = jinja2.Environment(undefined=jinja2.ChainableUndefined)
    print("Chainable:", env_chain.from_string("{{ request.metadata.user | default('Unknown') }}").render(request={}))
except Exception as e:
    print("Chainable Error:", type(e), e)
