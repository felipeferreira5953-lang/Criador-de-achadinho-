from flask import Flask, request, jsonify, render_template_string
import urllib.request, urllib.parse, re, json, hashlib, time, os

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"
app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V8 - DEBUG API REAL</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-3 bg-black text-white"><div class="max-w-[480px] mx-auto">
<div class="bg-zinc-900 border border-red-600 rounded-[16px] p-4">
<div class="bg-red-900/30 border border-red-600 rounded-xl p-3 mb-3">
<div class="font-black text-[13px] text-red-400">⚠️ SEU PRINT MOSTRA O PROBLEMA!</div>
<div class="text-[11px] mt-1 text-white">No topo: "Por favor, complete suas Informações de Pagamento" - A Shopee bloqueia API se pagamento não completo!</div>
<div class="text-[10px] mt-1 text-zinc-300">AppID: 18325950432 ✅ Válido | Mas precisa completar pagamento pra API retornar produto!</div>
</div>
<div class="flex justify-between"><span style="background:#00c950;color:#fff;font-size:10px;padding:5px 12px;border-radius:999px;font-weight:900">V8 - DEBUG REAL DA API</span><span style="font-size:10px;color:#0f0">Mostra erro real</span></div>
<h1 class="font-black text-[18px] mt-2">DEBUG API SHOPEE</h1>
<input id="link" placeholder="Cole link s.shopee.com.br/XXXX" class="w-full mt-3 bg-black border-2 border-white rounded-xl p-3 text-white font-bold text-[12px]">
<button id="go" class="w-full mt-3 p-3 rounded-xl font-black text-white" style="background:linear-gradient(135deg,#ff6a00,#ee0979)">🔍 TESTAR API COM SEU APPID REAL</button>
<div id="log" class="bg-black text-[#0f0] border border-green-900 rounded-xl p-2 mt-3 h-[300px] overflow-auto text-[9px] font-mono">V8 debug - vai mostrar resposta REAL da API Shopee com seu AppID...</div>
</div>
<div id="res" class="hidden">
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-3 mt-3">
<span class="font-black text-[12px]">📸 STORY</span>
<canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-xl mt-2"></canvas>
</div>
<div class="bg-zinc-900 border border-zinc-700 rounded-[16px] p-3 mt-3">
<span class="font-black text-[12px]">📱 LEGENDA</span>
<div id="msg" class="mt-2 bg-black border border-zinc-600 rounded-xl p-3 text-[12px] whitespace-pre-wrap"></div>
</div>
</div>
</div>
<script>
let DADOS=null;
function log(x){let e=document.getElementById('log');let d=document.createElement('div');d.textContent=new Date().toLocaleTimeString()+' -> '+x;e.appendChild(d);e.scrollTop=e.scrollHeight}
function brl(v){try{return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}catch(e){return 'R$ '+v}}
async function loadImage(src){return new Promise((res,rej)=>{let i=new Image();i.crossOrigin='anonymous';i.onload=()=>res(i);i.onerror=rej;i.src=src})}
async function gerar(d){
let c=document.getElementById('storyCanvas');let ctx=c.getContext('2d');
ctx.fillStyle='#000';ctx.fillRect(0,0,1080,1920);
ctx.fillStyle='#00FF88';ctx.font='900 40px system-ui';ctx.fillText('QUEIMA DE ESTOQUE',50,90);
ctx.fillStyle='#fff';ctx.font='900 58px system-ui';ctx.fillText('SHOPEE 🔥',50,160);
ctx.fillStyle='#fff';ctx.fillRect(40,200,1000,1000);
try{let img=await loadImage(d.image);let sc=Math.min(1000/img.width,1000/img.height);let nw=img.width*sc,nh=img.height*sc;ctx.drawImage(img,40+(1000-nw)/2,200+(1000-nh)/2,nw,nh)}catch(e){}
if(d.preco_atual){ctx.fillStyle='#00FF88';ctx.font='900 70px system-ui';ctx.fillText(brl(d.preco_atual),50,1350)}
}
document.getElementById('go').onclick=async()=>{
let l=document.getElementById('link').value.trim();if(!l){alert('Cole link');return}
document.getElementById('res').classList.remove('hidden');log('Testando link: '+l);
try{
let r=await fetch('/api/resolve?url='+encodeURIComponent(l));let j=await r.json();DADOS=j;
log('=== RESPOSTA REAL DA API SHOPEE ===');
log('Metodo: '+j.metodo);log('Item: '+j.item_id+' Shop: '+j.shop_id);log('Final URL: '+(j.final_url||'').slice(0,100));
log('--- API AFILIADO RAW ---');log(j.api_raw ? JSON.stringify(j.api_raw).slice(0,800) : 'SEM RESPOSTA');
log('--- ERRO API ---');log(j.erro_api||'nenhum');
log('--- PREÇO ---');log('Preço: '+(j.preco_atual||'null')+' Antes: '+(j.preco_antes||'null'));
log('--- FOTO ---');log('Foto: '+(j.image_original||'null').slice(0,120));
log('--- TITULO ---');log(j.title);
if(j.image)await gerar(j);
let legenda=`${j.title}\n\n${j.preco_atual?`💰 POR APENAS: ${brl(j.preco_atual)}`:''}\n\n${j.affiliate_link_original}`;
document.getElementById('msg').textContent=legenda;
}catch(e){log('ERRO JS: '+e.message)}
};
</script></body></html>
"""

def proxy_img(u):
    if not u: return ""
    try:
        return f"https://wsrv.nl/?url={urllib.parse.quote_plus(u)}&output=jpg&w=800&h=800&n=-1"
    except:
        return u

def call_api_debug(item_id, shop_id=None):
    """Testa 3 queries diferentes da API"""
    results = {}
    # Query 1 - productOfferV2 simples (a que usavamos)
    for qname, query in [
        ("productOfferV2_itemId", f"query {{ productOfferV2(itemId: {item_id}, limit: 1) {{ nodes {{ itemId productName imageUrl priceMin priceMax commissionRate }} }} }}"),
        ("productOfferV2_com_shop", f"query {{ productOfferV2(itemId: {item_id}, shopId: {shop_id or 0}, limit: 1) {{ nodes {{ itemId productName imageUrl priceMin priceMax }} }} }}" if shop_id else None),
        ("productOffer", f"query {{ productOffer(itemId: {item_id}) {{ productName imageUrl priceMin priceMax }} }}"),
    ]:
        if not query:
            continue
        try:
            payload = json.dumps({"query": query}, separators=(',', ':'))
            ts = str(int(time.time()))
            sig = hashlib.sha256(f"{APP_ID}{ts}{payload}{SECRET}".encode()).hexdigest()
            auth = f"SHA256 Credential={APP_ID}, Timestamp={ts}, Signature={sig}"
            req = urllib.request.Request(API_URL, data=payload.encode(), headers={"Content-Type":"application/json","Authorization":auth,"User-Agent":"Mozilla/5.0"}, method='POST')
            with urllib.request.urlopen(req, timeout=12) as r:
                body = r.read().decode()
                j = json.loads(body)
                results[qname] = j
                # se encontrou nodes, retorna logo
                nodes = j.get('data',{}).get('productOfferV2',{}).get('nodes',[]) if 'productOfferV2' in query else []
                if nodes:
                    return j, None, results
                if j.get('data',{}).get('productOffer'):
                    return j, None, results
        except Exception as e:
            results[qname+"_erro"] = str(e)[:200]
    return None, "todas_queries_vazias", results

def try_resolve_short(url):
    final_url=url; html=""
    try:
        headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 16_6)","Accept":"text/html","Accept-Language":"pt-BR","Referer":"https://shopee.com.br/"}
        req=urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            final_url=r.geturl(); html=r.read().decode(errors='ignore')[:50000]
            return final_url, html, "direct"
    except Exception as e:
        html=str(e)[:500]
    try:
        api=f"https://api.allorigins.win/get?url={urllib.parse.quote(url)}"
        req=urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            j=json.loads(r.read().decode()); html=j.get('contents','')[:50000]
            m=re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html)
            if m: final_url=m.group(0)
            return final_url, html, "allorigins"
    except:
        pass
    return final_url, html, "fail"

def extract_shop_item(text):
    if not text: return None,None
    m=re.search(r'shopee\.com\.br/[^/]+/(\d+)/(\d+)', text)
    if m: return m.group(1), m.group(2)
    m=re.search(r'-i\.(\d+)\.(\d+)', text)
    if m: return m.group(1), m.group(2)
    return None,None

def parse_html_fallback(html):
    title=None; image=None; price=None
    try:
        m=re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
        if not m: m=re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']', html, re.I)
        if m: title=m.group(1)
        m=re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html, re.I)
        if not m: m=re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html, re.I)
        if m: image=m.group(1)
        ms=re.findall(r'R\$\s*([\d\.,]+)', html)
        vals=[]
        for raw in ms[:10]:
            try:
                if '.' in raw and ',' in raw: v=float(raw.replace('.','').replace(',','.'))
                elif ',' in raw: v=float(raw.replace(',','.'))
                else: v=float(raw)
                if 5<=v<=50000: vals.append(v)
            except: pass
        if vals: price=min(sorted(set(vals)))
    except: pass
    return title,image,price

def resolve_backend(url):
    final_url, html, how = try_resolve_short(url)
    shop_id, item_id = extract_shop_item(final_url+" "+html)
    title="Achadinho Shopee"; image=None; preco=None; preco_antes=None; metodo="fallback"; erro=None; api_raw=None; all_attempts=None

    if item_id:
        api_data, api_err, all_attempts = call_api_debug(item_id, shop_id)
        api_raw = all_attempts
        if api_data:
            # tenta extrair de qualquer query
            data = api_data.get('data',{})
            nodes = data.get('productOfferV2',{}).get('nodes',[]) if 'productOfferV2' in data else []
            offer = data.get('productOffer')
            if nodes:
                n=nodes[0]
                image=n.get('imageUrl')
                title=n.get('productName') or title
                try:
                    pm=n.get('priceMin')
                    if pm:
                        v=float(str(pm).replace(',','.'))
                        preco=v/100000 if v>=100000 else (v/100 if v>1000 else v)
                    px=n.get('priceMax')
                    if px:
                        xf=float(str(px).replace(',','.'))
                        xf=xf/100000 if xf>=100000 else (xf/100 if xf>1000 else xf)
                        if xf and preco and xf>preco:
                            preco_antes=xf
                except:
                    pass
                metodo="API_AFILIADO_OK"
            elif offer:
                image=offer.get('imageUrl')
                title=offer.get('productName') or title
                try:
                    pm=offer.get('priceMin')
                    if pm:
                        v=float(str(pm).replace(',','.'))
                        preco=v/100000 if v>=100000 else (v/100 if v>1000 else v)
                except:
                    pass
                metodo="API_PRODUCT_OFFER_OK"
            else:
                erro=f"API retornou vazio: {str(api_data)[:300]} | Motivo provável: Informações de Pagamento incompletas no painel Shopee Afiliados (banner vermelho no seu print) ou produto fora da janela de comissão"
                metodo="API_VAZIA"
        else:
            erro=f"API erro: {api_err} | Tentativas: {str(all_attempts)[:500]}"
    else:
        erro="Não extraiu item_id/shop_id do link"

    # fallback HTML
    if not image or not preco:
        t,i,p = parse_html_fallback(html)
        if t and title=="Achadinho Shopee": title=t
        if i and not image: image=i
        if p and not preco: preco=p

    img_proxy = proxy_img(image) if image else ""
    return {
        "affiliate_link_original": url,
        "title": title[:150],
        "image": img_proxy,
        "image_original": image,
        "preco_atual": preco,
        "preco_antes": preco_antes,
        "metodo": metodo,
        "erro_api": erro,
        "api_raw": all_attempts,
        "final_url": final_url,
        "item_id": item_id,
        "shop_id": shop_id,
    }

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/resolve')
def api_resolve():
    url=request.args.get('url','')
    return jsonify(resolve_backend(url))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
