import os

sns_html = """
<div style="text-align:center; padding:20px; border-top:1px solid rgba(255,255,255,0.1); margin-bottom:20px;">
    <p style="color:#aaa; margin-bottom:10px;">แชร์ให้เพื่อน</p>
    <a href="https://www.facebook.com/sharer/sharer.php?u=" onclick="this.href+=location.href;return true;" target="_blank" style="font-size:1.8rem; color:#1877F2; margin:0 10px; text-decoration:none;"><i class="fab fa-facebook"></i></a>
    <a href="https://social-plugins.line.me/lineit/share?url=" onclick="this.href+=location.href;return true;" target="_blank" style="font-size:1.8rem; color:#06C755; margin:0 10px; text-decoration:none;"><i class="fab fa-line"></i></a>
    <a href="https://twitter.com/intent/tweet?url=" onclick="this.href+=location.href;return true;" target="_blank" style="font-size:1.8rem; color:white; margin:0 10px; text-decoration:none;"><i class="fab fa-x-twitter"></i></a>
</div>
"""

folder_path = "posts"
count = 0

print("🚀 디버깅 모드 시작...")

if not os.path.exists(folder_path):
    print("❌ 에러: 'posts' 폴더가 없습니다!")
    exit()

files = os.listdir(folder_path)
print(f"📂 폴더 내 파일 개수: {len(files)}개")

for filename in files:
    if filename.endswith(".html"):
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. 중복 체크 확인
        if "facebook.com/sharer" in content:
            print(f"⏩ 스킵 (이미 있음): {filename}")
            continue
            
        # 2. 태그 확인
        if "</body>" not in content:
            print(f"⚠️ 경고: </body> 태그 없음: {filename}")
            # 태그 없어도 강제로 맨 뒤에 붙임
            new_content = content + sns_html
        else:
            # 정상 교체
            new_content = content.replace("</body>", sns_html + "\n</body>")
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        count += 1
        # 너무 많으니까 10개까지만 로그 보여주고 나머지는 생략
        if count <= 10:
            print(f"✅ 수정 성공: {filename}")

print(f"\n🎉 총 {count}개 파일 수정 완료!")
