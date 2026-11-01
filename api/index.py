from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, re, json, hashlib, time

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

HTML = '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Achadinhos API</title><script src="https://cdn.tailwindcss.com"></script></head><body class="p-3 bg-[#f5f5f5]"><div class="max-w-[420px] mx-auto"><div class="bg-white border rounded-[16px] p-4"><div style="background:#00c950;color:#fff;font-size:10px;display:inline-block;padding:3px 8px;border-radius:999px;font-weight:900">API OFICIAL SHOPEE</div><h1 class="font-black text-[18px] mt-2">GERADOR ACHADINHOS</h1><input id="link" placeholder="https://s.shopee.com.br/XXXX" class="w-full border-2 border-black rounded-xl p-3 mt-3 font-bold text-[13px]"><button id="go" class="w-full p-3 rounded-xl mt-3 font-black text-white" style="background:linear-gradient(135deg,#ff6a00,#ee0979)">GERAR FOTO + PRECO REAL</button><div id="log" class="bg-black text-[#0f0] rounded-xl p-2 mt-3 h-[70px] overflow-auto text-[10px] font-mono">Pronto API 1832****</div></div><div id="res" class="hidden"><div class="bg-white border rounded-[16px] p-3 mt-3"><div id="imgBox" style="aspect-ratio:1/1;background:#eee;border-radius:12px;overflow:hidden;position:relative"><img id="img" style="width:100%;height:100%;object-fit:cover" referrerpolicy="no-referrer"><div id="load" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#fff;font-weight:800;font-size:12px">Carregando...</div><div id="over" style="position:absolute;bottom:0;left:0;right:0;padding:10px;background:linear-gradient(to top,rgba(0,0,0,.9),transparent);color:#fff;display:none"><div id="t" style="font-weight:900;font-size:12px"></div><div id="p" style="font-weight:900;color:#00FF88;margin-top:4px"></div></div></div></div><div class="bg-white border rounded-[16px] p-3 mt-3"><div id="msg" style="white-space:pre-wrap;font-size:13px;background:#e8ffe8;border:2px solid #a0e0a0;border-radius:12px;padding:12px"></div><button onclick="zap()" class="w-full p-3 rounded-xl mt-3 font-black text-white" style="background:#25D366">Enviar no Zap</button><div id="info" style="font-size:10px;color:#666;margin-top:8px"></div></div></div></div><script>\nlet ORIG="";function log(x){let e=document.getElementById(\'log\');let d=document.createElement(\'div\');d.textContent=new Date().toLocaleTimeString()+\' -> \'+x;e.appendChild(d);e.scrollTop=e.scrollHeight}function brl(v){return v.toLocaleString(\'pt-BR\',{style:\'currency\',currency:\'BRL\'})}\ndocument.getElementById(\'go\').onclick=async()=>{let l=document.getElementById(\'link\').value.trim();if(!l){alert(\'Cole link\');return}ORIG=l;document.getElementById(\'res\').classList.remove(\'hidden\');document.getElementById(\'load\').style.display=\'flex\';document.getElementById(\'over\').style.display=\'none\';log(\'Link: \'+ORIG);try{let r=await fetch(\'/?url=\'+encodeURIComponent(ORIG)+\'&t=\'+Date.now());let j=await r.json();log(\'METODO: \'+j.metodo);log(\'Preco: \'+(j.preco_atual||\'null\'));let img=document.getElementById(\'img\');let load=document.getElementById(\'load\');let over=document.getElementById(\'over\');if(j.image){img.src=j.image;img.onload=()=>{load.style.display=\'none\';over.style.display=\'block\';log(\'Foto ok\')};img.onerror=()=>{if(j.image_fallback){img.src=j.image_fallback}} }else{load.textContent=\'Sem foto\'}document.getElementById(\'t\').textContent=(j.title||\'Produto\').slice(0,70);if(j.preco_atual){document.getElementById(\'p\').textContent=j.preco_antes&&j.desconto>0?(\'DE \'+brl(j.preco_antes)+\' POR \'+brl(j.preco_atual)):brl(j.preco_atual);over.style.display=\'block\'}let bp=j.preco_atual?(j.preco_antes&&j.desconto>0?(\'💰 DE: ~\'+brl(j.preco_antes)+\'~ POR: \'+brl(j.preco_atual)+\'\\n🔥 \'+j.desconto+\'% OFF!\'):(\'💰 POR APENAS: \'+brl(j.preco_atual))):\'💰 OFERTA\';let m=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\\n\\n📦 ${j.title.toUpperCase()}\\n\\n${bp}\\n\\n⚡ API OFICIAL!\\n👇 LINK 👇\\n\\n${j.affiliate_link_original}\\n\\n⏰ Corre!`;document.getElementById(\'msg\').textContent=m;document.getElementById(\'info\').innerHTML=\'<span style=color:green;font-weight:700>🔒 Link fiel: \'+j.affiliate_link_original+\'</span><br>Metodo: \'+j.metodo} catch(e){log(\'ERRO: \'+e.message)}};function zap(){let t=encodeURIComponent(document.getElementById(\'msg\').textContent);window.open(\'https://wa.me/?text=\'+t,\'_blank\')}\n</script></body></html>\n'

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.geturl(), r.read().decode('utf-8', errors='ignore')
    except:
        return url, ""

def proxy_img(u):
    if not u:
        return ""
    if "wsrv.nl" in u:
        return u
    try:
        enc = urllib.parse.quote_plus(u)
        return f"https://wsrv.nl/?url={enc}&output=jpg&w=800"
    except:
        return u

def call_api(item_id):
    try:
        query = "query { productOfferV2(itemId: %s, limit: 1) { nodes { itemId productName imageUrl priceMin priceMax } } }" % str(item_id)
        payload_dict = {"query": query}
        payload = json.dumps(payload_dict, separators=(',', ':'))
        ts = str(int(time.time()))
        sig = hashlib.sha256(f"{APP_ID}{ts}{payload}{SECRET}".encode()).hexdigest()
        auth = f"SHA256 Credential={APP_ID}, Timestamp={ts}, Signature={sig}"
        req = urllib.request.Request(API_URL, data=payload.encode(), headers={"Content-Type":"application/json","Authorization":auth}, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode()), None
    except Exception as e:
        return None, str(e)

def resolve(url):
    try:
        final, html = fetch_url(url)
        item_id = None
        shop_id = None
        m = re.search(r'-i\.(\d+)\.(\d+)', final + html)
        if m:
            shop_id, item_id = m.group(1), m.group(2)
        if not item_id:
            m2 = re.search(r'"itemid"\s*:\s*(\d+)', html)
            if m2: item_id = m2.group(1)
        title = "Shopee Brasil"
        image = None
        preco = None
        preco_antes = None
        metodo = "fallback"
        erro = None
        if item_id:
            data, err = call_api(item_id)
            if err: erro = err
            elif data:
                if data.get('errors'): erro = str(data['errors'])[:200]
                nodes = data.get('data',{}).get('productOfferV2',{}).get('nodes',[])
                if nodes:
                    n = nodes[0]
                    title = n.get('productName') or title
                    image = n.get('imageUrl')
                    pm = n.get('priceMin')
                    px = n.get('priceMax')
                    try:
                        if pm:
                            preco = float(str(pm).replace(',','.'))
                            if preco > 1000: preco = preco/100 if preco < 100000 else preco/100000
                        if px:
                            pxf = float(str(px).replace(',','.'))
                            if pxf > (preco or 0): preco_antes = pxf
                    except: pass
                    metodo = "API_OFICIAL_SHOPEE"
        if not image:
            m = re.search(r'property="og:image" content="([^"]+)"', html)
            if m: image = m.group(1)
        if title == "Shopee Brasil":
            m = re.search(r'property="og:title" content="([^"]+)"', html)
            if m: title = m.group(1)
        if not preco:
            ms = re.findall(r'R\$\s*([\d\.,]+)', html)
            vals = []
            for raw in ms:
                try:
                    v = float(raw.replace('.','').replace(',','.')) if ',' in raw and '.' in raw else float(raw.replace(',','.'))
                    if 5 <= v <= 50000: vals.append(v)
                except: pass
            if vals: preco = sorted(set(vals))[0]
        img_proxy = proxy_img(image) if image else ""
        img_fallback = f"https://images.weserv.nl/?url={urllib.parse.quote_plus(image)}&output=jpg" if image else ""
        desconto = 0
        economia = 0
        if preco_antes and preco and preco_antes > preco:
            try:
                desconto = round((1-preco/preco_antes)*100)
                economia = round(preco_antes-preco,2)
            except: pass
        return {"affiliate_link_original": url, "title": title.strip(), "image": img_proxy, "image_fallback": img_fallback, "preco_atual": preco, "preco_antes": preco_antes, "desconto": desconto, "economia": economia, "metodo": metodo, "erro_api": erro, "final_url": final, "item_id": item_id, "shop_id": shop_id}
    except Exception as e:
        return {"affiliate_link_original": url, "title": "Erro", "image": "", "image_fallback": "", "preco_atual": None, "preco_antes": None, "desconto": 0, "economia": 0, "metodo": f"ERRO: {str(e)[:100]}", "erro_api": str(e), "final_url": url, "item_id": None, "shop_id": None}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            u = qs.get('url',[None])[0]
            if u:
                res = resolve(u)
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.send_header('Access-Control-Allow-Origin','*')
                self.end_headers()
                self.wfile.write(json.dumps(res, ensure_ascii=False).encode())
            else:
                self.send_response(200)
                self.send_header('Content-type','text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(HTML.encode())
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h1>Recarregue: {e}</h1>".encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
