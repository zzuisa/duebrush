import json
from utils.file_utils import load_json_file, save_json_file
from config import Config

class PaintingModel:
    """绘画数据模型"""
    
    @staticmethod
    def load_paintings():
        """加载所有绘画数据"""
        data = load_json_file(Config.PAINTINGS_FILE)
        return data.get('paintings', [])
    
    @staticmethod
    def save_paintings(paintings):
        """保存绘画数据"""
        data = {'paintings': paintings}
        save_json_file(Config.PAINTINGS_FILE, data)
    
    @staticmethod
    def get_by_id(painting_id):
        """根据ID获取绘画"""
        paintings = PaintingModel.load_paintings()
        for painting in paintings:
            if painting.get('id') == painting_id:
                return painting
        return None
    
    @staticmethod
    def create(painting_data):
        """创建新绘画"""
        paintings = PaintingModel.load_paintings()
        existing_ids = {p.get('id') for p in paintings}
        next_id = (max(existing_ids) + 1) if existing_ids and all(isinstance(x, int) for x in existing_ids) else 1
        
        new_painting = {**painting_data, 'id': next_id}
        paintings.append(new_painting)
        PaintingModel.save_paintings(paintings)
        return new_painting
    
    @staticmethod
    def update(painting_id, painting_data):
        """更新绘画"""
        paintings = PaintingModel.load_paintings()
        for idx, painting in enumerate(paintings):
            if painting.get('id') == painting_id:
                paintings[idx] = {**painting, **painting_data, 'id': painting_id}
                PaintingModel.save_paintings(paintings)
                return paintings[idx]
        return None
    
    @staticmethod
    def delete(painting_id):
        """删除绘画"""
        paintings = PaintingModel.load_paintings()
        original_count = len(paintings)
        paintings = [p for p in paintings if p.get('id') != painting_id]
        
        if len(paintings) < original_count:
            PaintingModel.save_paintings(paintings)
            return True
        return False
    
    @staticmethod
    def init_file():
        """初始化绘画文件"""
        if not Config.PAINTINGS_FILE.exists():
            PaintingModel.save_paintings([])
