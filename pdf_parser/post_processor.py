import re

def _is_header_footer(line: str):
    """过滤页眉页脚规则"""
    patterns = [
        r"第\s*\d+\s*页",  # 中文页码
        r"Page\s*\d+",    # 英文页码
        r"©\s*\d{4}.*",  # 版权声明
    ]
    return any(re.match(p, line.strip()) for p in patterns)

def reorganize_tables(text: str):
    """表格结构优化"""
    # 检测marker生成的表格
    table_blocks = re.findall(r"<table>(.*?)</table>", text, re.DOTALL)
    for table in table_blocks:
        # 转换为标准markdown表格
        processed_table = convert_to_markdown_table(table)
        text = text.replace(f"<table>{table}</table>", processed_table)
    return text


def convert_to_markdown_table(table_html: str):
    """将HTML表格转换为标准Markdown格式"""
    # 提取表格内容
    rows = re.findall(r"<tr>(.*?)</tr>", table_html, re.DOTALL)
    markdown_rows = []
    
    for i, row in enumerate(rows):
        # 提取单元格内容
        cells = re.findall(r"<td.*?>(.*?)</td>", row, re.DOTALL)
        cleaned_cells = [re.sub(r"\s+", " ", cell.strip()) for cell in cells]
        
        # 构造Markdown行
        markdown_row = "| " + " | ".join(cleaned_cells) + " |"
        markdown_rows.append(markdown_row)
        
        # 添加表头分隔线
        if i == 0:
            markdown_rows.append("|" + "|".join(["---"] * len(cells)) + "|")

    return "\n".join(markdown_rows)