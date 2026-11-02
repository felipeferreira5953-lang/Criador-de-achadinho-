from flask import Flask, request, jsonify, render_template_string
import urllib.request, urllib.parse, re, json, hashlib, time, os, base64

APP_ID = "18325950432"
SECRET = "O25HE4WDN6GGDCII4DUFFCZ7RDEHHGM6"
API_URL = "https://open-api.affiliate.shopee.com.br/graphql"
app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V16 - Grupo WhatsApp Auto</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="p-3 bg-[#050505] text-white"><div class="max-w-[470px] mx-auto">
<div class="bg-gradient-to-br from-zinc-900 to-black border border-zinc-800 rounded-[28px] p-6 shadow-2xl">
<div class="flex justify-between items-center"><span class="bg-gradient-to-r from-[#25D366] to-[#128C7E] text-white text-[11px] px-4 py-2 rounded-full font-black">V16 GRUPO AUTO 📲</span><span class="text-[10px] bg-white text-black px-2 py-1 rounded-full font-black">NOVO</span></div>
<h1 class="font-black text-[22px] mt-4">ENVIO AUTOMÁTICO PRO GRUPO</h1>
<div class="text-[11px] text-zinc-400">Conecta seu grupo e envia sozinho ao criar!</div>

<div class="mt-5 space-y-3">
<div class="bg-[#25D366]/10 border border-[#25D366]/30 rounded-2xl p-4">
<label class="text-[11px] font-bold text-[#25D366] flex items-center gap-2">🔗 LINK DO SEU GRUPO WHATSAPP:</label>
<input id="grupoLink" placeholder="https://chat.whatsapp.com/AbCdEf123456" class="w-full mt-2 bg-black border-2 border-[#25D366] rounded-2xl p-4 text-white font-bold text-[13px]" >
<div class="text-[9px] text-zinc-400 mt-2">Cole o link de convite do seu grupo - ex: https://chat.whatsapp.com/XXXX<br>O robô vai enviar automático pro grupo quando criar achadinho!</div>
<label class="text-[11px] font-bold text-white mt-3 block">🆔 ID do Grupo (auto):</label>
<input id="grupoId" placeholder="1203630...@g.us - preenche automático" class="w-full mt-1 bg-zinc-900 border border-zinc-700 rounded-xl p-3 text-white font-bold text-[11px]">
</div>

<div class="relative">
<label class="text-[11px] font-bold text-[#E1306C] flex items-center gap-2">📸 Seu Instagram (pequeno no topo):</label>
<input id="meuInsta" placeholder="@seuinstagram" class="w-full mt-1 bg-black border-2 border-[#E1306C] rounded-2xl p-4 text-white font-black text-[14px]" value="@filipe_ferreira12">
</div>

<div class="relative">
<label class="text-[11px] font-bold text-[#25D366]">📲 Seu WhatsApp (seu número):</label>
<input id="meuZap" placeholder="81999999999" class="w-full mt-1 bg-black border border-[#25D366] rounded-2xl p-3 text-white font-bold text-[14px]">
</div>

<div class="bg-[#25D366]/10 border border-[#25D366]/30 rounded-2xl p-3 flex items-center justify-between">
<label class="flex items-center gap-3 cursor-pointer"><input type="checkbox" id="autoGrupo" checked class="w-5 h-5 accent-[#25D366]"><span class="text-[12px] font-bold">✅ Enviar automático pro GRUPO ao criar</span></label>
</div>

<div class="bg-blue-500/10 border border-blue-500/30 rounded-2xl p-3">
<label class="text-[11px] font-bold text-blue-400">🤖 API Evolution (para envio auto em grupo):</label>
<input id="evoUrl" placeholder="https://sua-evolution.com - deixe vazio se não tem" class="w-full mt-1 bg-black border border-blue-500 rounded-xl p-3 text-white text-[11px]">
<input id="evoKey" placeholder="API Key Evolution - deixe vazio se não tem" class="w-full mt-2 bg-black border border-blue-500 rounded-xl p-3 text-white text-[11px]">
<div class="text-[9px] text-zinc-500 mt-1">Se não tem Evolution, o robô vai abrir WhatsApp normal e você encaminha pro grupo em 1 clique!</div>
</div>

<div class="relative">
<label class="text-[12px] font-black text-white">🔗 COLE LINK SHOPEE</label>
<input id="link" placeholder="https://s.shopee.com.br/XXXX" class="w-full mt-2 bg-white text-black border-4 border-[#ff0080] rounded-2xl p-5 text-[15px] font-black shadow-xl outline-none" autofocus>
<div id="status" class="absolute right-4 top-[50px] hidden"><span class="bg-[#00ff88] text-black text-[10px] px-3 py-1 rounded-full font-black animate-pulse">GERANDO E ENVIANDO...</span></div>
</div>
</div>
</div>

<div id="res" class="hidden">
<div class="bg-zinc-900 border-2 border-[#ff0080] rounded-[28px] p-4 mt-6 shadow-2xl">
<div class="flex justify-between items-center mb-4"><span class="font-black text-[13px]">🔥 STORY COM SEU INSTA</span><button onclick="baixarFix('storyCanvas','STORY.png')" class="bg-gradient-to-r from-[#ff0080] to-[#ff6a00] text-white px-4 py-2 rounded-full text-[11px] font-black">⬇️ BAIXAR</button></div>
<canvas id="storyCanvas" width="1080" height="1920" class="w-full bg-black rounded-2xl border border-zinc-800"></canvas>
<div class="grid grid-cols-2 gap-2 mt-3">
<button onclick="baixarFix('storyCanvas','STORY.png')" class="bg-white text-black p-3 rounded-xl font-black text-[13px]">📥 BAIXAR STORY</button>
<button onclick="enviarGrupo()" class="bg-[#25D366] text-white p-3 rounded-xl font-black text-[13px]">📲 ENVIAR PRO GRUPO</button>
</div>
</div>

<div class="bg-zinc-900 border border-zinc-800 rounded-[24px] p-4 mt-4">
<div class="flex justify-between items-center mb-3"><span class="font-black text-[13px]">🖼️ FEED COM SEU INSTA</span><button onclick="baixarFix('feedCanvas','FEED.png')" class="bg-white text-black px-4 py-2 rounded-full text-[11px] font-black">⬇️ Baixar Feed</button></div>
<canvas id="feedCanvas" width="1080" height="1080" class="w-full bg-black rounded-2xl border border-zinc-800"></canvas>
</div>

<div class="bg-gradient-to-br from-[#075E54] to-[#128C7E] border border-[#25D366] rounded-[28px] p-5 mt-5 shadow-2xl">
<div id="msg" class="bg-black/30 border border-white/20 rounded-2xl p-4 text-[14px] whitespace-pre-wrap text-white"></div>
<div class="grid grid-cols-1 gap-3 mt-4">
<button onclick="enviarGrupo()" class="bg-[#25D366] border-2 border-white text-white p-4 rounded-2xl font-black text-[15px]">📲 ENVIAR AGORA PRO GRUPO</button>
<button onclick="copiar()" class="bg-white text-black p-3 rounded-2xl font-black text-[13px]">📋 COPIAR LEGENDA</button>
</div>
<div id="grupoStatus" class="text-[11px] text-center mt-3 text-white/80"></div>
</div>
</div>
</div>

<script>
let savedZap = localStorage.getItem('meuZapNumero'); if(savedZap) document.getElementById('meuZap').value=savedZap;
let savedInsta = localStorage.getItem('meuInstaHandle'); if(savedInsta) document.getElementById('meuInsta').value=savedInsta; else document.getElementById('meuInsta').value='@filipe_ferreira12';
let savedGrupo = localStorage.getItem('grupoLink'); if(savedGrupo) document.getElementById('grupoLink').value=savedGrupo;
let savedGrupoId = localStorage.getItem('grupoId'); if(savedGrupoId) document.getElementById('grupoId').value=savedGrupoId;
let savedEvoUrl = localStorage.getItem('evoUrl'); if(savedEvoUrl) document.getElementById('evoUrl').value=savedEvoUrl;
let savedEvoKey = localStorage.getItem('evoKey'); if(savedEvoKey) document.getElementById('evoKey').value=savedEvoKey;

document.getElementById('meuZap').addEventListener('input',(e)=>{localStorage.setItem('meuZapNumero',e.target.value)});
document.getElementById('meuInsta').addEventListener('input',(e)=>{localStorage.setItem('meuInstaHandle',e.target.value)});
document.getElementById('grupoLink').addEventListener('input',(e)=>{localStorage.setItem('grupoLink',e.target.value); extrairGrupoId(e.target.value);});
document.getElementById('grupoId').addEventListener('input',(e)=>{localStorage.setItem('grupoId',e.target.value)});
document.getElementById('evoUrl').addEventListener('input',(e)=>{localStorage.setItem('evoUrl',e.target.value)});
document.getElementById('evoKey').addEventListener('input',(e)=>{localStorage.setItem('evoKey',e.target.value)});

function extrairGrupoId(link){
if(!link) return;
let id = link.split('/').pop().split('?')[0];
if(id && id.length>10){
document.getElementById('grupoId').value = id + '@g.us (link convite)';
localStorage.setItem('grupoId', document.getElementById('grupoId').value);
}
}

function brl(v){return v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'})}
async function loadImage(src){return new Promise((res,rej)=>{let i=new Image();i.crossOrigin='anonymous';i.onload=()=>res(i);i.onerror=rej;i.src=src})}

async function gerarComInsta(d){
let preco=d.preco_atual;let precoAntes=d.preco_antes;let desconto=d.desconto;let titulo=d.title;
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
try{let img=await loadImage(d.image);let sc=Math.min(980/img.width,980/img.height);let nw=img.width*sc,nh=img.height*sc;ctx1.drawImage(img,20+(1040-nw)/2,160+(1040-nh)/2,nw,nh)}catch(e){}
ctx1.fillStyle='#000';ctx1.strokeStyle='#00ff88';ctx1.lineWidth=6;ctx1.beginPath();ctx1.roundRect(20,1220,1040,450,30);ctx1.fill();ctx1.stroke();
ctx1.fillStyle='#fff';ctx1.font='900 32px system-ui';ctx1.fillText(titulo.slice(0,36).toUpperCase(),50,1280);
if(preco){ctx1.fillStyle='#00ff88';ctx1.font='900 80px system-ui';ctx1.fillText(brl(preco),50,1410);if(precoAntes&&desconto>0){ctx1.fillStyle='#ff6a00';ctx1.font='600 26px system-ui';ctx1.fillText(`DE ${brl(precoAntes)}`,50,1440)}}
ctx1.fillStyle='#ffcc00';ctx1.beginPath();ctx1.roundRect(20,1690,1040,110,20);ctx1.fill();ctx1.fillStyle='#000';ctx1.font='900 34px system-ui';ctx1.textAlign='center';ctx1.fillText('👇 LINK NA BIO - CORRE! 👇',540,1760);ctx1.textAlign='left';
ctx1.fillStyle='#fff';ctx1.font='900 22px system-ui';ctx1.textAlign='center';ctx1.fillText('⚡ SHOPEE OFICIAL • '+instaHandle+' ⚡',540,1860);ctx1.textAlign='left';
let c2=document.getElementById('feedCanvas');let ctx2=c2.getContext('2d');
let g2=ctx2.createLinearGradient(0,0,1080,0);g2.addColorStop(0,'#ff0080');g2.addColorStop(1,'#ff6a00');ctx2.fillStyle=g2;ctx2.fillRect(0,0,1080,1080);
ctx2.fillStyle='#000';ctx2.fillRect(0,0,1080,120);
ctx2.fillStyle='#fff';ctx2.font='700 20px system-ui';ctx2.textAlign='right';ctx2.fillText('📸 '+instaHandle,1050,35);ctx2.textAlign='left';
ctx2.fillStyle='#ffcc00';ctx2.font='900 36px system-ui';ctx2.fillText('🔥 QUEIMA DE ESTOQUE 🔥',30,80);
if(desconto>0){ctx2.fillStyle='#ffcc00';ctx2.beginPath();ctx2.arc(920,60,50,0,Math.PI*2);ctx2.fill();ctx2.fillStyle='#000';ctx2.font='900 26px system-ui';ctx2.textAlign='center';ctx2.fillText(`-${desconto}%`,920,68);ctx2.textAlign='left'}
ctx2.fillStyle='#fff';ctx2.beginPath();ctx2.roundRect(15,135,1050,600,20);ctx2.fill();
try{let img2=await loadImage(d.image);let sc2=Math.min(990/img2.width,560/img2.height);let nw2=img2.width*sc2,nh2=img2.height*sc2;ctx2.drawImage(img2,15+(1050-nw2)/2,135+(600-nh2)/2,nw2,nh2)}catch(e){}
ctx2.fillStyle='#000';ctx2.beginPath();ctx2.roundRect(15,750,1050,315,20);ctx2.fill();
ctx2.fillStyle='#fff';ctx2.font='900 28px system-ui';ctx2.fillText(titulo.slice(0,34).toUpperCase(),35,800);
if(preco){ctx2.fillStyle='#00ff88';ctx2.font='900 60px system-ui';ctx2.fillText(brl(preco),35,880)}
ctx2.fillStyle='#ffcc00';ctx2.beginPath();ctx2.roundRect(15,960,1050,90,15);ctx2.fill();ctx2.fillStyle='#000';ctx2.font='900 24px system-ui';ctx2.textAlign='center';ctx2.fillText(`👇 ${instaHandle} • LINK NOS COMENTÁRIOS 👇`,540,1015);ctx2.textAlign='left';
}

function baixarFix(canvasId, nomeArquivo){
try{
let canvas = document.getElementById(canvasId);
canvas.toBlob(function(blob){
if(blob){
let url = URL.createObjectURL(blob);
let a = document.createElement('a');a.href=url;a.download=nomeArquivo;document.body.appendChild(a);a.click();
setTimeout(()=>{document.body.removeChild(a);URL.revokeObjectURL(url);},100);
}else{
let dataURL = canvas.toDataURL('image/png');
let a = document.createElement('a');a.href=dataURL;a.download=nomeArquivo;a.click();
}
},'image/png',1.0);
}catch(e){alert('Erro baixar: '+e.message)}
}

let timeoutAuto=null;
async function processarLinkAuto(){
let meuZap=document.getElementById('meuZap').value.trim().replace(/[^0-9]/g,'');
let l=document.getElementById('link').value.trim();
if(!l || l.length<10) return;
if(l.indexOf('shopee.com.br')==-1 && l.indexOf('s.shopee')==-1) return;
if(meuZap.length>0) localStorage.setItem('meuZapNumero',meuZap);
let insta=document.getElementById('meuInsta').value.trim();
if(insta) localStorage.setItem('meuInstaHandle',insta);
document.getElementById('status').classList.remove('hidden');
document.getElementById('res').classList.remove('hidden');
try{
let r=await fetch('/api/resolve?url='+encodeURIComponent(l));
let j=await r.json();
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
if(document.getElementById('autoGrupo').checked){
setTimeout(()=>{enviarGrupo();},1000);
}
}catch(e){document.getElementById('status').classList.add('hidden')}
}
document.getElementById('link').addEventListener('paste',(e)=>{setTimeout(()=>{processarLinkAuto();},300);});
document.getElementById('link').addEventListener('input',(e)=>{clearTimeout(timeoutAuto);timeoutAuto=setTimeout(()=>{processarLinkAuto();},800);});

async function enviarGrupo(){
let grupoLink=document.getElementById('grupoLink').value.trim();
let grupoId=document.getElementById('grupoId').value.trim();
let msg=document.getElementById('msg').textContent;
let evoUrl=document.getElementById('evoUrl').value.trim();
let evoKey=document.getElementById('evoKey').value.trim();
let meuZap=document.getElementById('meuZap').value.trim().replace(/[^0-9]/g,'');
if(!msg){alert('Cole o link primeiro!');return}
document.getElementById('grupoStatus').textContent='🚀 Enviando pro grupo...';

if(evoUrl && evoKey && grupoId){
try{
let canvas=document.getElementById('storyCanvas');
let base64 = canvas.toDataURL('image/png').split(',')[1];
let payload={
number: grupoId.includes('@g.us') ? grupoId : grupoId+'@g.us',
mediatype: 'image',
media: base64,
caption: msg
};
let res=await fetch(evoUrl+'/message/sendMedia/'+evoKey,{
method:'POST',
headers:{'Content-Type':'application/json','apikey':evoKey},
body: JSON.stringify(payload)
});
if(res.ok){
document.getElementById('grupoStatus').textContent='✅ Enviado pro grupo com sucesso via Evolution!';
return;
}
}catch(e){
document.getElementById('grupoStatus').textContent='⚠️ Erro Evolution, abrindo WhatsApp manual...';
}
}

if(grupoLink){
window.open(grupoLink,'_blank');
setTimeout(()=>{
let numeroFormatado = meuZap.startsWith('55') ? meuZap : '55'+meuZap;
let canvas=document.getElementById('storyCanvas');
canvas.toBlob(function(blob){
let url=URL.createObjectURL(blob);
let a=document.createElement('a');a.href=url;a.download='GRUPO-'+Date.now()+'.png';a.click();
setTimeout(()=>{
window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`,'_blank');
document.getElementById('grupoStatus').textContent='📲 Imagem baixada! Agora encaminhe a imagem + legenda pro grupo!';
},500);
},'image/png');
},1000);
}else{
let numeroFormatado = meuZap.startsWith('55') ? meuZap : '55'+meuZap;
window.open(`https://wa.me/${numeroFormatado}?text=${encodeURIComponent(msg)}`,'_blank');
document.getElementById('grupoStatus').textContent='📲 WhatsApp aberto! Encaminhe pro seu grupo!';
}
}

function copiar(){navigator.clipboard.writeText(document.getElementById('msg').textContent);alert('Copiado! ✅')}
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
        with urllib.request.urlopen(req, timeout=12) as r:
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
            final_url=r.geturl(); html=r.read().decode(errors='ignore')[:20000]
            return final_url, html, "direct"
    except: pass
    try:
        api=f"https://api.allorigins.win/get?url={urllib.parse.quote(url)}"
        req=urllib.request.Request(api, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            j=json.loads(r.read().decode()); html=j.get('contents','')[:20000]
            m=re.search(r'https://shopee\.com\.br/[^\s"\'<>]+', html)
            if m: final_url=m.group(0)
            return final_url, html, "allorigins"
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
    title="Achadinho Shopee"; image=None; preco=None; preco_antes=None; metodo="API_OK"; comissao=None
    if item_id:
        res,_ = call_api_final(item_id)
        if res:
            title=res.get('title') or title
            image=res.get('image')
            preco=res.get('preco')
            preco_antes=res.get('preco_antes')
            comissao=res.get('comissao')
    img_proxy=proxy_img(image) if image else ""
    desconto=0
    if preco_antes and preco and preco_antes>preco:
        try: desconto=round((1-preco/preco_antes)*100)
        except: pass
    return {"affiliate_link_original":url,"title":title[:150],"image":img_proxy,"image_original":image,"preco_atual":preco,"preco_antes":preco_antes,"desconto":desconto,"comissao":comissao,"metodo":metodo,"final_url":final_url,"item_id":item_id,"shop_id":shop_id}

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/resolve')
def api_resolve():
    return jsonify(resolve_backend(request.args.get('url','')))

@app.route('/api/send_to_group', methods=['POST'])
def api_send_group():
    data=request.json
    return jsonify({"status":"ok","message":"Use frontend Evolution integration"})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
