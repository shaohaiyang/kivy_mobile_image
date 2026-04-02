import sys
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.utils import platform

class TestFontApp(App):
    def build(self):
        self.register_chinese_fonts()
        print(f"平台: {platform}")
        print(f"窗口标题: {self.title}")
        return None
    
    def register_chinese_fonts(self):
        if platform == 'macosx':
            try:
                LabelBase.register(
                    name='Chinese',
                    fn_regular='/System/Library/Fonts/PingFang.ttc'
                )
                print("✓ 注册 PingFang SC 字体成功")
            except Exception as e:
                print(f"✗ 注册 PingFang SC 字体失败: {e}")
                try:
                    LabelBase.register(
                        name='Chinese',
                        fn_regular='/System/Library/Fonts/STHeiti Medium.ttc'
                    )
                    print("✓ 注册 STHeiti Medium 字体成功")
                except Exception as e2:
                    print(f"✗ 注册 STHeiti Medium 字体失败: {e2}")
        elif platform == 'android':
            try:
                LabelBase.register(
                    name='Chinese',
                    fn_regular='/system/fonts/DroidSansFallback.ttf'
                )
                print("✓ 注册 Droid Sans Fallback 字体成功")
            except Exception as e:
                print(f"✗ 注册 Droid Sans Fallback 字体失败: {e}")
        else:
            print(f"平台 {platform} 未配置字体")

if __name__ == '__main__':
    app = TestFontApp()
    app.run()