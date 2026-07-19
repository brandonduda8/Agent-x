from core.genesis.entrepreneur.entrepreneur_engine import (
    entrepreneur_engine
)

from core.genesis.entrepreneur.venture_builder import (
    venture_builder
)

from core.genesis.entrepreneur.company_launcher import (
    company_launcher
)


print("=" * 60)
print("🧬 GENESIS AUTONOMOUS ENTREPRENEUR ENGINE TEST")
print("=" * 60)


venture = entrepreneur_engine.create_venture()

build = venture_builder.build(
    venture["company"]
)

launch = company_launcher.launch(
    venture["company"]
)


print({
    "venture": venture,
    "build": build,
    "launch": launch
})


print(
    entrepreneur_engine.report()
)
