from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, re, json, hashlib, time

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

HTML = '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Igual Telegram</title><script src="https://cdn.tailwindcss.com"></script></head><body class="p-3 bg-black text-white"><div class="max-w-[430px] mx-auto"><div class="bg-zinc-900 border border-zinc-800 rounded-[16px] p-4"><div class="flex justify-between"><span style="background:#00c950;color:#fff;font-size:10px;padding:4px 10px;border-radius:999px;font-weight:900">IGUAL TELEGRAM - IP BRASIL</span><span style="font-size:10px;color:#888">FOTO + PRECO REAL</span></div><h1 class="font-black text-[18px] mt-2">GERADOR ACHADINHOS</h1><input id="link" placeholder="https://s.shopee.com.br/XXXX" class="w-full mt-3 bg-black border-2 border-white rounded-xl p-3 text-white font-bold text-[13px]"><button id="go" class="w-full mt-3 p-3 rounded-xl font-black text-white" style="background:linear-gradient(135deg,#ff6a00,#ee0979)">GERAR IGUAL TELEGRAM 🔥</button><div id="log" class="bg-black text-[#0f0] border border-green-900 rounded-xl p-2 mt-3 h-[110px] overflow-auto text-[10px] font-mono">Pronto - resolvendo no seu celular (IP Brasil) igual bot Telegram...</div></div><div id="res" class="hidden"><div class="bg-zinc-900 border border-zinc-800 rounded-[16px] p-3 mt-3"><div class="flex justify-between mb-2"><span class="font-black text-[12px] text-white">📸 STORY 1080x1920</span><button onclick="baixarStory()" class="bg-white text-black px-3 py-1 rounded-full text-[11px] font-bold">Baixar Story</button></div><canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-xl"></canvas><div id="imgPreview" class="mt-2 text-[10px] text-zinc-400"></div></div><div class="bg-zinc-900 border border-zinc-800 rounded-[16px] p-3 mt-3"><span class="font-black text-[11px] text-white">📱 LEGENDA GRUPO COM VALOR REAL</span><div id="msg" class="mt-2 bg-black border border-zinc-700 rounded-xl p-3 text-[13px] whitespace-pre-wrap text-white"></div><div class="grid grid-cols-2 gap-2 mt-3"><button onclick="copiar()" class="bg-white text-black p-2 rounded-xl font-bold text-[12px]">Copiar Texto</button><button onclick="zap()" class="p-2 rounded-xl font-bold text-[12px] text-white" style="background:#25D366">Enviar Zap</button></div><div id="info" class="mt-2 text-[10px] text-zinc-500"></div></div></div></div><script>\nlet DADOS=null;\nfunction log(x){let e=document.getElementById(\'log\');let d=document.createElement(\'div\');d.textContent=new Date().toLocaleTimeString()+\' -> \'+x;e.appendChild(d);e.scrollTop=e.scrollHeight}\nfunction brl(v){return v.toLocaleString(\'pt-BR\',{style:\'currency\',currency:\'BRL\'})}\nfunction extractIds(text){let m=text.match(/-i\\.(\\d+)\\.(\\d+)/);if(m) return {shopId:m[1],itemId:m[2]};let m2=text.match(/i\\.(\\d+)\\.(\\d+)/);if(m2) return {shopId:m2[1],itemId:m2[2]};return {shopId:null,itemId:null}}\nasync function loadImage(src){return new Promise((res,rej)=>{let img=new Image();img.crossOrigin=\'anonymous\';img.onload=()=>res(img);img.onerror=rej;img.src=src})}\nasync function gerarStory(dados){\n  let c=document.getElementById(\'storyCanvas\');let ctx=c.getContext(\'2d\');\n  let grad=ctx.createLinearGradient(0,0,0,1920);grad.addColorStop(0,\'#1a1a1a\');grad.addColorStop(1,\'#000\');ctx.fillStyle=grad;ctx.fillRect(0,0,1080,1920);\n  ctx.fillStyle=\'#00FF88\';ctx.font=\'900 38px system-ui\';ctx.fillText(\'QUEIMA DE ESTOQUE\',50,100);\n  ctx.fillStyle=\'#fff\';ctx.font=\'900 56px system-ui\';ctx.fillText(\'SHOPEE 🔥\',50,170);\n  ctx.fillStyle=\'#fff\';ctx.fillRect(50,220,980,1080);\n  try{let prodImg=await loadImage(dados.image);let iw=prodImg.width,ih=prodImg.height;let scale=Math.min(980/iw,1080/ih);let nw=iw*scale,nh=ih*scale;let x=50+(980-nw)/2,y=220+(1080-nh)/2;ctx.drawImage(prodImg,x,y,nw,nh)}catch(e){ctx.fillStyle=\'#ccc\';ctx.font=\'bold 32px system-ui\';ctx.fillText(\'Sem foto\',400,750)}\n  let yBase=1360;\n  if(dados.preco_atual){if(dados.preco_antes&&dados.desconto>0){ctx.fillStyle=\'#888\';ctx.font=\'bold 32px system-ui\';ctx.fillText(\'DE \'+brl(dados.preco_antes),50,yBase);ctx.fillStyle=\'#00FF88\';ctx.font=\'900 64px system-ui\';ctx.fillText(\'POR \'+brl(dados.preco_atual),50,yBase+80);ctx.fillStyle=\'#000\';ctx.fillRect(50,yBase+110,420,70);ctx.fillStyle=\'#fff\';ctx.font=\'900 44px system-ui\';ctx.fillText(dados.desconto+\'% OFF\',70,yBase+160)}else{ctx.fillStyle=\'#00FF88\';ctx.font=\'900 72px system-ui\';ctx.fillText(brl(dados.preco_atual),50,yBase+70)}}else{ctx.fillStyle=\'#fff\';ctx.font=\'900 48px system-ui\';ctx.fillText(\'OFERTA IMPERDIVEL\',50,yBase+60)}\n  ctx.fillStyle=\'#fff\';ctx.font=\'bold 28px system-ui\';ctx.fillText(\'👇 LINK NA BIO / GRUPO 👇\',50,1780);\n  document.getElementById(\'imgPreview\').textContent=\'Story 1080x1920 gerado - \'+dados.metodo+\' - Item:\'+(dados.item_id||\'\')\n}\nasync function resolveNoCelular(shortUrl){\n  log(\'Passo 1: Resolvendo link curto NO SEU CELULAR (IP Brasil) igual Telegram faz...\');\n  // tenta microlink - tem CORS e resolve redirect\n  try{\n    log(\'Tentando microlink.io (proxy BR)...\');\n    let r=await fetch(\'https://api.microlink.io?url=\'+encodeURIComponent(shortUrl));\n    let j=await r.json();\n    if(j && j.data && j.data.url){\n      log(\'✅ Microlink resolveu: \'+j.data.url.slice(0,70));\n      let ids=extractIds(j.data.url);\n      if(ids.itemId){log(\'✅ Achou itemId: \'+ids.itemId+\' shopId: \'+ids.shopId); return {finalUrl:j.data.url, shopId:ids.shopId, itemId:ids.itemId, title:j.data.title, image:j.data.image?j.data.image.url:null}}\n      // se nao achou id na url final, tenta no html\n      if(j.data.description){let ids2=extractIds(j.data.description); if(ids2.itemId) return {finalUrl:j.data.url, shopId:ids2.shopId, itemId:ids2.itemId, title:j.data.title, image:j.data.image?j.data.image.url:null}}\n    }\n  }catch(e){log(\'Microlink falhou: \'+e.message)}\n  // tenta seguir redirect direto - navegador no Brasil consegue\n  try{\n    log(\'Tentando fetch direto no seu celular...\');\n    let r=await fetch(shortUrl,{redirect:\'follow\'});\n    log(\'Fetch final URL: \'+r.url.slice(0,80));\n    let ids=extractIds(r.url);\n    if(ids.itemId){log(\'✅ Achou itemId via fetch direto: \'+ids.itemId); return {finalUrl:r.url, shopId:ids.shopId, itemId:ids.itemId}}\n    // tenta ler html\n    let txt=await r.text();\n    let ids2=extractIds(txt);\n    if(ids2.itemId){log(\'✅ Achou itemId no HTML: \'+ids2.itemId); return {finalUrl:r.url, shopId:ids2.shopId, itemId:ids2.itemId}}\n  }catch(e){log(\'Fetch direto falhou (CORS normal): \'+e.message)}\n  // tenta allorigins\n  try{\n    log(\'Tentando allorigins (ultimo recurso)...\');\n    let r=await fetch(\'https://api.allorigins.win/get?url=\'+encodeURIComponent(shortUrl));\n    let j=await r.json();\n    let ids=extractIds(j.contents||\'\');\n    if(ids.itemId){log(\'✅ Achou via allorigins: \'+ids.itemId); return {finalUrl:j.status&&j.status.url||shortUrl, shopId:ids.shopId, itemId:ids.itemId}}\n    let idsUrl=extractIds(j.status&&j.status.url||\'\');\n    if(idsUrl.itemId) return {finalUrl:j.status.url, shopId:idsUrl.shopId, itemId:idsUrl.itemId}\n  }catch(e){log(\'AllOrigins falhou: \'+e.message)}\n  log(\'❌ Não conseguiu extrair itemId - vou mandar pro servidor tentar\');\n  return {finalUrl:shortUrl, shopId:null, itemId:null}\n}\ndocument.getElementById(\'go\').onclick=async()=>{\n  let l=document.getElementById(\'link\').value.trim();if(!l){alert(\'Cole link\');return}\n  document.getElementById(\'res\').classList.remove(\'hidden\');log(\'Link original: \'+l);\n  let resolved=await resolveNoCelular(l);\n  let itemId=resolved.itemId;let shopId=resolved.shopId;\n  log(\'Enviando pro backend oficial: itemId=\'+ (itemId||\'null\') +\' shopId=\'+(shopId||\'null\'));\n  try{\n    let apiUrl=\'/?url=\'+encodeURIComponent(l);\n    if(itemId){apiUrl=\'/?itemId=\'+itemId+\'&shopId=\'+(shopId||\'\')+\'&url=\'+encodeURIComponent(l)}\n    let r=await fetch(apiUrl+\'&t=\'+Date.now());let j=await r.json();\n    DADOS=j;\n    log(\'Backend retornou METODO: \'+j.metodo);log(\'Preco: \'+(j.preco_atual||\'null\')+\' Foto: \'+(j.image?\'ok\':\'null\'));\n    if(j.erro_api) log(\'Aviso: \'+j.erro_api.slice(0,100));\n    await gerarStory(j);\n    let bp=j.preco_atual ? (j.preco_antes&&j.desconto>0?`💰 DE: ~${brl(j.preco_antes)}~ POR: ${brl(j.preco_atual)}\\n🔥 ${j.desconto}% OFF - Economize ${brl(j.economia)}!`:`💰 POR APENAS: ${brl(j.preco_atual)}`):`💰 OFERTA IMPERDIVEL - Confira`;\n    let msg=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\\n\\n📦 ${j.title.toUpperCase()}\\n\\n${bp}\\n\\n⚡ API OFICIAL VERIFICADO!\\n👇 LINK COM DESCONTO AQUI 👇\\n\\n${j.affiliate_link_original}\\n\\n⏰ Corre que acaba rapido!`;\n    document.getElementById(\'msg\').textContent=msg;\n    document.getElementById(\'info\').innerHTML=`<span style=color:#0f0>🔒 Link fiel: ${j.affiliate_link_original}</span><br>Metodo: ${j.metodo} | ItemID: ${j.item_id||itemId||\'?\'} | IP: Brasil (celular) igual Telegram`\n  }catch(e){log(\'ERRO FINAL: \'+e.message)}\n};\nfunction baixarStory(){let c=document.getElementById(\'storyCanvas\');let a=document.createElement(\'a\');a.download=\'story-achadinho.png\';a.href=c.toDataURL(\'image/png\');a.click()}\nfunction copiar(){navigator.clipboard.writeText(document.getElementById(\'msg\').textContent);alert(\'Copiado!\')}\nfunction zap(){let t=encodeURIComponent(document.getElementById(\'msg\').textContent);window.open(\'https://wa.me/?text=\'+t,\'_blank\')}\n</script></body></html>\n'

def proxy_img(u):
    if not u: return ""
    if "wsrv.nl" in u or "weserv.nl" in u: return u
    try:
        enc = urllib.parse.quote_plus(u)
        return f"https://wsrv.nl/?url={enc}&output=jpg&w=800&h=800"
    except:
        return u

def call_api(item_id, shop_id=None):
    try:
        # tenta com itemId
        query = "query { productOfferV2(itemId: %s, limit: 1) { nodes { itemId productName imageUrl priceMin priceMax offerLink } } }" % str(item_id)
        payload = json.dumps({"query": query}, separators=(',', ':'))
        ts = str(int(time.time()))
        sig = hashlib.sha256(f"{APP_ID}{ts}{payload}{SECRET}".encode()).hexdigest()
        auth = f"SHA256 Credential={APP_ID}, Timestamp={ts}, Signature={sig}"
        req = urllib.request.Request(API_URL, data=payload.encode(), headers={"Content-Type":"application/json","Authorization":auth}, method='POST')
        with urllib.request.urlopen(req, timeout=12) as r:
            return json.loads(r.read().decode()), None
    except Exception as e:
        return None, str(e)

def extract_ids(text):
    m = re.search(r'-i\.(\d+)\.(\d+)', text)
    if m: return m.group(1), m.group(2)
    return None, None

def resolve_backend_fallback(url):
    # ultimo recurso se frontend nao mandou itemId
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            final = r.geturl()
            html = r.read().decode(errors='ignore')
            shop, item = extract_ids(final + html)
            return shop, item, final, html
    except:
        return None, None, url, ""

def resolve(url, item_id_front=None, shop_id_front=None):
    shop_id = shop_id_front
    item_id = item_id_front
    title = "Shopee Brasil"
    image = None
    preco = None
    preco_antes = None
    metodo = "fallback"
    erro = None
    final_url = url
    debug = ""
    # se frontend ja mandou itemId, usa direto na API oficial (igual Telegram)
    if item_id:
        metodo = "API_OFICIAL_VIA_FRONTEND_BR"
        data, err = call_api(item_id, shop_id)
        if err:
            erro = err
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
                        v = float(str(pm).replace(',','.'))
                        # Shopee retorna 1990 = 19.90 ou 19.90
                        if v > 1000 and v < 100000: preco = v/100 if v % 1 == 0 else v
                        elif v >= 100000: preco = v/100000
                        else: preco = v
                    if px:
                        pxf = float(str(px).replace(',','.'))
                        if pxf > 1000 and pxf < 100000: pxf = pxf/100 if pxf % 1 == 0 else pxf
                        elif pxf >= 100000: pxf = pxf/100000
                        if pxf and preco and pxf > preco: preco_antes = pxf
                except Exception as e:
                    erro = (erro or "") + f" price parse {e}"
                metodo = "API_OFICIAL_SHOPEE_IGUAL_TELEGRAM"
            else:
                metodo = "api_vazia_front"
        else:
            metodo = "api_sem_resposta"
    else:
        # fallback antigo se frontend nao conseguiu
        s, i, f, h = resolve_backend_fallback(url)
        final_url = f
        if i: item_id = i
        if s: shop_id = s
        if item_id:
            data, err = call_api(item_id, shop_id)
            if not err and data:
                nodes = data.get('data',{}).get('productOfferV2',{}).get('nodes',[])
                if nodes:
                    n = nodes[0]
                    title = n.get('productName') or title
                    image = n.get('imageUrl')
                    try:
                        pm = float(str(n.get('priceMin','')).replace(',','.'))
                        if pm > 1000 and pm < 100000: preco = pm/100 if pm % 1 == 0 else pm
                        else: preco = pm
                    except: pass
                    metodo = "API_OFICIAL_FALLBACK_BACKEND"
        debug = f"backend fallback final={final_url[:60]}"
    # proxy imagem
    img_proxy = proxy_img(image) if image else ""
    img_fallback = f"https://images.weserv.nl/?url={urllib.parse.quote_plus(image)}&output=jpg" if image else ""
    # preco fallback via regex se ainda null
    if not preco and not item_id:
        # tenta pegar preco de qualquer html que tenha
        try:
            req = urllib.request.Request("https://api.microlink.io?url="+urllib.parse.quote(url), headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as r:
                j = json.loads(r.read().decode())
                d = j.get('data',{})
                if d.get('title'): title = d.get('title')
                if d.get('image') and not image:
                    im = d['image']
                    image = im.get('url') if isinstance(im, dict) else im
                    img_proxy = proxy_img(image)
                    img_fallback = f"https://images.weserv.nl/?url={urllib.parse.quote_plus(image)}&output=jpg" if image else ""
                desc = d.get('description','')
                ms = re.findall(r'R\$\s*([\d\.,]+)', desc)
                vals=[]
                for raw in ms:
                    try:
                        if '.' in raw and ',' in raw: v=float(raw.replace('.','').replace(',','.'))
                        elif ',' in raw: v=float(raw.replace(',','.'))
                        else: v=float(raw)
                        if 5 <= v <= 50000: vals.append(v)
                    except: pass
                if vals:
                    vals=sorted(set(vals))
                    preco=vals[0]
                    maiores=[x for x in vals if x>preco]
                    if maiores: preco_antes=max(maiores[:2])
                    metodo = metodo + "+microlink_price"
        except: pass
    desconto=0; economia=0
    if preco_antes and preco and preco_antes>preco:
        try:
            desconto=round((1-preco/preco_antes)*100); economia=round(preco_antes-preco,2)
        except: pass
    return {"affiliate_link_original": url, "title": title[:120], "image": img_proxy, "image_original": image, "image_fallback": img_fallback, "preco_atual": preco, "preco_antes": preco_antes, "desconto": desconto, "economia": economia, "metodo": metodo, "erro_api": erro, "final_url": final_url, "item_id": item_id, "shop_id": shop_id, "debug": debug}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            u = qs.get('url',[None])[0]
            item_id = qs.get('itemId',[None])[0] or qs.get('item_id',[None])[0]
            shop_id = qs.get('shopId',[None])[0] or qs.get('shop_id',[None])[0]
            if u or item_id:
                res = resolve(u or "", item_id, shop_id)
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
            self.wfile.write(f"<h1>Erro {e}</h1>".encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
