import os
import shutil
import re
import zipfile

def setup_dataset_windows():
    zip_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'archive.zip')
    extract_target = r'D:\DeepLearning\my_dataset'
    
    print(f"Đang tìm file tại: {zip_path}")
    if not os.path.exists(zip_path):
        print("LỖI: Không tìm thấy file archive.zip trong thư mục Downloads!")
        return

    print(f"BƯỚC 1: Đang giải nén dữ liệu")
    os.makedirs(extract_target, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.infolist():
            try:
                # Python zipfile mặc định đọc sai thành cp437, ta ép nó về đúng UTF-8 của Kaggle
                member.filename = member.filename.encode('cp437').decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass # Bỏ qua các file rác hệ thống (.DS_Store...)
            
            # Khắc phục lỗi bảo mật đường dẫn tuyệt đối khi đổi tên file trên Windows
            # Tạo đường dẫn đầy đủ và an toàn
            target_path = os.path.join(extract_target, member.filename)
            
            if member.is_dir():
                os.makedirs(target_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with zip_ref.open(member) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)

    print("BƯỚC 2: Đang thanh lọc các thư mục ký tự rác...")
    base_dirs = [
        os.path.join(extract_target, 'CASIA-HWDB_Train', 'Train'),
        os.path.join(extract_target, 'CASIA-HWDB_Test', 'Test')
    ]
    
    hanzi_pattern = re.compile(r'[\u4e00-\u9fff]')
    deleted_count = 0
    
    for base_dir in base_dirs:
        if not os.path.exists(base_dir):
            continue
            
        for folder_name in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder_name)
            
            if os.path.isdir(folder_path) and not hanzi_pattern.search(folder_name):
                try:
                    shutil.rmtree(folder_path)
                    deleted_count += 1
                except Exception as e:
                    pass
                
    print(f"HOÀN TẤT! Đã bung file thành công và dọn dẹp {deleted_count} thư mục rác.")
    print(f"Toàn bộ dữ liệu sạch đã nằm gọn tại: {extract_target}")

if __name__ == "__main__":
    setup_dataset_windows()