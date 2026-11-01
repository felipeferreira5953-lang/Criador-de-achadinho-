from flask import Flask, request, jsonify, render_template_string
import urllib.request, urllib.parse, re, json, hashlib, time, os

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gerador Achadinhos - BR V3</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-3 bg-black text-white"><div class="max-w-[430px] mx-auto">
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-4">
<div class="flex justify-between"><span style="background:#00c950;color:#fff;font-size:10px;padding:4px 10px;border-radius:999px;font-weight:900">NOVO ROBO V3 - FOTO GARANTIDA</span><span style="font-size:10px;color:#0f0">Fly.io GRU</span></div>
<h1 class="font-black text-[20px] mt-2">GERADOR ACHADINHOS</h1>
<div class="text-[11px] text-zinc-400 mt-1">Hospedado em São Paulo - IP Brasil - V3 com Preço</div>
<input id="link" placeholder="Cole link Shopee s.shopee.com.br/XXXX" class="w-full mt-3 bg-black border-2 border-white rounded-xl p-3 text-white font-bold text-[13px]">
<button id="go" class="w-full mt-3 p-3 rounded-xl font-black text-white" style="background:linear-gradient(135deg,#ff6a00,#ee0979)">GERAR COM FOTO + PREÇO REAL</button>
<div id="log" class="bg-black text-[#0f0] border border-green-900 rounded-xl p-2 mt-3 h-[160px] overflow-auto text-[10px] font-mono">Pronto - V3 esperando link...</div>
</div>
<div id="res" class="hidden">
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-3 mt-3">
<div class="flex justify-between mb-2"><span class="font-black text-[12px]">📸 STORY 1080x1920</span><button onclick="baixarStory()" class="bg-white text-black px-3 py-1 rounded-full text-[11px] font-bold">Baixar</button></div>
<canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-xl"></canvas>
<img id="fotoReal" class="w-full mt-2 rounded-xl hidden">
</div>
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-3 mt-3">
<span class="font-black text-[11px]">📱 LEGENDA GRUPO (COM PREÇO)</span>
<div id="msg" class="mt-2 bg-black border border-zinc-600 rounded-xl p-3 text-[13px] whitespace-pre-wrap"></div>
<div class="grid grid-cols-2 gap-2 mt-3"><button onclick="copiar()" class="bg-white text-black p-2 rounded-xl font-bold text-[12px]">Copiar Texto</button><button onclick="zap()" class="p-2 rounded-xl font-bold text-[12px] text-white" style="background:#25D366">Zap</button></div>
<div id="info" class="mt-2 text-[10px] text-zinc-500"></div>
</div>
</div>
</div>
<script>
let DADOS=null;
function log(x){let e=document.getElementById('log');let d=document.createElement('div');d.textContent=new Date().toLocaleTimeString()+' -> '+x;e.appendChild(d);e.scrollTop=e.scrollHeight}
function brl(v){try{return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}catch(e){return 'R$ '+v}}
function extractIds(t){
  if(!t) return {shopId:null,itemId:null};
  let m=t.match(/-i\\.(\\d+)\\.(\\d+)/);if(m)return{shopId:m[1],itemId:m[2]};
  m=t.match(/i\\.(\\d+)\\.(\\d+)/);if(m)return{shopId:m[1],itemId:m[2]};
  m=t.match(/(\\d{5,})[^0-9]+(\\d{8,})/);if(m)return{shopId:m[1],itemId:m[2]};
  return{shopId:null,itemId:null}
}
async function loadImage(src){return new Promise((res,rej)=>{let i=new Image();i.crossOrigin='anonymous';i.onload=()=>res(i);i.onerror=rej;i.src=src})}
async function gerarStory(d){
let c=document.getElementById('storyCanvas');let ctx=c.getContext('2d');
let g=ctx.createLinearGradient(0,0,0,1920);g.addColorStop(0,'#1a1a1a');g.addColorStop(1,'#000');ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
ctx.fillStyle='#00FF88';ctx.font='900 38px system-ui';ctx.fillText('QUEIMA DE ESTOQUE',50,100);
ctx.fillStyle='#fff';ctx.font='900 56px system-ui';ctx.fillText('SHOPEE 🔥',50,170);
ctx.fillStyle='#fff';ctx.fillRect(50,220,980,1080);
try{let img=await loadImage(d.image);let sc=Math.min(980/img.width,1080/img.height);let nw=img.width*sc,nh=img.height*sc;ctx.drawImage(img,50+(980-nw)/2,220+(1080-nh)/2,nw,nh)}catch(e){ctx.fillStyle='#999';ctx.font='bold 26px system-ui';let txt=d.image_original?('Img: '+d.image_original.slice(0,40)):'Foto carregando...';ctx.fillText(txt,50,700)}
if(d.preco_atual){if(d.preco_antes&&d.desconto>0){ctx.fillStyle='#888';ctx.font='bold 32px system-ui';ctx.fillText('DE '+brl(d.preco_antes),50,1360);ctx.fillStyle='#00FF88';ctx.font='900 64px system-ui';ctx.fillText('POR '+brl(d.preco_atual),50,1440);ctx.fillStyle='#000';ctx.fillRect(50,1470,400,70);ctx.fillStyle='#fff';ctx.font='900 44px system-ui';ctx.fillText(d.desconto+'% OFF',70,1520)}else{ctx.fillStyle='#00FF88';ctx.font='900 72px system-ui';ctx.fillText(brl(d.preco_atual),50,1430)}}else{ctx.fillStyle='#fff';ctx.font='900 42px system-ui';ctx.fillText('OFERTA IMPERDÍVEL',50,1420)}
ctx.fillStyle='#fff';ctx.font='bold 28px system-ui';ctx.fillText('👇 LINK NA BIO / GRUPO 👇',50,1780);
}
document.getElementById('go').onclick=async()=>{
let l=document.getElementById('link').value.trim();if(!l){alert('Cole link');return}
document.getElementById('res').classList.remove('hidden');log('Link: '+l);
let ids=extractIds(l);
let q='/api/resolve?url='+encodeURIComponent(l);
if(ids.itemId){q='/api/resolve?itemId='+ids.itemId+'&shopId='+(ids.shopId||'')+'&url='+encodeURIComponent(l);log('ItemId direto: '+ids.itemId)}
try{let r=await fetch(q);let j=await r.json();DADOS=j;log('METODO: '+j.metodo+' | Preço: '+(j.preco_atual||'null')+' | Foto: '+(j.image?'ok':'null'));log('Final: '+(j.final_url||'').slice(0,90));if(j.erro_api)log('Erro: '+j.erro_api.slice(0,120));await gerarStory(j);
let fotoEl=document.getElementById('fotoReal');if(j.image_original){fotoEl.src=j.image_original;fotoEl.classList.remove('hidden')}else if(j.image){fotoEl.src=j.image;fotoEl.classList.remove('hidden')}
let bp=j.preco_atual?(j.preco_antes&&j.desconto>0?`💰 DE: ~${brl(j.preco_antes)}~ POR: ${brl(j.preco_atual)}\\n🔥 ${j.desconto}% OFF\\n💸 Você economiza ${brl(j.preco_antes-j.preco_atual)}`:`💰 POR APENAS: ${brl(j.preco_atual)}\\n🔥 OFERTA IMPERDÍVEL`):'💰 OFERTA IMPERDÍVEL - CLIQUE E CONFIRA O PREÇO';
let legenda=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\\n\\n📦 ${j.title.toUpperCase()}\\n\\n${bp}\\n\\n⭐ Produto Original Shopee\\n⚡ Link de Afiliado Verificado\\n👇 LINK COM DESCONTO NOS COMENTÁRIOS 👇\\n\\n${j.affiliate_link_original}\\n\\n⏰ Corre que acaba rápido!\\n#achadinhos #shopee #oferta`;
document.getElementById('msg').textContent=legenda;
document.getElementById('info').innerHTML=`Metodo: ${j.metodo} | Item: ${j.item_id||'?'} | Preço: ${j.preco_atual||'null'} | Img: ${(j.image_original||'').slice(0,35)}`;
}catch(e){log('ERRO JS: '+e.message)}
};
function baixarStory(){let c=document.getElementById('storyCanvas');let a=document.createElement('a');a.download='story-achadinho.png';a.href=c.toDataURL('image/png');a.click()}
function copiar(){navigator.clipboard.writeText(document.getElementById('msg').textContent);alert('Copiado!')}
function zap(){let t=encodeURIComponent(document.getElementById('msg').textContent);window.open('https://wa.me/?text='+t,'_blank')}
</script></body></html>
"""

def proxy_img(u):
    if not u: return ""
    try:
        enc = urllib.parse.quote_plus(u)
        return f"https://wsrv.nl/?url={enc}&output=jpg&w=800&h=800&n=-1"
    except:
        return u

def call_api(item_id):
    try:
        query = f"query {{ productOfferV2(itemId: {item_id}, limit: 1) {{ nodes {{ itemId productName imageUrl priceMin priceMax }} }} }}"
        payload = json.dumps({"query": query}, separators=(',', ':'))
        ts = str(int(time.time()))
        sig = hashlib.sha256(f"{APP_ID}{ts}{payload}{SECRET}".encode()).hexdigest()
        auth = f"SHA256 Credential={APP_ID}, Timestamp={ts}, Signature={sig}"
        req = urllib.request.Request(API_URL, data=payload.encode(), headers={"Content-Type":"application/json","Authorization":auth,"User-Agent":"Mozilla/5.0"}, method='POST')
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode()), None
    except Exception as e:
        return None, str(e)[:300]

def extract_ids(text):
    if not text:
        return None, None
    pats = [
        r'-i\.(\d+)\.(\d+)',
        r'i\.(\d+)\.(\d+)',
        r'itemid[^\d]*(\d+).*?shopid[^\d]*(\d+)',
        r'shopid[^\d]*(\d+).*?itemid[^\d]*(\d+)',
    ]
    for pat in pats:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            # tenta descobrir qual é item (geralmente maior)
            a,b = m.group(1), m.group(2)
            if 'itemid' in pat.lower():
                # primeira captura já é item se pat começa com itemid
                if pat.lower().startswith('itemid'):
                    item, shop = a, b
                else:
                    shop, item = a, b
            else:
                shop, item = a, b
                # heurística: itemId tem 10+ dígitos
                if len(a) > len(b) and len(a) >= 10:
                    item, shop = a, b
                elif len(b) >= 9:
                    item, shop = b, a if len(a) < len(b) else (a,b)
                    # no padrão -i.SHOP.ITEM, segundo é ITEM
                    if '-i.' in text or 'i.' in text:
                        shop, item = a, b
            if len(item) >= 8:
                return shop, item
    # fallback genérico: pega todos números grandes
    nums = re.findall(r'\d{8,}', text)
    if len(nums) >= 2:
        # pega os 2 últimos grandes
        return nums[-2], nums[-1]
    elif len(nums) == 1 and len(nums[0]) >= 10:
        return None, nums[0]
    return None, None

def try_resolve_short(url):
    final_url = url
    html = ""
    how = "init"
    # 1 - Direto
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9",
            "Referer": "https://shopee.com.br/",
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            final_url = r.geturl()
            html = r.read().decode(errors='ignore', limit=20000) if hasattr(r, 'read') else r.read().decode(errors='ignore')
            # pega primeiros 20k
            html = html[:20000]
            how = "direct"
            return final_url, html, how
    except Exception as e:
        how = f"direct_fail:{str(e)[:60]}"
    # 2 - allorigins raw
    try:
        api = f"https://api.allorigins.win/raw?url={urllib.parse.quote(url)}"
        req = urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            html = r.read().decode(errors='ignore')[:20000]
            m = re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html)
            if m:
                final_url = m.group(0)
            how = "allorigins_raw"
            return final_url, html, how
    except:
        pass
    # 3 - microlink que sempre retorna title e image
    try:
        api = f"https://api.microlink.io?url={urllib.parse.quote(url)}"
        req = urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            j = json.loads(r.read().decode())
            d = j.get('data',{})
            # microlink já resolve final url
            if d.get('url'):
                final_url = d.get('url')
            # junta html da descricao + title pra extrair id
            html = json.dumps(d)[:20000]
            how = "microlink"
            return final_url, html, how
    except Exception as e:
        how = f"all_fail:{str(e)[:50]}"
    return final_url, html, how

def resolve_backend(url, item_id_front=None, shop_id_front=None):
    shop_id = shop_id_front
    item_id = item_id_front
    title = "Achadinho Shopee"
    image = None
    preco = None
    preco_antes = None
    metodo = "fallback"
    erro = None
    final_url = url
    debug = ""
    microlink_data = {}

    # 1 - Se já tem itemId, chama API direto
    if item_id:
        data, err = call_api(item_id)
        if err:
            erro = err
            metodo = "api_erro_front"
        else:
            nodes = data.get('data',{}).get('productOfferV2',{}).get('nodes',[]) if data else []
            if nodes:
                n = nodes[0]
                title = n.get('productName') or title
                image = n.get('imageUrl')
                try:
                    pm = n.get('priceMin')
                    px = n.get('priceMax')
                    if pm:
                        v = float(str(pm).replace(',','.'))
                        preco = v/100000 if v>=100000 else (v/100 if v>1000 else v)
                    if px:
                        xf = float(str(px).replace(',','.'))
                        xf = xf/100000 if xf>=100000 else (xf/100 if xf>1000 else xf)
                        if xf and preco and xf>preco:
                            preco_antes = xf
                except Exception as pe:
                    erro = f"price_parse {pe}"
                metodo = "API_OFICIAL_FRONT_V3"
            else:
                erro = f"api vazia {str(data)[:150]}"
                metodo = "api_vazia_front"

    # 2 - Se não tem itemId ou falhou, resolve short link
    if not item_id or not image:
        f_url, html, how = try_resolve_short(url)
        final_url = f_url
        debug = html[:300]
        s,i = extract_ids(final_url + " " + html)
        if i and not item_id:
            item_id = i
            shop_id = s if s else shop_id
        # tenta API de novo com id resolvido
        if item_id and not preco:
            data, err = call_api(item_id)
            if not err and data:
                nodes = data.get('data',{}).get('productOfferV2',{}).get('nodes',[])
                if nodes:
                    n = nodes[0]
                    title = n.get('productName') or title
                    if not image:
                        image = n.get('imageUrl')
                    try:
                        pm = n.get('priceMin')
                        if pm and not preco:
                            v = float(str(pm).replace(',','.'))
                            preco = v/100000 if v>=100000 else (v/100 if v>1000 else v)
                        px = n.get('priceMax')
                        if px:
                            xf = float(str(px).replace(',','.'))
                            xf = xf/100000 if xf>=100000 else (xf/100 if xf>1000 else xf)
                            if xf and preco and xf>preco:
                                preco_antes = xf
                    except:
                        pass
                    metodo = f"API_OFICIAL_RESOLVIDO_V3_{how}"
                else:
                    erro = (erro or "") + f" api_vazia_resolvido {how}"
            else:
                erro = (erro or "") + f" api_erro_resolvido {err} {how}"

    # 3 - Fallback GARANTIDO via microlink para foto e preço
    try:
        api = f"https://api.microlink.io?url={urllib.parse.quote(url)}"
        req = urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            j = json.loads(r.read().decode())
            d = j.get('data',{})
            microlink_data = d
            if d.get('title') and title in ["Achadinho Shopee","Shopee Brasil"]:
                title = d.get('title')
            if d.get('image') and not image:
                im = d['image']
                image = im.get('url') if isinstance(im, dict) else im
            # preço via descrição
            if not preco:
                desc = d.get('description','') + " " + str(d.get('publisher',''))
                ms = re.findall(r'R\$\s*([\d\.,]+)', desc)
                vals=[]
                for raw in ms:
                    try:
                        if '.' in raw and ',' in raw:
                            v=float(raw.replace('.','').replace(',','.'))
                        elif ',' in raw:
                            v=float(raw.replace(',','.'))
                        else:
                            v=float(raw)
                        if 5 <= v <= 50000:
                            vals.append(v)
                    except:
                        pass
                if vals:
                    vals=sorted(set(vals))
                    preco=vals[0]
                    maiores=[x for x in vals if x>preco]
                    if maiores:
                        preco_antes=max(maiores[:2])
                    if not metodo.startswith("API"):
                        metodo = metodo + f"+microlink_preco"
                    else:
                        metodo = metodo + "+microlink"
    except Exception as e:
        if not erro:
            erro = f"microlink_fail {e}"

    # 4 - Se ainda sem imagem, tenta pegar og:image do html
    if not image and debug:
        m = re.search(r'og:image["\']?\s*content=["\']([^"\']+)', debug, re.IGNORECASE)
        if m:
            image = m.group(1)

    img_proxy = proxy_img(image) if image else ""
    desconto=0
    if preco_antes and preco and preco_antes>preco:
        try:
            desconto=round((1-preco/preco_antes)*100)
        except:
            pass
    return {
        "affiliate_link_original": url,
        "title": title[:150],
        "image": img_proxy,
        "image_original": image,
        "preco_atual": preco,
        "preco_antes": preco_antes,
        "desconto": desconto,
        "metodo": metodo,
        "erro_api": erro,
        "final_url": final_url,
        "item_id": item_id,
        "shop_id": shop_id,
        "debug": debug[:200]
    }

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/resolve')
def api_resolve():
    url = request.args.get('url','')
    item_id = request.args.get('itemId') or request.args.get('item_id')
    shop_id = request.args.get('shopId') or request.args.get('shop_id')
    if item_id:
        item_id = re.sub(r'[^0-9]', '', item_id)
    if shop_id:
        shop_id = re.sub(r'[^0-9]', '', shop_id)
    res = resolve_backend(url, item_id, shop_id)
    return jsonify(res)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
