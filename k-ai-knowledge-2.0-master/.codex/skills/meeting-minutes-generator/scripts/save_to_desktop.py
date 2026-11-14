import sys
from datetime import datetime
from pathlib import Path


def get_desktop_path() -> Path:
    """获取当前用户的桌面目录。"""
    home = Path.home()

    for desktop_name in ("Desktop", "桌面"):
        desktop = home / desktop_name
        if desktop.exists():
            return desktop

    desktop = home / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    return desktop


def save_meeting_minutes(content: str, filename: str | None = None) -> Path:
    """将会议纪要保存到桌面。"""
    content = content.strip()

    if not content:
        raise ValueError("会议纪要内容不能为空")

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"会议纪要_{timestamp}.md"

    if not filename.lower().endswith(".md"):
        filename += ".md"

    file_path = get_desktop_path() / filename
    file_path.write_text(content, encoding="utf-8")

    return file_path


def main() -> None:
    """
    参数格式：

    python upload.py "会议纪要内容"
    python upload.py "会议纪要内容" "文件名.md"
    """
    if len(sys.argv) < 2:
        print(
            '使用方式：python upload.py "会议纪要内容" ["文件名.md"]',
            file=sys.stderr,
        )
        sys.exit(1)

    # 第一个参数：Codex 传入的会议纪要内容
    meeting_content = sys.argv[1]

    # 第二个参数：可选文件名
    filename = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        saved_path = save_meeting_minutes(
            content=meeting_content,
            filename=filename,
        )
        print(f"保存成功：{saved_path}")

    except Exception as error:
        print(f"保存失败：{error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()