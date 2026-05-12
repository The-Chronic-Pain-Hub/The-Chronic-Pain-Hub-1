# Module 5 问卷数据录入说明

## 文件位置
📁 `Documents/Module5_Codebook_Simple.xlsx`

## 格式说明

### 只有3列：
1. **Question_ID** - 题目编号 (例如: PHQ_1, IEQ_2)
2. **Question_Text** - 题目文字 (从codebook复制)
3. **Scale_Values** - 量表值 (例如: "1=Not at all, 2=Several Days, 3=More than half the days, 4=Nearly every day")

### 重要规则：
- ✅ **Scale_Values只填第一行** - 每个量表的scale values只需要在第一个题目填写，其他行留空
- ✅ **列宽已自动调整** - 打开就能看清楚内容
- ✅ **一个量表一页** - 每个sheet是一个量表 (PHQ, IEQ, EDS...)

## 操作步骤

### 1. 打开Excel
看看 `PHQ (EXAMPLE)` sheet - 这是已经填好的示例

### 2. 逐个量表填写
比如填写IEQ (Injustice Experience Questionnaire):
```
Question_ID     | Question_Text                                           | Scale_Values
----------------|--------------------------------------------------------|------------------
IEQ_1           | I am suffering because of someone else's negligence    | 1=never, 2=seldom, 3=sometimes, 4=often, 5=all the time
IEQ_2           | It all seems so unfair                                 | (留空)
IEQ_3           | Nothing will ever make up for what I have gone through | (留空)
...
```

### 3. 从Codebook复制内容
打开 `Documents/MTurk_Pain_Codebook_Extracted.txt`，找到对应量表，复制：
- Question ID (如 IEQ_1)
- Question Text (题目文字)
- Scale Values (从SPSS Scoring部分，只第一行需要)

### 4. 多余的行删掉
如果量表只有5题，但Excel给了15行，把多余的删掉

### 5. 保存
直接保存Excel文件

## 导入JSON

研究人员填完后，开发人员运行：
```bash
cd Backend/scripts
python import_simple_excel.py
```

自动生成: `Backend/data/module5_questionnaire_full.json`

## 测试

现在可以用PHQ-9示例测试一下：
```bash
python import_simple_excel.py
```

应该看到：
```
✓ 9 questions
  Scale: 1-4, 4 labels
```

## 量表列表 (35个)

1. PHQ-9 (示例已填) ✅
2. IEQ (12题)
3. EDS (9题)
4. PSEQ (10题)
5. PB-SF
6. SSPQ (5题)
7. SOAPP
8. AFAQ
9. PCS (13题)
10. CPAQ (8题)
... (共35个)

## 常见问题

**Q: Scale_Values格式？**  
A: 用逗号分隔，格式: `1=标签, 2=标签, 3=标签...`

**Q: 如果量表有不同的scale（比如1-9但只标1,3,5,7,9）？**  
A: 也写全部，例如: `1=label, 3=label, 5=label, 7=label, 9=label`

**Q: Reverse coding怎么办？**  
A: 暂时不用管，后续手动调整JSON

**Q: 不确定题数？**  
A: Excel给了15行预留，填多少算多少，多余的删掉

---

**创建日期**: 2026-05-12  
**版本**: v1.0 (简化版)
