from core.genesis.approval_gateway import approval_gateway


print(
    approval_gateway.request_action(
        "Agent-X",
        "write_code",
        "Build Genesis mobile dashboard"
    )
)


payment = approval_gateway.request_action(
    "Revenue Agent",
    "create_payments",
    "Create Stripe checkout"
)


print(payment)


print(
    approval_gateway.approve(
        payment["id"]
    )
)


print(
    approval_gateway.report()
)
