from django.core.management.base import BaseCommand
from cars.models import Post, Comment
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = '向数据库添加示例论坛帖子和评论数据'

    def handle(self, *args, **kwargs):
        # 确保有一个管理员用户
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('创建管理员用户: admin'))
        
        # 获取管理员用户
        admin_user = User.objects.get(username='admin')
        
        # 创建一些普通用户
        users = []
        for i in range(1, 6):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'user{i}@example.com',
                    password='password123'
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'创建用户: {username}'))
            else:
                users.append(User.objects.get(username=username))
        
        # 确保至少有一个用户
        if not users:
            users = [admin_user]
        
        # 示例帖子数据
        posts_data = [
            {
                'title': '豪华车选择建议',
                'content': '我打算购买一辆豪华轿车，预算在100万左右。大家有什么推荐吗？我比较看重舒适性和科技配置。目前在考虑奔驰S级和宝马7系。',
                'author': random.choice(users)
            },
            {
                'title': '新能源车真的环保吗？',
                'content': '最近在考虑购买电动车，但听说电池生产和处理过程中的污染其实很严重。想听听大家对这个问题的看法，新能源车整体来说真的比传统燃油车更环保吗？',
                'author': random.choice(users)
            },
            {
                'title': '保时捷911与法拉利F8对比',
                'content': '最近有机会试驾了保时捷911和法拉利F8，想分享一下个人感受。911的操控性更为精准，日常驾驶也更舒适；而F8在极限状态下给人的刺激感更强，声浪也更具吸引力。大家有类似经历吗？',
                'author': random.choice(users)
            },
            {
                'title': '二手车购买攻略',
                'content': '打算购买一辆二手车，但担心踩坑。有什么经验可以分享吗？需要注意哪些问题？特别是如何判断车辆是否有重大事故史，以及如何评估合理价格？',
                'author': random.choice(users)
            },
            {
                'title': '自动驾驶技术的发展前景',
                'content': '随着特斯拉、小鹏等品牌不断推进自动驾驶技术，大家认为完全自动驾驶会在什么时候真正普及？目前各家车企的技术水平如何？欢迎讨论！',
                'author': admin_user
            },
            {
                'title': '轮胎选择与更换经验',
                'content': '最近要给我的SUV更换轮胎，纠结于选择什么品牌和型号。大家有什么推荐吗？我居住在北方，冬季道路条件较差，需要考虑雪地性能。',
                'author': random.choice(users)
            },
            {
                'title': '豪华SUV与轿车的对比',
                'content': '一直在纠结是买豪华SUV还是豪华轿车，预算在80万左右。家里有小孩，但平时也喜欢驾驶乐趣。SUV和轿车各有什么优缺点？',
                'author': random.choice(users)
            },
            {
                'title': '车漆保养小技巧',
                'content': '刚买了一辆新车，想好好保养车漆。有没有一些日常可以做的小技巧？推荐哪些品牌的车蜡或封釉？如何正确洗车才能减少对车漆的伤害？',
                'author': random.choice(users)
            }
        ]
        
        # 示例评论数据
        comments_data = [
            '完全同意你的观点，我有过类似的经历。',
            '谢谢分享，这些信息对我很有帮助。',
            '我持不同意见，我认为...',
            '请问你能提供更多具体细节吗？',
            '这个问题比较复杂，不能一概而论。',
            '我最近也在研究这个问题，找到了一些有用的资料可以分享。',
            '你考虑过其他替代方案吗？比如...',
            '作为这个领域的从业者，我想补充几点专业意见...',
            '我两年前就开始使用这款产品，体验非常好。',
            '价格是一个重要因素，你有没有考虑性价比问题？'
        ]
        
        # 创建帖子
        created_posts = []
        for post_data in posts_data:
            if not Post.objects.filter(title=post_data['title']).exists():
                post = Post.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    author=post_data['author']
                )
                created_posts.append(post)
                self.stdout.write(self.style.SUCCESS(f'成功添加帖子: {post_data["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'帖子已存在: {post_data["title"]}'))
        
        # 为每个帖子添加评论
        for post in created_posts:
            # 每个帖子添加2-5条评论
            num_comments = random.randint(2, 5)
            for _ in range(num_comments):
                Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=random.choice(comments_data)
                )
            
            self.stdout.write(self.style.SUCCESS(f'为帖子 "{post.title}" 添加了 {num_comments} 条评论'))
        
        self.stdout.write(self.style.SUCCESS(f'总共创建了 {len(created_posts)} 个帖子和相应的评论')) 