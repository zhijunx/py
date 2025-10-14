# only test jira
# 首先安装所需的库
# pip install jira pandas openpyxl xlsxwriter

# DOC REF
# https://jira.readthedocs.io/installation.html
# https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#about
# https://pandas.pydata.org/docs/reference/io.html
# https://www.runoob.com/pandas/pandas-excel.html
# https://xlsxwriter.readthedocs.io/worksheet.html

from jira import JIRA
from jira.exceptions import JIRAError
from jira.resources import User
import configparser
import os
import pandas as pd
import json
from datetime import datetime

def load_config():
    config = configparser.ConfigParser()
    config_paths = [
        './jira_config.ini',
    ]
    for path in config_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            config.read(expanded_path)
            return config
    raise FileNotFoundError("未找到配置文件")

def get_jira_from_config():
    try:
        config = load_config()

        jira_config = config['jira']
        jira = JIRA(
            server=jira_config['server'],
            basic_auth=(jira_config['username'], jira_config['api_token']),
            timeout=10
        )
        print(f"JIRA服务器: {jira.server_url}")
        print(f"当前用户: {jira.current_user()}")
        user_info = jira.myself()
        print(f"登录成功! 用户名: {user_info['displayName']}")
        print(f"邮箱: {user_info['emailAddress']}")
        return jira
    except JIRAError as e:
        print(f"JIRA登录失败: {e.status_code} - {e.text}")
        return False, None
    except Exception as e:
        print(f"其他错误: {e}")
        return False, None

# 获取所有项目
def get_jira_projects(jira_client):
    """获取所有项目信息"""
    try:
        projects = jira_client.projects()
        print("📋 项目列表:")
        for project in projects:
            if ((project.key == 'FERA' and project.name == 'Feraligatr-23282 ') or
                (project.key == 'ER23282' and project.name == 'NothingIOT&BES_23282')):
                print(f"• {project.key}: {project.name}")
                print(f"  类型: {getattr(project, 'projectTypeKey', '未知')}")
                print(f"  ID: {project.id}")
                print()
        return projects
    except JIRAError as e:
        print(f"获取项目失败: {e}")
        return []

# 获取当前用户的所有过滤器
def get_all_filters(jira_client):
    try:
        filters = jira_client.favourite_filters()
        print("📋 所有过滤器:")
        # ID:17896 名称：23282-未修复-filter
        for filter_obj in filters:
            if (filter_obj.name == '23282-未修复-filter'):
                print(f"• ID: {filter_obj.id}")
                print(f"  名称: {filter_obj.name}")
                print(f"  描述: {getattr(filter_obj, 'description', '无描述')}")
                print(f"  所有者: {filter_obj.owner.displayName}")
                print(f"  JQL: {filter_obj.jql}")
                print()
        return filters
    except Exception as e:
        print(f"获取过滤器失败: {e}")
        return []

# 获取当前用户的所有fields
def get_all_fields(jira_client):
    try:
        fields = jira_client.fields()

        data = []
        print("📋 所有fields:")
        for fields_obj in fields:
            data.append(fields_obj)
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(f"fields字段\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            json_str = json.dumps(data, indent=4, ensure_ascii=False)
            f.write(json_str)
            f.write("\n\n" + "=" * 50)
            f.write(f"\nfields字段结束")
        print("数据已保存到 output.txt")

        return fields
    except Exception as e:
        print(f"获取fields失败: {e}")
        return []

def export_jira_to_excel(jira, jql_query, output_file):
    """导出JIRA数据到Excel"""
    try:
        issues = jira.search_issues(jql_query, maxResults=1000)
        # 准备数据
        data = []
        # https://nothingtech.atlassian.net/browse/FERA-2119
        for issue in issues:
            data.append({
                '事务类型': issue.fields.issuetype,
                '密钥': issue.key,
                '摘要': issue.fields.summary,
                '经办人': getattr(issue.fields.assignee, 'displayName', '未分配'),
                '报告人': getattr(issue.fields.reporter, 'displayName', '未分配'),
                '状态': issue.fields.status.name,
                '已创建': issue.fields.created,
                '已更新': issue.fields.updated,
                '优先级': getattr(issue.fields.priority, 'name', '无'),
                'Issue Severity(严重程度)': issue.fields.customfield_10041,
                'Reproduce rate(复现概率)': issue.fields.customfield_10030,
            })
        # 创建DataFrame并导出到Excel
        df = pd.DataFrame(data)

        # 使用ExcelWriter获取工作簿和工作表对象（指定解析引擎使用xlsxwriter）
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:

            df.to_excel(writer, sheet_name='Sheet1', index=False)

            # 获取工作簿对象
            workbook = writer.book
            # print(f"工作簿类型: {type(workbook)}")
            # print(f"工作表名称: {workbook.sheetnames}")

            # 获取工作表对象
            worksheet = writer.sheets['Sheet1']
            # print(f"工作表类型: {type(worksheet)}")

            # 设置 C 列的宽度为 20
            worksheet.set_column('C:C', 20)

            # 创建蓝色下划线格式
            blue_underline_format = workbook.add_format({
                'font_color': 'blue',
                'underline': 1
            })

            # 定义前缀
            prefix = 'https://nothingtech.atlassian.net/browse/'
            # 为第二列添加超链接
            for row in range(1, len(df)+1):  # 从第1行开始（跳过标题行）
                b_column_data = df.iloc[row-1, 1]  # 获取第row行第二列数据（索引从0开始）
                new_b_column_data = prefix + b_column_data
                worksheet.write_url(row, 1, new_b_column_data, blue_underline_format, b_column_data) # 行索引跳过表头

            worksheet.set_column('B:B', 13, blue_underline_format)
            # 保存数据
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            print(f"数据已导出到: {output_file}")
        return []
    except Exception as e:
        print(f"获取issues失败: {e}")
        return []

if __name__ == '__main__':
    print('MAIN_ENTRY')
    jira = get_jira_from_config()
    # projects = get_jira_projects(jira)
    # filters = get_all_filters(jira)
    fields = get_all_fields(jira)
    jql_query = (
        'project IN (FERA, ER23282) AND '
        'type = Bug AND '
        'status IN ("In Progress", Open, NEW, ReOpen, Reject, "NEED MORE INFO", "Pre-Release/临时版本待验", Checking) '
        'ORDER BY created DESC, assignee ASC'
    )
    output_file = "jira_issues.xlsx"
    export_jira_to_excel(jira, jql_query, output_file)

