
from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, re, json
from html.parser import HTMLParser
import base64

class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.image = None
        self.price_meta = None
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta':
            prop = d.get('property') or d.get('name') or ''
            content = d.get('content') or ''
            if 'og:title' in prop and content:
                self.title = content
            if 'og:image' in prop and content:
                self.image = content
            if 'product:price:amount' in prop or 'og:price' in prop:
                self.price_meta = content

HTML_FINAL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GERADOR ACHADINHOS</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>body{background:#fff;color:#111;font-family:Inter,system-ui}.glass{background:#fff;border:1px solid #e5e5e5}.btn{background:linear-gradient(135deg,#ff6a00 0%,#ee0979 100%)}</style>
</head>
<body class="min-h-screen p-3">
<div class="max-w-[460px] mx-auto">
<div class="glass rounded-[16px] p-3">
<label class="text-[10px] font-bold uppercase">Seu link s.shopee.com.br (novo)</label>
<input id="aff" class="w-full mt-1 border-2 border-black rounded-xl p-3 text-[14px] font-bold" placeholder="https://s.shopee.com.br/XXXX">
<button id="btn" class="btn w-full mt-3 p-3 rounded-xl font-black text-white">GERAR FOTO + VALOR REAL ⚡</button>
<div id="log" class="bg-black text-[#0f0] rounded-xl p-2 mt-2 h-[80px] overflow-auto text-[10px] font-mono"></div>
</div>
<div id="result" class="hidden mt-3">
<div class="glass rounded-[16px] p-3">
<span class="text-[11px] font-black">📸 FOTO REAL</span>
<div id="fotoBox" class="w-full rounded-xl bg-gray-50 border overflow-hidden relative mt-2" style="aspect-ratio:1/1;background:#f5f5f5;">
<img id="fotoReal" class="w-full h-full object-cover" referrerpolicy="no-referrer">
<div id="fotoLoad" class="absolute inset-0 flex flex-col items-center justify-center bg-white gap-2"><div class="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full"></div><span class="text-[10px] font-bold">BUSCANDO FOTO REAL...</span></div>
<div id="priceOverlay" class="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/90 to-transparent text-white hidden"><p id="oTitle" class="font-black text-[12px]"></p><p id="oPrice" class="font-black text-[16px] text-[#00FF88] mt-1"></p></div>
</div>
<div class="grid grid-cols-2 gap-2 mt-2"><button onclick="baixar()" class="bg-black text-white p-2 rounded-xl text-[11px] font-bold">Baixar Foto</button><button onclick="copiar()" class="bg-white border border-black p-2 rounded-xl text-[11px] font-bold">Copiar Mensagem</button></div>
</div>
<div class="glass rounded-[16px] p-3 mt-3"><span class="text-[11px] font-black">📱 MENSAGEM COM VALOR REAL</span><div id="msg" class="bg-green-50 border-2 border-green-200 rounded-xl p-3 mt-2 text-[13px] whitespace-pre-wrap text-black font-medium"></div><button onclick="whatsapp()" class="w-full mt-2 bg-[#25D366] p-3 rounded-xl font-black text-[12px]">Enviar no Zap</button><div id="info" class="mt-2 text-[10px] text-gray-600"></div></div>
</div>
</div>
<script>
let ORIGINAL="";function log(t){const el=document.getElementById('log');const d=document.createElement('div');d.textContent=new Date().toLocaleTimeString()+" → "+t;el.appendChild(d);el.scrollTop=el.scrollHeight;}function formatBRL(v){return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});}
document.getElementById('btn').onclick=async()=>{
 ORIGINAL=document.getElementById('aff').value.trim();if(!ORIGINAL){alert('Cole link');return;}document.getElementById('result').classList.remove('hidden');document.getElementById('log').innerHTML="";document.getElementById('fotoLoad').classList.remove('hidden');document.getElementById('priceOverlay').classList.add('hidden');log(`Link fiel: ${ORIGINAL}`);log(`🚀 Buscando no servidor...`);try{
 const resp=await fetch(`?url=${encodeURIComponent(ORIGINAL)}`);
 const data=await resp.json();
 log(`DEBUG: title=${(data.title||'').slice(0,30)} img=${data.image? 'OK':'NULL'} preco=${data.preco_atual||'NULL'}`);
 const fotoReal=document.getElementById('fotoReal');
 const fotoLoad=document.getElementById('fotoLoad');
 const overlay=document.getElementById('priceOverlay');
 if(data.image){
   fotoReal.src=data.image;
   fotoReal.onload=()=>{fotoLoad.classList.add('hidden');overlay.classList.remove('hidden');log('✅ Foto carregada');};
   fotoReal.onerror=()=>{fotoLoad.innerHTML='<span class=text-[11px]>Foto bloqueada, mas link ok</span>';log('⚠️ Shopee bloqueou imagem direta, usando link original');};
 }else{
   fotoLoad.innerHTML='<span class=text-[11px]>Sem foto, mas valor ok</span>';
   log('⚠️ Sem foto no scraper');
 }
 document.getElementById('oTitle').textContent=(data.title||'Produto Shopee').slice(0,55);
 if(data.preco_atual){
   if(data.preco_antes && data.desconto>0){document.getElementById('oPrice').textContent=`DE ${formatBRL(data.preco_antes)} POR ${formatBRL(data.preco_atual)}`;}
   else{document.getElementById('oPrice').textContent=`${formatBRL(data.preco_atual)}`;}
   overlay.classList.remove('hidden');
 }else{
   document.getElementById('oPrice').textContent='OFERTA - Confira no link';
   overlay.classList.remove('hidden');
 }
 let blocoPreco="",blocoDesc="";
 if(data.preco_atual){
   if(data.preco_antes && data.desconto>0){blocoPreco=`💰 DE: ~${formatBRL(data.preco_antes)}~ POR: ${formatBRL(data.preco_atual)}`;blocoDesc=`🔥 ${data.desconto}% OFF - Economize ${formatBRL(data.economia)}!`;}
   else{blocoPreco=`💰 POR APENAS: ${formatBRL(data.preco_atual)}`;}
 }else{
   blocoPreco=`💰 OFERTA IMPERDÍVEL - Confira no link`;
 }
 const msg=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\n\n📦 ${data.title.toUpperCase()}\n\n${blocoPreco}\n${blocoDesc}\n\n⚡ PRODUTO VERIFICADO!\n👇 LINK COM DESCONTO 👇\n\n${data.affiliate_link_original}\n\n⏰ Corre!`;
 document.getElementById('msg').textContent=msg;
 document.getElementById('info').innerHTML=`<span class="text-green-700 font-bold">🔒 Link 100% fiel: ${data.affiliate_link_original}</span><br><span class=text-[9px]>Final: ${(data.final_url||'').slice(0,60)}</span>`;
 }catch(e){log(`❌ Erro: ${e.message}`);document.getElementById('fotoLoad').classList.add('hidden');}
};
function copiar(){navigator.clipboard.writeText(document.getElementById('msg').textContent);alert('Copiado!');}
function baixar(){const img=document.getElementById('fotoReal');if(img.src) window.open(img.src,'_blank'); else alert('Sem foto');}
function whatsapp(){const txt=encodeURIComponent(document.getElementById('msg').textContent);window.open(`https://wa.me/?text=${txt}`,'_blank');}
</script>
</body>
</html>
"""

def fetch_url(url, headers, timeout=15):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = r.geturl()
            data = r.read()
            try:
                text = data.decode('utf-8', errors='ignore')
            except:
                text = data.decode('latin1', errors='ignore')
            return final, text, r.headers
    except Exception as e:
        return url, "", {}

def resolve_shopee(url):
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://shopee.com.br/",
        "Cache-Control": "no-cache",
    }
    headers_api = {
        "User-Agent": ua,
        "Accept": "application/json",
        "Referer": "https://shopee.com.br/",
        "Accept-Language": "pt-BR,pt;q=0.9",
    }

    final_url, html, _ = fetch_url(url, headers)

    # Shopee short link sometimes returns JS redirect - try to extract target from html
    if "s.shopee.com.br" in final_url or len(html) < 5000:
        # try extract https://shopee.com.br/.*-i.xxx.yyy
        m = re.search(r'https://shopee\.com\.br/[^"\'\s<>]+-i\.(\d+)\.(\d+)', html)
        if m:
            final_url = m.group(0)
            # fetch product page again
            f2, h2, _ = fetch_url(final_url, headers)
            html = html + "\n" + h2
            final_url = f2 if "shopee.com.br" in f2 else final_url

    # try extract ids
    shop_id = None
    item_id = None
    for pat in [r'-i\.(\d+)\.(\d+)', r'shopid=(\d+).*?itemid=(\d+)', r'"shopid":(\d+).*?"itemid":(\d+)', r'itemid=(\d+).*?shopid=(\d+)']:
        mm = re.search(pat, final_url + "\n" + html)
        if mm:
            if 'shopid' in pat.lower() and 'itemid' in pat.lower():
                # order depends
                if pat.startswith('shopid'):
                    shop_id, item_id = mm.group(1), mm.group(2)
                elif 'itemid' in pat[:10]:
                    item_id, shop_id = mm.group(1), mm.group(2)
                else:
                    shop_id, item_id = mm.group(1), mm.group(2)
                    # fix if pat -i.
                    if pat == r'-i\.(\d+)\.(\d+)':
                        shop_id, item_id = mm.group(1), mm.group(2)
            else:
                shop_id, item_id = mm.group(1), mm.group(2)
            if shop_id and item_id:
                break

    # If still not found, try to find in script JSON
    if not shop_id:
        mm = re.search(r'"shop_id":\s*(\d+).+?"item_id":\s*(\d+)', html)
        if mm:
            shop_id, item_id = mm.group(1), mm.group(2)
        else:
            mm = re.search(r'"itemid":\s*(\d+).+?"shopid":\s*(\d+)', html)
            if mm:
                item_id, shop_id = mm.group(1), mm.group(2)

    title = None
    image = None
    preco_atual = None
    preco_antes = None

    # Try Shopee API v4
    if shop_id and item_id:
        try:
            api_url = f"https://shopee.com.br/api/v4/item/get?itemid={item_id}&shopid={shop_id}"
            f_api, j_text, _ = fetch_url(api_url, headers_api, timeout=10)
            j = json.loads(j_text)
            data = j.get('data') or j.get('item') or j
            if data:
                if data.get('name'):
                    title = data.get('name')
                # image
                img = data.get('image') or (data.get('images') and data.get('images')[0]) or data.get('imageUrl')
                if img:
                    if img.startswith('http'):
                        image = img
                    else:
                        image = f"https://down-br.img.susercontent.com/file/{img}"
                # price
                p_min = data.get('price_min') or data.get('price') or data.get('price_min_before_discount')
                p_before = data.get('price_min_before_discount') or data.get('price_before_discount') or data.get('original_price')
                # also try nested price_info
                if not p_min and data.get('price_info'):
                    p_min = data['price_info'].get('current_price') or data['price_info'].get('price')
                    p_before = data['price_info'].get('before_discount') or p_before
                def parse_price(v):
                    try:
                        v = int(v)
                        # shopee uses 100000 factor for BRL
                        if v >= 10000000:
                            return v/100000
                        elif v >= 100000:
                            return v/100000
                        elif v >= 1000:
                            return v/100
                        else:
                            return float(v)
                    except:
                        try:
                            return float(v)
                        except:
                            return None
                if p_min:
                    preco_atual = parse_price(p_min)
                if p_before:
                    preco_antes = parse_price(p_before)
        except Exception as e:
            pass

    # Fallback parse OG tags
    parser = MyParser()
    try:
        parser.feed(html[:200000])
    except:
        pass
    if not title and parser.title:
        title = parser.title
    if not image and parser.image:
        image = parser.image

    # Try extract price from html via regex if still missing
    if not preco_atual:
        # look for "price": or R$ pattern
        m_price = re.findall(r'"price"\s*:\s*"?(\d+)"?', html)
        if m_price:
            vals = []
            for pv in m_price:
                try:
                    pv_int = int(pv)
                    if 100000 <= pv_int <= 100000000:
                        vals.append(pv_int/100000)
                except:
                    pass
            if vals:
                preco_atual = min(vals)
        # R$ pattern
        if not preco_atual:
            matches = re.findall(r'R\$\s*([\d\.\,]+)', html)
            vals = []
            for raw in matches:
                norm = raw.replace('.', '').replace(',', '.') if ',' in raw else raw
                try:
                    v = float(norm)
                    if 5 <= v <= 50000:
                        vals.append(v)
                except:
                    pass
            if vals:
                vals = sorted(set(vals))
                preco_atual = vals[0]
                maiores = [x for x in vals if x > preco_atual]
                if maiores and not preco_antes:
                    preco_antes = max(maiores[:3])  # maior como antes

    desconto = 0
    economia = 0
    if preco_antes and preco_atual and preco_antes > preco_atual:
        try:
            desconto = round((1 - preco_atual/preco_antes)*100)
            economia = round(preco_antes - preco_atual, 2)
        except:
            pass

    return {
        "affiliate_link_original": url,
        "title": (title or "Produto Shopee Verificado").strip(),
        "image": image,
        "preco_atual": preco_atual,
        "preco_antes": preco_antes,
        "desconto": desconto,
        "economia": economia,
        "final_url": final_url,
        "shop_id": shop_id,
        "item_id": item_id
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        url_param = query.get('url', [None])[0]

        if url_param:
            result = resolve_shopee(url_param)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(HTML_FINAL.encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
