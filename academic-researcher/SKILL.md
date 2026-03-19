---
name: academic-researcher
description: |
  学术研究入口：文献综述、论文分析、学术写作等。涉及 arxiv 论文获取时，调用 arxiv-paper-reader skill。
  Use when: 文献综述、论文总结、方法论分析、引用格式、研究提案，或用户提及学术研究、论文、科学文献。
license: MIT
metadata:
  author: awesome-llm-apps
  version: "1.0.0"
---

# Academic Researcher

学术研究助手，作为多种学术任务的统一入口。

## 使用场景

- 文献综述
- 论文总结与分析
- 研究方法论分析
- 学术论证与结构
- 引用格式（APA、MLA、Chicago 等）
- 研究空白识别
- 研究提案撰写

## ArXiv 论文获取

当用户提供 arxiv URL（如 `arxiv.org/abs/2401.12345`）、论文 ID，或要求读取、解释、总结某篇 arxiv 论文时：

**应调用 `arxiv-paper-reader` skill**（`.agents/skills/arxiv-paper-reader/SKILL.md`）

该 skill 负责：从 AlphaXiv 获取结构化概览、必要时阅读 TeX 源码、生成总结报告。

## Paper Analysis Framework

When reviewing academic papers, address:

### 1. **Research Question & Significance**
- What is the core research question?
- Why does this research matter?
- What gap does it fill?
- How does it contribute to the field?

### 2. **Methodology**
- What research design was used?
- What is the sample/dataset?
- What are the key variables?
- Are methods appropriate for the question?
- What are methodological limitations?

### 3. **Key Findings**
- What are the main results?
- Are results statistically significant?
- How strong is the effect size?
- Are findings consistent with hypotheses?

### 4. **Interpretation & Implications**
- How do authors interpret results?
- What are theoretical implications?
- What are practical applications?
- How does this relate to prior research?

### 5. **Limitations & Future Directions**
- What are study limitations?
- What questions remain?
- What should future research address?

## Citation Formats

### APA (7th Edition)
```
Journal article:
Author, A. A., & Author, B. B. (Year). Title of article. Title of Periodical, volume(issue), pages. https://doi.org/xxx

Book:
Author, A. A. (Year). Title of book (Edition). Publisher.
```

### MLA (9th Edition)
```
Journal article:
Author Last Name, First Name. "Title of Article." Title of Journal, vol. #, no. #, Year, pages.

Book:
Author Last Name, First Name. Title of Book. Publisher, Year.
```

### Chicago (17th Edition - Notes)
```
Footnote:
1. First Name Last Name, "Title of Article," Title of Journal vol, no. # (Year): pages.

Bibliography:
Last Name, First Name. "Title of Article." Title of Journal vol, no. # (Year): pages.
```

## Literature Review Structure

```markdown
## Introduction
- Define the research question or topic
- Explain significance and scope
- Preview organization

## Theoretical Framework  
- Key theories and concepts
- How they relate to the topic

## [Theme 1]
- Synthesize relevant studies
- Note patterns and trends
- Identify agreements and disagreements

## [Theme 2]
[Continue for each theme/subtopic]

## Research Gaps
- What's missing from current literature
- Limitations of existing studies
- Opportunities for future research

## Conclusion
- Summary of key insights
- Implications for theory and practice

## References
[Formatted citation list]
```

## Academic Writing Standards

### Language
- Use precise, formal language
- Avoid colloquialisms and contractions
- Write in third person (or first person plural for own research)
- Use discipline-specific terminology correctly

### Argumentation
- Make claims supported by evidence
- Acknowledge counterarguments
- Distinguish between fact and interpretation
- Note study limitations honestly

### Structure
- Clear topic sentences
- Logical flow between paragraphs
- Smooth transitions
- Parallel structure in lists

## Output Format

For paper summaries:

```markdown
## Citation
[Full formatted citation]

## Research Question
[What the study investigates]

## Methodology
- **Design**: [Experimental, survey, qualitative, etc.]
- **Participants/Data**: [Sample description]
- **Measures**: [Key variables and instruments]
- **Analysis**: [Statistical or analytical methods]

## Key Findings
1. [Main finding with brief explanation]
2. [Second finding]
3. [Additional findings]

## Significance
[Why this research matters]

## Limitations
- [Methodological limitation]
- [Generalizability concerns]
- [Other caveats]

## Future Directions
[Suggested areas for future research]

## Personal Notes
[Optional: Connections to other work, questions, critiques]
```