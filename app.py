from flask import Flask, request, jsonify, render_template_string
import urllib.request, urllib.parse, re, json, hashlib, time, os

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V25 FIX Fly</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-3 bg-[#050505] text-white"><div class="max-w-[470px] mx-auto">
<div class="bg-gradient-to-br from-zinc-900 to-black border border-zinc-800 rounded-[28px] p-6 shadow-2xl">
<div class="flex justify-between"><span class="bg-[#00ff88] text-black text-[11px] px-4 py-2 rounded-full font-black">V25 FLY FIX ✅</span><span class="text-[10px] bg-white text-black px-2 py-1 rounded-full font-black">FUNCIONA</span></div>
<h1 class="font-black text-[19px] mt-4">FIX FLY - QUALQUER LINK!</h1>
<div class="text-[11px] text-zinc-400">Mensagem específica correta pra qualquer produto!</div>

<div class="mt-5 space-y-3">
<div class="bg-[#25D366]/10 border-2 border-[#25D366] rounded-2xl p-4">
<label class="text-[11px] font-bold text-[#25D366]">🔗 LINK DO SEU GRUPO:</label>
<input id="grupoLink" placeholder="https://chat.whatsapp.com/XXXX" class="w-full mt-2 bg-black border-2 border-[#25D366] rounded-2xl p-4 text-white font-bold text-[13px]">
<div id="grupoOk" class="hidden mt-2 bg-[#25D366] text-black text-[10px] px-3 py-1 rounded-full font-black">✅ Grupo conectado!</div>
</div>

<div class="relative">
<label class="text-[11px] font-bold text-[#E1306C]">📸 Seu Instagram:</label>
<input id="meuInsta" value="@filipe_ferreira12" class="w-full mt-1 bg-black border-2 border-[#E1306C] rounded-2xl p-4 text-white font-black text-[14px]">
</div>

<div class="bg-[#25D366] text-black rounded-2xl p-3 flex items-center gap-3">
<input type="checkbox" id="autoGrupo" checked class="w-5 h-5"><span class="text-[12px] font-black">✅ Mensagem automática pro grupo</span>
</div>

<div class="relative">
<label class="text-[12px] font-black text-white">🔗 COLE QUALQUER LINK SHOPEE:</label>
<input id="link" placeholder="https://s.shopee.com.br/XXXX" class="w-full mt-2 bg-white text-black border-4 border-[#ff0080] rounded-2xl p-5 text-[15px] font-black outline-none">
<div id="status" class="hidden mt-3 p-3 bg-[#00ff88] text-black rounded-xl text-[11px] font-black"></div>
<div id="errorMsg" class="hidden mt-2 p-3 bg-red-500 text-white rounded-xl text-[11px] font-bold"></div>
</div>
</div>
</div>

<div id="res" class="hidden">
<div class="bg-zinc-900 border-2 border-[#ff0080] rounded-[28px] p-4 mt-6">
<div class="flex justify-between mb-4"><span class="font-black text-[13px]">🖼️ ARTE</span><button onclick="baixarFix('storyCanvas','STORY.png')" class="bg-gradient-to-r from-[#ff0080] to-[#ff6a00] text-white px-4 py-2 rounded-full text-[11px] font-black">⬇️ BAIXAR</button></div>
<canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-2xl"></canvas>
</div>

<div class="bg-gradient-to-br from-[#075E54] to-[#128C7E] border-2 border-[#25D366] rounded-[28px] p-5 mt-5">
<div class="flex justify-between items-center mb-2"><span class="text-[11px] font-black text-white/80">💬 MENSAGEM ÚNICA:</span><span id="tipoDetectado" class="text-[10px] bg-[#ff0080] text-white px-3 py-1 rounded-full font-black"></span></div>
<div id="msg" class="bg-black/40 rounded-2xl p-4 text-[14px] whitespace-pre-wrap text-white border border-white/20"></div>
<div id="grupoStatus" class="mt-3 bg-black text-white p-3 rounded-xl text-[12px] font-bold text-center border border-[#25D366]">Pronto!</div>
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

function brl(v){ if(!v || isNaN(v) || v==0) return 'VER PREÇO NO LINK'; return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
async function loadImage(src){return new Promise((res,rej)=>{let i=new Image();i.crossOrigin='anonymous';i.onload=()=>res(i);i.onerror=()=>rej();i.src=src})}

function gerarMensagemUnicaPorProduto(titulo, preco, precoAntes, desconto, link, insta){
let t = titulo.toLowerCase();
let precoTxt = brl(preco);
let economiaTxt = desconto>0 ? ` (De ${brl(precoAntes)} por ${precoTxt} - ${desconto}% OFF!)` : '';
let tipo = '';
let msg = '';

function tem(palavra){ 
if(palavra==='ração'){ return t.includes(' ração ') || t.includes(' ração para') || t.startsWith('ração ') || (t.includes('ração') && (t.includes('cachorro') || t.includes('gato') || t.includes(' pet') || t.includes(' cães'))); }
if(palavra==='pet'){ return t.includes(' pet ') || t.includes(' para pet') || t.startsWith('pet ') || t.includes(' coleira pet'); }
return t.includes(palavra);
}

if(tem('yamasterol') || tem('yamá') || tem('cronograma') || tem('cabelo') || tem('hidratação') || tem('nutrição') || tem('reconstrução') || tem('argan') || tem('babosa') || tem('proteína hidrolisada') || tem('creme multifuncional') || tem('todos os tipos de cabelos')){
tipo='💇‍♀️ CABELO';
msg=`💇‍♀️ CABELO DE SALÃO EM CASA - RESULTADO PROFISSIONAL!

Seu cabelo ressecado, sem vida e com frizz? Acabou!

📦 ${titulo.toUpperCase()}

✨ KIT YAMASTEROL - O QUERIDINHO DAS BLOGUEIRAS!

${tem('argan') ? '✅ ARGAN - nutrição intensa, fim do ressecamento\\n' : ''}${tem('babosa') ? '✅ BABOSA - hidratação profunda e brilho espelhado\\n' : ''}${tem('proteína') ? '✅ PROTEÍNA HIDROLISADA - reconstrução e força total\\n' : ''}✅ Cronograma completo - 3 etapas que seu cabelo precisa
💖 Serve pra TODOS os tipos: liso, cacheado, crespo!

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

💇‍♀️ Kit 3 por preço de 1 - cabelo lindo não pode esperar!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('vonixx') || tem('pretinho') && tem('pneu') || tem('sintra') || tem('tok final') || tem('lavagem automotiva')){
tipo='🚗 CARRO';
msg=`🚗 SEU CARRO VAI BRILHAR IGUAL CARRO ZERO!

📦 ${titulo.toUpperCase()}

💎 KIT PROFISSIONAL VONIXX!

✅ Shampoo super concentrado - limpa sem agredir
✅ Cera Tok Final - brilho que dura semanas
✅ Sintra Fast - limpa interior sem esforço
✅ Pneu Pretinho que NÃO espirra

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

🏆 Quem ama carro não perde!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('mop') || tem('vassoura mágica') || tem('esfregão')){
tipo='🏠 CASA';
msg=`🏠 SUA CASA LIMPA EM METADE DO TEMPO!

📦 ${titulo.toUpperCase()}

✨ PRATICIDADE QUE TODA DONA DE CASA SONHA!

✅ Limpeza 3x mais rápida
✅ Alcança cantos difíceis
✅ Material premium que dura anos

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

🔥 Casa limpa = mente tranquila!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('air fryer') || tem('fritadeira') || tem('panela') && tem('antiaderente') || tem('liquidificador')){
tipo='🍳 COZINHA';
msg=`🍳 SUA COZINHA VAI VIRAR DE CHEF!

📦 ${titulo.toUpperCase()}

👨‍🍳 QUALIDADE PROFISSIONAL!

✅ Cozinha mais rápido
✅ Comida mais saborosa
✅ Fácil de limpar

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

⏰ Promoção de cozinha acaba rápido!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('fone de ouvido') || tem('smartwatch') || tem('caixa de som') || tem('jbl')){
tipo='🎧 ELETRÔNICOS';
msg=`🎧 TECNOLOGIA PREMIUM QUE VOCÊ SENTE NA HORA!

📦 ${titulo.toUpperCase()}

⚡ QUALIDADE QUE IMPRESSIONA!

✅ Som cristalino
✅ Bateria que dura o dia todo
✅ Conexão instantânea

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

📱 Eletrônico bom nesse preço some rápido!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('furadeira') || tem('parafusadeira') || tem('kit ferramentas')){
tipo='🔧 FERRAMENTAS';
msg=`🔧 FERRAMENTA QUE TODO HOMEM PRECISA!

📦 ${titulo.toUpperCase()}

💪 POTÊNCIA PROFISSIONAL!

✅ Motor potente
✅ Bateria de longa duração
✅ Resolve tudo sozinho

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

🛠️ Ferramenta boa nesse preço é achado!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('tênis') || tem('tenis') || tem('camiseta') || tem('camisa') || tem('bermuda')){
tipo='👕 MODA';
msg=`👕 ESTILO QUE CHAMA ATENÇÃO!

📦 ${titulo.toUpperCase()}

🔥 ESTILO E CONFORTO!

✅ Tecido premium - não desbota
✅ Caimento perfeito
✅ Confortável o dia todo

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

👟 Numeração acaba rápido!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else if(tem('pet') || tem('cachorro') || (tem('ração') && (tem('cachorro') || tem('gato')))){
tipo='🐶 PET';
msg=`🐶 SEU PET MERECE O MELHOR!

📦 ${titulo.toUpperCase()}

❤️ SEU PET MAIS FELIZ!

✅ Material 100% seguro
✅ Super confortável
✅ Resistente

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

🐕 Produto pet de qualidade some rápido!

⏰ OFERTA POR TEMPO LIMITADO!`;

}else{
tipo='🔥 OFERTA';
msg=`🔥 ACHADINHO IMPERDÍVEL!

📦 ${titulo.toUpperCase()}

⭐ PRODUTO CAMPEÃO DE VENDAS!

✅ Qualidade garantida Shopee
✅ Milhares de avaliações 5 estrelas
✅ Entrega rápida
✅ Preço de promoção

💥 POR APENAS: ${precoTxt}${economiaTxt}

📸 Instagram: ${insta}

👇 LINK COM DESCONTO 👇
${link}

⏰ Promoção relâmpago - pode acabar a qualquer momento!

⏰ OFERTA POR TEMPO LIMITADO!`;
}

return {msg, tipo};
}

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
if(d.image){ try{let img=await loadImage(d.image);let sc=Math.min(980/img.width,980/img.height);let nw=img.width*sc,nh=img.height*sc;ctx1.drawImage(img,20+(1040-nw)/2,160+(1040-nh)/2,nw,nh)}catch(e){} }
ctx1.fillStyle='#000';ctx1.strokeStyle='#00ff88';ctx1.lineWidth=6;ctx1.beginPath();ctx1.roundRect(20,1220,1040,580,30);ctx1.fill();ctx1.stroke();
ctx1.fillStyle='#fff';ctx1.font='900 32px system-ui';ctx1.fillText(titulo.slice(0,38).toUpperCase(),50,1290);
if(preco && preco>0){ctx1.fillStyle='#00ff88';ctx1.font='900 88px system-ui';ctx1.fillText(brl(preco),50,1430);if(precoAntes&&desconto>0){ctx1.fillStyle='#ff6a00';ctx1.font='600 28px system-ui';ctx1.fillText(`DE ${brl(precoAntes)}`,50,1470)}}
ctx1.fillStyle='#fff';ctx1.font='900 24px system-ui';ctx1.textAlign='center';ctx1.fillText('⚡ SHOPEE OFICIAL • '+instaHandle+' • OFERTA NO GRUPO ⚡',540,1860);ctx1.textAlign='left';
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
if(l.indexOf('shopee.com.br')==-1 && l.indexOf('s.shopee')==-1){document.getElementById('errorMsg').classList.remove('hidden'); document.getElementById('errorMsg').textContent='❌ Link precisa ser da Shopee!'; return;}
let insta=document.getElementById('meuInsta').value.trim();
if(insta) localStorage.setItem('meuInstaHandle',insta);
document.getElementById('status').classList.remove('hidden');
document.getElementById('status').textContent='🧠 Analisando produto e criando mensagem específica...';
document.getElementById('errorMsg').classList.add('hidden');
document.getElementById('res').classList.remove('hidden');
try{
let r=await fetch('/api/resolve?url='+encodeURIComponent(l));
if(!r.ok) throw new Error('Erro API');
let j=await r.json();
if(!j || !j.title) throw new Error('Produto não encontrado');
let instaTxt=document.getElementById('meuInsta').value.trim()||'@filipe_ferreira12';
let resultado = gerarMensagemUnicaPorProduto(j.title, j.preco_atual, j.preco_antes, j.desconto, j.affiliate_link_original, instaTxt);
document.getElementById('msg').textContent=resultado.msg;
document.getElementById('tipoDetectado').textContent=resultado.tipo;
document.getElementById('status').textContent='⚡ Gerando arte...';
await gerarComInsta(j);
document.getElementById('status').classList.add('hidden');
document.getElementById('grupoStatus').textContent='✅ Mensagem específica correta!';
if(document.getElementById('autoGrupo').checked){setTimeout(()=>{enviarGrupoManual();},500);}
}catch(e){
document.getElementById('status').classList.add('hidden');
document.getElementById('errorMsg').classList.remove('hidden');
document.getElementById('errorMsg').textContent='❌ Erro: '+e.message;
}
}
document.getElementById('link').addEventListener('paste',(e)=>{setTimeout(()=>{processarLinkAuto();},200);});
document.getElementById('link').addEventListener('input',(e)=>{clearTimeout(timeoutAuto);timeoutAuto=setTimeout(()=>{processarLinkAuto();},500);});

async function enviarGrupoManual(){
let grupoLink=document.getElementById('grupoLink').value.trim()||localStorage.getItem('grupoLink');
let msg=document.getElementById('msg').textContent;
if(!grupoLink){document.getElementById('grupoStatus').textContent='❌ Cole o link do grupo!'; return}
if(!msg){document.getElementById('grupoStatus').textContent='❌ Cole link Shopee!'; return}
document.getElementById('grupoStatus').textContent='🚀 Copiando mensagem específica...';
try{await navigator.clipboard.writeText(msg);}catch(e){}
document.getElementById('grupoStatus').innerHTML='✅ Mensagem específica copiada! Abrindo grupo...';
setTimeout(()=>{window.open(grupoLink,'_blank'); setTimeout(()=>{document.getElementById('grupoStatus').innerHTML='✅ Pronto! Mensagem 100% específica!<br>Qualquer link funciona!';},600);},400);
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
    try:
        headers={"User-Agent":"Mozilla/5.0 (iPhone)","Accept":"text/html","Accept-Language":"pt-BR","Referer":"https://shopee.com.br/"}
        req=urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            final_url=r.geturl(); html=r.read().decode(errors='ignore')[:30000]
            if 'shopee.com.br' in final_url: return final_url, html, "direct"
    except: pass
    try:
        api=f"https://api.allorigins.win/get?url={urllib.parse.quote(url)}"
        req=urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            j=json.loads(r.read().decode()); html_content=j.get('contents','')[:30000]
            m=re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html_content)
            if m: final_url=m.group(0)
            html=html_content
            if 'shopee.com.br' in final_url: return final_url, html, "allorigins"
    except: pass
    try:
        api=f"https://corsproxy.io/?{urllib.parse.quote(url)}"
        req=urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            html=r.read().decode(errors='ignore')[:30000]
            m=re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html)
            if m: final_url=m.group(0)
            if 'shopee.com.br' in final_url: return final_url, html, "corsproxy"
    except: pass
    return final_url, html, "fail"

def extract_shop_item(text):
    if not text: return None,None
    m=re.search(r'shopee\.com\.br/[^/]+/(\d+)/(\d+)', text)
    if m: return m.group(1), m.group(2)
    m=re.search(r'-i\.(\d+)\.(\d+)', text)
    if m: return m.group(1), m.group(2)
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
    img_proxy=proxy_img(image) if image else "https://via.placeholder.com/800x800.png?text=SHOPEE"
    desconto=0
    if preco_antes and preco and preco_antes>preco:
        try: desconto=round((1-preco/preco_antes)*100)
        except: pass
    return {"affiliate_link_original":url,"title":title[:150],"image":img_proxy,"image_original":image,"preco_atual":preco or 0,"preco_antes":preco_antes,"desconto":desconto,"comissao":comissao,"metodo":metodo,"final_url":final_url,"item_id":item_id,"shop_id":shop_id, "html_snippet": html[:2000]}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/resolve')
def api_resolve():
    url=request.args.get('url','')
    if not url: return jsonify({"error":"sem url"}), 400
    return jsonify(resolve_backend(url))

# === NOVA ROTA PARA SUA VERCEL USAR - NÃO QUEBRA NADA DO QUE JÁ EXISTE ===
@app.route('/expand')
def expand_for_vercel():
    url = request.args.get('url','')
    if not url:
        return jsonify({"ok": False, "error": "url vazia"}), 400
    
    data = resolve_backend(url)
    
    # Formato que a Vercel espera
    return jsonify({
        "ok": True,
        "original": data.get("affiliate_link_original"),
        "expanded": data.get("final_url"),
        "shopId": data.get("shop_id"),
        "itemId": data.get("item_id"),
        "ogTitle": data.get("title"),
        "ogImage": data.get("image_original") or data.get("image"),
        "title": data.get("title"),
        "image": data.get("image_original"),
        "image_proxy": data.get("image"),
        "preco_atual": data.get("preco_atual"),
        "preco_antes": data.get("preco_antes"),
        "desconto": data.get("desconto"),
        "affiliate_link_original": data.get("affiliate_link_original"),
        "final_url": data.get("final_url"),
        "region": "gru",
        "via": "seu robo Fly - IP brasileiro",
        "message": "Expandido no seu robo Fly GRU - IP brasileiro nao bloqueado"
    })

@app.route('/health')
def health():
    return jsonify({"status":"ok", "routes": ["/", "/api/resolve", "/expand", "/health"]})

if __name__=='__main__':
    port = int(os.environ.get('PORT',8080))
    app.run(host='0.0.0.0', port=port)
