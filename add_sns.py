import os

# ==========================================
# 1. 삽입할 SNS 섹션 HTML (다크모드 완벽 호환)
# ==========================================
sns_section_html = """
    <!-- SNS 공유 섹션 -->
    <div class="share-section">
        <p class="share-title">แชร์ให้เพื่อน (친구에게 공유)</p>
        <div class="share-buttons">
            <!-- Facebook -->
            <a href="https://www.facebook.com/sharer/sharer.php?u=" 
               onclick="this.href+=encodeURIComponent(window.location.href);return true;" 
               target="_blank" rel="noopener noreferrer" class="share-btn share-facebook" aria-label="Facebook">
                <i class="fab fa-facebook-f"></i>
            </a>
            <!-- LINE -->
            <a href="https://social-plugins.line.me/lineit/share?url=" 
               onclick="this.href+=encodeURIComponent(window.location.href);return true;" 
               target="_blank" rel="noopener noreferrer" class="share-btn share-line" aria-label="LINE">
                <i class="fab fa-line"></i>
            </a>
            <!-- Twitter (X) -->
            <a href="https://twitter.com/intent/tweet?url=" 
               onclick="this.href+=encodeURIComponent(window.location.href)+'&text='+encodeURIComponent(document.title);return true;" 
               target="_blank" rel="noopener noreferrer" class="share-btn share-twitter" aria-label="X (Twitter)">
                <i class="fab fa-x-twitter"></i>
            </a>
            <!-- Copy Link -->
            <button onclick="copyLink()" class="share-btn share-copy" aria-label="Copy Link">
                <i class="fas fa-link"></i>
            </button>
        </div>
        <div id="copy-toast" class="copy-toast">✅ คัดลอกลิงก์แล้ว!</div>
    </div>

    <style>
        .share-section { text-align: center; margin: 30px 0 20px; }
        .share-title { color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-bottom: 12px; }
        .share-buttons { display: flex; gap: 12px; justify-content: center; }
        .share-btn { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-decoration: none; color: white; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.1); cursor: pointer; transition: all 0.3s ease; font-size: 1.2rem; }
        .share-btn:hover { transform: translateY(-3px) scale(1.05); }
        .share-facebook:hover { background: #1877F2; border-color: #1877F2; box-shadow: 0 0 15px rgba(24,119,242,0.5); }
        .share-line:hover { background: #06C755; border-color: #06C755; box-shadow: 0 0 15px rgba(6,199,85,0.5); }
        .share-twitter:hover { background: #000; border-color: #333; box-shadow: 0 0 15px rgba(255,255,255,0.3); }
        .share-copy:hover { background: #a855f7; border-color: #a855f7; box-shadow: 0 0 15px rgba(168,85,247,0.5); }
        .copy-toast { position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%) translateY(20px); background: rgba(16,185,129,0.9); color: white; padding: 10px 20px; border-radius: 20px; font-weight: bold; opacity: 0; visibility: hidden; transition: all 0.3s; z-index: 1000; backdrop-filter: blur(5px); }
        .copy-toast.show { opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0); }
    </style>

    <script>
        function copyLink() {
            navigator.clipboard.writeText(window.location.href).then(() => {
                const toast = document.getElementById('copy-toast');
                toast.classList.add('show');
                setTimeout(() => toast.classList.remove('show'), 2000);
            });
        }
    </script>
"""

# ==========================================
# 2. 실행 로직 (posts 폴더 순회)
# ==========================================
folder_path = "posts"
count = 0

if not os.path.exists(folder_path):
    print("❌ Error: 'posts' 폴더가 없습니다.")
    exit()

print("🚀 SNS 버튼 추가 작업 시작...")

for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 중복 방지 (이미 추가된 경우 건너뜀)
        if "share-section" in content:
            continue
            
        # 삽입 위치: <div class="action-buttons"> 바로 위
        # 이 위치가 가장 자연스럽습니다 (글 다 읽고 -> 공유 or 다른 거 보기)
        target = '<div class="action-buttons">'
        
        if target in content:
            new_content = content.replace(target, sns_section_html + "\n    " + target)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            count += 1
            # 진행 상황 표시 (너무 많이 출력되면 느려지므로 50개마다 출력)
            if count % 50 == 0:
                print(f"✅ {count}개 파일 처리 완료...")

print(f"\n🎉 작업 끝! 총 {count}개 파일에 SNS 버튼을 심었습니다.")
