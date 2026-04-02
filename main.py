from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
from PIL import Image as PILImage, ImageEnhance, ImageFilter
from kivy.properties import StringProperty, ObjectProperty
import os
from datetime import datetime


class ImageEnhancerApp(App):
    title = StringProperty('图片一键美化')

    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.setup_title()
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
        self.title_label = Label(
            text=self.title,
            font_size=24,
            size_hint_y=None,
            height=40,
            bold=True
        )
        self.root.add_widget(self.title_label)

        self.image_display = Image(
            size_hint_y=0.7,
            allow_stretch=True,
            keep_ratio=True
        )
        self.root.add_widget(self.image_display)

        self.buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )

        self.select_button = Button(
            text='选择图片',
            size_hint_x=0.3
        )
        self.select_button.bind(on_press=self.select_image)
        self.buttons_layout.add_widget(self.select_button)

        self.enhance_button = Button(
            text='一键美化',
            size_hint_x=0.3,
            disabled=True
        )
        self.enhance_button.bind(on_press=self.enhance_image)
        self.buttons_layout.add_widget(self.enhance_button)

        self.save_button = Button(
            text='保存图片',
            size_hint_x=0.3,
            disabled=True
        )
        self.save_button.bind(on_press=self.save_image)
        self.buttons_layout.add_widget(self.save_button)

        self.root.add_widget(self.buttons_layout)

        self.status_label = Label(
            text='请选择一张图片',
            font_size=14,
            size_hint_y=None,
            height=30
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
            filters=['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']
        )
        file_chooser_layout.add_widget(filechooser)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        
        cancel_btn = Button(text='取消', size_hint_x=0.5)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        select_btn = Button(text='选择', size_hint_x=0.5)
        select_btn.bind(on_press=lambda x: self.load_selected_image(filechooser.selection, popup))
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(select_btn)
        
        content.add_widget(file_chooser_layout)
        content.add_widget(button_layout)

        popup = Popup(
            title='选择图片',
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
            self.enhanced_pil_image.save(save_path, 'JPEG', quality=95)
            
            self.status_label.text = f'已保存到: {save_path}'
            
            if os.path.exists('temp_enhanced.png'):
                os.remove('temp_enhanced.png')
                
        except Exception as e:
            self.status_label.text = f'保存失败: {str(e)}'


if __name__ == '__main__':
    ImageEnhancerApp().run()