import os
import time

from core.genesis.memory_engine import memory_engine


class GenesisLandingPageFactory:

    def __init__(self):

        self.name = "GENESIS LANDING PAGE FACTORY v1"
        self.pages = []


    def create_page(
        self,
        product_name,
        description,
        checkout_url
    ):

        print(
            f"🌐 Creating landing page: {product_name}"
        )


        html = f"""
<!DOCTYPE html>
<html>

<head>

<title>{product_name}</title>

<style>

body {{
font-family: Arial;
max-width:900px;
margin:auto;
padding:40px;
}}

.button {{

background:#635bff;
color:white;
padding:15px 30px;
border-radius:8px;
text-decoration:none;

}}

</style>

</head>


<body>


<h1>{product_name}</h1>

<h2>
AI automation built for modern businesses
</h2>


<p>
{description}
</p>


<h3>
Features
</h3>

<ul>

<li>AI powered automation</li>

<li>Save time and reduce costs</li>

<li>Scale your business faster</li>

</ul>


<a class="button" href="{checkout_url}">
Start Now
</a>


</body>

</html>
"""


        filename = (
            f"workspace/pages/"
            f"{product_name.replace(' ','_')}.html"
        )


        os.makedirs(
            "workspace/pages",
            exist_ok=True
        )


        with open(filename,"w") as f:

            f.write(html)



        result = {

            "product":
                product_name,

            "file":
                filename,

            "checkout":
                checkout_url,

            "timestamp":
                time.time()

        }


        self.pages.append(result)


        memory_engine.remember_knowledge(

            "landing_page",

            result,

            confidence=0.9

        )


        return result



    def report(self):

        return {

            "system":
                self.name,

            "pages":
                len(self.pages),

            "timestamp":
                time.time()

        }



landing_page_factory = GenesisLandingPageFactory()
