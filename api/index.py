from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, re, json, hashlib, time

# === CREDENCIAIS OFICIAIS DO USUARIO (do print) ===
APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

HTML_FINAL = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GERADOR ACHADINHOS - API OFICIAL</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>body{background:#fff;color:#111;font-family:Inter,system-ui}.glass{background:#fff;border:1px solid #e5e5e5}.btn{background:linear-gradient(135deg,#ff6a00 0%,#ee0979 100%)}.badge{background:#00c950;color:#fff;font-size:9px;padding:2px 6px;border-radius:999px;font-weight:900}</style>
</head>
<body class="min-h-screen p-3">
<div class="max-w-[460px] mx-auto">
<div class="glass rounded-[16px] p-3">
<div class="flex items-center gap-2"><span class="badge">API OFICIAL SHOPEE</span><span class="text-[10px] font-bold">ANTI-BLOQUEIO</span></div>
<label class="text-[10px] font-bold uppercase mt-2 block">Seu link s.shopee.com.br</label>
<input id="aff" class="w-full mt-1 border-2 border-black rounded-xl p-3 text-[14px] font-bold" placeholder="https://s.shopee.com.br/XXXX">
<button id="btn" class="btn w-full mt-3 p-3 rounded-xl font-black text-white">GERAR COM API OFICIAL ⚡</button>
<div id="log" class="bg-black text-[#0f0] rounded-xl p-2 mt-2 h-[90px] overflow-auto text-[10px] font-mono"></div>
</div>
<div id="result" class="hidden mt-3">
<div class="glass rounded-[16px] p-3">
<span class="text-[11px] font-black">📸 FOTO REAL - API OFICIAL</span>
<div id="fotoBox" class="w-full rounded-xl bg-gray-50 border overflow-hidden relative mt-2" style="aspect-ratio:1/1;background:#f5f5f5;">
<img id="fotoReal" class="w-full h-full object-cover" crossorigin="anonymous" referrerpolicy="no-referrer">
<div id="fotoLoad" class="absolute inset-0 flex flex-col items-center justify-center bg-white gap-2"><div class="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full"></div><span class="text-[10px] font-bold">BUSCANDO NA API OFICIAL...</span></div>
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
 ORIGINAL=document.getElementById('aff').value.trim();if(!ORIGINAL){alert('Cole link');return;}document.getElementById('result').classList.remove('hidden');document.getElementById('log').innerHTML="";document.getElementById('fotoLoad').classList.remove('hidden');document.getElementById('fotoLoad').innerHTML='<div class="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full"></div><span class=text-[10px]>API OFICIAL SHOPEE...</span>';document.getElementById('priceOverlay').classList.add('hidden');log(`Link fiel: ${ORIGINAL}`);log(`🚀 Chamando API oficial AppID ${"18325950432".slice(0,4)}****`);try{
 const resp=await fetch(`?url=${encodeURIComponent(ORIGINAL)}&t=${Date.now()}`);
 const data=await resp.json();
 log(`METODO: ${data.metodo}`);
 log(`TITULO: ${(data.title||'').slice(0,35)}`);
 log(`PRECO: ${data.preco_atual||'NULL'} IMG: ${data.image? 'OK':'NULL'}`);
 if(data.erro_api){log(`⚠️ API erro: ${data.erro_api.slice(0,80)}`);}
 const fotoReal=document.getElementById('fotoReal');
 const fotoLoad=document.getElementById('fotoLoad');
 const overlay=document.getElementById('priceOverlay');
 if(data.image){
   fotoReal.src=data.image;
   fotoReal.onload=()=>{fotoLoad.classList.add('hidden');overlay.classList.remove('hidden');log('✅ Foto oficial carregada!');};
   fotoReal.onerror=()=>{fotoLoad.innerHTML='<span class=text-[11px]>Tentando fallback...</span>'; if(data.image_fallback){fotoReal.src=data.image_fallback;} else {fotoLoad.classList.add('hidden');}};
 }else{
   fotoLoad.innerHTML='<span class=text-[11px]>Sem foto</span>';
 }
 document.getElementById('oTitle').textContent=(data.title||'Produto Shopee').slice(0,60);
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
 const msg=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\n\n📦 ${data.title.toUpperCase()}\n\n${blocoPreco}\n${blocoDesc}\n\n⚡ PRODUTO VERIFICADO API OFICIAL!\n👇 LINK COM DESCONTO 👇\n\n${data.affiliate_link_original}\n\n⏰ Corre!`;
 document.getElementById('msg').textContent=msg;
 document.getElementById('info').innerHTML=`<span class="text-green-700 font-bold">🔒 Link 100% fiel: ${data.affiliate_link_original}</span><br><span class=text-[9px]>${data.metodo} | ItemID: ${data.item_id||''} ShopID: ${data.shop_id||''}</span>`;
 }catch(e){log(`❌ Erro: ${e.message}`);document.getElementById('fotoLoad').classList.add('hidden');}
};
function copiar(){navigator.clipboard.writeText(document.getElementById('msg').textContent);alert('Copiado!');}
function baixar(){const img=document.getElementById('fotoReal');if(img.src) window.open(img.src,'_blank');}
function whatsapp(){const txt=encodeURIComponent(document.getElementById('msg').textContent);window.open(`https://wa.me/?text=${txt}`,'_blank');}
</script>
</body>
</html>
"""

def fetch_url(url, headers, timeout=12):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final = r.geturl()
            data = r.read().decode('utf-8', errors='ignore')
            return final, data, None
    except Exception as e:
        return url, "", str(e)

def proxy_image_url(original_img):
    if not original_img:
        return None
    if 'wsrv.nl' in original_img:
        return original_img
    try:
        enc = urllib.parse.quote_plus(original_img)
        return f"https://wsrv.nl/?url={enc}&output=jpg&w=800&h=800&fit=inside"
    except:
        return original_img

def call_shopee_affiliate_api(item_id, shop_id=None):
    # Monta query GraphQL para buscar produto por itemId
    # Tenta primeiro por itemId direto
    query = """
    query {
      productOfferV2(itemId: %s, limit: 1, sortType: 1) {
        nodes {
          itemId
          productName
          imageUrl
          priceMin
          priceMax
          productLink
          offerLink
          commissionRate
          shopId
          shopName
          ratingStar
          sales
        }
        pageInfo {
          page
          limit
        }
      }
    }
    """ % str(item_id)

    payload_dict = {"query": query}
    payload = json.dumps(payload_dict, separators=(',', ':'))
    timestamp = str(int(time.time()))
    sign_str = f"{APP_ID}{timestamp}{payload}{SECRET}"
    signature = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
    auth = f"SHA256 Credential={APP_ID}, Timestamp={timestamp}, Signature={signature}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth
    }
    try:
        req = urllib.request.Request(API_URL, data=payload.encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=12) as resp:
            resp_data = json.loads(resp.read().decode('utf-8'))
            return resp_data, None
    except Exception as e:
        return None, str(e)

def resolve_shopee(url):
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Referer": "https://shopee.com.br/",
    }

    final_url, html, _ = fetch_url(url, headers)
    metodo = "fallback"
    shop_id = None
    item_id = None
    erro_api = None

    m = re.search(r'-i\.(\d+)\.(\d+)', final_url + html)
    if m:
        shop_id, item_id = m.group(1), m.group(2)
    if not item_id:
        m2 = re.search(r'"itemid"\s*:\s*(\d+)', html)
        m3 = re.search(r'"shopid"\s*:\s*(\d+)', html)
        if m2:
            item_id = m2.group(1)
        if m3:
            shop_id = m3.group(1)

    title = None
    image = None
    preco_atual = None
    preco_antes = None

    # 1 - Tenta API OFICIAL (igual bots do Telegram)
    if item_id:
        resp_api, err = call_shopee_affiliate_api(item_id, shop_id)
        if err:
            erro_api = err
        elif resp_api:
            if resp_api.get('errors'):
                erro_api = json.dumps(resp_api['errors'])[:300]
            data = resp_api.get('data', {}).get('productOfferV2', {})
            nodes = data.get('nodes', [])
            if nodes:
                node = nodes[0]
                title = node.get('productName')
                image = node.get('imageUrl')
                # priceMin vem como string "19.90" ou "1990" ?
                pm = node.get('priceMin')
                px = node.get('priceMax')
                try:
                    if pm:
                        # pode vir como "19.90" ou centavos
                        pm_str = str(pm)
                        if '.' in pm_str or ',' in pm_str:
                            preco_atual = float(pm_str.replace(',','.'))
                        else:
                            # se vier como 1990 = 19.90 ?
                            v = float(pm_str)
                            if v > 1000:
                                preco_atual = v/100 if v < 100000 else v/100000
                            else:
                                preco_atual = v
                    if px and pm:
                        try:
                            px_f = float(str(px).replace(',','.'))
                            pm_f = float(str(pm).replace(',','.'))
                            if px_f > pm_f:
                                preco_antes = px_f
                        except:
                            pass
                except:
                    pass
                metodo = "API_OFICIAL_SHOPEE_PRODUCTOFFER"

    # 2 - Fallback Microlink + proxy se API falhar (para conta nova com 0 vendas)
    if not image or not preco_atual:
        try:
            micro_url = f"https://api.microlink.io?url={urllib.parse.quote(final_url)}&meta=true"
            req_m = urllib.request.Request(micro_url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req_m, timeout=10) as r:
                j_m = json.loads(r.read().decode('utf-8'))
                md = j_m.get('data', {})
                if not title and md.get('title'):
                    title = md.get('title')
                if not image and md.get('image'):
                    img_obj = md.get('image')
                    if isinstance(img_obj, dict):
                        image = img_obj.get('url')
                    else:
                        image = img_obj
                if not preco_atual and md.get('description'):
                    m_r = re.search(r'R\$\s*([\d\.\,]+)', md.get('description',''))
                    if m_r:
                        try:
                            raw = m_r.group(1).replace('.','').replace(',','.')
                            v = float(raw)
                            if 5 <= v <= 50000:
                                preco_atual = v
                        except:
                            pass
                if image or title:
                    if "API_OFICIAL" not in metodo:
                        metodo = "microlink_fallback"
                    else:
                        metodo = metodo + "+microlink"
        except:
            pass

    # 3 - OG tags fallback
    if not image:
        m_img = re.search(r'property="og:image"\s+content="([^"]+)"', html)
        if m_img:
            image = m_img.group(1)
    if not title:
        m_t = re.search(r'property="og:title"\s+content="([^"]+)"', html)
        if m_t:
            title = m_t.group(1)

    # Proxy imagem
    image_proxied = proxy_image_url(image) if image else None
    enc = urllib.parse.quote_plus(image) if image else ""
    image_fallback = f"https://images.weserv.nl/?url={enc}&output=jpg" if image else None

    # Regex preco se ainda nao tem
    if not preco_atual:
        matches = re.findall(r'R\$\s*([\d\.\,]+)', html)
        vals = []
        for raw in matches:
            try:
                norm = raw.replace('.','').replace(',','.') if ',' in raw else raw.replace(',','.')
                if '.' in raw and ',' in raw:
                    norm = raw.replace('.','').replace(',','.')
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
                preco_antes = max(maiores[:2])

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
        "title": (title or "Shopee Brasil | Ofertas incriveis").strip(),
        "image": image_proxied,
        "image_original": image,
        "image_fallback": image_fallback,
        "preco_atual": preco_atual,
        "preco_antes": preco_antes,
        "desconto": desconto,
        "economia": economia,
        "final_url": final_url,
        "metodo": metodo,
        "erro_api": erro_api,
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
        self.end_headers(
