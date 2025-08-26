from utils.file_utils import load_json_file, save_json_file
from config import Config

class SiteModel:
    """网站数据模型"""
    
    @staticmethod
    def load_site():
        """加载网站数据"""
        data = load_json_file(Config.SITE_FILE)
        return {
            'slider': data.get('slider', []),
            'authors': data.get('authors', [])
        }
    
    @staticmethod
    def save_site(data):
        """保存网站数据"""
        save_json_file(Config.SITE_FILE, data)
    
    @staticmethod
    def get_slider():
        """获取轮播图数据"""
        data = SiteModel.load_site()
        return data.get('slider', [])
    
    @staticmethod
    def set_slider(slider_data):
        """设置轮播图数据"""
        data = SiteModel.load_site()
        data['slider'] = slider_data
        SiteModel.save_site(data)
        return True
    
    @staticmethod
    def get_authors():
        """获取作者列表"""
        data = SiteModel.load_site()
        return data.get('authors', [])
    
    @staticmethod
    def get_author_by_id(author_id):
        """根据ID获取作者"""
        authors = SiteModel.get_authors()
        for author in authors:
            if author.get('id') == author_id:
                return author
        return None
    
    @staticmethod
    def create_author(author_data):
        """创建新作者"""
        data = SiteModel.load_site()
        authors = data.get('authors', [])
        existing_ids = {a.get('id') for a in authors}
        next_id = (max(existing_ids) + 1) if existing_ids and all(isinstance(x, int) for x in existing_ids) else 1
        
        new_author = {
            'id': next_id,
            'name': author_data.get('name', ''),
            'position': author_data.get('position', ''),
            'bio': author_data.get('bio', ''),
            'avatar': author_data.get('avatar', ''),
            'social': author_data.get('social', {})
        }
        authors.append(new_author)
        data['authors'] = authors
        SiteModel.save_site(data)
        return new_author
    
    @staticmethod
    def update_author(author_id, author_data):
        """更新作者信息"""
        data = SiteModel.load_site()
        authors = data.get('authors', [])
        for idx, author in enumerate(authors):
            if author.get('id') == author_id:
                authors[idx] = {**author, **author_data, 'id': author_id}
                data['authors'] = authors
                SiteModel.save_site(data)
                return authors[idx]
        return None
    
    @staticmethod
    def delete_author(author_id):
        """删除作者"""
        data = SiteModel.load_site()
        authors = data.get('authors', [])
        original_count = len(authors)
        authors = [a for a in authors if a.get('id') != author_id]
        
        if len(authors) < original_count:
            data['authors'] = authors
            SiteModel.save_site(data)
            return True
        return False
    
    @staticmethod
    def get_first_author():
        """获取第一个作者（向后兼容）"""
        authors = SiteModel.get_authors()
        if authors:
            return authors[0]
        return {"name": "", "bio": "", "avatar": ""}
    
    @staticmethod
    def set_first_author(author_data):
        """设置第一个作者（向后兼容）"""
        data = SiteModel.load_site()
        authors = data.get('authors', [])
        
        if authors:
            # 更新第一个作者
            authors[0].update({
                'name': author_data.get('name', authors[0].get('name', '')),
                'bio': author_data.get('bio', authors[0].get('bio', '')),
                'avatar': author_data.get('avatar', authors[0].get('avatar', '')),
            })
        else:
            # 创建第一个作者
            authors.append({
                'id': 1,
                'name': author_data.get('name', ''),
                'position': '',
                'bio': author_data.get('bio', ''),
                'avatar': author_data.get('avatar', ''),
                'social': {}
            })
        
        data['authors'] = authors
        SiteModel.save_site(data)
        return authors[0]
    
    @staticmethod
    def init_file():
        """初始化网站文件"""
        if not Config.SITE_FILE.exists():
            SiteModel.save_site({"slider": [], "authors": []})
