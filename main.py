from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import platform
from PIL import Image as PILImage, ImageEnhance, ImageFilter
from kivy.properties import StringProperty, ObjectProperty
import os
from datetime import datetime


class ImageEnhancerApp(App):
    title = StringProperty('图片一键美化')
    
    def register_chinese_fonts(self):
        if platform == 'macosx':
            try:
                LabelBase.register(
                    name='Chinese',
                    fn_regular='/System/Library/Fonts/PingFang.ttc'
                )
            except:
                try:
                    LabelBase.register(
                        name='Chinese',
                        fn_regular='/System/Library/Fonts/STHeiti Medium.ttc'
                    )
                except:
                    pass
        elif platform == 'android':
            try:
                LabelBase.register(
                    name='Chinese',
                    fn_regular='/system/fonts/DroidSansFallback.ttf'
                )
            except:
                pass

    def create_default_placeholder(self):
        """创建默认占位图片"""
        from PIL import Image, ImageDraw, ImageFont
        
        os.makedirs('assets', exist_ok=True)
        placeholder_path = 'assets/default_placeholder.png'
        
        # 如果已存在则不重新生成
        if os.path.exists(placeholder_path):
            return
        
        # 创建渐变背景
        img = Image.new('RGB', (600, 400), color='#F0F8FF')
        draw = ImageDraw.Draw(img)
        
        # 绘制渐变效果（从上到下的淡蓝色渐变）
        for y in range(400):
            r = int(227 + (240-227) * y / 400)
            g = int(242 + (248-242) * y / 400)
            b = int(253 + (255-253) * y / 400)
            draw.line([(0, y), (600, y)], fill=(r, g, b))
        
        # 绘制装饰性圆角矩形边框
        draw.rectangle([50, 80, 550, 320], outline='#4A90E2', width=4)
        
        # 绘制中心图标区域（相机图标示意）
        draw.ellipse([250, 130, 350, 230], outline='#64B5F6', width=3)
        draw.line([270, 190, 300, 180], fill='#64B5F6', width=3)
        draw.line([300, 180, 330, 170], fill='#64B5F6', width=3)
        draw.rectangle([280, 185, 320, 200], outline='#64B5F6', width=2)
        
        # 绘制文字
        title_text = self.title  # 使用应用标题
        subtitle_text = "点击下方按钮选择图片"
        
        # 尝试使用中文字体
        try:
            if platform == 'macosx':
                font_path = '/System/Library/Fonts/PingFang.ttc'
            else:
                font_path = None
            
            if font_path and os.path.exists(font_path):
                title_font = ImageFont.truetype(font_path, 48)
                subtitle_font = ImageFont.truetype(font_path, 24)
            else:
                title_font = None
                subtitle_font = None
        except:
            title_font = None
            subtitle_font = None
        
        # 绘制标题（使用 getbbox 计算居中位置）
        if title_font:
            try:
                title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
                title_width = title_bbox[2] - title_bbox[0]
                title_x = (600 - title_width) // 2
                draw.text((title_x, 260), title_text, fill='#1976D2', font=title_font)
            except:
                draw.text((300, 260), title_text, fill='#1976D2', anchor='mm')
        else:
            # 回退到默认字体
            draw.text((300, 260), title_text, fill='#1976D2', anchor='mm')
        
        # 绘制副标题
        if subtitle_font:
            try:
                sub_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
                sub_width = sub_bbox[2] - sub_bbox[0]
                sub_x = (600 - sub_width) // 2
                draw.text((sub_x, 320), subtitle_text, fill='#64B5F6', font=subtitle_font)
            except:
                draw.text((300, 320), subtitle_text, fill='#64B5F6', anchor='mm')
        else:
            draw.text((300, 320), subtitle_text, fill='#64B5F6', anchor='mm')
        
        # 保存图片
        img.save(placeholder_path, 'PNG')

    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.setup_title()
        self.register_chinese_fonts()
        self.setup_ui()
        
        return self.root

    def setup_title(self):
        if platform == 'android':
            self.title = '美化神器'
            Window.title = '美化神器'
        elif platform == 'macosx':
            self.title = '图片一键美化'
            Window.title = '图片一键美化'
        else:
            self.title = '图片一键美化'
            Window.title = '图片一键美化'

    def setup_ui(self):
        # 创建默认占位图
        self.create_default_placeholder()
        
        self.title_label = Label(
            text=self.title,
            font_size=32,
            size_hint_y=None,
            height=55,
            bold=True,
            font_name='Chinese'
        )
        self.root.add_widget(self.title_label)

        self.image_display = Image(
            source='assets/default_placeholder.png',
            size_hint_y=0.65,
            allow_stretch=True,
            keep_ratio=True
        )
        self.root.add_widget(self.image_display)

        self.buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=55,
            spacing=10
        )

        self.select_button = Button(
            text='选择图片',
            size_hint_x=0.3,
            font_size=20,
            font_name='Chinese'
        )
        self.select_button.bind(on_press=self.select_image)
        self.buttons_layout.add_widget(self.select_button)

        self.enhance_button = Button(
            text='一键美化',
            size_hint_x=0.3,
            font_size=20,
            font_name='Chinese',
            disabled=True
        )
        self.enhance_button.bind(on_press=self.enhance_image)
        self.buttons_layout.add_widget(self.enhance_button)

        self.save_button = Button(
            text='保存图片',
            size_hint_x=0.3,
            font_size=20,
            font_name='Chinese',
            disabled=True
        )
        self.save_button.bind(on_press=self.save_image)
        self.buttons_layout.add_widget(self.save_button)

        self.root.add_widget(self.buttons_layout)

        self.status_label = Label(
            text='请选择一张图片',
            font_size=20,
            size_hint_y=None,
            height=40,
            font_name='Chinese'
        )
        self.root.add_widget(self.status_label)

        self.current_image_path = None
        self.current_pil_image = None
        self.enhanced_pil_image = None

    def select_image(self, instance):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical')
        
        file_chooser_layout = BoxLayout(orientation='vertical')
        
        from kivy.uix.filechooser import FileChooserListView
        filechooser = FileChooserListView(
            filters=['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.webp'],
            font_name='Chinese'
        )
        file_chooser_layout.add_widget(filechooser)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45)
        
        cancel_btn = Button(text='取消', size_hint_x=0.5, font_size=18, font_name='Chinese')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        select_btn = Button(text='选择', size_hint_x=0.5, font_size=18, font_name='Chinese')
        select_btn.bind(on_press=lambda x: self.load_selected_image(filechooser.selection, popup))
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(select_btn)
        
        content.add_widget(file_chooser_layout)
        content.add_widget(button_layout)

        popup = Popup(
            title='选择图片',
            title_font='Chinese',
            title_size=22,
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def load_selected_image(self, selection, popup):
        if selection and len(selection) > 0:
            image_path = selection[0]
            try:
                self.current_image_path = image_path
                self.image_display.source = image_path
                self.current_pil_image = PILImage.open(image_path)
                self.enhanced_pil_image = None
                
                self.status_label.text = f'已加载: {os.path.basename(image_path)}'
                self.enhance_button.disabled = False
                self.save_button.disabled = True
                
                popup.dismiss()
            except Exception as e:
                self.status_label.text = f'加载失败: {str(e)}'

    def enhance_image(self, instance):
        if self.current_pil_image is None:
            self.status_label.text = '请先选择图片'
            return

        try:
            image = self.current_pil_image.copy()
            
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.15)
            
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.3)
            
            self.enhanced_pil_image = image
            
            temp_path = 'temp_enhanced.png'
            image.save(temp_path)
            self.image_display.source = temp_path
            
            self.status_label.text = '美化完成！可以保存图片'
            self.save_button.disabled = False
            
        except Exception as e:
            self.status_label.text = f'美化失败: {str(e)}'

    def save_image(self, instance):
        if self.enhanced_pil_image is None:
            self.status_label.text = '请先美化图片'
            return

        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if platform == 'android':
                from android.storage import primary_external_storage_path
                save_dir = primary_external_storage_path()
                filename = f'enhanced_{timestamp}.jpg'
                save_path = os.path.join(save_dir, 'Pictures', filename)
            else:
                save_dir = os.path.expanduser('~/Desktop')
                filename = f'enhanced_{timestamp}.jpg'
                save_path = os.path.join(save_dir, filename)
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 处理 RGBA 模式转 JPEG
            save_image = self.enhanced_pil_image
            if save_image.mode == 'RGBA':
                background = PILImage.new('RGB', save_image.size, (255, 255, 255))
                background.paste(save_image, mask=save_image.split()[3])
                save_image = background
            
            save_image.save(save_path, 'JPEG', quality=95)
            
            self.status_label.text = f'已保存到: {save_path}'
            
            if os.path.exists('temp_enhanced.png'):
                os.remove('temp_enhanced.png')
            
            # 恢复默认占位图
            if os.path.exists('assets/default_placeholder.png'):
                self.image_display.source = 'assets/default_placeholder.png'
                
        except Exception as e:
            self.status_label.text = f'保存失败: {str(e)}'


if __name__ == '__main__':
    ImageEnhancerApp().run()