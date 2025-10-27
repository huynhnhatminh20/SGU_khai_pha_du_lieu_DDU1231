import json
import base64
import re
from pathlib import Path


def save_notebook_images(notebook_path, output_dir="images"):
    """
    Trích xuất tất cả hình ảnh từ notebook và lưu vào thư mục
    
    Parameters:
    -----------
    notebook_path : str or Path
        Đường dẫn đến file notebook
    output_dir : str
        Thư mục đích lưu hình ảnh (mặc định: "images")
    
    Returns:
    --------
    dict : {
        'count': int (số lượng hình ảnh),
        'files': list (danh sách tên file đã lưu)
    }
    """
    
    notebook_path = Path(notebook_path)
    images_dir = Path(output_dir)
    images_dir.mkdir(exist_ok=True)
    
    # Đọc notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    image_count = 0
    saved_images = []
    
    # Duyệt qua các cell
    for cell_idx, cell in enumerate(nb['cells']):
        if 'outputs' not in cell:
            continue
        
        # Trích xuất tên từ cell source (từ comment hoặc code)
        cell_name = f"chart_{image_count + 1}"
        if 'source' in cell:
            source = ''.join(cell['source'])
            
            # Tìm comment dòng đầu tiên (# ...)
            first_line = source.split('\n')[0]
            if first_line.startswith('#'):
                # Lấy comment và làm tên file
                comment = first_line.strip('# ').strip()
                cell_name = comment.replace(" ", "_").replace(".", "_")
            
            # Hoặc tìm từ khóa plot type
            if 'kind=' in source:
                match = re.search(r"kind=['\"](\w+)['\"]", source)
                if match:
                    plot_type = match.group(1)
                    cell_name = f"{plot_type}_plot"
        
        # Duyệt qua outputs
        for output_idx, output in enumerate(cell['outputs']):
            # Tìm hình ảnh PNG
            if 'data' in output and 'image/png' in output['data']:
                image_data = output['data']['image/png']
                
                # Decode base64 thành binary
                try:
                    image_bytes = base64.b64decode(image_data)
                except Exception as e:
                    print(f"⚠ Lỗi decode cell {cell_idx}, output {output_idx}: {e}")
                    continue
                
                # Tạo tên file
                image_count += 1
                filename = f"{cell_name}_{image_count:02d}.png"
                
                # Lưu file
                filepath = images_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                
                saved_images.append(str(filepath))
    
    return {
        'count': image_count,
        'files': saved_images,
        'output_dir': str(images_dir.absolute())
    }


def print_save_summary(result):
    """In ra tóm tắt kết quả lưu hình"""
    print(f"\n{'='*60}")
    print(f" Hoàn tất: {result['count']} hình ảnh được lưu")
    print(f" Thư mục: {result['output_dir']}")
    print(f"{'='*60}")
    if result['files']:
        print(" Danh sách file:")
        for img in result['files']:
            print(f"   - {img}")
    else:
        print("  Không tìm thấy hình ảnh nào. Hãy chạy các cell vẽ biểu đồ trước!")
