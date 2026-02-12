# Mermaid 各类图表语法参考

## 1. 流程图 (Flowchart)

博客场景**优先使用 `graph LR`（横向）**，避免生成过高的竖图。

```mermaid
graph LR
    A["开始"] --> B{"条件判断"}
    B -->|是| C["处理A"]
    B -->|否| D["处理B"]
    C --> E["结束"]
    D --> E
```

**方向关键字：**

| 关键字 | 方向 | 适用场景 |
|--------|------|---------|
| `LR` | 左→右 | 博客文章首选，宽而矮 |
| `RL` | 右→左 | 反向流程 |
| `TD`/`TB` | 上→下 | 层级关系、少节点场景 |
| `BT` | 下→上 | 特殊场景 |

**节点形状：**

```mermaid
graph LR
    A["矩形（默认）"]
    B("圆角矩形")
    C(["体育场形"])
    D[["子程序"]]
    E[("数据库")]
    F{"菱形/判断"}
    G{{"六边形"}}
    H>"旗帜形"]
    I(("圆形"))
```

**连线样式：**

```
A --> B           实线箭头
A --- B           实线无箭头
A -.-> B          虚线箭头
A ==> B           粗线箭头
A -->|标签| B     带标签连线
A -- "标签" --> B  另一种标签写法
```

**子图：**

```mermaid
graph LR
    subgraph 前端
        A["用户界面"] --> B["API 调用"]
    end
    subgraph 后端
        C["路由"] --> D["业务逻辑"] --> E["数据库"]
    end
    B --> C
```

---

## 2. 时序图 (Sequence Diagram)

天然横向布局，适合博客。

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端
    participant D as 数据库

    U->>F: 提交表单
    F->>B: POST /api/data
    B->>D: INSERT 数据
    D-->>B: 成功
    B-->>F: 200 OK
    F-->>U: 显示成功提示
```

**箭头类型：**

```
->>    实线箭头（请求）
-->>   虚线箭头（响应）
-x     实线叉号（失败）
--x    虚线叉号
-)     实线开箭头（异步）
--)    虚线开箭头
```

**高级语法：**

```mermaid
sequenceDiagram
    participant A as 服务A
    participant B as 服务B

    A->>B: 请求
    activate B
    Note right of B: 处理中...
    B-->>A: 响应
    deactivate B

    alt 成功
        A->>B: 确认
    else 失败
        A->>B: 重试
    end

    loop 每5秒
        A->>B: 心跳检测
    end

    opt 可选操作
        A->>B: 日志上报
    end
```

---

## 3. 类图 (Class Diagram)

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
    }
    class Dog {
        +fetch() void
    }
    class Cat {
        +purr() void
    }

    Animal <|-- Dog : 继承
    Animal <|-- Cat : 继承
    Dog "1" --> "*" Toy : 拥有
```

**关系符号：**

```
<|--   继承
*--    组合
o--    聚合
-->    关联
--     链接
..>    依赖
..|>   实现
```

---

## 4. 状态图 (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> 待支付
    待支付 --> 已支付 : 支付成功
    待支付 --> 已取消 : 超时/用户取消
    已支付 --> 配送中 : 发货
    配送中 --> 已完成 : 签收
    配送中 --> 退货中 : 拒收
    退货中 --> 已退款 : 退款完成
    已完成 --> [*]
    已退款 --> [*]
    已取消 --> [*]
```

---

## 5. ER 图 (Entity Relationship)

天然横向，适合博客。

```mermaid
erDiagram
    USER ||--o{ ORDER : "下单"
    ORDER ||--|{ ORDER_ITEM : "包含"
    ORDER_ITEM }o--|| PRODUCT : "关联"

    USER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
        string status
    }
    PRODUCT {
        int id PK
        string name
        float price
    }
```

**关系基数：**

```
||--||   一对一
||--o{   一对多
}o--o{   多对多
||--|{   一对多（至少一个）
```

---

## 6. 甘特图 (Gantt)

天然横向时间轴，适合博客。

```mermaid
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD

    section 需求阶段
        需求分析     :done, a1, 2025-01-01, 7d
        方案设计     :done, a2, after a1, 5d

    section 开发阶段
        前端开发     :active, b1, after a2, 14d
        后端开发     :active, b2, after a2, 14d
        联调测试     :b3, after b1, 7d

    section 上线阶段
        部署上线     :c1, after b3, 3d
```

**任务状态：** `done`（已完成）、`active`（进行中）、`crit`（关键路径）

---

## 7. 思维导图 (Mindmap)

```mermaid
mindmap
    root((项目架构))
        前端
            React
            TypeScript
            Tailwind CSS
        后端
            Python
            FastAPI
            PostgreSQL
        运维
            Docker
            K8s
            CI/CD
```

---

## 8. 饼图 (Pie Chart)

```mermaid
pie title 用户来源分布
    "搜索引擎" : 45
    "社交媒体" : 25
    "直接访问" : 20
    "邮件推广" : 10
```

---

## 博客排版要点

1. **优先横向布局**：流程图用 `graph LR`，天然横向的图表（时序图、甘特图、ER 图）直接使用
2. **控制节点数量**：单图建议不超过 15 个节点，复杂流程拆成多图
3. **文本精简**：节点文本控制在 8 字以内，详细说明放正文
4. **中文引号**：所有中文节点文本用 `[""]` 包裹，避免解析错误
5. **子图分组**：超过 8 个节点时用 `subgraph` 分组，提升可读性
