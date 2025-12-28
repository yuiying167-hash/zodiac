import os

folder_path = "posts"
count = 0

print("🚀 연도 수정 시작...")

for filename in os.listdir(folder_path):
    if filename.endswith(".html"):
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "2024" in content:
            new_content = content.replace("2024", "2026")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1

print(f"🎉 {count}개 파일 연도 수정 완료!")
