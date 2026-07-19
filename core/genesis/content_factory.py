import time

from core.genesis.memory_engine import memory_engine


class GenesisContentFactory:

    def __init__(self):

        self.name = "GENESIS CONTENT FACTORY v1"

        self.generated = []



    def create_campaign(self, product, audience, angle):

        content = {

            "product":
                product,

            "audience":
                audience,

            "angle":
                angle,


            "linkedin_post":
                f"""
🚀 {product}

Businesses are losing time answering the same questions every day.

What if AI could handle customer conversations instantly?

✅ Faster responses
✅ More qualified leads
✅ Lower support costs

The future of business is intelligent automation.
""",


            "twitter_post":
                f"""
Building smarter businesses with {product}.

AI automation helps companies:
- save time
- respond faster
- increase revenue

The next generation of companies will be AI-powered.
""",


            "cold_email":
                f"""
Subject: Quick question about your customer support

Hi,

I noticed many businesses struggle with responding quickly to customers.

We built {product} to help automate conversations and improve response times.

Would you be interested in seeing how it works?

Thanks
""",


            "video_script":
                f"""
Hook:
Your customers are waiting too long.

Problem:
Slow responses lose sales.

Solution:
{product} uses AI automation to respond instantly.

Call to action:
Try it today.
"""

            ,

            "timestamp":
                time.time()

        }


        self.generated.append(content)


        memory_engine.remember_knowledge(
            "content_campaign",
            content,
            confidence=0.8
        )


        return content



    def report(self):

        return {

            "engine":
                self.name,

            "campaigns_created":
                len(self.generated),

            "timestamp":
                time.time()

        }



content_factory = GenesisContentFactory()
