import os
import csv

# 1. 设置路径（确保不管是双击运行还是命令行运行，都能找到）
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, 'data')
output_file = os.path.join(base_dir, '练习.txt')

# 2. 寻找生词表文件
# 优先找 csv，如果没有就找 xlsx（如果不确定，默认用 csv 处理）
data_file = None
for f in os.listdir(data_dir):
    if f.startswith('生词表') and (f.endswith('.csv') or f.endswith('.xlsx')):
        data_file = os.path.join(data_dir, f)
        break

if not data_file:
    print("错误：找不到生词表文件！请检查 data 文件夹里有没有'生词表'。")
    exit()

print(f"找到生词表：{data_file}")
print("开始处理，请稍候...")

# 3. 读取并筛选数据
words = []
try:
    # 尝试按 CSV 读取（如果文件是真正的文本CSV）
    with open(data_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append(row)
except UnicodeDecodeError:
    print("检测到不是标准 CSV 格式，尝试使用 GBK 编码读取...")
    with open(data_file, 'r', encoding='gbk') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append(row)
except Exception as e:
    print(f"读取文件出错，请检查文件格式：{e}")
    exit()

# 4. 过滤出 HSK4 的词
# 这里尝试自动匹配表头名称，兼容 "HSK等级"、"等级"、"级别" 等常见叫法
hsk4_words = []
for w in words:
    # 寻找判定等级的那一列
    level_key = None
    for key in w.keys():
        if '等级' in key or '级别' in key or 'level' in key.lower():
            level_key = key
            break
    
    if level_key:
        # 把 4、4级、HSK4 等等级统一处理
        level_val = str(w[level_key]).strip()
        if '4' in level_val:
            # 寻找词语和词性的列
            word_key = next((k for k in w.keys() if '词' in k and '性' not in k and '等级' not in k), None)
            pos_key = next((k for k in w.keys() if '词性' in k or 'POS' in k), None)
            
            if word_key:
                word = w[word_key]
                pos = w.get(pos_key, '词汇') if pos_key else '词汇'
                hsk4_words.append((word, pos))

# 5. 生成练习文件
with open(output_file, 'w', encoding='utf-8') as f:
    if not hsk4_words:
        f.write("未找到 HSK4 级别的生词。\n")
        print("未找到符合条件的数据，已生成空文件。")
    else:
        for word, pos in hsk4_words:
            f.write(f"请用“{word}”造一个句子。（{pos}）\n")
        print(f"成功生成练习！共找到 {len(hsk4_words)} 个词，结果已保存到：{output_file}")

print("运行结束！")