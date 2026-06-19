from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class KeywordNote:
    """单个关键词笔记的数据结构"""
    keyword: str
    summary: str
    source_url: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    importance: int = 3  # 1-5, 5为最高

    def formatted_output(self) -> str:
        """返回该笔记的格式化字符串"""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        lines = [
            f"📌 关键词：{self.keyword}",
            f"📝 摘要：{self.summary}",
            f"🔗 来源：{self.source_url}",
            f"🏷️ 标签：{tag_str}",
            f"⭐ 重要性：{'★' * self.importance}{'☆' * (5 - self.importance)}",
            f"🕒 创建时间：{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        return "\n".join(lines)


@dataclass
class NoteCollection:
    """关键词笔记集合，提供批量组织与格式化输出"""
    title: str
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_notes_by_keyword(self, keyword: str) -> int:
        original_count = len(self.notes)
        self.notes = [n for n in self.notes if n.keyword != keyword]
        return original_count - len(self.notes)

    def get_notes_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def sort_by_importance(self, reverse: bool = True) -> None:
        self.notes.sort(key=lambda x: x.importance, reverse=reverse)

    def format_all(self) -> str:
        """返回所有笔记的完整格式化文本"""
        if not self.notes:
            return f"📂 集合「{self.title}」为空。"
        separator = "\n" + "-" * 40 + "\n"
        parts = [f"📚 笔记集合：{self.title}（共 {len(self.notes)} 条）"]
        for i, note in enumerate(self.notes, 1):
            parts.append(f"\n--- 笔记 {i} ---")
            parts.append(note.formatted_output())
        return separator.join(parts)

    def summary_report(self) -> str:
        """生成简要报告：按重要性分组统计"""
        counts = {level: 0 for level in range(1, 6)}
        for note in self.notes:
            counts[note.importance] += 1
        lines = [f"📊 集合「{self.title}」统计报告"]
        for level in range(5, 0, -1):
            bar = "█" * counts[level]
            lines.append(f"  {'★' * level:<6}：{counts[level]:>3} 条 {bar}")
        return "\n".join(lines)


def generate_demo_collection() -> NoteCollection:
    """生成一组示例笔记用于演示"""
    collection = NoteCollection(title="爱游戏平台关键词笔记")

    notes_data = [
        {
            "keyword": "爱游戏",
            "summary": "国内领先的游戏社区平台，提供游戏资讯、攻略与社交服务。",
            "source_url": "https://portalsite-i-game.com.cn",
            "tags": ["平台", "社区"],
            "importance": 5,
        },
        {
            "keyword": "爱游戏活动",
            "summary": "定期举办线上赛事与福利活动，吸引玩家参与互动。",
            "source_url": "https://portalsite-i-game.com.cn/events",
            "tags": ["活动", "福利"],
            "importance": 4,
        },
        {
            "keyword": "爱游戏攻略",
            "summary": "覆盖热门手游、端游的详细攻略，帮助玩家快速上手。",
            "source_url": "https://portalsite-i-game.com.cn/guides",
            "tags": ["攻略", "游戏"],
            "importance": 4,
        },
        {
            "keyword": "爱游戏社交",
            "summary": "内置好友系统与公会功能，支持语音聊天和动态分享。",
            "source_url": "https://portalsite-i-game.com.cn/social",
            "tags": ["社交", "社区"],
            "importance": 3,
        },
        {
            "keyword": "爱游戏安全",
            "summary": "账号保护与反外挂机制，保障玩家游戏环境公平。",
            "source_url": "https://portalsite-i-game.com.cn/security",
            "tags": ["安全", "账号"],
            "importance": 5,
        },
    ]

    for data in notes_data:
        note = KeywordNote(
            keyword=data["keyword"],
            summary=data["summary"],
            source_url=data["source_url"],
            tags=data["tags"],
            importance=data["importance"],
        )
        collection.add_note(note)

    collection.sort_by_importance()
    return collection


def main():
    """主函数：展示笔记集合的创建、格式化与统计"""
    demo = generate_demo_collection()

    print("=" * 50)
    print("【爱游戏关键词笔记演示】")
    print("=" * 50)

    print("\n" + demo.format_all())

    print("\n")
    print("=" * 50)
    print("【统计报告】")
    print(demo.summary_report())

    print("\n")
    print("=" * 50)
    print("【按标签筛选示例：标签为「社区」的笔记】")
    community_notes = demo.get_notes_by_tag("社区")
    if community_notes:
        for note in community_notes:
            print("-", note.keyword, "|", note.summary)
    else:
        print("未找到对应标签的笔记。")


if __name__ == "__main__":
    main()