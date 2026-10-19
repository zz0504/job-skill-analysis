import requests
import os

# 测试文件
test_file = "test_data.csv"

# 检查文件是否存在
if not os.path.exists(test_file):
    # 创建测试文件
    with open(test_file, 'w', encoding='utf-8-sig') as f:
        f.write("岗位名称,公司名称,发布时间,技能要求\n")
        f.write("Java开发工程师,华为,2024-01-15,Java Spring MySQL Redis\n")
        f.write("Python工程师,阿里,2024-01-16,Python Django Flask\n")
    print(f"创建测试文件: {test_file}")

# 测试上传
url = "http://localhost:8000/api/v1/upload/"
print(f"\n上传地址: {url}")
print(f"文件: {test_file}")

try:
    with open(test_file, 'rb') as f:
        files = {'file': (test_file, f, 'text/csv')}
        response = requests.post(url, files=files)
        
    print(f"\n状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ 上传成功!")
        print(f"批次ID: {data.get('batch_id')}")
        print(f"数据条数: {data.get('total_count')}")
    else:
        print(f"\n❌ 上传失败!")
        print(f"错误信息: {response.text}")
        
except Exception as e:
    print(f"\n❌ 请求失败: {e}")
