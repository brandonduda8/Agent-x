from core.genesis.executive.executive_board import (
    executive_board
)


print("="*60)
print("👑 GENESIS EXECUTIVE BOARD TEST")
print("="*60)


opportunity = {
    "market":"Healthcare AI",
    "score":92
}


result = executive_board.evaluate(
    opportunity
)


print(result)


print({
    "system": executive_board.system,
    "cycles": len(executive_board.cycles)
})
