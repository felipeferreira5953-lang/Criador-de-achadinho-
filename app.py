
from flask import Flask, request, jsonify, render_template_string
import urllib.request, urllib.parse, re, json, hashlib, time, os

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gerador Achadinhos - BR</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-3 bg-black text-white"><div class="max-w-[430px] mx-auto">
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-4">
<div class="flex justify-between"><span style="background:#00c950;color:#fff;font-size:10px;padding:4px 10px;border-radius:999px;font-weight:900">NOVO ROBO - IP BRASIL</span><span style="font-size:10px;color:#0f0">Fly.io GRU</span></div>
<h1 class="font-black text-[20px] mt-2">GERADOR ACHADINHOS</h1>
<div class="text-[11px] text-zinc-400 mt-1">Hospedado em São Paulo - Shopee não bloqueia</div>
<input id="link" placeholder="Cole link Shopee s.shopee.com.br/XXXX" class="w-full mt-3 bg-black border-2 border-white rounded-xl p-3 text-white font-bold text-[13px]">
<button id="go" class="w-full mt-3 p-3 rounded-xl font-black text-white" style="background:linear-gradient(135deg,#ff6a00,#ee0979)">GERAR COM FOTO + PREÇO REAL</button>
<div id="log" class="bg-black text-[#0f0] border border-green-900 rounded-xl p-2 mt-3 h-[110px] overflow-auto text-[10px] font-mono">Pronto - IP Brasil...</div>
</div>
<div id="res" class="hidden">
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-3 mt-3">
<div class="flex justify-between mb-2"><span class="font-black text-[12px]">📸 STORY 1080x1920</span><button onclick="baixarStory()" class="bg-white text-black px-3 py-1 rounded-full text-[11px] font-bold">Baixar</button></div>
<canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-xl"></canvas>
</div>
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-3 mt-3">
<span class="font-black text-[11px]">📱 LEGENDA GRUPO</span>
<div id="msg" class="mt-2 bg-black border border-zinc-600 rounded-xl p-3 text-[13px] whitespace-pre-wrap"></div>
<div class="grid grid-cols-2 gap-2 mt-3"><button onclick="copiar()" class="bg-white text-black p-2 rounded-xl font-bold text-[12px]">Copiar Texto</button><button onclick="zap()" class="p-2 rounded-xl font-bold text-[12px] text-white" style="background:#25D366">Zap</button></div>
<div id="info" class="mt-2 text-[10px] text-zinc-500"></div>
</div>
</div>
</div>
<script>
let DADOS=null;
function log(x){let e=document.getElementById('log');let d=document.createElement('div');d.textContent=new Date().toLocaleTimeString()+' -> '+x;e.appendChild(d);e.scrollTop=e.scrollHeight}
function brl(v){return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
function extractIds(t){let m=t.match(/-i\\.(\\d+)\\.(\\d+)/);if(m)return{shopId:m[1],itemId:m[2]};let m2=t.match(/i\\.(\\d+)\\.(\\d+)/);if(m2)return{shopId:m2[1],itemId:m2[2]};return{shopId:null,itemId:null}}
async function loadImage(src){return new Promise((res,rej)=>{let i=new Image();i.crossOrigin='anonymous';i.onload=()=>res(i);i.onerror=rej;i.src=src})}
async function gerarStory(d){
let c=document.getElementById('storyCanvas');let ctx=c.getContext('2d');
let g=ctx.createLinearGradient(0,0,0,1920);g.addColorStop(0,'#1a1a1a');g.addColorStop(1,'#000');ctx.fillStyle=g;ctx.fillRect(0,0,1080,1920);
ctx.fillStyle='#00FF88';ctx.font='900 38px system-ui';ctx.fillText('QUEIMA DE ESTOQUE',50,100);
ctx.fillStyle='#fff';ctx.font='900 56px system-ui';ctx.fillText('SHOPEE 🔥',50,170);
ctx.fillStyle='#fff';ctx.fillRect(50,220,980,1080);
try{let img=await loadImage(d.image);let sc=Math.min(980/img.width,1080/img.height);let nw=img.width*sc,nh=img.height*sc;ctx.drawImage(img,50+(980-nw)/2,220+(1080-nh)/2,nw,nh)}catch(e){ctx.fillStyle='#999';ctx.font='bold 32px system-ui';ctx.fillText('Foto carregando...',350,700)}
if(d.preco_atual){if(d.preco_antes&&d.desconto>0){ctx.fillStyle='#888';ctx.font='bold 32px system-ui';ctx.fillText('DE '+brl(d.preco_antes),50,1360);ctx.fillStyle='#00FF88';ctx.font='900 64px system-ui';ctx.fillText('POR '+brl(d.preco_atual),50,1440);ctx.fillStyle='#000';ctx.fillRect(50,1470,400,70);ctx.fillStyle='#fff';ctx.font='900 44px system-ui';ctx.fillText(d.desconto+'% OFF',70,1520)}else{ctx.fillStyle='#00FF88';ctx.font='900 72px system-ui';ctx.fillText(brl(d.preco_atual),50,1430)}}else{ctx.fillStyle='#fff';ctx.font='900 48px system-ui';ctx.fillText('OFERTA IMPERDÍVEL',50,1420)}
ctx.fillStyle='#fff';ctx.font='bold 28px system-ui';ctx.fillText('👇 LINK NA BIO / GRUPO 👇',50,1780);
}
document.getElementById('go').onclick=async()=>{
let l=document.getElementById('link').value.trim();if(!l){alert('Cole link');return}
document.getElementById('res').classList.remove('hidden');log('Link: '+l);
let ids=extractIds(l);
let q='/api/resolve?url='+encodeURIComponent(l);
if(ids.itemId){q='/api/resolve?itemId='+ids.itemId+'&shopId='+(ids.shopId||'')+'&url='+encodeURIComponent(l);log('ItemId direto: '+ids.itemId)}
try{let r=await fetch(q);let j=await r.json();DADOS=j;log('METODO: '+j.metodo+' | Preço: '+(j.preco_atual||'null')+' | Foto: '+(j.image?'ok':'null'));await gerarStory(j);let bp=j.preco_atual?(j.preco_antes&&j.desconto>0?`💰 DE: ~${brl(j.preco_antes)}~ POR: ${brl(j.preco_atual)}\\n🔥 ${j.desconto}% OFF`:`💰 POR: ${brl(j.preco_atual)}`):'💰 OFERTA IMPERDÍVEL';document.getElementById('msg').textContent=`🚨 QUEIMA DE ESTOQUE SHOPEE 🚨\\n\\n📦 ${j.title.toUpperCase()}\\n\\n${bp}\\n\\n⚡ API OFICIAL VERIFICADO!\\n👇 LINK COM DESCONTO 👇\\n\\n${j.affiliate_link_original}\\n\\n⏰ Corre que acaba!`;document.getElementById('info').innerHTML=`Metodo: ${j.metodo} | Item: ${j.item_id||'?'} | Host: Fly.io GRU - Brasil`;}catch(e){log('ERRO: '+e.message)}
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
        return f"https://wsrv.nl/?url={enc}&output=jpg&w=800&h=800"
    except:
        return u

def call_api(item_id):
    try:
        query = f"query {{ productOfferV2(itemId: {item_id}, limit: 1) {{ nodes {{ itemId productName imageUrl priceMin priceMax }} }} }}"
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

def resolve_backend(url, item_id_front=None, shop_id_front=None):
    shop_id = shop_id_front
    item_id = item_id_front
    title = "Shopee Brasil"
    image = None
    preco = None
    preco_antes = None
    metodo = "fallback"
    erro = None
    final_url = url
    # Se frontend já mandou itemId, chama API direto (não é bloqueado)
    if item_id:
        data, err = call_api(item_id)
        if err:
            erro = err
            metodo = "api_erro"
        elif data:
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
                        preco = v/100 if v>1000 and v<100000 else (v/100000 if v>=100000 else v)
                    if px:
                        pxf = float(str(px).replace(',','.'))
                        pxf = pxf/100 if pxf>1000 and pxf<100000 else (pxf/100000 if pxf>=100000 else pxf)
                        if pxf and preco and pxf>preco: preco_antes = pxf
                except: pass
                metodo = "API_OFICIAL_FLY_GRU"
    else:
        # Backend em São Paulo resolve short link - IP Brasil não bloqueado
        try:
            # tenta resolver s.shopee.com.br direto - no Fly GRU funciona
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Linux; Android 12)"}, method='GET')
            with urllib.request.urlopen(req, timeout=10) as r:
                final_url = r.geturl()
                html = r.read().decode(errors='ignore')[:10000]
                s,i = extract_ids(final_url + " " + html)
                if i:
                    item_id = i
                    shop_id = s
                    data, err = call_api(item_id)
                    if not err and data:
                        nodes = data.get('data',{}).get('productOfferV2',{}).get('nodes',[])
                        if nodes:
                            n = nodes[0]
                            title = n.get('productName') or title
                            image = n.get('imageUrl')
                            try:
                                pm = float(str(n.get('priceMin','')).replace(',','.'))
                                preco = pm/100 if pm>1000 and pm<100000 else (pm/100000 if pm>=100000 else pm)
                            except: pass
                            metodo = "API_OFICIAL_BACKEND_GRU_DIRETO"
        except Exception as e:
            erro = str(e)[:120]
            metodo = "fallback_backend"
    img_proxy = proxy_img(image) if image else ""
    desconto = 0
    if preco_antes and preco and preco_antes>preco:
        try: desconto = round((1-preco/preco_antes)*100)
        except: pass
    return {"affiliate_link_original": url, "title": title[:120], "image": img_proxy, "image_original": image, "preco_atual": preco, "preco_antes": preco_antes, "desconto": desconto, "metodo": metodo, "erro_api": erro, "final_url": final_url, "item_id": item_id, "shop_id": shop_id}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/resolve')
def api_resolve():
    url = request.args.get('url','')
    item_id = request.args.get('itemId') or request.args.get('item_id')
    shop_id = request.args.get('shopId') or request.args.get('shop_id')
    res = resolve_backend(url, item_id, shop_id)
    return jsonify(res)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
