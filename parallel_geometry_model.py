import numpy as np
import random
 
class ParallelGeometryModel:
    def __init__(self):
        self.concepts = {}  # {名词: {"type": "A/B/C/D", "vec": np.array}}
        self.init_knowledge_base()

    def init_knowledge_base(self):
        """手动初始化一些名词（对应论文的A/B/C/D分类）"""
        base = {
            # A型：具体静态场景
            "草": "A", "树": "A", "蛋": "A", "笔": "A",
            # B型：动态过程
            "呼吸": "B", "跑步": "B", "吃饭": "B", "地震": "B",
            # C型：静态抽象（结构、关系）
            "体积": "C", "大小": "C", "形状": "C", "位置": "C",
            # D型：动态抽象（性质、机制）
            "力量": "D", "美丽": "D", "统一": "D", "和谐": "D",
            # 扩展一些接地气示例（可继续加）
            "广场舞": "B", "烧烤": "B", "电动车": "A", "大妈": "A",
            "盒饭": "A", "KTV": "B", "上班": "B", "睡觉": "B",
        }
        
        for word, typ in base.items():
            # 随机生成3维向量（实际可升级到768维）
            vec = np.random.randn(3)
            vec = vec / np.linalg.norm(vec)  # 单位向量
            self.concepts[word] = {"type": typ, "vec": vec}

    def cosine_similarity(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)

    def detect_parallel_patterns(self, threshold=0.92):
        """检测平行模式（相似度高 → 平行线）"""
        parallels = []
        keys = list(self.concepts.keys())
        for i in range(len(keys)):
            for j in range(i+1, len(keys)):
                w1, w2 = keys[i], keys[j]
                sim = self.cosine_similarity(self.concepts[w1]["vec"], self.concepts[w2]["vec"])
                if sim > threshold:
                    parallels.append((w1, w2, sim, self.concepts[w1]["type"]))
        return parallels

    def apply_knowledge_gravity(self, parallels):
        """知识引力：平行概念互相拉近"""
        for w1, w2, sim, _ in parallels:
            v1 = self.concepts[w1]["vec"]
            v2 = self.concepts[w2]["vec"]
            avg = (v1 + v2) / 2
            self.concepts[w1]["vec"] = v1 * 0.85 + avg * 0.15
            self.concepts[w2]["vec"] /= np.linalg.norm(self.concepts[w2]["vec"])
            self.concepts[w1]["vec"] /= np.linalg.norm(self.concepts[w1]["vec"])

    def think(self, input_text):
        """模拟思考：输入句子 → 找平行 → 施加引力 → 输出洞见"""
        print(f"\n【输入】{input_text}")
        
        # 简单分词（实际可用 jieba，这里用空格/逗号拆）
        words = [w.strip() for w in input_text.replace("，", " ").replace("。", " ").split() if w in self.concepts]
        
        if not words:
            return "没有识别到知识库里的名词～"
        
        parallels = self.detect_parallel_patterns()
        self.apply_knowledge_gravity(parallels)
        
        print("【检测到平行模式】（共性产生平行线）")
        for w1, w2, sim, typ in parallels[:5]:  # 显示前5条
            print(f"   {w1}（{typ}） || {w2}  相似度 {sim:.3f}")
        
        insight = random.choice([
            "这些平行概念在引力作用下正在融合成更高层认知！",
            "知识引力已将它们拉近，形成新的四维基础设施片段。",
            "大脑正在构建平行模式网络……思考已启动！"
        ])
        print(f"【AI思考输出】{insight}")
        return "思考完成！知识几何结构已更新。"

# 运行演示
if __name__ == "__main__":
    model = ParallelGeometryModel()
    print("=== 平行几何知识模型 v0.1 已启动 ===\n")
    print("基于论文核心：A/B/C/D名词 + 平行模式 + 知识引力\n")
    
    tests = [
        "草和树在广场舞旁边",
        "体积和大小影响美丽",
        "呼吸和跑步在烧烤摊发生",
        "力量和统一带来和谐",
        "大妈和广场舞产生力量"
    ]
    
    for t in tests:
        model.think(t)
