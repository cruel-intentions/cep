import json
import urllib
from urllib.parse import urlencode

mkargs = lambda uf_id: urlencode({"localidades": f"n6[n3[{uf_id}]]"})
mkurl = lambda uf_id: f'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2020/variaveis/9324?{mkargs(uf_id)}'

curl_cmd = lambda uf: f"""
    curl \\
       '{mkurl(uf["id"])}' \\
        -o ./raw/cities/{uf["sigla"]}_ibge_population.json"""

ufs = lambda: json.load(open("./raw/uf_ibge.json"))

print(
    "\nsleep 2".join(
        map(curl_cmd, ufs())
    )
)
