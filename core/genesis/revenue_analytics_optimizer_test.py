from core.genesis.revenue_analytics_optimizer import (
    revenue_analytics_optimizer
)


print("=" * 60)
print("📊 GENESIS REVENUE ANALYTICS OPTIMIZER TEST")
print("=" * 60)


revenue_analytics_optimizer.record_result(
    "AI Automation Campaign",
    "Healthcare AI",
    "AI automation package",
    5000,
    "WON"
)


revenue_analytics_optimizer.record_result(
    "AI Automation Campaign",
    "Real Estate AI",
    "AI automation package",
    5000,
    "WON"
)


analysis = (
    revenue_analytics_optimizer
    .analyze_performance()
)


optimization = (
    revenue_analytics_optimizer
    .generate_optimization(
        analysis
    )
)


print(analysis)

print(optimization)

print(
    revenue_analytics_optimizer.report()
)
