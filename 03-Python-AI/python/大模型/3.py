import json
import os
from datasets import Dataset

# 配置
project_dir = "output/legal_consultation_model_cpu"
PROCESSED_DATA_DIR = project_dir + "/data/processed"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# --------------------------
# 直接用你之前的8条数据，不再依赖raw_data.json
# --------------------------
raw_data = [
    {
        "instruction": "你是一名劳动法律师,专门处理劳动合同､工资纠纷等问题｡",
        "input": "公司拖欠3 个月工资,没有劳动合同,怎么维权?",
        "output": "根据《劳动合同法》第82､85 条:1)收集工资转账记录､考勤记录等证据;2)向劳动监察大队投诉(12333)或申请劳动仲裁(免费);3)未签劳动合同可主张最多11 个月双倍工资差额;4)仲裁时效1 年｡建议尽快行动｡"
    },
    {
        "instruction": "你是一名劳动法律师,专门处理劳动合同､工资纠纷等问题｡",
        "input": "试用期被辞退有补偿吗?",
        "output": "根据《劳动合同法》:试用期辞退是否有补偿分情况:1)公司证明不符合录用条件-无补偿;2)公司无法证明或违法辞退-赔偿金1 个月工资;3)经济补偿为半个月工资｡建议要求书面辞退通知,保留证据｡"
    },
    {
        "instruction": "你是一名合同法律师,专门处理租赁､借款等合同纠纷｡",
        "input": "租房合同没到期,房东要卖房让我搬走,怎么办?",
        "output": "根据《民法典》第725 条买卖不破租赁原则:1)您有权继续居住至合同期满;2)您享有优先购买权;3)如被强制清退可报警并起诉索赔;4)协商搬离可要求退还租金､押金及搬家补偿｡保留好合同和付款凭证｡"
    },
    {
        "instruction": "你是一名合同法律师,专门处理租赁､借款等合同纠纷｡",
        "input": "朋友借钱不还,只有微信转账记录,能起诉吗?",
        "output": "可以起诉｡微信转账记录可作为证据,但需补充:1)聊天记录证明借款合意;2)催款记录;3)转账电子凭证｡向被告住所地法院起诉,1 万元以下诉讼费50 元｡诉讼时效3 年｡"
    },
    {
        "instruction": "你是一名婚姻家事律师,专门处理离婚､财产分割等问题｡",
        "input": "离婚时婚前买的房,婚后一起还贷,怎么分割?",
        "output": "根据《民法典》:1)房产归婚前购房方所有;2)婚后共同还贷及增值部分需补偿对方;3)补偿公式:共同还贷本息÷购房总成本×房产现值×50%｡例如共同还贷100 万,购房总价300 万,现值600 万,则补偿约100 万｡保留好还贷记录｡"
    },
    {
        "instruction": "你是一名婚姻家事律师,专门处理离婚､财产分割等问题｡",
        "input": "父母去世没留遗嘱,房产怎么继承?",
        "output": "根据《民法典》继承编:1)第一顺序继承人:配偶､子女､父母,平均分配;2)流程:办理继承公证￫房产过户;3)法定继承免契税､个税;4)如协商不成可向法院起诉｡注意继承时效问题｡"
    },
    {
        "instruction": "你是一名刑事辩护律师,专门处理刑事案件咨询｡",
        "input": "醉驾血液酒精含量150mg/100ml,会怎么判?",
        "output": "根据《刑法》第133 条之一:1)≥80mg/100ml 构成危险驾驶罪;2)150mg/100ml 通常判2-3 个月拘役,可能缓刑,罚金5000-10000 元;3)从重情节:事故､高速驾驶､逃避检查等;4)后果:案底影响子女政审,吊销驾照5 年｡建议委托律师争取不起诉或缓刑｡"
    },
    {
        "instruction": "你是一名消费者权益保护律师｡",
        "input": "网购商品与描述不符,商家不退货怎么办?",
        "output": "根据《消费者权益保护法》:1)网购7 日内可无理由退货(定制､鲜活除外);2)商品不符可要求退货､更换或修理;3)欺诈行为可要求退一赔三(最低500 元);4)维权途径:平台投诉￫12315 投诉￫法院起诉｡保留商品照片､描述截图､聊天记录｡"
    }
]

print(f"原始数据量: {len(raw_data)}")

# 2. 简单过滤(只检查空值)
cleaned_data = []
for ex in raw_data:
    if ex.get("output") and len(ex["output"].strip()) > 10:
        cleaned_data.append(ex)
print(f"清洗后数据量: {len(cleaned_data)}")

# 3. 格式化为文本格式
def format_text(example):
    system = example["instruction"]
    user = example["input"]
    assistant = example["output"]
    text = f"系统指令:{system}\n用户问题:{user}\n法律建议: {assistant}"
    return {"text": text, "system": system, "user": user, "assistant": assistant}

formatted_data = [format_text(ex) for ex in cleaned_data]

# 保存为jsonl 格式
output_file = f"{PROCESSED_DATA_DIR}/train.jsonl"
with open(output_file, "w", encoding="utf-8") as f:
    for item in formatted_data:
        json_line = json.dumps(item, ensure_ascii=False)
        f.write(json_line + os.linesep)

print(f"预处理完成,数据保存至: {output_file}")
print(f" 共{len(formatted_data)} 条训练数据")

# 检查数据文件
print("检查数据文件...")
with open(output_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"总行数: {len(lines)}")
    if lines:
        first_line = lines[0]
        print(f"第一行内容:\n{first_line[:386]}")
        print(f"第一行长度: {len(first_line)}")
        try:
            data = json.loads(first_line)
            print(f"JSON 解析成功!")
            print(f" 键: {list(data.keys())}")
        except json.JSONDecodeError as e:
            print(f"解析失败: {e}")