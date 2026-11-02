from flask import Flask, request, jsonify, render_template_string
import urllib.request, urllib.parse, re, json, hashlib, time, os

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"
app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V19 - FIX Imagem e Mensagem</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-3 bg-[#050505] text-white"><div class="max-w-[470px] mx-auto">
<div class="bg-gradient-to-br from-zinc-900 to-black border border-zinc-800 rounded-[28px] p-6 shadow-2xl">
<div class="flex justify-between"><span class="bg-[#00ff88] text-black text-[11px] px-4 py-2 rounded-full font-black">V19 FIX TOTAL ✅</span><span class="text-[10px] bg-white text-black px-2 py-1 rounded-full font-black">CORRIGIDO</span></div>
<h1 class="font-black text-[20px] mt-4">VOLTOU A FUNCIONAR!</h1>
<div class="text-[11px] text-zinc-400">Imagem + mensagem automática pro grupo!</div>

<div class="mt-5 space-y-3">
<div class="bg-[#25D366]/10 border-2 border-[#25D366] rounded-2xl p-4">
<label class="text-[11px] font-bold text-[#25D366]">🔗 LINK DO SEU GRUPO:</label>
<input id="grupoLink" placeholder="https://chat.whatsapp.com/XXXX" class="w-full mt-2 bg-black border-2 border-[#25D366] rounded-2xl p-4 text-white font-bold text-[13px]">
<div id="grupoOk" class="hidden mt-2 bg-[#25D366] text-black text-[10px] px-3 py-1 rounded-full font-black">✅ Grupo conectado!</div>
<div class="text-[9px] text-zinc-400 mt-1">Ex: https://chat.whatsapp.com/DofBN3bkc0klgc...</div>
</div>

<div class="relative">
<label class="text-[11px] font-bold text-[#E1306C]">📸 Seu Instagram:</label>
<input id="meuInsta" value="@filipe_ferreira12" class="w-full mt-1 bg-black border-2 border-[#E1306C] rounded-2xl p-4 text-white font-black text-[14px]">
</div>

<div class="bg-[#25D366] text-black rounded-2xl p-3 flex items-center gap-3">
<input type="checkbox" id="autoGrupo" checked class="w-5 h-5"><span class="text-[12px] font-black">✅ Enviar mensagem automática pro grupo</span>
</div>

<div class="relative">
<label class="text-[12px] font-black text-white">🔗 COLE LINK SHOPEE AQUI:</label>
<input id="link" placeholder="https://s.shopee.com.br/XXXX" class="w-full mt-2 bg-white text-black border-4 border-[#ff0080] rounded-2xl p-5 text-[15px] font-black outline-none">
<div id="status" class="hidden mt-3 p-3 bg-[#00ff88] text-black rounded-xl text-[11px] font-black">⚡ Gerando...</div>
<div id="errorMsg" class="hidden mt-2 p-3 bg-red-500 text-white rounded-xl text-[11px] font-bold"></div>
</div>
</div>
</div>

<div id="res" class="hidden">
<div class="bg-zinc-900 border-2 border-[#ff0080] rounded-[28px] p-4 mt-6">
<div class="flex justify-between mb-4"><span class="font-black text-[13px]">🖼️ SUA ARTE (baixa se quiser)</span><button onclick="baixarFix('storyCanvas','STORY.png')" class="bg-gradient-to-r from-[#ff0080] to-[#ff6a00] text-white px-4 py-2 rounded-full text-[11px] font-black">⬇️ BAIXAR</button></div>
<canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-2xl"></canvas>
</div>

<div class="bg-gradient-to-br from-[#075E54] to-[#128C7E] border-2 border-[#25D366] rounded-[28px] p-5 mt-5">
<div class="text-[11px] font-black text-white/80 mb-2">💬 MENSAGEM AUTOMÁTICA:</div>
<div id="msg" class="bg-black/40 rounded-2xl p-4 text-[14px] whitespace-pre-wrap text-white border border-white/20"></div>
<div id="grupoStatus" class="mt-3 bg-black text-white p-3 rounded-xl text-[12px] font-bold text-center border border-[#25D366]">Pronto pra enviar pro grupo!</div>
<div class="grid grid-cols-2 gap-2 mt-3">
<button onclick="enviarGrupoManual()" class="bg-[#25D366] border-2 border-white text-white p-4 rounded-2xl font-black text-[13px]">📲 ENVIAR PRO GRUPO</button>
<button onclick="copiar()" class="bg-white text-black p-3 rounded-2xl font-black text-[13px]">📋 COPIAR</button>
</div>
</div>
</div>
</div>

<script>
let savedInsta = localStorage.getItem('meuInstaHandle'); if(savedInsta) document.getElementById('meuInsta').value=savedInsta;
let savedGrupo = localStorage.getItem('grupoLink'); if(savedGrupo) {document.getElementById('grupoLink').value=savedGrupo; document.getElementById('grupoOk').classList.remove('hidden');}

document.getElementById('meuInsta').addEventListener('input',(e)=>{localStorage.setItem('meuInstaHandle',e.target.value)});
document.getElementById('grupoLink').addEventListener('input',(e)=>{
localStorage.setItem('grupoLink',e.target.value);
if(e.target.value.includes('chat.whatsapp.com')) document.getElementById('grupoOk').classList.remove('hidden');
});

function brl(v){ if(!v || isNaN(v)) return 'VER PREÇO NO LINK'; return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
async function loadImage(src){return new Promise((res,rej)=>{let i=new Image();i.crossOrigin='anonymous';i.onload=()=>res(i);i.onerror=()=>rej();i.src=src})}

async function gerarComInsta(d){
let preco=d.preco_atual;let precoAntes=d.preco_antes;let desconto=d.desconto||0;let titulo=d.title||'ACHADINHO SHOPEE';
let instaHandle=document.getElementById('meuInsta').value.trim()||'@filipe_ferreira12';
if(!instaHandle.startsWith('@')) instaHandle='@'+instaHandle;
let c1=document.getElementById('storyCanvas');let ctx1=c1.getContext('2d');
let g=ctx1.createLinearGradient(0,0,0,1920);g.addColorStop(0,'#ff0080');g.addColorStop(0.3,'#ff6a00');g.addColorStop(0.6,'#1a1a1a');g.addColorStop(1,'#000');ctx1.fillStyle=g;ctx1.fillRect(0,0,1080,1920);
ctx1.fillStyle='#000';ctx1.fillRect(0,0,1080,140);
ctx1.fillStyle='#fff';ctx1.font='700 22px system-ui';ctx1.textAlign='right';ctx1.fillText('📸 '+instaHandle,1040,45);ctx1.textAlign='left';
ctx1.fillStyle='#ffcc00';ctx1.font='900 36px system-ui';ctx1.fillText('⚠️  ATENÇÃO  ⚠️',40,55);
ctx1.fillStyle='#fff';ctx1.font='900 50px system-ui';ctx1.fillText('QUEIMA DE ESTOQUE',40,110);
if(desconto>0){ctx1.save();ctx1.translate(850,200);ctx1.rotate(-15*Math.PI/180);ctx1.fillStyle='#ffcc00';ctx1.beginPath();ctx1.arc(0,0,100,0,Math.PI*2);ctx1.fill();ctx1.fillStyle='#000';ctx1.font='900 44px system-ui';ctx1.textAlign='center';ctx1.fillText(`-${desconto}%`,0,12);ctx1.restore();ctx1.textAlign='left'}
ctx1.fillStyle='#fff';ctx1.beginPath();ctx1.roundRect(20,160,1040,1040,30);ctx1.fill();
if(d.image){ try{let img=await loadImage(d.image);let sc=Math.min(980/img.width,980/img.height);let nw=img.width*sc,nh=img.height*sc;ctx1.drawImage(img,20+(1040-nw)/2,160+(1040-nh)/2,nw,nh)}catch(e){ ctx1.fillStyle='#000';ctx1.font='900 30px system-ui';ctx1.fillText('FOTO DO PRODUTO', 350, 700);} }
ctx1.fillStyle='#000';ctx1.strokeStyle='#00ff88';ctx1.lineWidth=6;ctx1.beginPath();ctx1.roundRect(20,1220,1040,450,30);ctx1.fill();ctx1.stroke();
ctx1.fillStyle='#fff';ctx1.font='900 32px system-ui';let t=titulo.slice(0,36).toUpperCase();ctx1.fillText(t,50,1280);
if(preco){ctx1.fillStyle='#00ff88';ctx1.font='900 80px system-ui';ctx1.fillText(brl(preco),50,1410);if(precoAntes&&desconto>0){ctx1.fillStyle='#ff6a00';ctx1.font='600 26px system-ui';ctx1.fillText(`DE ${brl(precoAntes)}`,50,1440)}}
ctx1.fillStyle='#ffcc00';ctx1.beginPath();ctx1.roundRect(20,1690,1040,110,20);ctx1.fill();ctx1.fillStyle='#000';ctx1.font='900 34px system-ui';ctx1.textAlign='center';ctx1.fillText('👇 LINK NA BIO - CORRE! 👇',540,1760);ctx1.textAlign='left';
ctx1.fillStyle='#fff';ctx1.font='900 22px system-ui';ctx1.textAlign='center';ctx1.fillText('⚡ SHOPEE OFICIAL • '+instaHandle+' ⚡',540,1860);ctx1.textAlign='left';
}

function baixarFix(canvasId, nomeArquivo){
try{
let canvas = document.getElementById(canvasId);
canvas.toBlob(function(blob){let url = URL.createObjectURL(blob);let a = document.createElement('a');a.href=url;a.download=nomeArquivo;document.body.appendChild(a);a.click();setTimeout(()=>{document.body.removeChild(a);URL.revokeObjectURL(url);},100);},'image/png',1.0);
}catch(e){}
}

let timeoutAuto=null;
async function processarLinkAuto(){
let l=document.getElementById('link').value.trim();
if(!l || l.length<10) return;
if(l.indexOf('shopee.com.br')==-1 && l.indexOf('s.shopee')==-1){document.getElementById('errorMsg').classList.remove('hidden'); document.getElementById('errorMsg').textContent='❌ Link precisa ser da Shopee! Ex: https://s.shopee.com.br/XXXX'; return;}
let insta=document.getElementById('meuInsta').value.trim();
if(insta) localStorage.setItem('meuInstaHandle',insta);
document.getElementById('status').classList.remove('hidden');
document.getElementById('status').textContent='⚡ Resolvendo link curto s.shopee...';
document.getElementById('errorMsg').classList.add('hidden');
document.getElementById('res').classList.remove('hidden');
try{
document.getElementById('status').textContent='⚡ Buscando produto na Shopee...';
let r=await fetch('/api/resolve?url='+encodeURIComponent(l));
if(!r.ok) throw new Error('Erro API: '+r.status);
let j=await r.json();
console.log('Dados recebidos:', j);
if(!j || !j.title){throw new Error('Produto não encontrado - tente outro link');}
document.getElementById('status').textContent='⚡ Gerando arte...';
await gerarComInsta(j);
let instaTxt=document.getElementById('meuInsta').value.trim()||'@filipe_ferreira12';
let legenda=`🔥 SUPER OFERTA RELÂMPAGO 🔥

📦 ${j.title.toUpperCase()}

💥 POR APENAS: ${brl(j.preco_atual)}
${j.desconto>0?`⚡ ${j.desconto}% OFF - De ${brl(j.preco_antes)} por ${brl(j.preco_atual)}`:''}

📸 Instagram: ${instaTxt}

👇 LINK COM DESCONTO 👇
${j.affiliate_link_original}

⏰ OFERTA POR TEMPO LIMITADO!

#achadinhos #shopee #oferta`;
document.getElementById('msg').textContent=legenda;
document.getElementById('status').classList.add('hidden');
document.getElementById('grupoStatus').textContent='✅ Pronto! Imagem + mensagem geradas!';

if(document.getElementById('autoGrupo').checked){
setTimeout(()=>{enviarGrupoManual();},800);
}

}catch(e){
console.error(e);
document.getElementById('status').classList.add('hidden');
document.getElementById('errorMsg').classList.remove('hidden');
document.getElementById('errorMsg').textContent='❌ Erro: '+e.message+' - Tente novamente ou outro link';
document.getElementById('grupoStatus').textContent='❌ Erro ao gerar - tente outro link';
}
}
document.getElementById('link').addEventListener('paste',(e)=>{setTimeout(()=>{processarLinkAuto();},300);});
document.getElementById('link').addEventListener('input',(e)=>{clearTimeout(timeoutAuto);timeoutAuto=setTimeout(()=>{processarLinkAuto();},1000);});

async function enviarGrupoManual(){
let grupoLink=document.getElementById('grupoLink').value.trim();
let msg=document.getElementById('msg').textContent;
if(!grupoLink){
let salvo=localStorage.getItem('grupoLink');
if(salvo) grupoLink=salvo; else {document.getElementById('grupoStatus').textContent='❌ Cole o link do grupo primeiro!'; return}
}
if(!msg){document.getElementById('grupoStatus').textContent='❌ Cole o link Shopee primeiro!'; return}
document.getElementById('grupoStatus').textContent='🚀 Copiando mensagem automática...';
try{await navigator.clipboard.writeText(msg);}catch(e){}
document.getElementById('grupoStatus').innerHTML='✅ Mensagem copiada!<br>Abrindo seu grupo...';
setTimeout(()=>{
window.open(grupoLink,'_blank');
setTimeout(()=>{document.getElementById('grupoStatus').innerHTML='✅ <b>MENSAGEM AUTOMÁTICA PRONTA!</b><br>👉 Grupo aberto! Só colar a mensagem!<br><br>🖼️ Imagem só baixa se clicar em ⬇️ Baixar';},600);
},500);
}

function copiar(){navigator.clipboard.writeText(document.getElementById('msg').textContent); document.getElementById('grupoStatus').textContent='📋 Mensagem copiada! ✅'}
</script></body></html>
"""

def proxy_img(u):
    if not u: return ""
    try: return f"https://wsrv.nl/?url={urllib.parse.quote_plus(u)}&output=jpg&w=800&h=800&n=-1"
    except: return u

def parse_price_correctly(v):
    if v is None: return None
    try:
        s=str(v).strip()
        if '.' in s: return float(s)
        else:
            f=float(s)
            return f/100000 if f>=100000 else (f/100 if f>=10000 else f)
    except: return None

def call_api_final(item_id):
    try:
        query = f"query {{ productOfferV2(itemId: {item_id}, limit: 1) {{ nodes {{ itemId productName imageUrl priceMin priceMax commissionRate }} }} }}"
        payload = json.dumps({"query": query}, separators=(',', ':'))
        ts = str(int(time.time()))
        sig = hashlib.sha256(f"{APP_ID}{ts}{payload}{SECRET}".encode()).hexdigest()
        auth = f"SHA256 Credential={APP_ID}, Timestamp={ts}, Signature={sig}"
        req = urllib.request.Request(API_URL, data=payload.encode(), headers={"Content-Type":"application/json","Authorization":auth,"User-Agent":"Mozilla/5.0"}, method='POST')
        with urllib.request.urlopen(req, timeout=15) as r:
            j=json.loads(r.read().decode())
            nodes=j.get('data',{}).get('productOfferV2',{}).get('nodes',[])
            if nodes:
                n=nodes[0]
                preco=parse_price_correctly(n.get('priceMin'))
                preco_max=parse_price_correctly(n.get('priceMax'))
                preco_antes=preco_max if (preco_max and preco and preco_max>preco) else None
                try: comm=float(n.get('commissionRate','0'))
                except: comm=0
                return {"title":n.get('productName'),"image":n.get('imageUrl'),"preco":preco,"preco_antes":preco_antes,"comissao":comm}, None
            else: return None, "vazio"
    except Exception as e: return None, str(e)[:200]

def try_resolve_short(url):
    final_url=url; html=""
    # 1 - Direto
    try:
        headers={"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15","Accept":"text/html,application/xhtml+xml","Accept-Language":"pt-BR,pt;q=0.9","Referer":"https://shopee.com.br/"}
        req=urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            final_url=r.geturl(); html=r.read().decode(errors='ignore')[:30000]
            if 'shopee.com.br' in final_url and ('-i.' in final_url or '/-/' not in final_url or 'item' in html.lower()):
                return final_url, html, "direct"
    except: pass
    # 2 - AllOrigins
    try:
        api=f"https://api.allorigins.win/get?url={urllib.parse.quote(url)}"
        req=urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            j=json.loads(r.read().decode()); html_content=j.get('contents','')[:30000]
            m=re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html_content)
            if m: final_url=m.group(0)
            html=html_content
            if 'shopee.com.br' in final_url:
                return final_url, html, "allorigins"
    except: pass
    # 3 - CorsProxy
    try:
        api=f"https://corsproxy.io/?{urllib.parse.quote(url)}"
        req=urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            html=r.read().decode(errors='ignore')[:30000]
            m=re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html)
            if m: final_url=m.group(0)
            if 'shopee.com.br' in final_url:
                return final_url, html, "corsproxy"
    except: pass
    return final_url, html, "fail"

def extract_shop_item(text):
    if not text: return None,None
    # tenta vários padrões
    m=re.search(r'shopee\.com\.br/[^/]+/(\d+)/(\d+)', text)
    if m: return m.group(1), m.group(2)
    m=re.search(r'-i\.(\d+)\.(\d+)(?:\?|$|")', text)
    if m: return m.group(1), m.group(2)
    m=re.search(r'"shopid":\s*(\d+)[^}]*"itemid":\s*(\d+)', text)
    if m: return m.group(1), m.group(2)
    m=re.search(r'itemid["\']?\s*[:=]\s*["\']?(\d+)', text, re.I)
    if m: 
        shop=re.search(r'shopid["\']?\s*[:=]\s*["\']?(\d+)', text, re.I)
        if shop: return shop.group(1), m.group(1)
    return None,None

def resolve_backend(url):
    final_url, html, how = try_resolve_short(url)
    shop_id, item_id = extract_shop_item(final_url+" "+html)
    title="Achadinho Shopee"; image=None; preco=None; preco_antes=None; metodo=f"API_OK_{how}"; comissao=None
    if item_id:
        res,_ = call_api_final(item_id)
        if res:
            title=res.get('title') or title
            image=res.get('image')
            preco=res.get('preco')
            preco_antes=res.get('preco_antes')
            comissao=res.get('comissao')
    # fallback se não achou item_id mas tem html tenta pegar imagem titulo
    if not image and html:
        m=re.search(r'"imageUrl"\s*:\s*"([^"]+)"', html)
        if m: image=m.group(1)
    img_proxy=proxy_img(image) if image else "https://via.placeholder.com/800x800.png?text=SHOPEE"
    desconto=0
    if preco_antes and preco and preco_antes>preco:
        try: desconto=round((1-preco/preco_antes)*100)
        except: pass
    return {"affiliate_link_original":url,"title":title[:150],"image":img_proxy,"image_original":image,"preco_atual":preco or 0,"preco_antes":preco_antes,"desconto":desconto,"comissao":comissao,"metodo":metodo,"final_url":final_url,"item_id":item_id,"shop_id":shop_id,"debug_how":how}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/resolve')
def api_resolve():
    url=request.args.get('url','')
    if not url: return jsonify({"error":"sem url"}), 400
    return jsonify(resolve_backend(url))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
