import os
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

# 指定输出目录
results_dir = r'D:\大學用\資料結構\期末\results'

# 创建目录
os.makedirs(results_dir, exist_ok=True)

# 设置 output_dir 为新创建的目录路径
output_dir = results_dir

# 第1步：读取CSV文件
data = pd.read_csv('DSfinal - 工作表1.csv')

# 第2步：预处理数据
def preprocess_data(row):
    return f"在{row['地點']}，温度是{row['溫度(°C)']}，濕度是{row['濕度']}，時間是{row['時間']}，冷氣狀況是{row['冷氣狀況(12燈)']}，除濕機狀況是{row['除濕機狀況(16燈)']}，空氣品質是{row['空氣品質']}。"

data['text'] = data.apply(preprocess_data, axis=1)

# 第3步：创建训练数据集和测试数据集
train_data, test_data = train_test_split(data['text'], test_size=0.2, random_state=42)

# 将训练数据和测试数据保存为文本文件
os.makedirs('data', exist_ok=True)
with open('data/train.txt', 'w', encoding='utf-8') as f:
    for item in train_data:
        f.write("%s\n" % item)

with open('data/test.txt', 'w', encoding='utf-8') as f:
    for item in test_data:
        f.write("%s\n" % item)

# 第4步：选择模型和框架
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# 创建数据集
train_dataset = TextDataset(tokenizer=tokenizer, file_path='data/train.txt', block_size=128)
test_dataset = TextDataset(tokenizer=tokenizer, file_path='data/test.txt', block_size=128)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 第5步：设置训练参数并开始训练
training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()
