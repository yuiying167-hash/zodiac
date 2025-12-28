import os
import time
import random
import anthropic  # ✅ OpenAI 대신 Anthropic 사용

# ==========================================
# 🔑 여기에 Claude API 키를 넣으세요!
# ==========================================
API_KEY = "your_key" 
client = anthropic.Anthropic(api_key=API_KEY)

# ==========================================
# 1. 기초 데이터 (태국어)
# ==========================================
zodiacs = [
    {"id": "rat", "name": "ชวด (หนู)", "icon": "🐭", "element": "น้ำ", "trait": "ฉลาด, ปรับตัวเก่ง"},
    {"id": "ox", "name": "ฉลู (วัว)", "icon": "🐮", "element": "ดิน", "trait": "อดทน, ซื่อสัตย์"},
    {"id": "tiger", "name": "ขาล (เสือ)", "icon": "🐯", "element": "ไม้", "trait": "กล้าหาญ, เป็นผู้นำ"},
    {"id": "rabbit", "name": "เถาะ (กระต่าย)", "icon": "🐰", "element": "ไม้", "trait": "อ่อนโยน, โรแมนติก"},
    {"id": "dragon", "name": "มะโรง (งูใหญ่)", "icon": "🐲", "element": "ดิน", "trait": "มั่นใจ, ทะเยอทะยาน"},
    {"id": "snake", "name": "มะเส็ง (งูเล็ก)", "icon": "🐍", "element": "ไฟ", "trait": "ลึกลับ, มีเสน่ห์"},
    {"id": "horse", "name": "มะเมีย (ม้า)", "icon": "🐴", "element": "ไฟ", "trait": "รักอิสระ, ร่าเริง"},
    {"id": "goat", "name": "มะแม (แพะ)", "icon": "🐐", "element": "ดิน", "trait": "ใจดี, ขี้เกรงใจ"},
    {"id": "monkey", "name": "วอก (ลิง)", "icon": "🐵", "element": "โลหะ", "trait": "ขี้เล่น, แก้ปัญหาเก่ง"},
    {"id": "rooster", "name": "ระกา (ไก่)", "icon": "🐔", "element": "โลหะ", "trait": "เจ้าระเบียบ, ตรงไปตรงมา"},
    {"id": "dog", "name": "จอ (หมา)", "icon": "🐶", "element": "ดิน", "trait": "ซื่อสัตย์, รักเพื่อน"},
    {"id": "pig", "name": "กุน (หมู)", "icon": "🐷", "element": "น้ำ", "trait": "มองโลกในแง่ดี, ใจกว้าง"}
]

genders = [
    {"code": "mf", "title": "ชาย ❤️ หญิง", "icon": "👫", "desc": "คู่รักชายหญิง"},
    {"code": "mm", "title": "ชาย ❤️ ชาย", "icon": "👬", "desc": "คู่รักชาย-ชาย (Boy's Love)"},
    {"code": "ff", "title": "หญิง ❤️ หญิง", "icon": "👭", "desc": "คู่รักหญิง-หญิง (Girl's Love)"}
]

# ==========================================
# 2. 점수 계산 (고정 로직)
# ==========================================
def get_score(idx1, idx2):
    base = 91
    seed = (idx1 * 17 + idx2 * 31) % 9 
    score = base + seed
    
    if score >= 98: return score, "S", "เนื้อคู่ชัดๆ! ดวงสมพงศ์กันสูงสุดๆ", "ความรักที่สมบูรณ์แบบ"
    elif score >= 95: return score, "A+", "เข้ากันได้ดีเยี่ยม! ความรักราบรื่น", "คู่สร้างคู่สม"
    else: return score, "A", "คู่ที่เข้าใจกันดี มีความสุขด้วยกัน", "ความรักที่มั่นคง"

# ==========================================
# 3. [핵심] Claude에게 글쓰기 시키기
# ==========================================
def generate_ai_content(me, partner, gender, score_data):
    score, grade, comment, summary = score_data
    
    # 이미 파일이 있으면 스킵
    filename = f"posts/{me['id']}-{partner['id']}-{gender['code']}.html"
    if os.path.exists(filename):
        print(f"⏩ 스킵 (이미 있음): {filename}")
        return None

    print(f"🤖 Claude 작성 중... {me['name']} vs {partner['name']} ({gender['desc']})")

    prompt = f"""
    You are a highly respected Thai Astrologer (Horacharn) with deep knowledge of ancient Zodiac wisdom.
    Write a VERY DETAILED, POETIC, and ROMANTIC analysis in Thai Language (ภาษาไทย).
    
    [Target Couple]
    - Person A: {me['name']} ({me['trait']})
    - Person B: {partner['name']} ({partner['trait']})
    - Relationship Type: {gender['desc']} (Strictly follow this gender context!)
    - Compatibility Score: {score}/100

    [IMPORTANT INSTRUCTIONS]
    1. **DO NOT use "You" (คุณ).** Instead, ALWAYS use specific terms like:
       - For Male-Female: "หนุ่ม{me['name']}" (Rat Man) and "สาว{partner['name']}" (Ox Woman).
       - For Male-Male: "หนุ่ม{me['name']}" and "หนุ่ม{partner['name']}".
       - For Female-Female: "สาว{me['name']}" and "สาว{partner['name']}".
    2. Write at least 600 words.
    3. Output ONLY the HTML body content (No <html> tags).

    [Required Structure]
    
    1. <p> (Intro) Start poetic. Describe the meeting of {me['element']} element and {partner['element']} element. </p>
    
    2. <h3 style="color:var(--pink-primary);">❤ ความเข้ากันได้ของนิสัย</h3>
    <p> Analyze their personalities in detail. 
       Example: "หนุ่ม{me['name']} ผู้มีความฉลาด... จะหลงใหลในความอ่อนโยนของ สาว{partner['name']}..." 
       Discuss daily life, money management, and travel styles using their Zodiac names.
    </p>
    
    3. <h3 style="color:var(--purple-primary);">⚡ จุดที่ต้องระวังและการปรับตัว</h3>
    <p> Discuss potential conflicts specific to {me['name']} and {partner['name']}. Suggest solutions. </p>
    
    4. <div class="advice-box">
         <p><strong>🔮 คำทำนายอนาคต:</strong> Predict their long-term future.</p>
       </div>
    
    5. <h4 style="color:var(--pink-primary);">เคล็ดลับมัดใจ (Love Tips):</h4>
    <ul class="tips-list">
        <li>Tip about communication for {me['name']} and {partner['name']}.</li>
        <li>Tip about dates/activities.</li>
        <li>Tip about intimacy/trust.</li>
    </ul>
    """




    try:
        # ✅ Claude API 호출 부분
        message = client.messages.create(
            model="claude-3-haiku-20240307", # 👈 여기를 이렇게 바꾸세요!
            max_tokens=4000,
            
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    
    except Exception as e:
        print(f"❌ API Error: {e}")
        return "<p>กำลังคำนวณข้อมูล... กรุณารีเฟรชหน้านี้อีกครั้ง</p>"

# ==========================================
# 4. 전체 HTML 조립
# ==========================================
def get_full_html(me, partner, gender, score_data, ai_content):
    score, grade, comment, summary = score_data
    
    if not ai_content: return None

    page_title = f"ดูดวง {me['name']} {gender['icon']} {partner['name']} | ดวงความรัก 12 นักษัตร"
    meta_desc = f"เช็คดวงความรักปี {me['name']} กับ {partner['name']} ({gender['desc']}) ได้คะแนน {score}% - {summary}"

    # (이하 HTML 템플릿은 이전과 동일)
    return f'''<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <meta name="description" content="{meta_desc}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💕</text></svg>">
    <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3198582468837090" crossorigin="anonymous"></script>
    <style>
        :root {{ --gradient-bg: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 40%, #2d1b4e 100%); --gradient-pink: linear-gradient(135deg, #ff6b9d 0%, #ff8fab 100%); --gradient-gold: linear-gradient(135deg, #ffd700 0%, #ffab00 100%); --pink-primary: #ff6b9d; --glass-bg: rgba(255, 255, 255, 0.08); --glass-border: rgba(255, 255, 255, 0.15); --text-primary: #ffffff; --text-secondary: rgba(255, 255, 255, 0.8); --glow-pink: 0 0 20px rgba(255, 107, 157, 0.5); }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Sarabun', sans-serif; background: var(--gradient-bg); color: var(--text-primary); min-height: 100vh; padding-bottom: 50px; overflow-x: hidden; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; position: relative; z-index: 10; }}
        .glass-card {{ background: var(--glass-bg); backdrop-filter: blur(20px); border: 1px solid var(--glass-border); border-radius: 24px; padding: 25px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); }}
        h1 {{ font-size: 1.5rem; margin-bottom: 5px; background: var(--gradient-pink); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }}
        .score-circle {{ width: 150px; height: 150px; margin: 20px auto; border-radius: 50%; background: conic-gradient(#ff6b9d 0deg, #a855f7 {score * 3.6}deg, rgba(255,255,255,0.1) 0deg); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(255,107,157,0.5); }}
        .score-inner {{ width: 120px; height: 120px; border-radius: 50%; background: #1a1a3e; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .score-number {{ font-size: 2.5rem; font-weight: 800; color: #fff; }}
        .grade-badge {{ display: inline-block; padding: 5px 20px; background: var(--gradient-pink); border-radius: 20px; font-weight: bold; margin-bottom: 10px; }}
        .zodiac-pair {{ font-size: 3rem; margin-bottom: 10px; text-align: center; }}
        .score-section {{ text-align: center; }}
        .trait-box, .advice-box {{ background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; margin-top: 15px; line-height: 1.6; }}
        .tips-list {{ list-style: none; padding: 0; }}
        .tips-list li {{ margin-bottom: 8px; color: var(--text-secondary); border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; }}
        .btn-group {{ display: flex; gap: 10px; margin-top: 30px; }}
        .btn {{ flex: 1; padding: 15px; border-radius: 50px; text-decoration: none; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 8px; }}
        .btn-back {{ background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.2); }}
        .btn-lotto {{ background: var(--gradient-gold); color: #1a1a2e; }}
        .ad-box {{ background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; margin: 20px 0; padding: 10px; text-align: center; min-height: 100px; }}
        .ad-label {{ font-size: 0.7em; color: #666; display: block; margin-bottom: 5px; }}
        footer {{ text-align: center; margin-top: 40px; color: #666; font-size: 0.8rem; }}
    </style>
</head>
<body>
<div class="container">
    <div class="ad-box"><span class="ad-label">Advertisement</span><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3198582468837090" data-ad-slot="5807274060" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>
    <div class="glass-card score-section">
        <div class="zodiac-pair">{me['icon']} {gender['icon']} {partner['icon']}</div>
        <h1>{me['name']} & {partner['name']}</h1>
        <p style="color:#aaa; margin-bottom:20px;">{gender['desc']}</p>
        <div class="score-circle"><div class="score-inner"><span class="score-number">{score}%</span><span style="font-size:0.8rem; color:#aaa;">ความเข้ากัน</span></div></div>
        <div class="grade-badge">เกรด {grade}</div>
        <p style="font-size:1.1rem; margin-bottom: 10px;">✨ {comment}</p>
    </div>
    <div class="ad-box"><span class="ad-label">Sponsored</span><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3198582468837090" data-ad-slot="5807274060" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>
    <div class="glass-card" style="text-align: left;">
        <h3 style="color:var(--pink-primary); margin-bottom:15px;"><i class="fas fa-star"></i> บทวิเคราะห์ดวงความรัก </h3>
        {ai_content}
    </div>
    <div class="btn-group">
        <a href="/" class="btn btn-back"><i class="fas fa-arrow-left"></i> เลือกคู่ใหม่</a>
        <a href="https://lottery.spattra.com" class="btn btn-lotto"><i class="fas fa-ticket-alt"></i> ตรวจหวย</a>
    </div>
    <div class="ad-box"><span class="ad-label">Advertisement</span><ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3198582468837090" data-ad-slot="5807274060" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script></div>
    <footer><p>© 2024 Zodiac Love Match</p></footer>
</div>
</body>
</html>'''

# ==========================================
# 5. 실행
# ==========================================
if __name__ == "__main__":
    if not os.path.exists("posts"):
        os.makedirs("posts")

    count = 0
    print("🚀 Claude AI 글쓰기 시작!")
    
    for g in genders:
        for i, me in enumerate(zodiacs):
            for j, partner in enumerate(zodiacs):
                
                filename = f"posts/{me['id']}-{partner['id']}-{g['code']}.html"
                
                # 중복 실행 방지
                if os.path.exists(filename):
                    print(f"⏩ 스킵: {filename}")
                    continue

                score_data = get_score(i, j)
                
                # Claude 호출
                ai_content = generate_ai_content(me, partner, g, score_data)
                
                if ai_content:
                    html_content = get_full_html(me, partner, g, score_data, ai_content)
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    
                    count += 1
                    print(f"✅ 생성 완료 ({count}): {filename}")
                    
                    # API 속도 조절 (너무 빠르면 차단될 수 있음)
                    time.sleep(0.5)

    print(f"\n🎉 작업 끝! 총 {count}개 파일 생성 완료.")