"""Hindi pages: /hi/emi-calculator and /hi/blog/credit-card-statement-date-vs-due-date.

Written in everyday Hindi (the way people in India talk about loans and cards: EMI, स्टेटमेंट डेट, ड्यू डेट),
not machine-translated. Numbers match the English pages; if you change one, change both.
hreflang links between the two versions come from ALTERNATES in build-pages.py."""
import html
import build_pages as bp

B = bp.B
AUTHOR = {"@type": "Person", "@id": B + "/about#aditya", "name": "Aditya Pratap Singh", "url": B + "/about", "jobTitle": "Founder"}
RBI_CC = ('RBI, Master Direction – Credit Card and Debit Card – Issuance and Conduct Directions, 2022 (मार्च 2024 तक अपडेटेड)',
          'https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12300')
FINAL = '<div class="final"><h2>आज से अपनी स्ट्रीक शुरू करें</h2><p>आदतें, पैसा, रिमाइंडर और सेहत, सब एक ऐप में। दो मिनट में सेटअप, 7 दिन फ़्री।</p><a class="btn lime" href="/app#signup">फ़्री ट्रायल शुरू करें</a></div>'
faq_html = lambda faq: ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in faq)
faq_ld = lambda faq: {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

EMI_CALC = '''<div class="calc" id="emi"><div class="fields">
<label>लोन की रकम (₹)<input id="eP" type="number" inputmode="numeric" value="500000" min="1000"></label>
<label>ब्याज दर (% सालाना)<input id="eR" type="number" inputmode="decimal" value="12" step="0.1" min="0"></label>
<label>अवधि (महीने)<input id="eN" type="number" inputmode="numeric" value="60" min="1"></label>
<label>हर महीने अतिरिक्त भुगतान (₹)<input id="eX" type="number" inputmode="numeric" value="2000" min="0"></label></div>
<div class="out"><div><small>मासिक EMI</small><b id="oE">–</b></div><div><small>कुल ब्याज</small><b id="oI">–</b></div><div><small>कुल भुगतान</small><b id="oT">–</b></div><div><small>अतिरिक्त भुगतान से</small><b id="oS">–</b></div></div>
<p class="note" id="oNote"></p></div>
<script>
const f=n=>'₹'+Math.round(n).toLocaleString('en-IN');
function emiCalc(){const P=+eP.value||0,r=(+eR.value||0)/1200,n=Math.max(1,+eN.value||1),x=+eX.value||0;
const E=r?P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1):P/n;oE.textContent=f(E);oI.textContent=f(E*n-P);oT.textContent=f(E*n);
let b=P,m=0,int=0;while(b>0.5&&m<1200){const i=b*r;int+=i;b=b+i-Math.min(E+x,b+i);m++}
const saved=(E*n-P)-int;oS.textContent=x>0?`${n-m} महीने पहले`:'–';oNote.textContent=x>0?`हर महीने ${f(x)} ज़्यादा चुकाने पर लोन ${n} की जगह ${m} महीनों में ख़त्म होगा और लगभग ${f(saved)} ब्याज बचेगा।`:'प्रीपेमेंट से कितना ब्याज बचता है, यह देखने के लिए हर महीने की अतिरिक्त रकम डालें।'}
['eP','eR','eN','eX'].forEach(id=>document.getElementById(id).addEventListener('input',emiCalc));emiCalc();
</script>'''

def emi_page():
    path = '/hi/emi-calculator'
    title = 'EMI कैलकुलेटर हिंदी में: लोन की किस्त और ब्याज | Self Streak'
    desc = 'होम, कार, पर्सनल और एजुकेशन लोन के लिए मुफ़्त EMI कैलकुलेटर। अपनी मासिक किस्त, कुल ब्याज और हर महीने थोड़ा ज़्यादा चुकाने से होने वाली बचत देखें।'
    faq = [('क्या यह EMI कैलकुलेटर मुफ़्त है?', 'हाँ, इस पेज का कैलकुलेटर पूरी तरह मुफ़्त है। रिमाइंडर के साथ अपने सारे लोन ट्रैक करना Self Streak Plus का हिस्सा है (7 दिन फ़्री, फिर ₹199 महीना)।'),
           ('क्या प्रीपेमेंट से हमेशा पैसे बचते हैं?', 'प्रीपेमेंट से ब्याज कम होता है, लेकिन कुछ फ़िक्स्ड-रेट लोन पर प्रीपेमेंट चार्ज लगता है। RBI के नियमों के अनुसार व्यक्तिगत फ़्लोटिंग-रेट लोन पर फ़ोरक्लोज़र या प्रीपेमेंट चार्ज नहीं लगता। अपना लोन एग्रीमेंट ज़रूर देखें।'),
           ('पहले लोन चुकाएँ या निवेश करें?', 'आम नियम यह है: पहले ऊँचे ब्याज वाला कर्ज़ (क्रेडिट कार्ड, पर्सनल लोन) चुकाएँ और एक इमरजेंसी फ़ंड रखें। Self Streak का AI प्लान आपकी अपनी आमदनी और लोन के हिसाब से यह तय करने में मदद करता है।'),
           ('EMI में ब्याज और मूलधन कैसे बँटता है?', 'शुरुआती महीनों में EMI का बड़ा हिस्सा ब्याज में जाता है। जैसे-जैसे बकाया घटता है, हर किस्त में मूलधन का हिस्सा बढ़ता जाता है।')]
    inner = f'''<header style="padding-top:20px"><div class="wrap"><div class="kick">लोन और EMI</div>
<h1>EMI कैलकुलेटर: अपनी लोन की किस्त जानें</h1><p class="lead">अपनी मासिक EMI, कुल ब्याज, और हर महीने थोड़ी अतिरिक्त रकम चुकाने से कितना समय और ब्याज बचता है, यह तुरंत देखें। फिर अपने सारे लोन और EMI एक जगह ट्रैक करें।</p>
<div class="cta"><a class="btn lime" href="/app#signup">7 दिन फ़्री आज़माएँ →</a><a class="btn" href="/emi-calculator" hreflang="en-IN">Read in English</a></div>
{EMI_CALC}<p class="short">EMI कैलकुलेटर तीन चीज़ों से आपकी तय मासिक किस्त निकालता है: लोन की रकम, सालाना ब्याज दर और अवधि। उदाहरण: ₹5 लाख का लोन 12% पर 5 साल के लिए लें तो EMI लगभग ₹11,122 बनती है, और कुल मिलाकर करीब ₹1.67 लाख ब्याज जाता है। हर महीने थोड़ा ज़्यादा चुकाने से दोनों घटते हैं।</p>
<p class="upd">अपडेट: {bp.UPDATED}</p></div></header>
<main class="wrap">
<section><h2>EMI कैसे निकाली जाती है</h2>
<p>EMI = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1)। यहाँ P लोन की रकम है, r मासिक ब्याज दर है (सालाना दर ÷ 12 ÷ 100) और n महीनों की संख्या है।</p>
<p>शुरुआती महीनों में EMI का ज़्यादातर हिस्सा ब्याज में जाता है, बाद में मूलधन ज़्यादा चुकता होता है। इसीलिए हर महीने छोटी-सी अतिरिक्त रकम भी बड़ा फ़र्क डालती है: वह सीधे मूलधन घटाती है, तो अगले हर महीने का ब्याज कम हो जाता है।</p></section>
<section><h2>एक नहीं, हर लोन ट्रैक करें</h2><div class="grid">
<div class="card"><b>सारी EMI एक जगह</b><p>होम, पर्सनल, कार, एजुकेशन, गोल्ड या परिवार से लिया उधार: बकाया, EMI, ब्याज दर और बचे महीने।</p></div>
<div class="card"><b>ड्यू डेट से पहले रिमाइंडर</b><p>हर EMI से 2 दिन पहले याद दिलाता है। "पेड" मार्क करें, बकाया अपने-आप अपडेट हो जाता है।</p></div>
<div class="card"><b>कर्ज़-मुक्त होने की तारीख</b><p>देखें कि आप किस महीने कर्ज़ से मुक्त होंगे, और एवलांच या स्नोबॉल तरीके से यह कैसे बदलती है।</p></div>
<div class="card"><b>AI रीपेमेंट प्लान</b><p>आपकी असली आमदनी, बजट और लोन पर बना महीने-दर-महीने का प्लान।</p></div></div></section>
<section><h2>लोन लेने से पहले ध्यान रखें</h2><ul class="list">
<li>सिर्फ़ ब्याज दर नहीं, प्रोसेसिंग फ़ीस और बीमा जैसे दूसरे चार्ज भी जोड़कर देखें।</li>
<li>कोशिश करें कि सारी EMI मिलाकर आपकी टेक-होम सैलरी के एक तिहाई से ज़्यादा न हों, ताकि रोज़मर्रा के खर्च और बचत के लिए जगह बचे।</li>
<li>लंबी अवधि से EMI छोटी दिखती है, पर कुल ब्याज बहुत बढ़ जाता है। ऊपर कैलकुलेटर में अवधि बदलकर फ़र्क देखें।</li>
<li>बोनस या इंक्रीमेंट मिले तो उसका एक हिस्सा प्रीपेमेंट में लगाएँ।</li></ul></section>
{bp.shots_html('emi-calculator', 'ऐप में ऐसा दिखता है')}
<section><h2>सवाल-जवाब</h2>{faq_html(faq)}</section>
<section><h2>और पढ़ें</h2><div class="guides"><a href="/hi/blog/credit-card-statement-date-vs-due-date">क्रेडिट कार्ड स्टेटमेंट डेट और ड्यू डेट में फ़र्क<span>बिल कब बनता है, कब तक चुकाना है, और ब्याज से कैसे बचें।</span></a>
<a href="/emi-calculator/home-loan" hreflang="en-IN">Home loan EMI calculator (English)<span>EMI tables by amount and tenure, interest by year and prepayment savings.</span></a>
<a href="/emi-calculator/personal-loan" hreflang="en-IN">Personal loan EMI calculator (English)<span>EMI tables by amount and tenure, interest by year and prepayment savings.</span></a></div></section>
{FINAL}</main>'''
    graph = [{"@type": "WebPage", "@id": B + path + "#page", "url": B + path, "name": 'EMI कैलकुलेटर', "description": desc,
              "isPartOf": {"@id": B + "/#website"}, "about": {"@id": B + "/#app"}, "dateModified": bp.UPDATED, "inLanguage": "hi-IN"}, faq_ld(faq)]
    return path, bp.shell(path, title, desc, 'EMI कैलकुलेटर · Self Streak', graph, [('Self Streak', '/'), ('EMI कैलकुलेटर', path)], inner, lang='hi-IN')

CC_BODY = '''
<section><h2 id="statement-date">स्टेटमेंट डेट क्या है?</h2>
<p>स्टेटमेंट डेट (जिसे बिलिंग डेट भी कहते हैं) वह दिन है जब कार्ड कंपनी एक बिलिंग साइकिल बंद करके आपका बिल बनाती है। पिछली स्टेटमेंट डेट के अगले दिन से लेकर इस तारीख तक की हर खरीदारी नए स्टेटमेंट में आती है। स्टेटमेंट डेट के बाद किया गया खर्च अगले महीने के बिल में जाता है।</p>
<p>उदाहरण: आपकी स्टेटमेंट डेट हर महीने की 5 तारीख है। 3 मार्च को की गई ₹4,000 की खरीदारी 5 मार्च के स्टेटमेंट में आएगी। वहीं 6 मार्च को की गई ₹4,000 की खरीदारी 5 अप्रैल के स्टेटमेंट में आएगी।</p></section>
<section><h2 id="due-date">ड्यू डेट (भुगतान की आख़िरी तारीख) क्या है?</h2>
<p>ड्यू डेट वह आख़िरी दिन है जब तक स्टेटमेंट डेट पर बना बिल चुकाना होता है। ज़्यादातर भारतीय कार्ड दोनों तारीखों के बीच 15 से 20 दिन देते हैं। अगर स्टेटमेंट डेट 5 है, तो ड्यू डेट 23 या 25 हो सकती है।</p>
<p>स्टेटमेंट में दो रकम दिखती हैं: <b>टोटल अमाउंट ड्यू</b> (इस बिल का पूरा खर्च) और <b>मिनिमम अमाउंट ड्यू</b> (आमतौर पर कुल का लगभग 5%, साथ में कोई EMI और फ़ीस)। ब्याज से बचने के लिए पूरा टोटल अमाउंट ड्यू चुकाना ज़रूरी है।</p></section>
<section><h2 id="interest-free-period">ब्याज-मुक्त अवधि कैसे काम करती है</h2>
<p>ब्याज-मुक्त अवधि खरीदारी के दिन से उस बिल की ड्यू डेट तक का समय है, जिसमें वह खरीदारी आती है। यह इस पर निर्भर करती है कि आपने साइकिल में कब खर्च किया:</p>
<div class="tw"><table><thead><tr><th>खरीदारी की तारीख</th><th>किस बिल में</th><th>ड्यू डेट</th><th>ब्याज-मुक्त दिन</th></tr></thead><tbody>
<tr><td>6 मार्च (स्टेटमेंट के अगले दिन)</td><td>5 अप्रैल का स्टेटमेंट</td><td>25 अप्रैल</td><td>लगभग 50 दिन</td></tr>
<tr><td>20 मार्च</td><td>5 अप्रैल का स्टेटमेंट</td><td>25 अप्रैल</td><td>लगभग 36 दिन</td></tr>
<tr><td>4 अप्रैल (स्टेटमेंट से एक दिन पहले)</td><td>5 अप्रैल का स्टेटमेंट</td><td>25 अप्रैल</td><td>लगभग 21 दिन</td></tr></tbody></table></div>
<p>यानी कोई बड़ी, पहले से तय खरीदारी स्टेटमेंट डेट के ठीक बाद करें तो चुकाने के लिए सबसे ज़्यादा समय मिलता है। सही दिन आपके कार्ड की साइकिल पर निर्भर करते हैं।</p>
<p>अगर पिछला बकाया बचा है, तो ब्याज-मुक्त अवधि ख़त्म हो जाती है। RBI के नियम कहते हैं कि कार्ड कंपनी को अपनी शर्तों में साफ़ बताना होगा कि पिछले बिल का कोई भी बकाया बचा हो तो ब्याज-मुक्त अवधि लागू नहीं रहती। असल में, पूरा बिल न चुकाने पर नई खरीदारी पर भी उसी दिन से ब्याज लगने लगता है।</p></section>
<section><h2 id="minimum-due">सिर्फ़ मिनिमम ड्यू चुकाना इतना महँगा क्यों है</h2>
<p>मिनिमम ड्यू चुकाने से अकाउंट ठीक रहता है और लेट फ़ीस नहीं लगती, लेकिन बाकी रकम पर ब्याज लगता है, आमतौर पर 3–3.75% महीना (यानी सालाना लगभग 36–45%)।</p>
<p>एक हिसाब देखिए: ₹60,000 का बकाया, 3.5% मासिक ब्याज, और आप हर महीने सिर्फ़ 5% मिनिमम (कम से कम ₹500) चुकाते हैं और कार्ड पर नया खर्च नहीं करते। इसे चुकाने में लगभग <b>141 महीने</b> (करीब 12 साल) लगेंगे और लगभग <b>₹1,11,917</b> ब्याज जाएगा, यानी असली बकाये का लगभग दोगुना। इसीलिए RBI हर स्टेटमेंट पर यह चेतावनी देना ज़रूरी करता है कि सिर्फ़ मिनिमम चुकाने से भुगतान महीनों या सालों तक खिंचता है और ब्याज पर ब्याज लगता है।</p>
<p>अपने बिल के लिए यह हिसाब <a href="/credit-card-interest-calculator" hreflang="en-IN">क्रेडिट कार्ड इंटरेस्ट कैलकुलेटर</a> में देखें।</p></section>
<section><h2 id="rbi-rules">RBI के नियम जो आपको बचाते हैं</h2>
<p>क्रेडिट और डेबिट कार्ड पर RBI का मास्टर डायरेक्शन (2022, मार्च 2024 तक अपडेटेड) कुछ ज़रूरी नियम तय करता है:</p>
<ul class="list">
<li><b>लेट फ़ीस और क्रेडिट रिपोर्ट के लिए 3 दिन की छूट।</b> कार्ड कंपनी लेट पेमेंट चार्ज तभी लगा सकती है, या क्रेडिट ब्यूरो को "पास्ट ड्यू" तभी बता सकती है, जब ड्यू डेट के तीन दिन बाद भी भुगतान बकाया रहे।</li>
<li><b>लेट फ़ीस सिर्फ़ बकाया रकम पर।</b> लेट पेमेंट चार्ज सिर्फ़ उस रकम पर लगता है जो ड्यू डेट के बाद भी बाकी है, पूरे टोटल अमाउंट ड्यू पर नहीं।</li>
<li><b>आप बिलिंग साइकिल बदल सकते हैं।</b> कार्ड कंपनी को कम से कम एक बार आपको अपनी सुविधा की बिलिंग डेट चुनने देनी होगी, हेल्पलाइन, ऐप या नेट बैंकिंग जैसे किसी तरीके से।</li>
<li><b>ब्याज सिर्फ़ असली बकाये पर।</b> ब्याज सिर्फ़ बकाया रकम पर लगता है, जिसमें किए गए भुगतान, रिफ़ंड और रिवर्स हुए ट्रांज़ैक्शन घटाए जाते हैं।</li></ul>
<p>3 दिन की छूट एक सुरक्षा है, प्लान नहीं। बिना चुकाए बकाये पर ब्याज ड्यू डेट से ही लग सकता है, इसलिए समय पर भुगतान करें।</p></section>
<section><h2 id="choose-dates">सबसे अच्छी स्टेटमेंट डेट कैसे चुनें</h2>
<p>अगर सैलरी 1 तारीख को आती है, तो 5 से 10 तारीख के आसपास की ड्यू डेट अच्छी रहती है, क्योंकि तब खाते में पैसा होता है। वहाँ से 15–20 दिन पीछे गिनें, वही स्टेटमेंट डेट माँगें। दो कार्ड हों तो उनकी ड्यू डेट अलग-अलग रखें, ताकि भुगतान महीने भर में बँट जाएँ।</p></section>
<section><h2 id="payment-timing">भुगतान कब "हुआ" माना जाता है?</h2>
<p>भुगतान तब गिना जाता है जब कार्ड कंपनी को पैसा मिलता है, तब नहीं जब आप भेजते हैं। कार्ड वाले बैंक के अपने ऐप, UPI या उसी बैंक की नेट बैंकिंग से किया भुगतान आमतौर पर उसी दिन दिख जाता है। दूसरे बैंक, चेक या थर्ड-पार्टी ऐप से किए भुगतान में एक से तीन कामकाजी दिन लग सकते हैं, और शनिवार-रविवार या बैंक की छुट्टियाँ इसे और बढ़ा सकती हैं।</p>
<p>सुरक्षित आदत यह है कि ड्यू डेट से कम से कम दो-तीन कामकाजी दिन पहले भुगतान करें और कार्ड अकाउंट में उसके दिखने तक भुगतान का रेफ़रेंस नंबर संभालकर रखें। अगर ड्यू डेट रविवार या छुट्टी के दिन पड़े, तो यह न मानें कि वह अपने-आप अगले कामकाजी दिन पर खिसक जाएगी; अपना स्टेटमेंट देखें या कार्ड कंपनी से पूछें।</p>
<p>रिफ़ंड उल्टा काम करता है। RBI के नियमों के अनुसार ड्यू डेट से पहले आए रिफ़ंड, फ़ेल या रिवर्स हुए ट्रांज़ैक्शन की रकम बकाये में से घटाई जानी चाहिए, यानी बड़ा रिफ़ंड आपकी चुकाने वाली रकम कम कर सकता है। भुगतान से पहले कार्ड ऐप में नई रकम देख लें।</p></section>
<section><h2 id="never-miss">ड्यू डेट कभी न चूकें: चार आदतें</h2>
<ol class="list">
<li>सुरक्षा के लिए कम से कम मिनिमम ड्यू का ऑटो-डेबिट लगा दें।</li>
<li>पूरी रकम ड्यू डेट से कुछ दिन पहले ख़ुद चुकाएँ।</li>
<li>अगले बिल पर अब तक कितना खर्च हो चुका है, यह नज़र में रखें, ताकि बिल देखकर झटका न लगे।</li>
<li>ऐसा रिमाइंडर लें जो सिर्फ़ तारीख नहीं, रकम भी बताए।</li></ol>
<p><a href="/credit-card-bill-reminder" hreflang="en-IN">Self Streak का क्रेडिट कार्ड ट्रैकर</a> हर कार्ड की स्टेटमेंट और ड्यू डेट याद रखता है, खर्च को "इस बिल" और "अगले बिल" में बाँटकर दिखाता है, और हर ड्यू डेट से दो दिन पहले याद दिलाता है। इसके लिए कार्ड नंबर या बैंक लॉगिन की ज़रूरत नहीं।</p></section>
'''
CC_FAQ = [('क्या स्टेटमेंट डेट और ड्यू डेट एक ही हैं?', 'नहीं। स्टेटमेंट डेट पर बिल बनता है; ड्यू डेट, जो आमतौर पर 15–20 दिन बाद आती है, उसे चुकाने की आख़िरी तारीख है।'),
          ('एक दिन लेट भुगतान करने पर क्या होगा?', 'RBI के नियमों के अनुसार लेट फ़ीस और क्रेडिट ब्यूरो रिपोर्टिंग तभी होती है जब अकाउंट तीन दिन से ज़्यादा बकाया रहे। फिर भी बिना चुकाए बकाये पर ब्याज लग सकता है, और बकाया पूरा चुकाने तक नई खरीदारी पर ब्याज-मुक्त अवधि नहीं मिलती।'),
          ('क्या सिर्फ़ मिनिमम ड्यू चुकाने से क्रेडिट स्कोर पर असर पड़ता है?', 'समय पर कम से कम मिनिमम चुकाने से लेट पेमेंट का निशान नहीं लगता। लेकिन लिमिट के मुकाबले ज़्यादा बकाया होने से स्कोर फिर भी घट सकता है, और ब्याज तेज़ी से बढ़ता है।')]

def cc_post():
    path = '/hi/blog/credit-card-statement-date-vs-due-date'
    title = 'कार्ड की स्टेटमेंट डेट और ड्यू डेट में फ़र्क | Self Streak'
    desc = 'स्टेटमेंट डेट और ड्यू डेट का मतलब, ब्याज-मुक्त अवधि कैसे काम करती है, सिर्फ़ मिनिमम ड्यू चुकाना महँगा क्यों है, और RBI के वे नियम जो आपको बचाते हैं।'
    h1 = 'क्रेडिट कार्ड स्टेटमेंट डेट और ड्यू डेट: किसका क्या मतलब है'
    words = len(__import__('re').sub('<[^>]+>', ' ', CC_BODY).split())
    toc = ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in __import__('re').findall(r'<h2 id="([^"]+)">(.*?)</h2>', CC_BODY))
    inner = f'''<article><header style="padding-top:20px"><div class="wrap"><div class="kick">क्रेडिट कार्ड</div>
<h1>{h1}</h1><p class="lead">क्रेडिट कार्ड पर आप क्या और कब चुकाएँगे, यह दो तारीखें तय करती हैं। इन्हें सही समझ लिया तो कार्ड लगभग 50 दिन तक का बिना ब्याज का उधार है। गलत समझा तो हर महीने 3–4% ब्याज देना पड़ता है।</p>
<p class="byline">लेखक: <a href="/about">Aditya Pratap Singh</a> · प्रकाशित 2026-11-13 · अपडेट {bp.UPDATED} · <a href="/blog/credit-card-statement-date-vs-due-date" hreflang="en-IN">Read in English</a></p>
<p class="short"><b>छोटा जवाब:</b> <b>स्टेटमेंट डेट</b> वह दिन है जब कार्ड का महीने का बिल बनता है; पिछले स्टेटमेंट के बाद का सारा खर्च इसमें आता है। <b>ड्यू डेट</b> उस बिल को चुकाने की आख़िरी तारीख है, जो आमतौर पर 15–20 दिन बाद होती है। ड्यू डेट तक पूरी रकम चुका दें तो कोई ब्याज नहीं लगता।</p></div></header>
<main class="wrap">
<section><h2 style="font-size:18px">इस गाइड में</h2><ol class="list">{toc}</ol></section>
{CC_BODY}
<section><h2>सवाल-जवाब</h2>{faq_html(CC_FAQ)}</section>
<section><h2>स्रोत</h2><ul class="list src"><li><a href="{RBI_CC[1]}" rel="noopener" target="_blank">{html.escape(RBI_CC[0])}</a></li></ul><p class="note">यह गाइड सामान्य जानकारी है, वित्तीय सलाह नहीं। अपने कार्ड की ब्याज दर और चार्ज उसकी MITC (मोस्ट इम्पॉर्टेंट टर्म्स एंड कंडीशंस) में देखें।</p></section>
{FINAL}
<section><h2>और पढ़ें</h2><div class="guides"><a href="/hi/emi-calculator">EMI कैलकुलेटर<span>अपनी लोन की मासिक किस्त, कुल ब्याज और प्रीपेमेंट की बचत देखें।</span></a>
<a href="/credit-card-bill-reminder" hreflang="en-IN">Credit card bill reminder (English)<span>Track each card’s statement and due dates, with reminders before every due date.</span></a></div></section></main></article>'''
    graph = [{"@type": "BlogPosting", "@id": B + path + "#post", "headline": h1, "description": desc, "url": B + path, "mainEntityOfPage": B + path,
              "datePublished": '2026-11-13', "dateModified": bp.UPDATED, "author": AUTHOR, "publisher": {"@id": B + "/#org"}, "image": bp.og_for(path),
              "inLanguage": "hi-IN", "wordCount": words, "isPartOf": {"@id": B + "/blog#blog"},
              "translationOfWork": {"@id": B + "/blog/credit-card-statement-date-vs-due-date#post"}}, faq_ld(CC_FAQ)]
    head = f'<meta property="article:published_time" content="2026-11-13"><meta property="article:modified_time" content="{bp.UPDATED}"><meta name="author" content="Aditya Pratap Singh">\n'
    return path, bp.shell(path, title, desc, h1, graph, [('Self Streak', '/'), ('गाइड', '/blog'), ('स्टेटमेंट डेट बनाम ड्यू डेट', path)], inner,
                          og_type='article', head_extra=head, lang='hi-IN')

def build():
    for fn in (emi_page, cc_post):
        path, page = fn(); bp.write(path, page)
