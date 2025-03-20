from django.core.management.base import BaseCommand
from cars.models import Car
from django.core.files import File
from django.conf import settings
import os
import requests
from io import BytesIO

class Command(BaseCommand):
    help = '向数据库添加示例车辆数据'

    def handle(self, *args, **kwargs):
        # 示例车辆数据
        cars_data = [
            {
                'name': '奔驰 S级',
                'brand': '奔驰',
                'model': 'S 350 L',
                'year': 2023,
                'price': 1099000.00,
                'description': '奔驰S级是梅赛德斯-奔驰的旗舰轿车，代表着豪华与科技的完美结合。配备最新的MBUX智能系统，提供卓越的驾乘体验。',
                'image_url': 'https://images.unsplash.com/photo-1616788494672-ec7ca25fdda9?w=800'
            },
            {
                'name': '宝马 7系',
                'brand': '宝马',
                'model': '750Li xDrive',
                'year': 2023,
                'price': 1299000.00,
                'description': '全新BMW 7系融合了优雅的设计和创新科技，配备了最新的iDrive 8.0系统，为驾驶者提供极致的驾驶乐趣。',
                'image_url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800'
            },
            {
                'name': '保时捷 911',
                'brand': '保时捷',
                'model': 'Carrera S',
                'year': 2023,
                'price': 1580000.00,
                'description': '保时捷911是跑车领域的标杆，完美展现了运动性能与日常实用性的平衡。搭载3.0升双涡轮增压发动机。',
                'image_url': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800'
            },
            {
                'name': '特斯拉 Model S',
                'brand': '特斯拉',
                'model': 'Plaid',
                'year': 2023,
                'price': 999900.00,
                'description': '特斯拉Model S Plaid是目前最快的量产电动车之一，百公里加速仅需2.1秒，续航里程超过600公里。',
                'image_url': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800'
            },
            {
                'name': '法拉利 F8',
                'brand': '法拉利',
                'model': 'Tributo',
                'year': 2023,
                'price': 3380000.00,
                'description': '法拉利F8 Tributo是品牌最新的中置后驱跑车，搭载3.9升V8双涡轮增压发动机，最大功率720马力。',
                'image_url': 'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800'
            },
            # 新增车辆数据
            {
                'name': '兰博基尼 Urus',
                'brand': '兰博基尼',
                'model': 'Performante',
                'year': 2023,
                'price': 3980000.00,
                'description': '兰博基尼Urus是一款超级运动型SUV，完美融合了超跑性能和SUV的实用性。4.0升V8双涡轮增压发动机，最大功率666马力。',
                'image_url': 'https://images.unsplash.com/photo-1566473965997-3de9c817e938?w=800'
            },
            {
                'name': '奥迪 RS e-tron GT',
                'brand': '奥迪',
                'model': 'RS e-tron GT',
                'year': 2023,
                'price': 1608800.00,
                'description': '奥迪RS e-tron GT是品牌首款纯电动超跑，双电机总输出功率598马力，百公里加速仅需3.3秒。',
                'image_url': 'https://images.unsplash.com/photo-1614200187524-dc4b892acf16?w=800'
            },
            {
                'name': '玛莎拉蒂 MC20',
                'brand': '玛莎拉蒂',
                'model': 'Cielo',
                'year': 2023,
                'price': 2988000.00,
                'description': '玛莎拉蒂MC20采用全新Nettuno V6发动机，最大功率630马力，百公里加速2.9秒，极速超过325km/h。',
                'image_url': 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800'
            },
            {
                'name': '阿斯顿马丁 DBX',
                'brand': '阿斯顿马丁',
                'model': '707',
                'year': 2023,
                'price': 2980000.00,
                'description': 'DBX707是阿斯顿马丁首款超豪华性能SUV，搭载4.0升V8双涡轮增压发动机，最大功率707马力。',
                'image_url': 'https://images.unsplash.com/photo-1615455976161-bcf6c0531c8c?w=800'
            },
            {
                'name': '宾利 飞驰',
                'brand': '宾利',
                'model': 'Speed',
                'year': 2023,
                'price': 3980000.00,
                'description': '宾利飞驰Speed搭载6.0升W12发动机，最大功率635马力，百公里加速3.8秒，完美诠释了奢华与性能的统一。',
                'image_url': 'https://images.unsplash.com/photo-1621135802920-133df287f89c?w=800'
            },
            {
                'name': '劳斯莱斯 幻影',
                'brand': '劳斯莱斯',
                'model': 'Extended',
                'year': 2023,
                'price': 8880000.00,
                'description': '劳斯莱斯幻影代表着汽车工业的巅峰之作，6.75升V12双涡轮增压发动机，为尊贵乘客提供无与伦比的舒适体验。',
                'image_url': 'https://images.unsplash.com/photo-1631295868223-63265b40d9e4?w=800'
            },
            # 新增日系豪华品牌
            {
                'name': '雷克萨斯 LS',
                'brand': '雷克萨斯',
                'model': '500h',
                'year': 2023,
                'price': 1148000.00,
                'description': '雷克萨斯LS是品牌旗舰轿车，采用3.5L V6混合动力系统，完美展现日式工艺与科技的结合。',
                'image_url': 'https://images.unsplash.com/photo-1619682817481-e994891cd1f5?w=800'
            },
            {
                'name': '英菲尼迪 QX60',
                'brand': '英菲尼迪',
                'model': 'SENSORY',
                'year': 2023,
                'price': 498800.00,
                'description': '全新英菲尼迪QX60采用2.5T增压发动机，配备智能四驱系统，为家庭用户提供豪华与实用的完美平衡。',
                'image_url': 'https://images.unsplash.com/photo-1600705722908-bab2ad1a6919?w=800'
            },
            # 新能源汽车品牌
            {
                'name': '蔚来 ET7',
                'brand': '蔚来',
                'model': '首发版',
                'year': 2023,
                'price': 458000.00,
                'description': '蔚来ET7是品牌旗舰轿车，搭载150kWh超长续航电池包，NEDC续航里程可达1000公里，百公里加速3.8秒。',
                'image_url': 'https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800'
            },
            {
                'name': '小鹏 P7',
                'brand': '小鹏',
                'model': '四驱高性能版',
                'year': 2023,
                'price': 349900.00,
                'description': '小鹏P7采用双电机全时四驱系统，最大功率430kW，百公里加速4.1秒，NEDC续航里程562公里。',
                'image_url': 'https://images.unsplash.com/photo-1619767886558-efdc259b6e09?w=800'
            },
            # 韩系高端品牌
            {
                'name': '捷尼赛思 G80',
                'brand': '捷尼赛思',
                'model': '豪华版',
                'year': 2023,
                'price': 499800.00,
                'description': '捷尼赛思G80是现代汽车集团的豪华品牌旗舰，搭载3.5T V6发动机，最大功率380马力，展现韩系豪华新风范。',
                'image_url': 'https://images.unsplash.com/photo-1600705722908-bab2ad1a6919?w=800'
            },
            # 运动型轿车
            {
                'name': '阿尔法·罗密欧 Giulia',
                'brand': '阿尔法·罗密欧',
                'model': 'Quadrifoglio',
                'year': 2023,
                'price': 888000.00,
                'description': 'Giulia Quadrifoglio搭载2.9升V6双涡轮增压发动机，最大功率510马力，百公里加速3.9秒，完美诠释意大利运动精神。',
                'image_url': 'https://images.unsplash.com/photo-1606220838315-056192d5e927?w=800'
            },
            # 豪华SUV
            {
                'name': '路虎 揽胜',
                'brand': '路虎',
                'model': 'SV Autobiography',
                'year': 2023,
                'price': 2980000.00,
                'description': '全新一代路虎揽胜采用4.4升V8双涡轮增压发动机，配备全地形反馈2系统，展现顶级豪华与越野性能的完美结合。',
                'image_url': 'https://images.unsplash.com/photo-1606016159991-dfe4f2746ad5?w=800'
            }
        ]

        # 确保media/cars目录存在
        cars_media_dir = os.path.join(settings.MEDIA_ROOT, 'cars')
        os.makedirs(cars_media_dir, exist_ok=True)

        for car_data in cars_data:
            # 检查车辆是否已存在
            if not Car.objects.filter(name=car_data['name'], brand=car_data['brand']).exists():
                # 下载图片
                response = requests.get(car_data['image_url'])
                if response.status_code == 200:
                    # 创建一个临时的BytesIO对象
                    img_temp = BytesIO(response.content)
                    
                    # 从URL中获取文件名
                    image_name = f"{car_data['brand']}_{car_data['name']}.jpg"
                    
                    # 创建新的车辆记录
                    car = Car(
                        name=car_data['name'],
                        brand=car_data['brand'],
                        model=car_data['model'],
                        year=car_data['year'],
                        price=car_data['price'],
                        description=car_data['description']
                    )
                    
                    # 保存图片
                    car.image.save(image_name, File(img_temp), save=True)
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'成功添加车辆: {car_data["brand"]} {car_data["name"]}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'下载图片失败: {car_data["brand"]} {car_data["name"]}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'车辆已存在: {car_data["brand"]} {car_data["name"]}')
                ) 