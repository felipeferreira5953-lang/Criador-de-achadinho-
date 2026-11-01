from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse, re, json, hashlib, time

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

HTML = '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Achadinhos Story</title><script src="https://cdn.tailwindcss.com"></script><style>body{background:#111;color:#fff;font-family:system-ui} .glass{background:#1a1a1a;border:1px solid #333} canvas{max-width:100%;height:auto;border-radius:16px}</style></head><body class="p-3"><div class="max-w-[440px] mx-auto"><div class="glass rounded-[16px] p-4"><div class="flex justify-between items-center"><span style="background:#00c950;color:#fff;font-size:10px;padding:3px 8px;border-radius:999px;font-weight:900">API OFICIAL + STORY</span><span style="font-size:10px;color:#888">FOTO + PRECO</span></div><input id="link" placeholder="https://s.shopee.com.br/XXXX" class="w-full mt-3 bg-black border border-zinc-700 rounded-xl p-3 text-white font-bold text-[13px]"><button id="go" class="w-full mt-3 p-3 rounded-xl font-black text-white" style="background:linear-gradient(135deg,#ff6a00,#ee0979)">GERAR STORY + GRUPO 🔥</button><div id="log" class="bg-black text-[#0f0] rounded-xl p-2 mt-3 h-[90px] overflow-auto text-[10px] font-mono">API Oficial pronta AppID 1832**** - pronto pra gerar story</div></div><div id="res" class="hidden"><div class="glass rounded-[16px] p-3 mt-3"><div class="flex justify-between items-center mb-2"><span class="font-black text-[12px]">📸 STORY 1080x1920</span><button onclick="baixarStory()" class="bg-white text-black px-3 py-1 rounded-full text-[11px] font-bold">Baixar Story</button></div><canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-zinc-900"></canvas><div id="imgPreview" class="mt-2 text-[10px] text-zinc-400"></div></div><div class="glass rounded-[16px] p-3 mt-3"><span class="font-black text-[11px]">📱 LEGENDA GRUPO (COM VALOR)</span><div id="msg" class="mt-2 bg-zinc-900 border border-zinc-800 rounded-xl p-3 text-[13px] whitespace-pre-wrap"></div><div class="grid grid-cols-2 gap-2 mt-3"><button onclick="copiar()" class="bg-white text-black p-2 rounded-xl font-bold text-[12px]">Copiar Texto</button><button onclick="zap()" class="p-2 rounded-xl font-bold text-[12px] text-white" style="background:#25D366">Enviar no Zap</button></div><div id="info" class="mt-2 text-[10px] text-zinc-500"></div></div></div></div><script>\nlet ORIG=""; let DADOS=null;\nfunction log(x){let e=document.getElementById(\'log\');let d=document.createElement(\'div\');d.textContent=new Date().toLocaleTimeString()+\' -> \'+x;e.appendChild(d);e.scrollTop=e.scrollHeight}\nfunction brl(v){return v.toLocaleString(\'pt-BR\',{style:\'currency\',currency:\'BRL\'})}\nasync function loadImage(src){return new Promise((res,rej)=>{let img=new Image();img.crossOrigin=\'anonymous\';img.onload=()=>res(img);img.onerror=rej;img.src=src;})}\nasync function gerarStory(dados){\n  let c=document.getElementById(\'storyCanvas\');let ctx=c.getContext(\'2d\');\n  // fundo gradiente\n  let grad=ctx.createLinearGradient(0,0,0,1920);grad.addColorStop(0,\'#1a1a1a\');grad.addColorStop(1,\'#000\');ctx.fillStyle=grad;ctx.fillRect(0,0,1080,1920);\n  // titulo topo\n  ctx.fillStyle=\'#00FF88\';ctx.font=\'900 38px system-ui\';ctx.fillText(\'QUEIMA DE ESTOQUE\',50,100);\n  ctx.fillStyle=\'#fff\';ctx.font=\'900 56px system-ui\';ctx.fillText(\'SHOPEE 🔥\',50,170);\n  // caixa produto\n  ctx.fillStyle=\'#fff\';ctx.fillRect(50,220,980,1080);\n  try{\n    let prodImg=await loadImage(dados.image);\n    // centraliza imagem no quadrado 980x1080 contain\n    let iw=prodImg.width, ih=prodImg.height;\n    let scale=Math.min(980/iw,1080/ih);let nw=iw*scale, nh=ih*scale;\n    let x=50+(980-nw)/2, y=220+(1080-nh)/2;\n    ctx.drawImage(prodImg,x,y,nw,nh);\n  }catch(e){ctx.fillStyle=\'#ccc\';ctx.font=\'bold 32px system-ui\';ctx.fillText(\'Sem foto\',400,750)}\n  // preco\n  let yBase=1360;\n  if(dados.preco_atual){\n    ctx.fillStyle=\'#fff\';ctx.font=\'bold 34px system-ui\';\n    if(dados.preco_antes && dados.desconto>0){\n      ctx.fillStyle=\'#888\';ctx.font=\'bold 32px system-ui\';ctx.fillText(\'DE \'+brl(dados.preco_antes),50,yBase);\n      ctx.fillStyle=\'#00FF88\';ctx.font=\'900 64px system-ui\';ctx.fillText(\'POR \'+brl(dados.preco_atual),50,yBase+80);\n      ctx.fillStyle=\'#000\';ctx.fillRect(50,yBase+110,420,70);\n      ctx.fillStyle=\'#fff\';ctx.font=\'900 44px system-ui\';ctx.fillText(dados.desconto+\'% OFF\',70,yBase+160);\n    }else{\n      ctx.fillStyle=\'#00FF88\';ctx.font=\'900 72px system-ui\';ctx.fillText(brl(dados.preco_atual),50,yBase+70);\n    }\n  }else{\n    ctx.fillStyle=\'#fff\';ctx.font=\'900 48px system-ui\';ctx.fillText(\'OFERTA IMPERDIVEL\',50,yBase+60);\n  }\n  // rodapé link\n  ctx.fillStyle=\'#fff\';ctx.font=\'bold 28px system-ui\';ctx.fillText(\'👇 LINK NA BIO / GRUPO 👇\',50,1780);\n  ctx.fillStyle=\'#666\';ctx.font=\'18px system-ui\';ctx.fillText(dados.affiliate_link_original.slice(0,55),50,1820);\n  document.getElementById(\'imgPreview\').textContent=\'Story gerado 1080x1920 - \'+ (dados.metodo||\'\') +\' - Item:\'+ (dados.item_id||\'\')\n}\ndocument.getElementById(\'go\').onclick=async()=>{\n  let l=document.getElementById(\'link\').value.trim();if(!l){alert(\'Cole link\');return}\n  ORIG=l;document.getElementById(\'res\').classList.remove(\'hidden\');log(\'Resolvendo link curto via proxy...\');log(\'Link: \'+ORIG);\n  try{\n    let r=await fetch(\'/?url=\'+encodeURIComponent(ORIG)+\'&t=\'+Date.now());let j=await r.json();\n    DADOS=j;\n    log(\'METODO: \'+j.metodo);log(\'Titulo: \'+(j.title||\'\').slice(0,45));log(\'Preco: \'+(j.preco_atual||\'null\')+\' Antes:\'+(j.preco_antes||\'null\'));log(\'Foto: \'+(j.image?\'ok\':\'null\'));\n    if(j.erro_api) log(\'API aviso: \'+j.erro_api.slice(0,120));\n    if(j.debug) log(\'Debug: \'+j.debug.slice(0,150));\n    await gerarStory(j);\n    let bp=j.preco_atual ? (j.preco_antes&&j.desconto>0?`💰 DE: ~${brl(j.preco_antes)}~ POR: ${brl(j.preco_atual)}\\n🔥 ${j.desconto}% OFF - Economize ${brl(j.economia)}!`:`💰 POR APENAS: ${brl(j.preco_atual)}`):`💰 OFERTA IMPERDIVEL - Confira no link`;\n    let msg=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\\n\\n📦 ${j.title.toUpperCase()}\\n\\n${bp}\\n\\n⚡ PRODUTO VERIFICADO API OFICIAL!\\n👇 LINK COM DESCONTO AQUI 👇\\n\\n${j.affiliate_link_original}\\n\\n⏰ Corre que acaba rapido!`;\n    document.getElementById(\'msg\').textContent=msg;\n    document.getElementById(\'info\').innerHTML=`<span style=color:#0f0>🔒 Link fiel: ${j.affiliate_link_original}</span><br>Metodo: ${j.metodo} | ItemID: ${j.item_id||\'?\'} ShopID: ${j.shop_id||\'?\'} | Foto: ${j.image?\'OK\':\'FALHOU\'}`\n  }catch(e){log(\'ERRO: \'+e.message)}\n};\nfunction baixarStory(){let c=document.getElementById(\'storyCanvas\');let a=document.createElement(\'a\');a.download=\'story-achadinho-1080x1920.png\';a.href=c.toDataURL(\'image/png\');a.click()}\nfunction copiar(){navigator.clipboard.writeText(document.getElementById(\'msg\').textContent);alert(\'Copiado pro grupo!\')}\nfunction zap(){let t=encodeURIComponent(document.getElementById(\'msg\').textContent);window.open(\'https://wa.me/?text=\'+t,\'_blank\')}\n</script></body></html>\n'

def fetch_via_microlink(short_url):
    try:
        api = f"https://api.microlink.io?url={urllib.parse.quote(short_url)}&meta=true&images=true"
        req = urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            j = json.loads(r.read().decode())
            d = j.get('data',{})
            final_url = d.get('url','')
            title = d.get('title','')
            desc = d.get('description','')
            img = None
            if d.get('image'):
                if isinstance(d['image'], dict):
                    img = d['image'].get('url')
                else:
                    img = str(d['image'])
            # tenta pegar imagem do array
            if not img and d.get('images'):
                try:
                    img = d['images'][0].get('url') if isinstance(d['images'][0], dict) else d['images'][0]
                except:
                    pass
            return final_url, title, img, desc, d
    except Exception as e:
        return "", "", None, "", {"error": str(e)}

def fetch_url_simple(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15","Accept":"text/html,application/xhtml+xml"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.geturl(), r.read().decode('utf-8', errors='ignore')
    except:
        return url, ""

def proxy_img(u):
    if not u:
        return ""
    if "wsrv.nl" in u or "weserv.nl" in u:
        return u
    try:
        enc = urllib.parse.quote_plus(u)
        return f"https://wsrv.nl/?url={enc}&output=jpg&w=800&h=800"
    except:
        return u

def call_api(item_id):
    try:
        query = "query { productOfferV2(itemId: %s, limit: 1, sortType: 1) { nodes { itemId productName imageUrl priceMin priceMax offerLink productLink } } }" % str(item_id)
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
    shop_id = None
    item_id = None
    m = re.search(r'-i\.(\d+)\.(\d+)', text)
    if m:
        shop_id, item_id = m.group(1), m.group(2)
        return shop_id, item_id
    # tenta padrao shopid itemid separado
    m1 = re.search(r'"shopid"\s*:\s*(\d+)', text)
    m2 = re.search(r'"itemid"\s*:\s*(\d+)', text)
    if m1: shop_id = m1.group(1)
    if m2: item_id = m2.group(1)
    if item_id:
        return shop_id, item_id
    # tenta /product/ 123456789?
    m3 = re.search(r'/product[^/]*-(\d+)', text)
    if m3:
        # as vezes itemid sozinho
        pass
    return shop_id, item_id

def resolve(url):
    debug_info = ""
    final_via_micro, title_micro, img_micro, desc_micro, raw_micro = fetch_via_microlink(url)
    debug_info += f"micro final={final_via_micro[:80]} "
    final_simple, html_simple = fetch_url_simple(url)
    # junta textos para procurar id
    combined = (final_via_micro + " " + final_simple + " " + html_simple)[:8000]
    shop_id, item_id = extract_ids(combined)
    if not item_id:
        # tenta extrair do raw microlink json string
        try:
            shop_id2, item_id2 = extract_ids(json.dumps(raw_micro))
            if item_id2:
                item_id = item_id2
                shop_id = shop_id2 or shop_id
        except:
            pass
    title = title_micro or "Shopee Brasil"
    image = img_micro
    preco = None
    preco_antes = None
    metodo = "microlink"
    erro_api = None
    # 1) Tenta API oficial se tem item_id
    if item_id:
        data, err = call_api(item_id)
        if err:
            erro_api = err
            metodo = f"api_erro_{err[:30]}"
        elif data:
            if data.get('errors'):
                erro_api = str(data['errors'])[:300]
            nodes = data.get('data',{}).get('productOfferV2',{}).get('nodes',[])
            if nodes:
                n = nodes[0]
                if n.get('productName'): title = n.get('productName')
                if n.get('imageUrl'): image = n.get('imageUrl')
                pm = n.get('priceMin')
                px = n.get('priceMax')
                try:
                    if pm:
                        v = float(str(pm).replace(',','.'))
                        if v > 1000 and v < 10000000:
                            # se vier 1990 = 19.90? testa: se v>1000 e <100k divide por 100
                            if v < 100000:
                                preco = v/100 if v % 1 == 0 and v > 100 else v
                            else:
                                preco = v/100000
                        else:
                            preco = v
                        # corrige se ainda grande
                        if preco and preco > 50000:
                            preco = preco/100
                    if px:
                        pxf = float(str(px).replace(',','.'))
                        if pxf > 1000: pxf = pxf/100 if pxf < 100000 else pxf/100000
                        if pxf and preco and pxf > preco:
                            preco_antes = pxf
                except Exception as e:
                    erro_api = (erro_api or "") + f" parse price {e}"
                metodo = "API_OFICIAL_SHOPEE"
            else:
                metodo = "api_vazia"
                if not image:
                    image = img_micro
    else:
        metodo = "sem_itemid_microlink"
        # tenta og:image do html_simple
        if not image:
            m = re.search(r'property="og:image" content="([^"]+)"', html_simple)
            if m: image = m.group(1)
    # fallback titulo
    if title == "Shopee Brasil" and html_simple:
        m = re.search(r'property="og:title" content="([^"]+)"', html_simple)
        if m: title = m.group(1)
    # fallback preco do desc_micro
    if not preco:
        # procura R$ no desc e html
        for txt in [desc_micro, html_simple]:
            ms = re.findall(r'R\$\s*([\d\.,]+)', txt)
            vals = []
            for raw in ms:
                try:
                    if '.' in raw and ',' in raw:
                        v = float(raw.replace('.','').replace(',','.'))
                    elif ',' in raw:
                        v = float(raw.replace(',','.'))
                    else:
                        v = float(raw)
                    if 5 <= v <= 50000:
                        vals.append(v)
                except: pass
            if vals:
                vals = sorted(set(vals))
                preco = vals[0]
                maiores = [x for x in vals if x > preco]
                if maiores:
                    preco_antes = max(maiores[:2])
                break
    img_proxy = proxy_img(image) if image else ""
    # fallback via weserv se wsrv falhar
    img_fallback = ""
    if image:
        enc = urllib.parse.quote_plus(image)
        img_fallback = f"https://images.weserv.nl/?url={enc}&output=jpg"
    desconto = 0
    economia = 0
    if preco_antes and preco and preco_antes > preco:
        try:
            desconto = round((1-preco/preco_antes)*100)
            economia = round(preco_antes-preco,2)
        except: pass
    return {
        "affiliate_link_original": url,
        "title": title.strip()[:120],
        "image": img_proxy,
        "image_original": image,
        "image_fallback": img_fallback,
        "preco_atual": preco,
        "preco_antes": preco_antes,
        "desconto": desconto,
        "economia": economia,
        "metodo": metodo,
        "erro_api": erro_api,
        "final_url": final_via_micro or final_simple,
        "item_id": item_id,
        "shop_id": shop_id,
        "debug": debug_info + f" raw_len={len(str(raw_micro))}"
    }

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
            self.wfile.write(f"<h1>Erro: {e}</h1>".encode())
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
