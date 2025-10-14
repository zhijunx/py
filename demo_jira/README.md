## jira_test.py使用方法
### 登录JIRA账号密码
jira_test.py 目录新建一个**jira_config.ini**配置文件，server写访问主页，用户名写自己邮箱，api_token 写自己密码或者token API，格式参考如下：
```
[jira]
server = https://XXX.atlassian.net
username = XXX@XXX
api_token = password or token API
```
### 设定导出excel表标题行内容
修改**export_jira_to_excel**函数，配置内容如下：
```
事务类型': issue.fields.issuetype,
密钥': issue.key,
摘要': issue.fields.summary,
经办人': getattr(issue.fields.assignee, 'displayName', '未分配'),
报告人': getattr(issue.fields.reporter, 'displayName', '未分配'),
状态': issue.fields.status.name,
已创建': issue.fields.created,
已更新': issue.fields.updated,
优先级': getattr(issue.fields.priority, 'name', '无'),
Issue Severity(严重程度)': issue.fields.customfield_10041,
Reproduce rate(复现概率)': issue.fields.customfield_10030,
```
具体配置字段可查看output.txt文本（执行jira_test.py自动生成)内容

### 过滤jira筛选内容
修改main函数**jql_query**字段，配置内容如下：
```
jql_query = (
    'project IN (FERA, ER23282) AND '
    'type = Bug AND '
    'status IN ("In Progress", Open, NEW, ReOpen, Reject, "NEED MORE INFO", "Pre-Release/临时版本待验", Checking) '
    'ORDER BY created DESC, assignee ASC'
)
```
JQL查询语法可直接复制JIRA系统自己创建好的过滤器JQL语法
