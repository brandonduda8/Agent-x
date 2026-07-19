import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

from core.genesis.stripe_manager import stripe_manager


print("================================")
print("💳 GENESIS STRIPE TEST")
print("================================")


print(
    stripe_manager.report()
)


if stripe_manager.connected:

    print(
        "✅ Stripe is ready for Genesis revenue automation"
    )

else:

    print(
        "❌ Stripe connection failed"
    )
