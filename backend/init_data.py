import os
import sys
import json
import random
from passlib.context import CryptContext

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import (
    SessionLocal, init_db, User, Course, CourseResource, 
    KnowledgeNode, KnowledgeEdge, LearningRecord, Question, 
    ForumPost, StudentAnswer, Notification, ForumReply, PostLike
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def init():
    print("开始初始化全量真实数据...")
    init_db()
    db = SessionLocal()
    
    print("清空旧数据库...")
    try:
        db.query(Notification).delete()
        db.query(PostLike).delete() 
        db.query(ForumReply).delete()
        db.query(StudentAnswer).delete()
        db.query(LearningRecord).delete()
        db.query(KnowledgeEdge).delete()
        db.query(KnowledgeNode).delete()
        db.query(Question).delete()
        db.query(CourseResource).delete()
        db.query(Course).delete()
        db.query(ForumPost).delete()
        db.query(User).delete()
        db.commit()
    except Exception as e:
        print(f"清空数据时遇到轻微错误(可忽略): {e}")
        db.rollback()

    print("👤 创建基础用户 (密码均为 123456)...")
    default_pwd = get_password_hash("123456")
    
    users = [
        User(username="admin", role="admin", full_name="系统管理员", hashed_password=default_pwd),
        User(username="teacher", role="teacher", full_name="张教授", hashed_password=default_pwd),
        User(username="student", role="student", full_name="小明", hashed_password=default_pwd, learn_time=120)
    ]
    db.add_all(users)
    db.commit()

    teacher_id = db.query(User).filter(User.role == "teacher").first().id
    student_id = db.query(User).filter(User.role == "student").first().id

    courses_data = [
        {
            "title": "Python 编程基础",
            "desc": "适合零基础的编程入门课，涵盖变量、循环、函数与面向对象。",
            "nodes": ["变量与类型", "控制流(If/Loop)", "函数(Function)", "类与对象"],
            "resources": [
                {"title": "Python 环境安装指南", "type": "video", "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"},
                {"title": "变量命名规范手册", "type": "document", "url": "#"}
            ],
            "questions": [
                {"q": "Python 中打印输出的函数是？", "opts": ["echo()", "print()", "console.log()", "write()"], "ans": 1},
                {"q": "列表的定义使用什么符号？", "opts": ["()", "{}", "[]", "<>"], "ans": 2},
                {"q": "def 关键字用于定义什么？", "opts": ["类", "变量", "函数", "模块"], "ans": 2}
            ]
        },
        {
            "title": "高中数学：必修一",
            "desc": "深入浅出讲解集合、函数概念及基本初等函数。",
            "nodes": ["集合的概念", "函数的定义域", "指数函数", "对数函数"],
            "resources": [
                {"title": "集合的运算视频", "type": "video", "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"},
                {"title": "函数性质总结.pdf", "type": "document", "url": "#"}
            ],
            "questions": [
                {"q": "集合 {1, 2} 的子集个数是？", "opts": ["2", "3", "4", "5"], "ans": 2},
                {"q": "函数 y=x^2 是什么函数？", "opts": ["奇函数", "偶函数", "非奇非偶", "既奇又偶"], "ans": 1},
                {"q": "log2(8) 的值是？", "opts": ["2", "3", "4", "8"], "ans": 1}
            ]
        },
        {
            "title": "大学物理：力学篇",
            "desc": "涵盖牛顿运动定律、功与能、动量守恒等核心物理概念。",
            "nodes": ["牛顿第一定律", "加速度", "动能定理", "万有引力"],
            "resources": [
                {"title": "牛顿定律演示实验", "type": "video", "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"}
            ],
            "questions": [
                {"q": "力的国际单位是？", "opts": ["焦耳", "瓦特", "牛顿", "帕斯卡"], "ans": 2},
                {"q": "F = ma 是牛顿第几定律？", "opts": ["第一", "第二", "第三", "第四"], "ans": 1},
                {"q": "自由落体的加速度约为？", "opts": ["9.8 m/s²", "10.5 m/s²", "8.9 m/s²", "12 m/s²"], "ans": 0}
            ]
        },
        {
            "title": "英语语法核心突破",
            "desc": "系统讲解时态、语态及从句，助你攻克语法难关。",
            "nodes": ["一般现在时", "现在进行时", "定语从句", "虚拟语气"],
            "resources": [
                {"title": "10分钟搞定时态", "type": "video", "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"}
            ],
            "questions": [
                {"q": "She ___ to school every day.", "opts": ["go", "goes", "going", "gone"], "ans": 1},
                {"q": "I have ___ the book.", "opts": ["read", "reads", "reading", "red"], "ans": 0},
                {"q": "Better late ___ never.", "opts": ["then", "than", "when", "that"], "ans": 1}
            ]
        },
        {
            "title": "世界历史概览",
            "desc": "从古文明到现代社会，探索人类历史的重大转折点。",
            "nodes": ["古埃及文明", "罗马帝国", "工业革命", "二战史"],
            "resources": [
                {"title": "二战纪录片片段", "type": "video", "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"}
            ],
            "questions": [
                {"q": "工业革命起源于哪个国家？", "opts": ["美国", "法国", "英国", "德国"], "ans": 2},
                {"q": "二战结束于哪一年？", "opts": ["1943", "1944", "1945", "1946"], "ans": 2},
                {"q": "金字塔是哪个文明的象征？", "opts": ["古印度", "古埃及", "古巴比伦", "古中国"], "ans": 1}
            ]
        },
        {
            "title": "化学基础：元素与反应",
            "desc": "探索微观世界，理解原子结构与化学反应原理。",
            "nodes": ["元素周期表", "原子结构", "化学键", "氧化还原反应"],
            "resources": [
                {"title": "神奇的化学反应", "type": "video", "url": "https://media.w3.org/2010/05/sintel/trailer.mp4"}
            ],
            "questions": [
                {"q": "水的化学式是？", "opts": ["H2O", "CO2", "O2", "NaCl"], "ans": 0},
                {"q": "原子核由什么组成？", "opts": ["质子和电子", "质子和中子", "中子和电子", "只有质子"], "ans": 1},
                {"q": "PH值小于7表示溶液呈？", "opts": ["酸性", "碱性", "中性", "未知"], "ans": 0}
            ]
        }
    ]

    for c_data in courses_data:
        print(f"📚 创建课程: {c_data['title']}...")
        course = Course(
            title=c_data['title'],
            description=c_data['desc'],
            teacher_id=teacher_id,
            status="published"
        )
        db.add(course)
        db.commit()

        for res in c_data['resources']:
            db.add(CourseResource(
                course_id=course.id, 
                title=res['title'], 
                type=res['type'], 
                url=res['url']
            ))

        for q in c_data['questions']:
            db.add(Question(
                course_id=course.id,
                content=q['q'],
                options_json=json.dumps(q['opts'], ensure_ascii=False),
                correct_answer=q['ans'],
                type="choice" 
            ))
            
        nodes = []
        for i, label in enumerate(c_data['nodes']):
            node = KnowledgeNode(
                course_id=course.id,
                label=label,
                weight=1.0 + (i * 0.2)
            )
            nodes.append(node)
        db.add_all(nodes)
        db.commit()

        for i in range(len(nodes) - 1):
            db.add(KnowledgeEdge(
                source_id=nodes[i].id,
                target_id=nodes[i+1].id,
                relation_type="prerequisite"
            ))

        if "Python" in c_data['title']:
            db.add(LearningRecord(
                student_id=student_id,
                knowledge_node_id=nodes[0].id,
                mastery_level=1.0,
                status="mastered"
            ))

    print("创建社区讨论...")
    posts = [
        ForumPost(title="Python 列表推导式怎么用？", content="求大佬解释一下列表推导式的语法...", author_id=student_id),
        ForumPost(title="牛顿第三定律的适用范围", content="在非惯性系下还成立吗？", author_id=student_id),
        ForumPost(title="欢迎各位同学！", content="我是张老师，有问题随时在讨论区提问。", author_id=teacher_id, type="notice")
    ]
    db.add_all(posts)
    
    db.commit()
    db.close()
    print("\n全量真实数据初始化完成！")
    print("--------------------------------")
    print("学生账号: student  / 123456")
    print("教师账号: teacher  / 123456")
    print("管理员:   admin    / 123456")
    print("--------------------------------")

if __name__ == "__main__":
    init()