from PIL import Image, ImageEnhance, ImageFilter
import io
import os


def test_pillow_features():
    """测试 Pillow 所有需要的功能"""
    print("=== 开始测试 Pillow 功能 ===\n")
    
    all_passed = True
    
    # 测试 1: 图像创建
    print("测试 1: 图像创建")
    try:
        test_img = Image.new('RGB', (100, 100), color='red')
        print("  ✓ 创建图像成功")
    except Exception as e:
        print(f"  ✗ 创建图像失败: {e}")
        all_passed = False
        return False
    
    # 测试 2: JPEG 保存
    print("\n测试 2: JPEG 保存")
    try:
        buffer = io.BytesIO()
        test_img.save(buffer, 'JPEG', quality=90)
        print("  ✓ JPEG 保存成功")
    except Exception as e:
        print(f"  ✗ JPEG 保存失败: {e}")
        all_passed = False
    
    # 测试 3: PNG 保存
    print("\n测试 3: PNG 保存")
    try:
        buffer_png = io.BytesIO()
        test_img.save(buffer_png, 'PNG')
        print("  ✓ PNG 保存成功")
    except Exception as e:
        print(f"  ✗ PNG 保存失败: {e}")
        all_passed = False
    
    # 测试 4: 图像增强 - 对比度
    print("\n测试 4: 图像增强 - 对比度")
    try:
        enhancer = ImageEnhance.Contrast(test_img)
        enhanced = enhancer.enhance(1.2)
        print("  ✓ 对比度增强成功")
    except Exception as e:
        print(f"  ✗ 对比度增强失败: {e}")
        all_passed = False
    
    # 测试 5: 图像增强 - 亮度
    print("\n测试 5: 图像增强 - 亮度")
    try:
        enhancer = ImageEnhance.Brightness(test_img)
        enhanced = enhancer.enhance(1.1)
        print("  ✓ 亮度增强成功")
    except Exception as e:
        print(f"  ✗ 亮度增强失败: {e}")
        all_passed = False
    
    # 测试 6: 图像增强 - 色彩
    print("\n测试 6: 图像增强 - 色彩")
    try:
        enhancer = ImageEnhance.Color(test_img)
        enhanced = enhancer.enhance(1.15)
        print("  ✓ 色彩增强成功")
    except Exception as e:
        print(f"  ✗ 色彩增强失败: {e}")
        all_passed = False
    
    # 测试 7: 图像增强 - 锐化
    print("\n测试 7: 图像增强 - 锐化")
    try:
        enhancer = ImageEnhance.Sharpness(test_img)
        enhanced = enhancer.enhance(1.3)
        print("  ✓ 锐化增强成功")
    except Exception as e:
        print(f"  ✗ 锐化增强失败: {e}")
        all_passed = False
    
    # 测试 8: 图像滤镜
    print("\n测试 8: 图像滤镜")
    try:
        sharpened = test_img.filter(ImageFilter.SHARPEN)
        blurred = test_img.filter(ImageFilter.BLUR)
        print("  ✓ 图像滤镜成功")
    except Exception as e:
        print(f"  ✗ 图像滤镜失败: {e}")
        all_passed = False
    
    # 测试 9: 文件系统保存
    print("\n测试 9: 文件系统保存")
    try:
        test_path = 'test_output.jpg'
        test_img.save(test_path, 'JPEG', quality=95)
        if os.path.exists(test_path):
            print("  ✓ 文件保存成功")
            os.remove(test_path)
        else:
            print("  ✗ 文件未创建")
            all_passed = False
    except Exception as e:
        print(f"  ✗ 文件保存失败: {e}")
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ 所有测试通过！")
        print("=" * 40)
        return True
    else:
        print("✗ 部分测试失败")
        print("=" * 40)
        return False


if __name__ == '__main__':
    success = test_pillow_features()
    exit(0 if success else 1)