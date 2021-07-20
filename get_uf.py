
curl_cmd = lambda uf: f"""
    curl 'https://buscacepinter.correios.com.br/app/faixa_cep_uf_localidade/carrega-faixa-cep-uf.php' \\
            -H 'content-type: application/x-www-form-urlencoded; charset=utf-8' \\
            --data-raw 'letraLocalidade=&ufaux=&pagina=%2Fapp%2Ffaixa_cep_uf_localidade%2Findex.php&mensagem_alerta=&uf={uf}&localidade=&cepaux=' \\
            -o ./raw/uf/{uf}.json"""

ufs = lambda: """AC
AL
AM
AP
BA
CE
DF
ES
GO
MA
MG
MS
MT
PA
PB
PE
PI
PR
RJ
RN
RO
TO
RR
RS
SC
SE
SP""".split("\n")
print("""
sleep 2
""".join(list(map(curl_cmd, ufs()))))
