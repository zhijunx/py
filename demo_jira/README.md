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

### 选择JIRA过滤器筛选序号
```
0A4455@YFRJ1025 MINGW64 /d/ME/demo/py/demo_jira (main)
$ py test_jira.py
MAIN_ENTRY
JIRA服务器: https://nothingtech.atlassian.net
当前用户: 712020:83091d11-149d-46a2-b390-5d9fc6b05278
登录成功! 用户名: Zhijun Hong_O
邮箱: zhijun.hong_o@nothing.tech
� 所有过滤器:
========================================
� 可供选择的数据键 (Available Keys):
 1. 23282 watched        2. 23282 开发问题数目统计
 3. 23282-BES未修复-filter  4. 23282-ER23282未修复-filter
 5. 23282-JIRA-commet-filter 6. 23282-JIRA-filter
 7. 23282-MP0必解-filter   8. 23282-MP1必解-filter
 9. 23282-MP2必解-filter  10. 23282-NT未修复-filter
11. 23282-NT未修复3/31之前-filter12. 23282-TR4必解问题单-filter
13. 23282-zhijun        14. 23282-严重-filter
15. 23282-严重未修复-filter  16. 23282-已修复-filter
17. 23282-已修复问题单-filter 18. 23282-库总-filter
19. 23282-库总-TR3A-995-filter20. 23282-未修复-filter
21. 23282-未修复pre-release-filter22. 23282-阻塞-filter
23. Feraligatr-23282 block_filter24. Feraligatr-23282 bug分类_filter
25. Feraligatr-23282 critical_filter26. Feraligatr-23282 库总_filter
27. Feraligatr-23282 未解决bug_filter28. NothingIOT&BES_23282 block_filter
29. NothingIOT&BES_23282 critical_filter30. NothingIOT&BES_23282 库总_filter
31. NothingIOT&BES_23282 未修复_filter
========================================

请输入您想查询的键的序号 (例如：1, 2, 3...)：
（输入 'exit or q' 退出程序）
> 3

----------------------------------------
✅ 查询结果 (序号 3）：
键 (Key):   23282-BES未修复-filter
值 (Value): project IN (FERA, ER23282)
AND type = Bug
AND status IN ("In Progress", Open, NEW, ReOpen, Reject, "NEED MORE INFO")
AND assignee IN (712020:6976685a-b8a3-41a2-9d07-749525332e25, 712020:51fdf2c1-0f3f-4c81-8c14-4c9725287805, 712020:2de3457c-ae12-484e-b8f5-0c9f2c51ce53, 712020:38a32a4e-bc
ab-4c67-ba0e-3ed2801be80b)
ORDER BY created DESC (类型: str)
----------------------------------------
� 所有fields:
数据已保存到 output.txt
数据已导出到: jira_issues.xlsx
```
执行脚本后会自动提示选择对应过滤器，比如填写数字3后按Enter按键会自动导出对应JIRA数据
