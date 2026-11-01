from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, re, json
from html.parser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.image = None
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta':
            if d.get('property') == 'og:title':
                self.title = d.get('content')
            if d.get('property') == 'og:image':
                self.image = d.get('content')

HTML_FINAL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AGENTE 1 ARQUIVO SÓ - VERCEL</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>body{background:#fff;color:#111;font-family:Inter,system-ui}.glass{background:#fff;border:1px solid #e5e5e5}.btn{background:linear-gradient(135deg,#ff6a00 0%,#ee0979 100%)}</style>
</head>
<body class="min-h-screen p-3">
<div class="max-w-[460px] mx-auto">
<div class="glass rounded-[16px] p-3">
<label class="text-[10px] font-bold uppercase">Seu link s.shopee.com.br (novo)</label>
<input id="aff" class="w-full mt-1 border-2 border-black rounded-xl p-3 text-[14px] font-bold" placeholder="https://s.shopee.com.br/5AthUrbuhN">
<button id="btn" class="btn w-full mt-3 p-3 rounded-xl font-black text-white">GERAR FOTO + VALOR REAL ⚡</button>
<div id="log" class="bg-black text-[#0f0] rounded-xl p-2 mt-2 h-[80px] overflow-auto text-[10px] font-mono"></div>
</div>
<div id="result" class="hidden mt-3">
<div class="glass rounded-[16px] p-3">
<span class="text-[11px] font-black">📸 FOTO REAL</span>
<div id="fotoBox" class="w-full rounded-xl bg-gray-50 border overflow-hidden relative mt-2" style="aspect-ratio:1/1;"><img id="fotoReal" class="w-full h-full object-cover"><div id="fotoLoad" class="absolute inset-0 flex items-center justify-center bg-white"><div class="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full"></div></div><div id="priceOverlay" class="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/90 to-transparent text-white hidden"><p id="oTitle" class="font-black text-[12px]"></p><p id="oPrice" class="font-black text-[16px] text-[#00FF88] mt-1"></p></div></div>
<div class="grid grid-cols-2 gap-2 mt-2"><button onclick="baixar()" class="bg-black text-white p-2 rounded-xl text-[11px] font-bold">Baixar Foto</button><button onclick="copiar()" class="bg-white border border-black p-2 rounded-xl text-[11px] font-bold">Copiar Mensagem</button></div>
</div>
<div class="glass rounded-[16px] p-3 mt-3"><span class="text-[11px] font-black">📱 MENSAGEM SEM # COM VALOR REAL</span><div id="msg" class="bg-green-50 border-2 border-green-200 rounded-xl p-3 mt-2 text-[13px] whitespace-pre-wrap text-black font-medium"></div><button onclick="whatsapp()" class="w-full mt-2 bg-[#25D366] p-3 rounded-xl font-black text-[12px]">Enviar no Zap</button><div id="info" class="mt-2 text-[10px] text-gray-600"></div></div>
</div>
</div>
<script>
let ORIGINAL="";function log(t){const $log=document.getElementById('log');const d=document.createElement('div');d.textContent=new Date().toLocaleTimeString()+" → "+t;$log.appendChild(d);$log.scrollTop=$log.scrollHeight;}function formatBRL(v){return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});}
document.getElementById('btn').onclick=async()=>{
 ORIGINAL=document.getElementById('aff').value.trim();if(!ORIGINAL){alert('Cole link');return;}document.getElementById('result').classList.remove('hidden');document.getElementById('log').innerHTML="";log(`Link fiel: ${ORIGINAL}`);log(`🚀 Servidor Vercel...`);try{const resp=await fetch(`?url=${encodeURIComponent(ORIGINAL)}`);const data=await resp.json();log(`✅ ${data.title?.slice(0,40)}`);const fotoReal=document.getElementById('fotoReal');const fotoLoad=document.getElementById('fotoLoad');const overlay=document.getElementById('priceOverlay');if(data.image){fotoReal.src=data.image;fotoReal.onload=()=>{fotoLoad.classList.add('hidden');overlay.classList.remove('hidden');};}document.getElementById('oTitle').textContent=(data.title||'Produto').slice(0,55);if(data.preco_atual){if(data.preco_antes && data.desconto>0){document.getElementById('oPrice').textContent=`DE ${formatBRL(data.preco_antes)} POR ${formatBRL(data.preco_atual)}`;}else{document.getElementById('oPrice').textContent=`${formatBRL(data.preco_atual)}`;}}let blocoPreco="",blocoDesc="";if(data.preco_atual){if(data.preco_antes && data.desconto>0){blocoPreco=`💰 DE: ~${formatBRL(data.preco_antes)}~ POR: ${formatBRL(data.preco_atual)}`;blocoDesc=`🔥 ${data.desconto}% OFF!`;}else{blocoPreco=`💰 POR APENAS: ${formatBRL(data.preco_atual)}`;}}else{blocoPreco=`💰 OFERTA - Confira no link`;}const msg=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\n\n📦 ${data.title.toUpperCase()}\n\n${blocoPreco}\n${blocoDesc}\n\n⚡ PRODUTO VERIFICADO!\n👇 LINK COM DESCONTO 👇\n\n${data.affiliate_link_original}\n\n⏰ Corre!`;document.getElementById('msg').textContent=msg;document.getElementById('info').innerHTML=`<span class="text-green-700 font-bold">🔒 Link 100% fiel: ${data.affiliate_link_original}</span>`;}catch(e){log(`❌ Erro: ${e.message}`);}};
function copiar(){navigator.clipboard.writeText(document.getElementById('msg').textContent);alert('Copiado!');}function baixar(){const img=document.getElementById('fotoReal');if(img.src) window.open(img.src,'_blank');}function whatsapp(){const txt=encodeURIComponent(document.getElementById('msg').textContent);window.open(`https://wa.me/?text=${txt}`,'_blank');}
</script>
</body>
</html>
"""

def resolve_shopee(url):
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            final_url = resp.geturl()
            html = resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {"affiliate_link_original": url, "title": "Produto Shopee", "image": None, "preco_atual": None, "error": str(e), "final_url": url}

    if "s.shopee.com.br" in final_url:
        m = re.search(r'https://shopee\.com\.br/[^"\'\s<>]+-i\.\d+\.\d+', html)
        if m:
            final_url = m.group(0)
            try:
                req2 = urllib.request.Request(final_url, headers=headers)
                with urllib.request.urlopen(req2, timeout=10) as r2:
                    html += "\n" + r2.read().decode('utf-8', errors='ignore')
            except:
                pass

    parser = MyParser()
    try:
        parser.feed(html)
    except:
        pass
    title = parser.title
    image = parser.image
    preco_atual = None
    preco_antes = None

    m = re.search(r'-i\.(\d+)\.(\d+)', final_url)
    if not m:
        m = re.search(r'-i\.(\d+)\.(\d+)', html)
    if m:
        shop_id = m.group(1)
        item_id = m.group(2)
        try:
            api_url = f"https://shopee.com.br/api/v4/item/get?itemid={item_id}&shopid={shop_id}"
            req_api = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req_api, timeout=10) as r_api:
                j = json.loads(r_api.read().decode('utf-8'))
                data = j.get('data')
                if data:
                    if data.get('name'):
                        title = data.get('name')
                    img_file = data.get('image') or (data.get('images') and data.get('images')[0])
                    if img_file:
                        image = f"https://down-br.img.susercontent.com/file/{img_file}"
                    p_min = data.get('price_min') or data.get('price')
                    p_before = data.get('price_min_before_discount')
                    if p_min:
                        v = int(p_min)
                        preco_atual = v/100000 if v>=100000 else v/100 if v>=1000 else v
                    if p_before:
                        v = int(p_before)
                        preco_antes = v/100000 if v>=100000 else v/100 if v>=1000 else v
        except:
            pass

    if not preco_atual:
        matches = re.findall(r'R\$\s*([\d\.\,]+)', html)
        vals = []
        for raw in matches:
            norm = raw.replace('.','').replace(',','.')
            if '.' in raw and ',' in raw:
                norm = raw.replace('.','').replace(',','.')
            elif ',' in raw and '.' not in raw:
                norm = raw.replace(',','.')
            try:
                v = float(norm)
                if 10 <= v <= 50000:
                    vals.append(v)
            except:
                pass
        if vals:
            vals = sorted(set(vals))
            preco_atual = vals[0]
            maiores = [x for x in vals if x > preco_atual]
            if maiores and not preco_antes:
                preco_antes = max(maiores)

    desconto = 0
    economia = 0
    if preco_antes and preco_atual and preco_antes > preco_atual:
        desconto = round((1 - preco_atual/preco_antes)*100)
        economia = round(preco_antes - preco_atual, 2)

    return {
        "affiliate_link_original": url,
        "title": title or "Produto Shopee Verificado",
        "image": image,
        "preco_atual": preco_atual,
        "preco_antes": preco_antes,
        "desconto": desconto,
        "economia": economia,
        "final_url": final_url
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        url_param = query.get('url', [None])[0]

        if url_param:
            # API resolve
            result = resolve_shopee(url_param)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
        else:
            # HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_FINAL.encode('utf-8'))
