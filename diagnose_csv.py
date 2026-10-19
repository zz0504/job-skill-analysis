import pandas as pd
import os

test_file = "test_data.csv"

# 查看CSV文件内容
print("=" * 60)
print("1. CSV文件内容:")
print("=" * 60)
with open(test_file, 'r', encoding='utf-8-sig') as f:
    print(f.read())

# 读取CSV
print("\n" + "=" * 60)
print("2. Pandas读取结果:")
print("=" * 60)
try:
    df = pd.read_csv(test_file, encoding='utf-8-sig')
    print(f"列名: {list(df.columns)}")
    print(f"数据:\n{df}")
    
    # 模拟字段映射
    print("\n" + "=" * 60)
    print("3. 字段映射处理:")
    print("=" * 60)
    
    print(f"原始列: {list(df.columns)}")
    
    if '公司名称' in df.columns and '公司' not in df.columns:
        df['公司'] = df['公司名称']
        print(f"✅ 添加'公司'列")
    
    if '技能要求' in df.columns and '技能描述' not in df.columns:
        df['技能描述'] = df['技能要求']
        print(f"✅ 添加'技能描述'列")
    
    print(f"\n处理后列: {list(df.columns)}")
    print(f"\n最终数据:\n{df}")
    
    # 检查必需字段
    print("\n" + "=" * 60)
    print("4. 检查必需字段:")
    print("=" * 60)
    required = ['岗位名称', '公司', '发布时间']
    for field in required:
        exists = field in df.columns
        print(f"{field}: {'✅' if exists else '❌'}")
        
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
