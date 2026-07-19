from core.genesis.android_skill_engine import android_skill_engine


skill = android_skill_engine.create_skill(

    "Genesis Notification Assistant",

    "Create Android notifications from Genesis events",

    "Hermes",

    "notification.create"

)


print(skill)


print(
    android_skill_engine.activate_skill(
        skill["id"]
    )
)


print(
    android_skill_engine.discover_skills()
)


print(
    android_skill_engine.status()
)
