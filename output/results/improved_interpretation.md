# 族群政治排斥与武装冲突的关系：详细分析

## 1. 描述性统计

- **排除族群比例**: 41.17%
- **包容族群冲突率**: 0.0159
- **排斥族群冲突率**: 0.1071
- **比率**: 排斥族群的冲突率是包容族群的 6.72 倍

### 地理聚集度与排斥状态的交叉分析

| 族群类型 | 地理分散 | 地理聚集 |
|---------|---------|--------|
| 包容族群 | 0.0176 | 0.0158 |
| 排斥族群 | 0.1241 | 0.1057 |

- 对地理分散族群，排斥增加了 0.1065 的冲突概率
- 对地理聚集族群，排斥增加了 0.0900 的冲突概率
- 排斥效应的差异: 0.0165

## 2. 基础模型结果

- **排斥系数**: 2.0025 (+2.0025)
- **p值**: 0.0000
- **显著性**: ***
- **优势比**: 7.4074，表明排斥族群发生冲突的几率是包容族群的 7.41 倍
- **边际效应**: 0.3811

## 3. 完整模型结果

| 变量 | 系数 | 标准误 | p值 | 显著性 |
|------|------|--------|-----|--------|
| excluded | 2.3349 | 0.4130 | 0.0000 | *** |
| geo_concentrated | -0.0859 | 0.3763 | 0.8195 |  |
| upgraded10 | 0.8610 | 0.2274 | 0.0002 | *** |
| excluded:geo_concentrated | -0.0931 | 0.4224 | 0.8255 |  |
| excluded:upgraded10 | -0.8204 | 0.3083 | 0.0078 | *** |

## 4. 交互效应分析

### 地理聚集度的调节作用

- **地理聚集基础效应**: -0.0859
- **排斥基础效应**: 2.3349
- **交互效应**: -0.0931

#### 不同条件下的总效应

| 族群类型 | 地理分散 | 地理聚集 | 差异 |
|---------|---------|--------|------|
| 包容族群 | 0 | -0.0859 | -0.0859 |
| 排斥族群 | 2.3349 | 2.1559 | -0.1790 |
| 排斥的边际效应 | 2.3349 | 2.2418 | -0.0931 |

这表明地理聚集**减弱**了排斥对冲突的影响，即地理聚集的排斥族群与地理分散的排斥族群相比，冲突概率的增加较小。

## 5. 未来冲突分析

- **排斥对未来冲突的系数**: 1.9411
- **p值**: 0.0000
- **显著性**: ***

- **当前vs未来比较**: 排斥对当前冲突的系数为2.0025，对未来冲突的系数为1.9411
  这表明排斥对当前冲突的影响比对未来冲突更强。

## 6. 主要发现总结

1. **排斥显著增加冲突风险**: 被政治排斥的族群确实更容易参与武装冲突，这一效应在统计上高度显著。

2. **地理聚集度的调节作用不显著**: 研究未发现地理聚集对排斥-冲突关系有显著的调节作用。

## 7. 研究问题的直接回答

### 问题：被排斥的族群是否更容易在之后某一年参与武装冲突？

**答案：是的**

研究结果表明，被政治排斥的族群确实更容易在之后参与武装冲突。这一发现具有统计显著性，系数为1.9411，p值为0.0000。

描述性统计显示，排斥族群在未来一年的冲突发生率为0.1036，而包容族群为0.0163，前者是后者的6.35倍。

