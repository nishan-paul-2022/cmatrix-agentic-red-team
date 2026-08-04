# WHEN LLMS MEET CYBERSECURITY: A SYSTEMATIC LITERATURE REVIEW 

**Jie Zhang**<sup>1</sup><sup>_,_2</sup> **, Haoyu Bu**<sup>1</sup><sup>_,_2</sup> **, Hui Wen**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **, Yongji Liu**<sup>1</sup><sup>_,_2</sup> **, Haiqiang Fei**<sup>1</sup><sup>_,_2</sup> **, Rongrong Xi**<sup>1</sup><sup>_,_2</sup> **, Lun Li**<sup>1</sup> **, Yun Yang**<sup>1</sup><sup>_,_2</sup> **, Hongsong Zhu**<sup>1</sup><sup>_,_2</sup><sup>_,∗_</sup> **, Dan Meng**<sup>1</sup><sup>_,_2</sup> 

1 Institute of Information Engineering, Chinese Academy of Sciences, Beijing, China 

2 School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China `{zhangjie, wenhui, zhuhongsong}@iie.ac.cn` 

## **ABSTRACT** 

The rapid development of large language models (LLMs) has opened new avenues across various fields, including cybersecurity, which faces an evolving threat landscape and demand for innovative technologies. Despite initial explorations into the application of LLMs in cybersecurity, there is a lack of a comprehensive overview of this research area. This paper addresses this gap by providing a systematic literature review, covering the analysis of over 300 works, encompassing 25 LLMs and more than 10 downstream scenarios. Our comprehensive overview addresses three key research questions: the construction of cybersecurity-oriented LLMs, the application of LLMs to various cybersecurity tasks, the challenges and further research in this area. This study aims to shed light on the extensive potential of LLMs in enhancing cybersecurity practices and serve as a valuable resource for applying LLMs in this field. We also maintain and regularly update a list of practical guides on LLMs for cybersecurity at https://github.com/tmylla/Awesome-LLM4Cybersecurity. 

## **1 Introduction** 

Large language models (LLMs), represented by advanced models such as ChatGPT [1], Llama [2], and their derivatives [3, 4, 5] have marked a significant advancement in artificial intelligence. Leveraging massive data and advanced neural network architectures, these models have demonstrated remarkable capabilities in understanding and generating human language [6, 7]. They not only set new benchmarks for achieving artificial general intelligence (AGI) but also show unique adaptability and effectiveness when collaborating with domain experts [8, 9]. Such research enables LLMs to be tailored to specific challenges in various fields, thereby promoting progress and development in areas such as healthcare, law, education, and software engineering [10, 11, 12, 13, 14, 15]. In the cybersecurity domain, exploring LLM applications can lay the foundations for further model development and utilization while highlighting potential transformative impacts [16, 17, 18, 19, 20]. 

Cybersecurity is a critical issue given the growing number of cyber threats that pose significant risks to individuals, organizations, and governments [21, 22, 23]. The rapid evolution and dynamic nature of cybersecurity pose challenges as adversaries continuously adapt strategies to exploit vulnerabilities and evade detection [24, 25]. While traditional approaches ( _e.g._ , signature-based detection, and rule-based systems) often struggle to keep pace with the evolving threat landscape, advancements in AI, particularly LLMs have opened new avenues for enhancing cybersecurity [26]. On one hand, open-sourced LLMs ( _e.g._ , LLaMA [2, 27]) support the development of cybersecurity-enhanced domain LLMs such as RepairLlama [28] and Hackmentor [29] to address unique cybersecurity challenges. On the other hand, advanced LLMs such as ChatGPT solve complex tasks via prompt engineering, in-context learning, and chains-of-thought despite the lack of cybersecurity-specific training [30]. These preliminary efforts show LLMs can aid cybersecurity tasks with promising results. 

Despite the initial efforts of LLMs in cybersecurity, the field still faces several challenges [17, 31]. First, many studies rely on case studies without comprehensive methodology, raising concerns about scalability and reproducibility. In addition, the field lacks connectivity and in-depth analysis between studies. With the rapid increase in the amount of LLM research in this field, conducting a systematic overview is essential to guide the field into a new stage of 

Table 1: **The main cybersecurity tasks and applications where LLMs have been utilized.** 

||**Vulnerability**<br>**Detection**|**(In)secure**<br>**Code**<br>**Generation**|**Program**<br>**Repairing**|**Binary**|**IT**<br>**Operations**|**Threat**<br>**Intelligence**|**Anomaly**<br>**Detection**|**LLM**<br>**Assisted**<br>**Attack**|**Others**|
|---|---|---|---|---|---|---|---|---|---|
|**RQ1**|✓|✓|✓|✓|✓|-|-|-|✓|
|**RQ2**|✓|✓|✓|-|-|✓|✓|✓|✓|
|**RQ3**|-|-|-|-|✓|-|✓|✓|-|



development, in which the application of LLM is not just experimental but also has strategic impact [18, 19, 20]. Therefore, this work aims to conduct an extensive review of domain-specific LLMs tailored for cybersecurity, explore the breadth of LLM applications in this area, and identify emerging challenges to lay the foundation for future studies. 

This survey aims to provide a comprehensive overview of the application of LLM in cybersecurity. We seek to address three key questions: 

- RQ1: How to construct cybersecurity-oriented domain LLMs? 

- RQ2: What are the potential applications of LLMs in cybersecurity? 

- RQ3: What are the challenge and further research for the application of LLMs in cybersecurity? 

By exploring these questions, we aim to bridge the gap between the advancement in LLMs and its potential impact on enhancing cybersecurity practices. We will delve into various cybersecurity tasks and applications to which LLMs are applicable, including vulnerability detection, secure code generation, program repair, binary, IT operations, threat intelligence, anomaly detection, and LLM-assisted attack, as shown in Table 1. 

For the first question, we summarize the principles of existing cybersecurity LLMs, detailing their key techniques, the data used for model construction, and well-trained domain LLMs for special tasks. We provide insights into constructing domain models, which are valuable for researchers and practitioners looking to build customized LLMs based on specific requirements, such as computational limits, private data, and local knowledge bases (Section 3). For the second question, we conduct an extensive survey on the usage of existing LLMs in more than 10 cybersecurity tasks, including threat intelligence, vulnerability detection, program repairing, and others. This analysis not only helps us understand how LLMs benefit cybersecurity in various aspects but also allows us to identify their strengths when applied to domain-specific tasks. By demonstrating the diverse capabilities of LLMs, we aim to illustrate their potential to enhance and transform the cybersecurity field (Section 4). The third question highlights the challenges that need to be overcome when applying LLMs in cybersecurity. LLMs’ inherent vulnerabilities and susceptibilities lead to these attack challenges, especially attacks against LLMs and LLM jailbreaking. Additionally, we also explore further research directions for applying LLM to cybersecurity, guiding researchers and practitioners to promote advancement in this field (Section 5). 

In summary, this paper contributes by providing a comprehensive review of the state-of-the-art LLM applications in cybersecurity, highlighting the potential advantages and challenges, and proposing future research directions. The subsequent sections of this paper are organized as follows. Section 2 outlines the scope of this paper. Section 3 summarizes existing LLMs for cybersecurity. Section 4 details how LLMs can be applied to various cybersecurity tasks. Section 5 highlights the challenges and promising opportunities for future research. Section 6 draws the conclusion. 

## **2 Preliminary** 

In this review paper, we systematically investigate the application progress of LLMs in cybersecurity, covering more than 300 academic papers since 2023. Through an exhaustive study and comprehensive analysis, we aim to provide a detailed overview of the current state, challenges, and future directions of LLM applications in cybersecurity. As shown in Figure 1, this emerging research field continues to gain attention, and LLM can be used to solve various tasks. This not only highlights the current and potential impact of LLMs in cybersecurity, but also offers practical guidance for future research. Therefore, this section first summarizes the surveyed papers from two aspects: one is the LLMs used in cybersecurity, and the other is the category of cybersecurity tasks to which LLMs can be applied. 

### **2.1 LLMs in Cybersecurity** 

LLMs have emerged as a transformative technology in the field of artificial intelligence, demonstrating remarkable capabilities in natural language understanding, generation, and reasoning [32, 6, 7]. These models, trained with large amounts of data, have the potential to revolutionize various fields, including the critical area of cybersecurity [19, 20]. 

2 


![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0003-00.png)



![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0003-01.png)


<!-- Start of picture text -->
(b) Word cloud<br><!-- End of picture text -->

Figure 1: **Statistic of surveyed papers.** 

The application of LLMs in cybersecurity is expected to enhance threat detection, automated vulnerability analysis, intelligent defense mechanisms, and more. 

LLMs can be categorized into two main types: open-source and closed-source mod ~~<u>el</u>~~ s ~~.~~ Open-source LLMs ( _e.g._ , Llama [2] and Mixtral [5]) provide model weights, and researchers can fine-tune the mo ~~de~~ ls for specific cybersecurity tasks. This adaptability is particularly valuable in cybersecurity scenarios, such as private data and models fine-tuned to customized needs. However, open-source LLMs may lack the performance and scale of closed-source LLMs. On the other hand, closed-source LLMs (often referred to as commercial LLMs, _e.g._ , ChatGPT [1] and Gemini [33]), provide state-of-the-art performance and are maintained by commercial entities, often with access restrictions. While these models excel in accuracy and efficiency, their lack of transparency can raise concerns about potential biases and limitations in cybersecurity applications. 

In the field of cybersecurity, there is a growing need for intelligent tools that can understand, analyze, and generate secure code. Code-based LLMs ( _e.g._ , CodeLlama [34] and StarCoder [35, 36]) are particularly well suited to address this demand. Unlike text-based LLMs are trained on vast amounts of natural language data, code-based LLMs are specifically designed to understand and work with programming languages. Code-based LLMs are trained on large code bases covering multiple programming languages, allowing them to capture the complexity of syntax, semantics, and common coding patterns. This specialized training enables them to perform a variety of tasks, including code completion, bug detection, and automated code review. In the context of cybersecurity, these capabilities are useful for identifying potential vulnerabilities, suggesting secure coding practices, and remediating security vulnerabilities. 

### **2.2 Cybersecurity Categories of LLMs Application** 

Cybersecurity has become a critical concern due to the increasing reliance on interconnected systems and the continued emergence of sophisticated cyber threats [21, 23]. The field of cybersecurity encompasses a wide range of practices, technologies, and strategies aimed at protecting computer systems, networks, and data from unauthorized access, attacks, damage, or disruption [24, 25]. AI techniques, especially LLMs, have shown great potential in revolutionizing various aspects of cybersecurity [20]. The applications of LLMs in cybersecurity are wide-ranging, including threat intelligence, vulnerability detection, malware detection, and anomaly detection, fuzz and program repair, LLM assisted attack(in)secure code generation, and others. 

- Threat Intelligence: It is very difficult to extract information from a large number of threat intelligence documents. Some researchers turn to LLMs to organize and analyze these massive and cluttered data. 

- Vulnerability Detection: This is a critical task in cybersecurity, and has seen novel approaches emerge through the integration of LLMs. 

- Malware Detection: LLMs can serve as both the static analysis assistant and the dynamic debugging assistant, improving the efficiency and effectiveness of the process. 

- Anomaly Detection: It mainly refers to security anomalies such as malicious traffic in the flow, virus files in the system, anomalies in logs, etc. 

3 

Table 2: **A Summary of LLMs used in cybersecurity (this paper).** 

|**Organization**|**LLMs**|**Size**|**Open-Source**|**Count**|**Link**|
|---|---|---|---|---|---|
||GPT-3.5|175B|_×_|86|https://chat.openai.com/|
|OpenAI|GPT-4<br>Codex|-<br>-|_×_<br>_×_|56<br>13|https://chat.openai.com/<br>https://openai.com/blog/openai-codex|
||davinci(-002,-003)|175B|_×_|9|https://openai.com/blog/openai-api|
|Google|Bard&Gemini<br>PaLM(-1,-2)|-<br>540B|_×_<br>_×_|12<br>7|https://gemini.google.com/<br>https://ai.google.dev/models/palm|
|Anthropic|Claude(-1,-2)|-|_×_|2|https://claude.ai/|
|Github|Copilot|-|_×_|2|https://github.com/features/copilot|
|Microsoft|BingChat|-|_×_|2|https://www.bing.com/chat|
|EleutherAI|GPT-J<br>GPT-Neo|6B<br>2.7B|✓<br>✓|2<br>3|https://huggingface.co/EleutherAI/gpt-j-6b<br>https://huggingface.co/EleutherAI/gpt-neo-2.7B|
||Llama(-1,-2)|7B/13B/70B|✓|38|https://huggingface.co/meta-llama|
|Meta|LlamaGuard<br>InCoder|7B<br>1B/6B|✓<br>✓|1<br>4|https://huggingface.co/meta-llama/LlamaGuard-7b<br>https://huggingface.co/facebook/incoder-1B|
|LMSYS|Vicuna|7B/13B|✓|12|https://huggingface.co/lmsys/vicuna-7b-v1.5|
|LianjiaTech|BELLE|7B/13B|✓|1|https://github.com/LianjiaTech/BELLE/|
|Databricks|Dolly|6B|✓|3|https://huggingface.co/databricks/dolly-v1-6b|
|-|Guanaco|7B|✓|2|https://huggingface.co/JosephusCheung/Guanaco|
|Salesforce|CodeGen(-1,-2)<br>CodeT5|3B/7B/16B<br>6B|✓<br>✓|9<br>3|https://github.com/salesforce/CodeGen/<br>https://huggingface.co/Salesforce/codet5p-6b|
|BigCode|StarCoder(-1,-2)|3B/7B/15B|✓|3|https://huggingface.co/bigcode/|
|THUDM|ChatGLM|6B|✓|8|https://github.com/THUDM/ChatGLM-6B|
|KaistAI|Prometheus|7B/13B|✓|1|https://github.com/kaistAI/Prometheus|
|MilAI|Mistral|7B|✓|6|https://huggingface.co/mistralai/Mistral-7B-v0.1|
|stra|Mixtral|8*7B|✓|5|https://huggingface.co/mistralai/Mixtral-8x7B-v0.1|




![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0004-02.png)



![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0004-03.png)



![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0004-04.png)


Figure 2: **Treemap for cybersecurity categories of LLMs’ application.** 

4 

- Fuzz: Traditional fuzzing techniques are effective in discovering software vulnerabilities, but their inherent limitations can affect their efficiency and effectiveness. The LLM-based approach for fuzzing is a promising area of research. 

- Program Repair: Program repair is task-intensive and patching defects requires sufficient experience and knowledge. Many studies have proved the effectiveness of LLMs about this issue. 

- LLM-Assisted Attacks: Many are not satisfied with LLMs’ positive applications. They have discovered the effectiveness of LLMs in launching network attacks such as phishing emails and penetration testing. 

- (In)secure Code Generation: Is there a risk in the code generated by LLMs? Moreover, can LLMs correct their code through some strategies? 

- Others: In addition to the aspects mentioned above, we have also collected some researches which prove the importance of LLMs in the field of cybersecurity, there are fewer application studies of LLM in its field. 

## **3 RQ1: How to construct cybersecurity-oriented domain LLMs?** 

The cybersecurity domain is facing escalating threats, demanding intelligent and efficient solutions to deal with complex and evolving attacks [37, 38, 39]. LLMs provide new opportunities for the cybersecurity community [18, 19]. Trained on massive data, LLMs have acquired rich knowledge and developed strong understanding and reasoning capabilities, providing powerful decision-making for cybersecurity. 

Advancing cybersecurity requires LLMs tailored to the field, leveraging their potential to learn domain-specific data and knowledge. This section firstly introduce several domain datasets for evaluating the cybersecurity capabilities of LLMs [40, 41, 42], which can guide for selecting an appropriate LLM as the base model when constructing cybersecurity LLMs. Then, we focus on key technologies for constructing cybersecurity LLMs, including training methods such as continual pre-training (CPT) [43, 44] and supervised fine-tuning (SFT) [45, 46] of LLMs, as well as technical implementations like full-parameters fine-tuning and parameter-efficient fine-tuning (PEFT) [47]. Finally, we summarize existing customized LLMs for specific cybersecurity tasks [48, 29], including vulnerability detection, program repair, secure code generation, etc. 


![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0005-08.png)


<!-- Start of picture text -->
Cybersecurity knowledge,<br>Secure code generation, IT<br>operations capability, etc.<br>Selection of Base Model (§ 3.1)<br>Continual pre-training(CPT),<br>Supervised fine-tuning(SFT)<br>Full-parameter fine-tuning,<br>RQ1:<br>Key Technologies to Fine-tuning (§ 3.2) Parameter-efficient fine-tuning<br>Cybersecurity<br>Domain LLMs<br>Vulnerability detection,  Secure<br>code generation, Program<br>repair, Binary, IT operation,<br>Cybersecurity knowledge, etc.<br>Fine-tuned Domain LLMs (§ 3.3)<br><!-- End of picture text -->

Figure 3: **An overview of RQ1.** 

### **3.1 Selection of Base Model for Constructing Domain LLM by Evaluating Cybersecurity Capabilities** 

It is challenging to train a cybersecurity LLM from scratch. The general practice is to choose a general-purpose LLM as the base model and then fine-tune it. However, how do we select the appropriate base model among various LLMs? **The basic idea is to choose the LLM with strong cybersecurity capabilities or those that perform well in specific security tasks** . Such models are better at understanding and addressing security-related problems. Existing evaluation of LLM cybersecurity capabilities can be divided into three categories: cybersecurity knowledge, secure code generation, and IT operations capability. 

5 

**Cybersecurity knowledge** evaluation focuses on evaluating the model’s understanding of cybersecurity concepts and its ability to provide accurate information on security threats and mitigation strategies. CyberBench [49] is a domain-specific, multi-task benchmarking tool for evaluating LLMs’ capabilities in cybersecurity tasks. It offers a generic and consistent approach that alleviates the limitations previously encountered in evaluating LLMs in this domain. SecEval [50] is designed to evaluate cybersecurity knowledge in LLMs. It provides more than 2,000 multiple-choice questions in 9 domains: _Software Security, Application Security, System Security, Web Security, Cryptography, Memory Safety, Network Security, and PenTest_ . By facilitating the evaluation of ten state-of-the-art foundational models, this study provides new insights into their performance in the cybersecurity domain. By combining expert knowledge with the collaboration of LLMs, [40] create the CyberMetric benchmark dataset, which contains 10,000 questions and is designed to evaluate the cybersecurity knowledge of various LLMs within the cybersecurity field. SecQA [51] is a dataset of multiple-choice questions generated by GPT-4 based on the textbook “Computer Systems Security: Planning for Success,” which is designed specifically to assess LLMs’ understanding and application of security principles. SecQA provides questions at two tiers of complexity, which can not only serve as an assessment tool but also facilitate the advancement of LLM applications in environments that require a high level of security awareness. In addition, SECURE [52] is a benchmark designed to assess LLMs’ performance in realistic cybersecurity scenarios, which includes 6 datasets to evaluate the capabilities of knowledge extraction, understanding, and reasoning in the Industrial Control System scenarios. 

**Secure code generation** tests the model’s capability to generate code that is not only functional but also adheres to security best practices, aiming to minimize vulnerabilities. CyberSecEval [41] is a security coding benchmark that aims at assessing the potential security risks and tendencies to facilitate cyber attacks when LLMs generate code. By evaluating seven models including Llama 2, Code Llama, and OpenAI’s GPT, CyberSecEval effectively pinpoints key cybersecurity risks and provides practical insights for model improvement. LLMSecEval [42] is a dataset of 150 natural language prompts based on the narrative descriptions of various vulnerabilities that appear in MITRE’s Top 25 Common Weakness Enumeration (CWE) rankings. LLMSecEval evaluates the security of LLM-generated code by comparing it to secure implementation examples for each prompt. SecurityEval [53] focuses on the security evaluation of code generation models to prevent the creation of vulnerable code and thus avoid potential misuse by developers. This dataset includes 130 samples covering 75 types of vulnerabilities mapped to CWE. PythonSecurityEval [54] is a real-world dataset collected from actual scenarios on Stack Overflow, which is designed to evaluate LLMs’ ability to generate secure Python code and their capacity to fix security vulnerabilities. DebugBench [55] has 4,253 instances covering four major bug categories and 18 minor types in C++, Java, and Python. This comprehensive evaluation clarifies the advantages and disadvantages of LLMs in automated debugging, which marks a major step in understanding their applicability and restraint in practical coding scenarios. EvilInstructCoder [56] is designed to assess the cybersecurity vulnerabilities of instruction-tuned Code LLMs to adversarial attacks. By incorporating practical threat models to reflect real-world adversaries with varying capabilities and evaluating the exploitability of instruction-tuned Code LLMs under these diverse adversarial attack scenarios. Eyeballvul [57] is a benchmark designed to test the vulnerability detection capabilities of language models at scale, which have contained 24,000+ vulnerabilities across 6,000+ revisions and 5,000+ repositories. 

**IT operations capability** is used to evaluate the model’s proficiency in managing and securing IT infrastructures, including awareness of security situations, security threat analysis, and incident response. NetEval [58] is an evaluation set designed to measure the common knowledge and reasoning abilities of LLMs in NetOps. This set contains 5,732 questions related to NetOps, covering five different NetOps subdomains. With NetEval, researchers systematically evaluate the NetOps capabilities of 26 publicly available LLMs. Additionally, OpsEval [59] contains 7184 multichoice questions and 1736 question-answering formats in English and Chinese. It aims to analyze the root cause of faults, operational script generation, and alert information summarization to evaluate the performance of LLMs in IT operational tasks comprehensively. [60] develop a thorough framework for evaluating LLMs’ capabilities in various network-related tasks and conduct an exhaustive study on LLMs’ comprehension of computer networks. 

In addition, NYU CTF Dataset [61] and Cybench [62] are used to assess LLMs capacity to solve Capture the Flag (CTF) challenges in cybersecurity, aiming to improve the efficiency of LLMs in interactive cybersecurity tasks and automated task planning. AttackER [63] consists of 18 distinct types of entities, which can be used for entity recognition in attack attribution and investigation tasks, revealing the potential of LLMs capabilities to improve the named entity recognition tasks in cybersecurity datasets. SEvenLLM [64] is a framework to benchmark, elicit, and improve cybersecurity incident analysis and response abilities in LLMs for security events. 

The evaluation of LLMs’ cybersecurity capabilities not only guides the basic model during fine-tuning but also demonstrates that general LLMs have certain cybersecurity capabilities. This supports the feasibility of directly using LLMs (without fine-tuning) to aid cybersecurity applications, as discussed in section 4. Furthermore, these studies help researchers and developers recognize the limitations of LLMs in the field of cybersecurity, thereby providing the direction for artificial intelligence toward higher standards and more professional security development. 

6 

### **3.2 Key Technologies in Constructing Domain LLMs** 

LLMs have demonstrated remarkable language understanding and generation capabilities by leveraging the transformer architecture and self-supervised pre-training strategies [65, 66, 32]. However, developing a specialized LLM for cybersecurity from scratch requires a lot of computational resources, which is impractical for most research teams. Fortunately, existing general LLMs have acquired extensive knowledge and demonstrated excellent generalization capabilities [2, 27, 67, 5]. **By combining these pre-trained LLMs with domain datasets for training, we can adopt a more efficient approach to enhance the model’s cybersecurity capabilities.** This approach not only significantly reduces the computational demands of pre-training, but also maximizes the use of the knowledge that LLMs have learned. Thereby, the model can understand and perform cybersecurity-related tasks, such as automated threat detection, vulnerability identification, and security policy recommendations. 


![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0007-02.png)


<!-- Start of picture text -->
PEFT<br>Small-scale Training Data<br>Low Computational Resources<br>Unlabeled data Labeled Data<br>CPT SFT<br>Broad Knowledge Specific Task<br>High Computational Resources<br>Large-scale Training Data<br>FULL<br><!-- End of picture text -->

Figure 4: **Comparison of Domain LLM Training Approaches** . _CPT_ and _SFT_ offer methods to enhance domainspecific performance based on existing LLMs, while _FULL_ parameter training and _PEFT_ represent different technical pathways within these training processes. 

To apply general LLMs to cybersecurity, researchers mainly employ two approaches: continual pre-training (CPT) and supervised fine-tuning (SFT). 

**Continual pre-training** involves further training of pre-trained LLMs using a large amount of unlabeled domainspecific data [43, 44, 68, 69]. This method aims to improve the model’s understanding and application of domain knowledge, significantly improving its broad applicability within the cybersecurity field. CPT is based on the core assumption that even after extensive pre-training, the model still has the potential for further enhancement, especially in specific domains or tasks. The process usually involves several key steps: first, select a dataset that can appropriately represent the characteristics of the target domain; second, determine the strategy for continuous pre-training; and finally, perform pre-training and adjust the model architecture or optimization algorithm as needed to adapt to the new training objectives. 

**Supervised Fine-Tuning** uses labeled domain-specific data for training, enabling direct optimization of the model’s performance on specific cybersecurity tasks [45, 46]. Compared to CPT, SFT focuses on improving the performance of a specific task. In SFT, the model weights are refined via gradients calculated from a task-specific loss function. This function quantifies the deviation between the model’s predictions and the actual labels, thus promoting the learning of task-oriented patterns. SFT relies on the utilization of high-quality, human-annotated data, which is a collection of prompts and their corresponding responses. SFT is important for LLMs such as ChatGPT, which are designed to follow user instructions and focus on specific tasks in context. This specific type of fine-tuning is also referred to as instruction fine-tuning. 

In the context of CPT and SFT, researchers have the option of employing either full-parameter fine-tuning or parameterefficient fine-tuning (PEFT). 

**Full-parameter fine-tuning** is a classical approach that adjusts all parameters of the model during training. This allows the model to fully adapt and specialize to the target domain. By optimizing all parameters, the model can achieve 

7 

optimal performance for specific tasks or datasets. However, full parameter updates require considerable computing power and time, posing challenges in efficiency and scalability, especially as the number of LLM parameters continues to increase. 

Conversely, **PEFT** methods fine-tune only a small number of model parameters or additional parameters while freezing most parameters of the pre-trained LLMs, which greatly reduces the computational costs. It also helps in portability, and users can fine-tune the model using PEFT methods to obtain tiny checkpoints of only a few MB in size. In summary, PEFT methods are favored because they enable users to obtain comparable performance to full fine-tuning while having only a small number of trainable parameters. There are several PEFT methods, such as adapter tuning, prefix tuning, prompt tuning, LoRA, QLoRA, and so on: 

_Adapter tuning_ [70] inserts adapters after the multi-head attention and feed-forward layers in the transformer architecture, which updates only the parameters in the adapter during fine-tuning while keeping the rest of the model parameters frozen. _P-tuning_ [71] automatically learns optimal task-specific prompt embeddings by introducing trainable prompt tokens, eliminating the need for manual prompt design and potentially improving performance with the addition of anchor tokens. _Prefix tuning_ [72] keeps the language model parameters frozen and optimizes small, continuous, task-specific vectors called prefixes. _Prompt tuning_ [73] fine-tunes for specific tasks through learning soft prompts by backpropagating and merging labeled examples. _LoRA_ [74] is a small trainable submodule that can be inserted into the transformer architecture. It freezes the pre-trained model weights and inserts a trainable low-rank decomposition matrix into each layer of the model, reducing the number of trainable parameters for downstream tasks. After training, the matrix parameters are combined with the original LLM. _QLoRA_ [75] is a further optimization of LoRA, which carries out gradient backpropagation to a low-rank adapter with a frozen 4-bit quantized pre-trained language model, reducing the memory requirement for fine-tuning while being almost comparable to full fine-tuning. 

By integrating these techniques, researchers can select appropriate methods to construct LLMs tailored to the specific needs of the cybersecurity domain, as shown in Figure 4. Furthermore, emerging technologies also provide insights for the construction of cybersecurity LLMs. For example, model editing techniques [76, 77] can precisely modify LLMs to incorporate cybersecurity knowledge without negatively affecting other knowledge. Prompt engineering [78, 79, 80], by designing effective prompts to guide LLMs towards desired outputs, can alleviate the bottleneck of training data and resources required for constructing cybersecurity LLMs. 

### **3.3 Fine-tuned Domain LLMs for Cybersecurity** 

**The researchers have used the above techniques and base models to customize LLMs to address specific problems in the field of cybersecurity.** These efforts highlight the great potential of integrating domain-specific knowledge to enhance the capabilities of LLMs, especially for key applications including vulnerability detection, fault Localization, program repair, and so on. 

**Vulnerability detection** involves identifying and classifying potential security vulnerabilities in software code. [81] fine-tunes WizardCoder [82] with LoRA specifically for vulnerability detection, focusing on the binary classification of whether Java functions contain vulnerabilities. [48] performs partial parameters fine-tuning on FalconLLM [4] using C code samples to obtain SecureFalcon, which can distinguish between vulnerable and non-vulnerable samples with a detection accuracy of up to 96%, and further proposes a method for repairing vulnerabilities using FalconLLM. [83] introduces a new fault localization method based on the language model, named LLMAO. LLMAO adds bidirectional adapter layers on CodeGen [84, 85], enabling the model to learn bidirectional representations of codes and predict the probability of defects in code lines. Detect Llama [86] is fine-tuned on Code-Llama with 17k dataset, outperforming GPT-4 in smart contract vulnerability detection. 

**Secure code generate** via LLMs aims to improve the security of automatically generated code by mitigating vulnerability risks. [87] proposes a new approach called vulnerability-constrained decoding, which integrates vulnerability tags during model training. By avoiding generating code with these labels, the model significantly reduces the generation of vulnerable code. Fine-tuning on GPT-J [88] shows a notable reduction in vulnerabilities in the generated code. [89] focuses on improving the security of code generation by LLMs via instruction tuning. They convert CodeLlama [34] to SafeCoder using supervised fine-tuning on a dataset containing both secure and insecure programs. This approach achieves significant security improvements (approximately 30%) across various popular LLMs and datasets while remaining practical. 

**Automated program repair** aims to automatically fix software bugs without human intervention. [28] proposes a new program repair approach called RepairLLaMA, which significantly improves LLMs’ program repair capabilities by applying LoRA fine-tuning to CodeLlama. It outperforms GPT-4 on the Java benchmarks Defects4J and HumanEvalJava. [90] first creates an instruction dataset APR-INSTRUCTION by using prompt engineering, then fine-tunes LLMs using four different PEFT methods based on this data to improve the model’s automated program repair capabilities. 

8 

**Binary** is the most basic form of computer code, it is important to learn what it means and how to use it. [91] demonstrates the benefits of LLMs for binary analysis. They continually train StarCoder [35, 36] on specialized binary code corpus and new tasks, leading to the development of Nova and Nova<sup>+</sup> . After SFT, the enhanced LLMs effectively address specific tasks such as binary code similarity detection, binary code translation, and binary code recovery. 

**IT operations** manage routine tasks and activities to keep the infrastructure running for other services. [92] describes a specialized LLM for IT operations, named Owl, which is supervised fine-tuned of Llama on the collected Owl-Instruct dataset. Owl outperforms existing models in IT-related tasks and demonstrates effective generalization capabilities on the Owl-Bench benchmark. 

**Cybersecurity knowledge assistants** help to improve users’ security awareness and assist users in defending against cyber attacks through interaction with users. [29] proposes Hackmentor, a cybersecurity knowledge assistant. They develop a dataset of cybersecurity instructions and conversations and train Hackmentor using LoRA by fine-tuning on Llama and Vicuna [3]. CyberPal [93] is fine-tuned using SecKnowledge, a domain knowledge-driven cybersecurity instruction dataset, to build a security-specialized LLM capable of answering and following complex security-related instructions. This demonstrates the potential of LLMs in cybersecurity applications. 

In addition to enhancing the cybersecurity capabilities of general LLMs through SFT and CPT, **specialized securityoriented LLMs can be developed by leveraging innovative model architectures and proprietary large-scale datasets for independent pretraining** . The Machine Language Model (MLM) is a large model designed for the machine language domain, utilizing an innovative architecture to align multimodal data across machine language, natural language, and source code [94, 95, 96]. This approach not only addresses the limitations of existing LLMs in comprehending machine language but also introduces transformative advancements in software reverse engineering and software security detection. TrafficFormer [97] is an efficient pre-training model designed for traffic data. Given the characteristics of traffic data, it introduces fine-grained multi-classification tasks in the pre-training stage to enhance the representation of traffic data; in the fine-tuning stage, it uses the random initialization characteristics of the field to propose a traffic data enhancement method to help the traffic model focus on key information. In this way, the accuracy of the model’s traffic detection and protocol understanding is improved. These developments pave the way for novel research directions in the field of cybersecurity. 

Answer to Q1: For researchers, it is feasible to construct the domain LLM by fine-tuning a general LLM with cybersecurity data using methods such as CPT and SFT, and the implementation technique depends on the specific application scenario, resource availability, and the expected level of performance improvement. 

## **4 RQ2: What are the potential applications of LLMs in cybersecurity?** 

This section introduces the application of LLMs in various cybersecurity tasks, encompassing offline defense ( _e.g._ , threat intelligence), online defense ( _e.g._ , vulnerability detection, malware detection, and anomaly detection), software testing ( _e.g._ , fuzz and program repair), attack assistance ( _e.g._ , LLM assisted attack), source code generation and analysis ( _e.g._ , (in)secure code generation), and other security-related applications ( _e.g._ , honeypot, botnet, SoC security, etc.). By reviewing the key advancements in each topic, this paper aims to offer **a comprehensive perspective on the evolution of the cybersecurity landscape driven by LLMs integration** . 

### **4.1 Threat Intelligence** 

Since LLMs have shown excellent analysis and summarization capabilities in natural language processing tasks, [98] assesses the performance of an LLM system built on the GPT to extract CTI information, highlight the relevance of using LLMs for CTI. More researchers have used LLMs to assist in the generation and analysis of cyber threat intelligence (CTI). 

[99] introduces a framework known as LocalIntel, which aims to provide users with reliable threat intelligence by allowing LLMs to summarize knowledge after querying global and local knowledge databases. Global knowledge mainly refers to well-documented reports on cybersecurity threats from CWE and CVE, while local knowledge is customized by the organization for practical purposes to supplement global knowledge. [100] also conducts similar work to extract security knowledge from a wide range of knowledge bases and automatically generate reports using LLMs. A few similar efforts are as follows. 

[101] employs LLM to generate descriptions of cyber attacks and fine-tune the model using information collected from ATT&CK and CAPEC. Then, they compare the performance of the fine-tuned LLMs with the directly used LLMs (GPT-3.5) in describing attacks. In another work, [102] studies the application of LLMs in cybersecurity to 

9 


![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0010-00.png)


<!-- Start of picture text -->
Assisting the generation of CTI, Assisting the analysis of<br>CTI, LLMs as security response specialist<br>Threat Intelligence (§ 4.1)<br>Vulnerability detection capability assessment of LLMs,<br>Improving detection capabilities through prompt<br>engineering, Vulnerabilities datasets preparation<br>Vulnerability Detection (§ 4.2)<br>Static analysis assistant, Dynamic debugging assistant<br>Malware Detection (§ 4.3)<br>Log-based anomaly detection, Web content security,<br>Digital Forensic<br>Anomaly Detection (§ 4.4)<br>Testing against general APIs, Testing Deep-Learning<br>Libraries, Testing against Protocol, Testing against BusyBox<br>Fuzz (§ 4.5)<br>RQ2:  Evaluation of LLMs' program repair capability, Combined<br>Applications of LLMs  LLM with static analysis tools, Improvement through<br>in Cybersecurity  different strategies, Target-specific program repairing<br>Program Repair (§ 4.6)<br>LLM-Assisted Privilege Escalation Attacks, LLM-Assisted<br>CTF Challenges, LLM-Assisted Phishing Website/Email<br>Generation, LLM-Assisted Payload Generation, LLM-<br>Enabled Automated Penetration Testing, Proxies for Attacks<br>LLM Assisted Attack (§ 4.7)<br>Evaluation of the security of LLM-generated code,<br>Enhancing the security of LLM-generated code, Static<br>analysis assistant, Dynamic debugging assistant<br>(In)secure Code Genaration (§ 4.8)<br>IoT Fingerprint, Botnet, Security Patch Detection, SoC<br>Security, Taint Analysis, Input-Output Safeguard, Honeypot,<br>Incidence Response, Network Management, Vulnerabilities<br>Reproduction, DomainQA, and so on<br>Others (§ 4.9)<br><!-- End of picture text -->

Figure 5: **An overview of RQ2.** 

explain and summarize cyberattack Tactics, Techniques, and Procedures (TTPs) from the MITRE ATT&CK framework. It compares the effectiveness of encoder-only and decoder-only models for TTP analysis and introduces Retrieval Augmented Generation (RAG) to enhance decoder-only models without fine-tuning. The study finds that RAG significantly improves the explanation of TTPs by providing relevant context, highlighting the potential of LLMs in threat intelligence. LMCloudHunter [103] leverages LLMs to automatically generate generic signature detection rule candidates from textual and visual OSCTI data. [104] discusses the capability of LLMs to automatically analyze and summarize software supply chain security vulnerabilities. They evaluate LLMs’ performance in replicating manual assessments of 69 faults, focusing on classification accuracy. The results show that LLMs show good potential, especially when the data is comprehensive, but still cannot replace human analysts in this specific field. [105] evaluates the performance of various LLMs in the field of threat intelligence, including ChatGPT, GPT4all, Dolly, etc. The study examines the capabilities of these chatbots in binary classification and named entity recognition (NER) tasks using a Twitter-based open-source intelligence (OSINT) dataset. While the LLMs demonstrate promising results in binary classification, their effectiveness in NER for cybersecurity entity recognition is limited, which highlights the need for further development of LLM technology to enhance CTI applications. 

Specifically for digital forensics, [106] proposes a method to automate the generation of reports. They study the structure of forensic reports to identify common sections and assess the feasibility of LLMs in generating these sections. Through a case study approach, the article evaluates the strengths and limitations of LLMs in creating different sections of forensic reports. 

Given that most threat intelligence providers offer information in an unstructured format, [107] and [108] propose innovative solutions to the common problem of extracting useful information from unstructured data. The former designs a framework named aCTIon, which includes downloading and parsing raw reports, extracting useful information with LLM, and exporting structured reports following STIX [109] standard. The latter constructs the knowledge graph of unstructured threat intelligence and fine-tunes LLMs to automate information extraction tasks. Also, by leveraging 

10 

the capabilities of LLMs in instruction prompting and in-context learning, [110] propose a fully automatic LLMbased framework, AttacKG, which comprises four consecutive modules: rewriter, parser, identifier, and summarizer, to construct attack knowledge graphs from CTI. [111] explore the application of open-source LLMs for extracting meaningful triples from CTI texts. Then, the extracted data is utilized to construct a knowledge graph, offering a structured and queryable representation of threat intelligence. 

In addition to extracting valuable information from large amounts of text, report deduplication is also an important research focus in this field. [112] uses LLMs to alleviate the problem of bug report deduplication. They leverage LLMs as an intermediate step to improve the performance of REP [113] (a traditional method of measuring the similarity between bug reports) by identifying keywords, thereby improving its effectiveness. 

There are also studies that attempt to use LLMs as experienced security response experts. [114] uses LLMs as suggestion providers to mitigate vulnerabilities through prompt engineering. They design a system that is able to retrieve relative CVE & CWE information after the user enters a vulnerability description. LLMs’ mitigation suggestions are a subcomponent of the system. [115] believes that LLMs are not only question-answering assistants with expertise but also able to perform actions based on the user’s description ( _e.g._ , instructing the host’s intrusion detection system to block a specific IP). To enhance strategic reasoning in cybersecurity, [116] introduces Crimson, a system that uses LLMs to associate CVEs with MITRE ATT&CK techniques to improve threat prediction and defense. The core concept is the Retrieval-Aware Training (RAT) process, which refines LLMs to generate accurate cybersecurity strategies, thereby significantly reducing errors and hallucinations. By integrating real-time data retrieval and domain-specific fine-tuning, Crimson enhances the models’ interpretability and strategic consistency, providing a proactive approach to cybersecurity threat intelligence. [117] develop an AI agent designed to automate the labor-intensive and repetitive tasks associated with analyzing CTI reports. By leveraging the advanced capabilities of LLMs, the AI agent can accurately extract important information from large volumes of text and generate Regex to help SOC analysts accelerate the process of establishing correlation rules. [118] introduces a QA model based on Retrieval Augmented Generation (RAG) techniques together with LLMs and provides answers to the users’ queries based on the knowledge base that contains curated information about cyber-attacks investigations and attribution or on outside resources provided by the users. 

Considering the quality assessment of threat intelligence provided by intelligence platforms, [119] propose a novel CTI quality assessment framework that combines knowledge graphs and LLMs. In this verifier, LLMs automatically extract OSCTI key claims to be verified and utilize a knowledge graph consisting of paragraphs for fact-checking. This significantly improves the performance of LLMs in intelligence quality assessment. 

### **4.2 Vulnerability Detection** 

This section provides an overview of the main studies on vulnerability detection using LLMs. Through these studies, we aim to shed light on the progress, challenges, and future directions of leveraging LLMs to enhance cyber security. 

_(In this section, we blur the concepts of "vulnerability" and "software defect")_ 

**Whether LLMs have the ability to detect vulnerabilities?** The following papers conduct preliminary studies on this question. Although their results may vary due to some unknown reasons ( _e.g._ , they may use different datasets), in general, they all show that LLMs are promising for vulnerability detection [120, 121, 122, 123, 124]. 

[125] initially evaluates whether GPT-3 and GPT-3.5 could identify some known CWE vulnerabilities in Java code. The results show that the application effect in vulnerability detection tasks is not good and needs further improvement and research. In another work, [126] uses LLMs (including GPT-3.5, CodeGen, and GPT-4) to analyze several common vulnerabilities ( _e.g._ , SQL injection, overflow). The conclusion confirms that LLMs do have the ability to detect vulnerabilities, but the false positive rate is high. However, [127] fine-tunes GPT on various vulnerable code benchmarks to detect software vulnerabilities and achieve good performances. Similarly, [128] concludes that LLMs are generally able to perform better vulnerability detection than existing static analysis and deep learning-based tools. With carefully designed prompts, desirable results can be obtained on synthetic datasets, but performance degrades on more challenging real-world datasets. [129] compares the performance of a wide range of open-source and proprietary models with Python code snippets in assisting vulnerability discovery. Their research suggests that LLMs can be effectively used to enhance the efficiency and quality of code reviews, particularly in detecting security issues within software code. [81] fine-tunes WizardCoder for vulnerability detection and investigate whether the encountered performance limit is due to the limited capacity of CodeBERT-like models. Their results suggest that this is indeed the case and that LLMs have great potential for application in vulnerability detection. [130] presents LLift, a framework that leverages LLMs to assist static program analysis, specifically for detecting use-before-initialization (UBI) defects. LLift interacts with static analysis tools and LLMs, demonstrating 50% accuracy in real-world scenarios and identifying 13 previously unknown UBI bugs in the Linux kernel. [131] assess the ability of various LLMs to detect Android code vulnerabilities 

11 

listed in the latest Open Worldwide Application Security Project (OWASP) Mobile Top 10. While the reported findings regarding code vulnerability analysis show promise, they also reveal significant discrepancies among the different LLMs. Moreover, [132] thoroughly analyzes the capabilities of LLMs in detecting vulnerabilities within source code by testing the models beyond their usual applications. It also paves the way for LLM-based vulnerability detection by addressing two key aspects: model training and dataset curation 

**Improving detection capabilities through different strategies.** Instead of directly providing code to LLM and asking it to answer, many researchers would adopt various strategies in advance. They believe that simply providing code is not enough and that the code needs to be further preprocessed or more information needs to be provided to LLMs for vulnerability reasoning. 

[133] proposes a code sequence embedding (CSE) that combines the AST, DFG, and CFG of the code as input to the model. Then, the model captures the semantic information with the help of conformer mechanism [134], an improved architecture of Transformer. [135] not only provides the code to GPT but also provides the API call sequence and data flow diagrams. [136] conducts a similar experiment to compare the performance of the model when different levels of information are given, including asking for the vulnerability point directly, giving some CWE information, and telling LLMs what vulnerabilities are in the code. [137] focuses on Android platform vulnerabilities and compares the performance of LLMs on three conditions: asking LLMs to find vulnerabilities directly, providing vulnerability summaries before asking and granting LLMs permission to request any file in the APK after providing the APK core (AndroidManifest.xml and MainActivity.java). [138] focuses on the security of Android systems against filesystem vulnerabilities. They present PathSentinel, which leverages LLMs to generate targeted exploit code based on the identified vulnerabilities and generated input payloads, reducing the engineering effort required for writing test applications. DLAP [139] combines the advantages of deep learning models for specific tasks and LLM’s powerful general understanding ability, and achieves excellent vulnerability detection performance. [140] reframes vulnerability detection as an anomaly detection task by viewing vulnerable code as an anomaly within the LLM’s predicted code distribution. This approach frees the model from the need for labeled data, allowing it to learn a representation of vulnerable code. Ultimately, it results in a detector that identifies software vulnerabilities at the line-level granularity. 

There are some studies that use retrieval-augmented generation (RAG) based on additional knowledge bases to facilitate LLM for vulnerability detection. [141] explores three different strategies for augmenting both single and multi-statement vulnerabilities using LLMs: Mutation, Injection, and Extension. These strategies potentially alleviate the shortage of data. [142] proposed Vul-RAG, which leverages knowledge-level RAG framework to detect vulnerability. And the vulnerability knowledge generated by Vul-RAG can serve as high-quality explanations to further improve the manual detection accuracy. 

In addition to the above efforts, researchers have also proposed many innovative ideas to improve the vulnerability detection ability of LLMs. [143] proposes an innovative two-stage framework named GPTLENS, which includes two adversarial agent roles: auditor and critic. The auditor performs during the generation phase and its main goal is to identify potential vulnerabilities in the smart contract. In contrast, the critic works during the identification phase its main goal is to evaluate the vulnerabilities generated by the auditor. [144] uses traditional algorithms (TF-IDF and BM25) to match the code under analysis with the code in the vulnerability corpus to determine similarity. The code under analysis is presented to LLMs together with similar corpus entries. Based on in-context learning, LLMs can more accurately determine whether the code contains the identified vulnerability type. [145] specifically focuses on vulnerability detection in smart contracts and introduce a tool called GPTScan. GPTScan first parses the smart contract project to determine the reachability of the functions, retaining only those that may have vulnerabilities. Subsequently, GPTScan uses GPT to match candidate functions with predefined vulnerability types. Finally, GPTScan asks GPT to confirm the vulnerability. VulLLM [146] combines multi-task learning with LLMs, introducing two auxiliary tasks—vulnerability localization and vulnerability explanation—in addition to the primary vulnerability detection task. This approach enhances the model’s ability to understand the root causes of code vulnerabilities, thereby improving its generalization capabilities. 

To improve LLM’s ability to reason about vulnerabilities, [147] proposes LLM4Vuln, which separates the vulnerability reasoning capabilities of LLMs from others ( _e.g._ , proactively seeking more information, employing relevant vulnerability knowledge, and following instructions to output structured results). They allow LLMs to request additional contextual information about the target code. Moreover, they conclude that the more information input to LLMs is not the better. Too much information such as full vulnerabilities report, and a large amount of invocation context, may lead to distractions. [148] proposes a new method called MuCoLD, which simulates a multi-role code review process for vulnerability detection in software. By playing different roles, such as developers and testers, LLMs participate in discussions to reach a consensus on the existence and classification of vulnerabilities. IRIS [149] combines LLMs with static analysis to enable reasoning over the entire codebase. It automatically infers taint specifications and performs contextual analysis, thereby reducing reliance on human-generated specifications and manual inspection. 

12 

In addition to detecting vulnerabilities in specific programs, recent studies have attempted to use LLMs to infer lists of affected libraries from vulnerability reports. [150] observes that many vulnerability reports in the national vulnerability database (NVD) either omitted affected libraries or provided incomplete or incorrect library names, increasing the risk of third-party library vulnerabilities. To address this problem, they propose VulLibGen, a method designed to detect vulnerabilities in third-party libraries. VulLibGen takes only vulnerability descriptions as input and uses the inherent knowledge of LLMs to generate a list of library names that may be affected by the reported vulnerabilities. 

[151] explores the application of ChatGPT for vulnerability management. They evaluate ChatGPT’s capabilities in predicting security bugs, evaluating severity, repairing vulnerabilities, and verifying patch correctness. The results reveal that while ChatGPT can assist in identifying and mitigating software security threats, it needs enhancements to perform more nuanced tasks, such as vulnerability prioritization and patch validation. 

**Construction of vulnerability detection datasets.** In addition to the methods of retraining or fine-tuning the models, the construction of the dataset is also important for vulnerability detection. 

[152] introduces a new vulnerable source code dataset called DiverseVul, which contains 18,945 vulnerable functions (covering 150 CWEs) and 330,492 non-vulnerable functions, all written in C/C++. They also explore 11 different deep learning architectures and conclude that despite the remarkable success of LLMs, they still face challenges such as high false positive rates, low F1 scores, and difficulty in identifying complex CWEs for vulnerability detection. [153] introduces a comprehensive vulnerability benchmark dataset called VulBench, which includes high-quality data from CTF challenges and real-world applications with detailed annotations of vulnerability types and causes for each vulnerable function. [154] creates a dataset containing 112,000 vulnerable C code instances with detailed information about the specific vulnerability, including CWE number, location, and function name. Notably, all the code in this dataset is generated by GPT-3.5, which illustrates the application potential of vulnerable code synthesized by LLMs. Source Code Processing Engine (SCoPE) [155] is a framework that incorporates strategized techniques to reduce the size and normalize C/C++ functions. Additionally, SCoPE refines the CVEFixes dataset, which can be used for fine-tuning pre-trained LLMs for software vulnerability detection. 

### **4.3 Malware Detection** 

In malware detection, LLMs can serve as both the static analysis assistant and the dynamic debugging assistant, improving the efficiency and effectiveness of the process, and making it an important part of defending against cyber threats. 

**LLMs as the static analysis assistant.** [156] explores the application of LLMs, such as OpenAI’s Codex, in the field of reverse engineering, particularly in understanding software functionality and extracting information from the code. LLMs are primarily used to analyze the functionality of C code provided by reverse engineering tools such as Ghidra. These C codes are obtained from binary files through the process of decompilation. Decompilation is also an important task in reverse engineering. [157] introduces an LLM tailored for decompilation that focuses on converting compiled machine code back into human-readable source code. They fine-tune a model called DeepSeek-Coder on a large number of C code and assembly code pairs and evaluate the performance of their work by recompiling and executing the decompiled code. [158] explores the potential and limitations of LLMs for code analysis tasks, especially when dealing with obfuscated code. In the experiments, they conduct tests that allow LLMs to generate de-obfuscated versions of code, _i.e._ , to recover more readable original code from obfuscated code. 

[159] focuses on how to improve LLM’s semantic understanding of programs through fuzz testing. Their core idea is that programs with their basic units ( _e.g._ , functions, and subroutines) are designed to exhibit diverse behaviors and provide possible outputs given different inputs. Thus, through fuzz testing, various inputs trigger different functions of the code that can help LLMs understand the behavior and semantics of the program more thoroughly.. [160] introduces ASTxplainer, an explainability method for LLMs in coding scenarios. It aligns token predictions with Abstract Syntax Tree (AST) nodes, enabling detailed evaluation and visualization of model predictions. ASTxplainer consists of AsC-Eval for structural performance estimation, AsC-Causal for causal analysis, and AsC-Viz for visualization. These components provide a more comprehensive explanation of how LLMs work when generating or analyzing code. 

[161] focuses on how LLMs can be utilized to aid in dynamic analysis of malware. The core idea of the research is to use GPT-4 to generate explanatory text for each API call, and then use BERT to generate a series of API sequences to be executed based on the previous analysis. This approach can theoretically generate representations for all API calls without the need to train the dataset during the generation process. [162] uses LLM (specifically ChatGPT) to analyze the linguistic and strategic elements of ransomware communications. By examining a range of ransomware samples, the study identifies patterns and strategies used in ransom notes, revealing the evolution of ransomware strategies characterized by sophisticated language use and psychological manipulation. [163] also discusses the potential and challenges of LLMs in generating strategies against ransomware. [164] employs GPT-3 and GPT-4 to detect potential 

13 

malware in the npm ecosystem by analyzing JavaScript packages. The study introduces SocketAI Scanner, a multi-stage workflow that utilizes iterative self-refinement, zero-shot role-playing, and chain of thought prompting techniques to enhance the model’s ability to identify malicious intent within code. By comparing LLMs’ performance with static analysis tools, the paper demonstrates that LLMs can effectively pinpoint malware with higher precision and lower false positive rates. 

Binary malware summarization aims to automatically generate human-readable descriptions of malware behaviors from executable files, facilitating tasks like malware cracking and detection. [165] introduces a novel code summarization framework, namely MALSIGHT, which can iteratively generate descriptions of binary malware by exploring malicious source code and benign pseudocode. At the same time, they construct the first malware summary dataset, MalS and MalP, to support further research. 

**LLMs as the dynamic debugging assistant.** [55] introduces DebugBench, a benchmark for evaluating LLMs’ debugging capabilities in programming. It consists of 4253 instances across various bug categories in C++, Java, and Python. The benchmark is constructed by collecting code snippets from LeetCode, implanting bugs with GPT-4, and conducting rigorous quality assessment. [166] addresses the challenge of automated Graphical User Interface (GUI) testing for mobile applications. They propose a novel approach called GPTDroid that formulates the GUI testing as a question and answering (Q&A) task, where the LLM is asked to chat with the mobile apps by passing GUI page information to generate testing scripts. These scripts are executed and iterations of the application’s responses are fed back to the model to guide further exploration. [167] proposes an approach called FLAG to assist human debuggers in identifying and localizing security and functional bugs in code. FLAG takes a code file as input and regenerates each line in the file for comparison. It compares the original code with LLM-generated code to flag notable differences as anomalies for further inspection. 

### **4.4 Anomaly Detection** 

We investigate some methods to incorporate LLMs into cybersecurity frameworks for anomaly detection, underscoring their critical role in maintaining network integrity and safeguarding against cyber intrusions. 

**Log-based anomaly detection.** [168] tests 60 language models fine-tuned for log analysis, including models with different architectures such as BERT, RoBERTa, DistilRoBERTa, GPT-2 and GPT-Neo. The results show that these fine-tuned models can be effectively used for log analysis, especially for domain adaptation for specific log types. Targeting service logs on Huawei Cloud, [169] proposes a framework called ScaleAD, which aims to provide an accurate, lightweight, and adaptive solution for log anomaly detection in cloud systems. When ScaleAD’s Trie-based Detection Agent (TDA) detects suspicious anomaly logs, it queries the LLM to validate these logs. The LLM determines whether the logs are anomalous or not by understanding the semantics of the log content and gives the corresponding confidence scores. [170] proposes a log anomaly detection framework named LogGPT. This framework consists of three main components: log preprocessing, prompt construction, and response parser. The log preprocessing component filters, parses and groups raw log messages into a structured format for further analysis. The response parser extracts the output returned by ChatGPT for detailed analysis and evaluation of the detected anomalies. [171] performs similar work. The difference is that they fine-tune GPT-2 by introducing a Top-K reward metric, which directs the model to focus on the most relevant parts of the log sequence, thus improving the accuracy of anomaly detection. [172] introduces an online log analysis method called LogPrompt. They employ LLMs to parse unstructured logs and generate reports with a specific structure. LogPrompt then utilizes chain of thought and in-context learning methods to progressively reason about log content and provide normal/abnormal judgments. [173] introduces LEMUR, a cutting-edge log parsing framework that enhances log analysis with entropy sampling for efficient log clustering and semantic understanding using LLMs. LEMUR addresses the limitations of traditional parsers by discarding manual rules and focusing on semantic information. Relying on semantic understanding of LLMs, the framework accurately distinguishes between parameters and invariant tokens, leading to impressive efficiency and state-of-the-art performance in log template merging and categorization. 

**Web content security.** LLMs can assist in the detection of phishing and spam. [174] presents a model named Improved Phishing and Spam Detection Model (IPSDM), a fine-tuned model based on DistilBERT and RoBERTa. They emphasizes the potential of LLMs to revolutionize the field of email security and suggests that these models can be valuable tools for improving the security of information systems. Another work also conduct spam detection with LLMs, [175] evaluate ChatGPT’s performance in spam detection and find it outperforms BERT on a low-resource Chinese dataset but lags on a larger English dataset. The study also highlights the positive impact of increasing prompts on ChatGPT’s accuracy. [176] introduces a spear-phishing detection approach utilizing LLMs to generate “prompted contextual document vectors.” By posing targeted questions to LLMs about email content, the method quantifies the presence of common persuasion principles, creating vectors that capture the malicious intent within spear-phishing emails. The approach utilizes the reasoning capabilities of LLMs and outperforms traditional phishing detection 

14 

methods. In addition to detecting phishing emails, there are studies on generating phishing emails using LLMs. [177] evaluates the performance of GPT-4 in creating phishing emails and compare its effectiveness with traditional phishing methods called V-Triad method, which relys on manual design based on general rules and cognitive heuristics. They also explore the use of LLMs in detecting phishing emails, where models like GPT, Claude, PaLM, and LLaMA demonstrate strong capabilities in identifying malicious intent, sometimes surpassing human detection rates. 

In addition, LLMs can be used for malicious URLs, DDoS attacks, and other cyber threat detection. Based on the website content, [178] uses the knowledge distillation approach to detect malicious URLs. Specifically, unlabeled URLs are classified and labels are generated by a teacher model. The student model trained with this label improves accuracy with significantly fewer parameters and is therefore suitable for malicious URL detection. [179] explores the potential of LLMs in detecting DDoS attacks by investigating the performance of LLMs on two datasets. For the CICIDS 2017 dataset, they fine-tune LLMs with labeled pcap files to enable traffic classification through few-shot learning. Urban IoT dataset is a real-world anonymized dataset containing 4060 IoT devices. Considering the complexity of this dataset, they fine-tune LLMs separately depending on whether the correlation of traffic between IoT devices is considered or not. [180] encodes the network traffic by employing a novel encoding technique called Privacy-Preserving Fixed-Length Encoding (PPFLE). Then they train a model named SecurityBERT with these encoded data to perform a classification task on network traffic. Specifically, their model targets IoT devices to achieve efficient and accurate cyber threat detection on resource-limited IoT devices. [181] studies the interpretation of decision tree models in network intrusion detection (NID) systems. They convert the path and structure data of the decision tree into text format and provide it to LLMs to generate explanations. Moreover, LLMs provide additional background knowledge to help users understand why certain features are important in categorization. [182] introduces HuntGPT, a system that integrates LLMs with traditional machine learning for anomaly detection. The system utilizes a random forest classifier trained on the KDD99 dataset to identify cyber threats. To enhance interpretability, the system employs XAI techniques such as SHAP and Lime and combines them with the GPT-3.5 conversational agent. 

**Digital Forensic.** [183] assesses the applicability of ChatGPT for digital forensics. ChatGPT is used to help determine if a file has been downloaded to a PC and if the file has been executed by a specific user. In addition, ChatGPT is also used to detect browser history, Windows event logs, and interactions with cloud platform machines. 

### **4.5 Fuzz** 

Although traditional fuzzing techniques are effective in discovering software vulnerabilities, their inherent limitations can affect their efficiency and effectiveness. One significant drawback is that traditional fuzzers operate in a largely random or semi-random manner, which is time-consuming and inefficient because they may not explore all possible execution paths. Additionally, the mutated seeds are usually artificially crafted, which makes the time and labor costs high. Although all of the above problems have been studied for many years and there are many ways to mitigate them, the emergence of LLMs provides a new way of thinking in the field of fuzz testing [184, 185]. 

**What are the advantages of LLMs fuzz over traditional methods?** [186] evaluates the performance of ChatGPT in generating test cases directly (without tuning) and compare it with two traditional testing tools ( _i.e._ , SIEGE, and TRANSFER). Their experiments show that LLMs outperform traditional methods in generating test cases when a detailed description of the vulnerability, possible exploits, and code context are given. 

There are some advantages of LLMs over traditional tools. One of the most important factors is that LLMs lead to a shift from random mutation to guided mutation. [187] introduces a GPT-based seed mutator to the traditional gray-box fuzz testing, selecting seeds from a seed pool and requesting variants from ChatGPT to generate higher-quality inputs. Another factor is that LLMs have a strong understanding of programming languages, enabling them to perform testing tasks in multiple languages. Most traditional methods can only fuzz specific programming languages. [188] tests 6 languages code ( _i.e._ , C, C++, Go, SMT2, Java, and Python) with a method named Fuzz-Loop, which automatically mutates test cases based on LLMs. Most traditional fuzz methods fail to achieve high code coverage in all codes, while LLMs have mastered the logic of code and can generate more targeted test cases for areas with low coverage. For example, [189] uses Codex to generate test cases against low-coverage functions when SBST (Search-Based Software Testing, a traditional fuzz method) reaches coverage plateau. Specifically, the raw character sequences generated by the Codex are deserialized into an internal test case representation compatible with SBST to leverage its mutation operations and fitness functions. 

**Specific fuzzing strategies for different testing objects.** Depending on the test subject, the strategy should be adjusted when fuzzing with LLMs. For **testing against general APIs** , [190] investigates the effectiveness of LLMs in generating invocation code. They compare LLM-based generation with traditional program analysis methods and find that LLMs can automatically generate a large number of effective fuzzing drivers while reducing human intervention. The research introduces query strategies, iterative improvements, and the use of examples to enhance LLM performance. Although 

15 

it’s all about testing APIs, the strategy for **testing deep-learning libraries** needs to be modified. Because programs that call deep learning libraries usually have strict requirements on tensor dimensions, ignoring this would cause the fuzzer to perform meaningless tests. [191] proposes TitanFuzz, a tool specifically for generating test cases for deep learning libraries. Their training corpus contains a large number of code snippets that call the DL library APIs, so that the language syntax and semantics, and complex DL API constraints can be learned to efficiently generate DL programs. FuzzGPT [192] is also about fuzzing the DL library. The difference is that FuzzGPT focuses on using historical error-triggered code snippets to guide LLMs to generate test cases. 

In addition to the above research, we have collected some studies targeting other testing objects. **Testing against Protocol** . [193] discusses how to find security vulnerabilities in protocol implementations in the absence of a machinereadable protocol specification. They train LLMs with massive human-readable protocol documents and ask LLMs to mutate interactive messages for protocol fuzz ( _e.g._ , HTTP). **Testing against BusyBox** . Specifically targeting BusyBox, a popular utility in Linux-based devices, [194] introduces two fuzzing methods. One is to use LLMs to generate target-specific initial seeds for fuzzing, which significantly improves the efficiency of identifying crashes and potential vulnerabilities. The other is crash reuse, which employs previously acquired crash data to streamline the testing process for new targets. 

### **4.6 Program Repairing** 

The software development lifecycle is deeply impacted by the presence of bugs, with their detection and resolution being costly. Researchers are motivated to find new ways to automatically identify and correct bugs/vulnerabilities with LLMs [195]. 

**Evaluation of existing LLMs on program repairing.** For state-of-the-art LLMs (open-sourced or proprietary), many studies have evaluated their capabilities for program repairing. [196] explores the application of OpenAI’s Codex to the field of automatic program repair (APR), specifically its ability to locate and fix bugs in software. They use the QuixBugs benchmark, which includes 40 bugs in Python and Java, to evaluate the effectiveness of Codex in APR tasks. Notably, Codex outperforms numerous existing APR methods even without retraining. [197] conducts similar work with the previous one. Both studies evaluate LLMs for automatic program repair on QuixBugs benchmark. In this work, ChatGPT is evaluated instead of Codex. [198] discusses the application of Gemini in automating the repair of software vulnerabilities, especially for vulnerabilities found by the sanitizer tool in C/C++, Java, and Go code. The authors argue that while the success rate seems low, it has the potential to significantly reduce engineering effort over time. [199] evaluates the performance of three LLMs, Gemini Pro, GPT-4, and GPT-3.5, on codes with identified vulnerabilities from real-world code reviews. The findings indicate that GPT-4 outperforms the other models, but all LLMs have great potential, especially for conciseness, clarity, and accuracy of responses. [200] selects 9 LLMs and compare them with traditional automated program repair methods, demonstrating the superior effectiveness of LLMs in this field. 

[201] explores the potential of LLMs for zero-shot vulnerability repair in code. Through extensive experiments with various LLMs in synthetic, artifactual, and real-world security scenarios, they demonstrate that while LLMs show promise in repairing simple cases, they struggle with more complex, real-world examples. The study reveals the limitations and strengths of LLMs in cybersecurity and urges further research into the application of LLMs in program repairing. [202] compares the capabilities of LLMs and deep learning-based APR models in fixing Java vulnerabilities. They evaluate the performance of 5 LLMs (Codex, CodeGen, CodeT5, PLBART, and InCoder), 4 fine-tuned LLMs, and 4 deep learning-based APR techniques on two real-world Java vulnerability benchmarks ( _i.e._ , Vul4J and VJBench). They design code transformations to address the overlapping of train and test sets faced by Codex, and create a new Java vulnerability remediation benchmark, VJBench, to better evaluate LLMs and APR techniques. [203] investigate LLM-based function-level APR, focusing on the effects of the few-shot learning mechanism and the inclusion of auxiliary repair-relevant information. The study shows that LLMs with zero-shot learning are already effective for function-level APR, but applying the few-shot learning mechanism results in varying repair performance. Additionally, they find that directly incorporating auxiliary repair-relevant information into LLMs significantly enhances function-level repair performance. 

**Combined LLMs with static analysis tools.** Instead of using LLMs alone for program repair, some studies have combined them with traditional program analysis tools to increase the efficiency of those tools. [54] proposes a new approach called Feedback-Driven Security Patching (FDSP), which passes feedback from Bandit to LLM. With the help of the static code analysis tool, LLM can generate potential solutions to address security vulnerabilities. Each suggested solution, along with the corresponding vulnerable code segment, is fed back to LLM for verification and validation. [204] introduces a program repair framework called InferFix that incorporates the latest static analyzers for fixing critical security and performance vulnerabilities. Inferfix consists of two main components: a retriever and a generator. The retriever aims to search for semantically similar vulnerabilities and their associated fixes. The generator 

16 

is fine-tuned on vulnerability fix data, with prompts enhanced by bug type annotations and semantically similar fixes, thereby improving the model’s ability to generate effective proposals. 

**Improving repair capabilities through different strategies.** To improve the performance of LLMs on program repair tasks, researchers have proposed some methodologies. D4C [205] is a straightforward prompting framework for APR. By aligning the output to LLMs training objective and allowing LLMs to refine the whole program without first identifying faulty statements, D4C greatly improve LLM’s APR capability. [206] proposes an approach called SELF-DEBUGGING. Even if there is no human feedback about the correctness of the code or error messages, this method can identify the error by observing the execution results and explaining the code generated by natural language. [207] explores the application of Self-Consistency (an approach for improving model reasoning ability [208]) in program repair. By incorporating commit-logs as reasoning paths in few-shot prompts, Self-Consistency enables LLMs to generate diverse solutions. The most frequent solution from multiple samples is selected to improve patch accuracy. Similarly, VRpilot [209] is based on reasoning and patch validation feedback. The method uses a chain-of-thought prompt to reason about a vulnerability before generating patch candidates and iteratively refines the prompts based on feedback from external tools on previously generated patches, improving patch accuracy. DRCodePilot [210] is designed to enhance GPT-4-Turbo’s APR capabilities by incorporating design rationales (DR) into the prompt instruction, along with a utility feedback-based self-reflective framework. This framework prompts GPT-4 to reconsider and refine its outputs by referencing the provided patch and suggested identifiers. 

Additionally, [211] introduces a novel approach that leverages the entropy of LLMs in combination with prior APR tools to enhance all stages of the APR process. By using entropy-delta for patch ranking and classification, this method can rank correct patches more effectively than state-of-the-art machine learning tools. ThinkRepair [212] is an LLM-based autonomous two-stage automatic program repair framework. In the collection stage, CoT prompts guide the LLM to automatically gather various reasoning chains that form the foundation of the repair knowledge. In the repair stage, sample selection is performed for few-shot learning, with interactive feedback from the LLM. This approach significantly improves LLMs’ bug fixing capability. [213] proposes a program repair framework named Repilot. It starts by masking the buggy code segment and then utilizes LLMs to generate candidate patches. During the generation, Repilot consults the completion engine to prune infeasible tokens and proactively completes the code when necessary. This approach enhances the compilation rate and correctness of patches while reducing the number of invalid attempts in the generation process. [214] introduces SecRepair, a system that uses LLMs to detect and fix code vulnerabilities in the software. It utilizes reinforcement learning with the semantic reward mechanism to improve the model’s ability to generate accurate code comments and descriptions, guiding developers to address security issues. ARJA-CLM [215] integrates a multi-objective evolutionary algorithm with a code language model to fix multi-location bugs in Java projects. It does this by predicting the correct statement for masked buggy positions using the powerful code-filling capabilities of CodeLLMs. [216] launches Contrastrepair to provide more accurate feedback by providing LLMs with contrastive test case pairs (a failing test and a passing test), thereby enhancing conversation-driven repair framework. The key insight is to minimize the difference between the generated passing test and the failing one, effectively isolating bug causes. ContrastRepair interacts with ChatGPT repeatedly to generate patches until a plausible fix is generated. Unlike previous function-level approaches, [217] investigates the performance of LLMs in repository-level program repair, which needs to consider interactions and dependencies between code that may span multiple functions or files. In this work, they propose a benchmark named RepoBugs, which includes 124 bugs from open source repositories to evaluate the performance of LLMs. 

Fine-tuning is also necessary to unlock state-of-the-art performance in program repair. MORepair [218] is a multiobjective fine-tuning approach that instructs LLMs to generate high-quality patches. It involves adapting the LLM parameters to the syntactic nuances of code transformation and specifically fine-tuning the model to understand the logical reasoning behind code changes in the training data. This fine-tuning strategy enables LLM to achieve superior performance in program repair. [219] fine-tunes LLM on datasets containing C code vulnerabilities. They specifically design a structured representation of the code and provide it to LLM, including the line number of the code that needs to be repaired, the vulnerability description ( _i.e._ , CWE description), and the complete source code. The output of LLM is also structured and can be directly patched, which enables the code to be repaired automatically without manual intervention. [220] explores how LLMs can achieve excellent APR performance through process supervision and feedback. They first construct a dataset called CodeNet4Repair, which is filled with multiple repair records for supervised fine-tuning. Then,they develop a reward model that provides feedback on the fine-tuned LLM’s actions, progressively optimizing its policy for better repair. [221] proposes continual merging and empirically studies the capabilities of merged adapters in Code LLMs for the APR task. Specifically, task-specific adapters are first trained for the LLM, and then MergeRepair is used to merge multiple task-specific adapters, considering the order and weight of the merged adapters for better APR. 

**Target-specific program repairing.** We also investigate some studies on program repairing for some specific targets. [222] proposes a framework called ZeroLeak, which explore how LLMs can be used to automatically generate repair 

17 

code to address side-channel vulnerabilities in software. ZeroLeak guides LLMs to generate patches for specific vulnerabilities through zero-shot learning. Once generated, these patches are inspected by dynamic analysis tools to ensure that they not only function correctly, but also prevent information leakage. [223] introduces a novel framework named DIVAS. The framework maps user-defined SoC specifications to Common Weakness Enumerations (CWEs), generates SystemVerilog Assertions (SVAs) for verification, and enforces security policies. DIVAS automates the process of vulnerability detection and policy enforcement, reducing manual effort and enhancing SoC security. [224] constructs a corpus of hardware security vulnerabilities and utilize LLMs to automatically remediate Verilog code containing these vulnerabilities. [225] focuses on the software implementation of neural networks and related memory safety issues, including NULL pointer dereferencing, out-of-bounds access, double-free errors, and memory leaks. They propose detecting these vulnerabilities and automatically repairing them with the help of LLMs. [226] focuses on the application of LLMs( _e.g._ , ChatGPT and Bard) in repairing security vulnerabilities in JavaScript programs.Using the top 25 CWEs of 2023 as a reference, they selecte JavaScript-related vulnerabilities to evaluate the accuracy of the models in generating the correct patches. Their findings highlight the potential of LLMs for JavaScript security, emphasizing the effectiveness of LLMs for programming languages used for web development. To convert a regular C/C++ program into its HLS-compatible counterpart (HLS-C), [227] proposes an LLM-driven program repair framework that takes standard C/C++ code as input and automatically generates the corresponding HLS-C code for synthesis, minimizing human repair effort. 

### **4.7 LLM Assisted Attack** 

A report [228] from the workshop organized by Google on January 1, 2024 highlight the dual-use issue of Generative Artificial Intelligence (GenAI). These techniques can be used for both positive purposes and potentially for malicious attacks. In this section, we discuss current attacks with the help of LLMs in detail. 

**Current status of LLM-assisted attacks.** [229] points out that ChatGPT has both positive and potentially negative impacts on cybersecurity. They list various types of threats to cybersecurity today, including malware attacks, phishing, and password attacks. They also mention the potential application of ChatGPT in social engineering attacks. [230] also conduct similar work on the impact of generative AI in cybersecurity and privacy. Furthermore, [231] explores the potential of LLMs for network threat testing, particularly in supporting threat-related actions and decisions. Experimenting on virtual machines, they discuss in detail how automated attacks guided by LLMs can be launched against devices in a network. They conclude that while this work is preliminary, it demonstrates that LLMs shows strong potential for cyber threats. For existing accessible malicious LLMs, [232] conducts a systematic study of 212 real-world Malla (malicious LLM), revealing how they spread and work in the underground market. They examine in detail the Malla ecosystem, development frameworks, exploitation techniques, and the effectiveness of Malla in generating various malicious content. They also provide insights into how cybercriminals utilize LLMs and strategies for combating such cybercrime. 

Specifically, there are various means of executing automatic attacks with the help of LLMs. 

**LLM-Enabled Automated Penetration Testing.** [233] introduces a tool called PentestGPT designed to perform automated penetration tests. PentestGPT consists of three modules: inference, generation and parsing. Each module reflects a specific role in the penetration testing team so that the system can more realistically simulate automated penetration tests. [234] also conducts a study on penetration testing with the help of LLMs. The study investigates two use cases: high-level task planning for security testing and low-level vulnerability hunting within vulnerable virtual machines. They cerate a feedback loop between LLM-generated operations and the virtual machine, allowing LLMs to analyze the state of the system to find vulnerabilities and suggest attack vectors. [235] points out the importance of integrating penetration testing with vulnerability remediation into a cohesive system. They proposes PenHeal, a two-stage LLM-based framework designed to autonomously identify and mitigate security vulnerabilities. The framework integrates two LLM-enabled components: the Pentest Module, which detects multiple vulnerabilities within a system, and the Remediation Module, which recommends optimal remediation strategies. [236] developes CIPHER (Cybersecurity Intelligent Penetration-testing Helper for Ethical Researchers), a LLM trained using over 300 high-quality write-ups of vulnerable machines, hacking techniques, and documentation of open-source penetration testing tools. Additionally, they introduce the Findings, Action, Reasoning, and Results (FARR) Flow augmentation to enhance penetration testing write-ups, establishing a fully automated pentesting simulation benchmark tailored for LLMs. 

**LLM-Assisted Automatic Full-Life-Cycle Cyberattack.** [237] proposes AUTOATTACKER, a system that leverages LLMs to automate the execution of "keystroke-operated" cyberattacks that mimic human operations. The system employs LLMs to generate precise attack commands for various techniques and environments, transforming potential manual operations into automated and efficient processes. AUTOATTACKER consists of multiple modules that interact iteratively with the LLM to construct complex attack sequences using functions such as summarization, planning, 

18 

and action selection. AURORA [238] is another automatic end-to-end framework for cyberattack construction and emulation. It can autonomously build multi-stage cyberattack plans based on CTI reports, construct the emulation infrastructure, and execute the attack procedures. [239] introduces Occupy AI, a customized and fine-tuned LLM specifically designed to automate and execute cyberattacks. This specialized AI-driven tool is proficient in crafting attack steps and generating executable code for various cyber threats, including phishing, malware injection, and system exploitation. 

**LLM-Assisted Phishing Website/Email Generation.** [240] uses LLM to automatically generate advanced phishing attacks. In the proposed attack method, LLMs are used for the following functions: cloning target websites, modifying login forms to capture credentials, obfuscating code, automating domain name registration, and automating script deployment. [241] examines the potential of LLMs like ChatGPT, GPT-4, Claude, and Bard to generate phishing attacks. The study finds that these models can effectively create convincing phishing websites and emails, mimicking well-known brands and employing evasive tactics to avoid detection. The research also develops a BERT-based detection tool that achieves high accuracy in identifying malicious prompts, serving as a countermeasure against the misuse of LLMs for phishing scams. [242] compares the effectiveness of smishing (SMS phishing) messages created by GPT-4 and human authors, demonstrating that LLM-generated messages are generally perceived as more convincing than those authored by humans. The study also finds that targets are unable to identify whether a message was AI-generated or human-authored and struggle to pinpoint criteria that could help make this distinction. This poses a challenge against personalized AI-enabled social engineering attacks. 

**LLM-Assisted Privilege Escalation Attacks.** [243] uses LLM to assist in completing penetration tests. They develop an automated Linux privilege escalation benchmark to evaluate the performance of different LLMs. At the same time, they design a tool called Wintermute to quickly explore the ability of LLMs to bootstrap privilege escalation. 

**LLM-Assisted Payload Generation.** [244] proposes to write payloads with the help of LLMs to launch cyber attacks. This study shows the high efficiency of LLMs by generating executable code for the top 10 MITRE weaknesses observed in 2022 using ChatGPT and Bard respectively. In addition, LLM-generated payloads tend to be more complex and targeted than manually crafted payloads. 

**LLM-Assisted Attack Graph Generation.** [245] explores the approach of leveraging LLMs to automate the generation of attack graphs by intelligently chaining CVEs based on their preconditions and effects. They also show how to utilize LLMs to create attack graphs from threat reports. 

**LLM-Assisted Capture The Flag (CTF) Challenges.** [246] investigates the potential of existing LLMs in solving CTF competitions. They select a number of representative challenges from common CTF categories to evaluate the performance of LLMs, including GPT-3.5, PaLM2, and Prometheus. Their research results demonstrate that LLMs can indeed help participants cope with CTF challenges to a certain extent, albeit not comprehensively. 

**Proxies for Attacks.** [247] uses ChatGPT as a proxy between the victim and the network controlled by the attackers (C&C), which allows the attacker to remotely control the victim’s system without communicating directly, making it difficult to track down the attackers. 

### **4.8 (In)secure Code Generation** 

There have been many previous works that have confirmed that LLMs do have good code comprehension capabilities [89, 82, 34, 35]. However, the security of the generated code is very important, and some studies have explored this issue. 

**Evaluation of the security of LLM-generated code.** It is very important to know whether the code generated by LLMs has security risks. [248] conducts an experiment to explore whether code written by undergraduate computer science students with the help of LLMs poses any additional security risks. Participants are tasked with implementing a singly-linked ’shopping list’ structure in C and they are divided into two groups: a control group that doesn’t have access to Codex, and an assisted group that does. The results show that LLM does not significantly increase the risk of introducing security vulnerabilities when used as a code assistant. [249] conducts an empirical study investigating bugs in code generated by LLMs, focusing on three models: CodeGen, PanGu-Coder, and Codex. The research identifies 10 unique bug patterns among 333 collected errors, and these patterns are confirmed by 34 LLM practitioners and researchers. [250] study how LLMs generate vulnerabilities when writing simple C programs using a neutral zero-shot prompt. They collected code generated by Gemini-pro, GPT-4, Falcon-180B, CodeLLama2-13B, and other LLMs under neutral prompts, which constitute the FormAI-v2 dataset. The study found that at least 63.47% of the generated programs are vulnerable, highlighting the risks of using LLM-generated code. 

There are many studies exploring the security of code generated by state-of-the-art LLMs. [251] investigates the security of code generated by GitHub Copilot. They design 89 different execution scenarios for Copilot, resulting in 1,689 programs. These programs are then analyzed for vulnerabilities, particularly focusing on the top 25 CWEs identified by 

19 

MITRE. [252] introduces CodeSecEval, a meticulously curated dataset designed to address 44 critical vulnerability types with 180 distinct samples. The dataset is then used for precisely evaluating and enhancing the security aspects of code generated by LLMs. The study reveals that current models frequently overlook security issues during both code generation and repair processes, leading to the creation of vulnerable code. [253] delves into the potential of LLMs in security-oriented program analysis. Their evaluation focuses on two representative LLMs, ChatGPT and CodeBERT, evaluating their performance on analysis tasks of varying difficulty, including vulnerability analysis, bug fixing, fuzzing, and assembly code analysis. [254] evaluates the code generated by ChatGPT, focusing on aspects such as correctness, understandability, and security. Through an empirical study using LeetCode questions and CWE scenarios, they analyze the quality of code snippets generated by ChatGPT and its ability to improve the code through multi-round dialogue. The results reveal that while ChatGPT is able to generate functionally correct code, it encounters challenges in complex reasoning and ensuring code security. 

On the other hand, [255] proposes a framework called SALLM specifically for evaluating the security of code generated by LLMs. SALLM consists of three components: a prompt dataset detailing Python programs, a code generation environment that requires different solutions from LLMs, and a systematic evaluation model that leverages Docker to execute the generated code. [256] focuses on enhancing the quality evaluation of code generation. Recognizing that existing benchmarks often have a limited set of test cases, they introduced a code synthesis evaluation framework, EvalPlus. EvalPlus significantly expands the number of test cases in the evaluation dataset by deploying an automatic test input generator that combines LLMs with a mutation-based strategy. [257] collects 228 code scenarios and analyze 8 LLMs in an automated framework to determine whether LLMs can reliably identify security-related vulnerabilities. They point out that current LLMs fall short in automated vulnerability detection tasks and outline several limitations exhibited by current LLMs. [258] evaluates the performance of ChatGPT-3.5 on generating code, including an examination of code security in 10 programming languages. 

**Do LLMs know whether the generated code is safe or not?** [259] conducts a series of experiments to evaluate the security of LLM-generated code and to discover vulnerabilities in generated code under various scenarios. The results show that while LLMs may identify vulnerabilities in the generated code when prompted for review, they still generate unsafe code unless explicitly instructed otherwise. A significant challenge they faced stems from the uninterpretability of deep neural networks, which causes LLMs to give inconsistent responses when repeatedly asked about code security, without a clear strategy to maximize successful identification. 

To ensure the generation of secure codes, LLMSecGuard [260] enhance code security through the synergy between static code analyzers and LLMs. [261] takes a more direct approach to customize LLMs through specific mechanisms. They propose a method named svGen, which makes LLMs generate safe or unsafe code based on the user’s security preferences. In addition to the descriptions for the generated code, they also introduce property-specific continuous vectors (called prefixes), which are sequences of vectors that match the shape of the LLMs’ hidden states. These prefixes are optimized to influence the LLM’s generation process by setting initial hidden states that steer the code toward meeting the desired security criteria, all without modifying the underlying weights of the LLM. 

Fine-tuning LLMs for secure code generation is feasible. [262] reveals that fine-tuning LLMs can improve secure code generation by 6.4% for C language and 5.4% for C++ language. Additionally, fine-tuning with function-level and block-level datasets achieves the best performance in secure code generation, compared to file-level and line-level datasets. [89] introduces SafeCoder, an innovative instruction tuning approach that enhances the security of code generation by LLMs. SafeCoder combines traditional instruction tuning with security-specific fine-tuning using a high-quality dataset collected through an automated pipeline from GitHub. This approach significantly enhances code security without compromising the LLMs’ utility across various tasks, demonstrating its adaptability and effectiveness in enhancing the security of LLM-generated code. 

In addressing the question of how to best iteratively refine code, [263] points out that the process exposes an exploreexploit tradeoff, which can be framed as a multi-armed bandit problem, and solved using Thompson Sampling. The resulting LLM-based program synthesis algorithm is widely applicable. [264] discusses iterative code repair in both high and low-resource languages, where an LLM fixes an incorrect program by reasoning about errors and generating new code. Specifically, they delve into guiding the model to generate secure code through chain-of-thought reasoning. 

### **4.9 Others** 

Apart from the previously described categories, there are a few scattered studies on the application of LLMs in the field of cybersecurity, which are also of research value. 

**IoT Fingerprint.** [265] proposes a method for Internet devices fingerprint generation. Their approach is divided into two steps. First, raw text data obtained from web scans is converted into a stable embedded representation with 

20 

RoBERTa. Next, the embedding is clustered using the HDBSCAN and the fingerprint is generated based on the clustering. 

**Botnet.** [266] introduces a LLM-driven botnet called fox8 on Twitter. The fox8 botnet contains over one thousand users controlled by AI. They post machine-generated content and stolen images to spread fake and harmful information, engaging with each other through replies and retweets. 

**Security Patch Detection.** [267] proposes a system named LLMDA, whose main goal is to improve the identification of security patches in open-source software (OSS). LLMs are used to generate explanatory descriptions of patches and synthetic data, which helps to augment existing datasets. 

**SoC Security.** [268] explores the potential of integrating LLMs into the system-on-chip (SoC) security verification paradigm. They provide a systematic evaluation of LLM applications about vulnerability insertion, security assessment, security verification, and countermeasure development. 

**Taint Analysis.** [269] introduces LATTE, a static binary taint analysis tool supported by LLMs. LLMs help to identify the chain of data dependencies between taint sources and possible vulnerability triggers. LLMs could provide an understanding of code structure and semantics in the process. 

**LLMs’ Input-Output Safeguard.** [270] proposes Llama Guard to detect the risk in LLM’s prompt and response. Using labeled security risk text, they perform instruction tuning on Llama2-7b to obtain this model. 

**Honeypot.** [271] designs a dynamic and real-time fake honeypot by giving response generated by LLMs, which mainly focus on changing the limitation that honeypots are easily recognizable. In their experiment, most people can’t recognize whether the remote host is a real one or a honeypot generated by LLMs. [272] systematically investigates the use of LLMs to create a variety of honeytokens. They design different types of honeytokens to evaluate the optimal prompts, including configuration files, databases, and log files. They test 210 different prompt structures, based on 16 prompt-building blocks, and demonstrate that LLMs can generate a wide array of honeytokens using the presented prompt structures. LLMPot [273] is a novel approach for designing honeypots in ICS networks that harnesses the power of LLMs. It aims to automate and optimize the creation of realistic honeypots with vendor-agnostic configurations, applicable to any control logic, thereby eliminating the manual effort and specialized knowledge traditionally required. 

**Incidence Response.** [274] advocates for the application of ChatGPT to enhance incident response planning (IRP) in cybersecurity. It suggests that LLMs can draft initial plans, recommend best practices, and identify documentation gaps. The paper highlights the potential of LLMs to streamline IRP processes, emphasizing the value of human oversight to ensure accuracy and relevance. 

**Network Management.** [275] explores how LLMs can be used to generate task-specific code from natural language queries to improve network management. They develop and release a test benchmark, NeMoEval, covering two network management applications: network traffic analysis and network lifecycle management. 

**Vulnerabilities Reproduction.** [276] proposes an approach called AdbGPT that utilizes LLMs to automatically reproduce vulnerabilities in vulnerability reports by prompting engineering without training or hard coding. 

**Expertise Q&A on cybersecurity domain.** [277] conducts an empirical study of ChatGPT’s performance in answering Stack Overflow programming questions. The main drawbacks of the LLM answers are fake information and excessive length of the content. Still some testers like its comprehensiveness and good style of language presentation. Due to the difficulty of recognizing misleading information given by LLMs, this is an area that has yet to be researched. 

Answer to Q2: LLMs have shown great potential in the field of cybersecurity, assisting in various aspects such as threat intelligence, anomaly detection, vulnerability detection, and so on. LLM security copilot can effectively empower the automation and intelligence of cybersecurity, helping to address security risk challenges. Although relevant research has made certain progress, it is still worth further exploration to better apply LLMs in the field of cybersecurity. 

## **5 RQ3: What are the challenge and further research for the application of LLMs in cybersecurity?** 

### **5.1 Challenge** 

The application of LLMs in cybersecurity represents a cutting-edge field, demonstrating the power of LLMs in dealing with complex and dynamic cyber threats. **However, despite their strengths, LLMs are not without challenges,** 

21 


![](images/51-when-llms-meet-cybersecurity-a-systematic-literature-review.pdf-0022-00.png)


<!-- Start of picture text -->
Backdoor attack, Prompt injection<br>attack, Others<br>Attaks Against LLMs<br>Adversarial prompt, Red-teaming,<br>Others<br>Challenge (§ 5.1) LLMs Jailbreaking<br>Deceptive behaviors, Data leakage,<br>and so on<br>RQ3:  Others<br>Challenge &<br>Further Research<br>Addrees complex cybersecurity task,<br>Automated attack, Assist in cyber<br>defense, Enhance domain applications<br>Further Research (§ 5.2) LLM Agent for Cybersecurity<br><!-- End of picture text -->

Figure 6: **An overview of RQ3.** 

**especially their inherent vulnerabilities and susceptibilities to attacks** [16, 278]. Among the critical concerns are the phenomena of LLMs-oriented attacks and LLMs jailbreaking. These vulnerabilities highlight the double-edged nature of LLM applications in cybersecurity. On one hand, the powerful comprehension and predictive capabilities of LLMs can significantly promote the intelligence of cybersecurity systems. On the other hand, their intrinsic weaknesses facilitate exploitation and pose serious security risks, undermining their reliability and integrity in cybersecurity applications. 

We delve into these challenges from two key perspectives: attacks against LLMs, which examines the susceptibility of LLMs to various forms of attacks [279, 280, 281], and LLMs Jailbreaking, focusing on the phenomenon of LLMs generating unsafe or unintended content when prompted in certain ways, despite being designed with safeguards [282, 283]. Through an analysis of these dimensions, we aim to illuminate the complexities of exploiting LLMs in cybersecurity, highlighting the need for caution and strategic foresight in their application. 

**Attaks Against LLMs.** The vulnerabilities of LLMs make them susceptible to attacks by malicious users. We focus on two types of attacks: backdoor attacks and prompt injection attacks. 

_Backdoor Attack_ manipulates model outputs to achieve attackers’ objectives by embedding specific triggers in the model or its inputs. [284] proposes a novel backdoor attack methodology called BadGPT, specifically targeting language models that have been fine-tuned through reinforcement learning, such as ChatGPT. This approach involves embedding backdoors within the reward model, which can be activated via specific trigger prompts. Such activation allows attackers to control the model’s output to align with their preferences, showcasing a critical security vulnerability. In another study, [285] introduces a novel backdoor attack strategy, ICLAttack, which aims at exploiting the inherent context learning capabilities of LLMs. The ICLAttack framework encompasses two primary attack vectors: poisoning demonstration examples and poisoning demonstration prompts. By embedding backdoor triggers within the model’s context, ICLAttack is able to influence the model’s behavior without the need for fine-tuning, thus revealing universal vulnerabilities within LLMs. Furthermore, [286] reveals a backdoor attack mechanism tailored to prompt-based LLMs, called PoisonPrompt. The method injects backdoors into the language model through two steps: poisoned prompt generation and bi-level optimization. PoisonPrompt can alter the normal prediction of the model in case of specific trigger activations without affecting the performance of the model on downstream tasks, posing a subtle but powerful threat to the integrity of LLMs. 

_Prompt Injections Attack_ involve attackers inserting malicious commands into inputs, compelling the model to execute actions aligned with the attackers’ intentions. [287] conducts a comprehensive investigation of prompt-to-SQL (P2SQL) injection attacks against web applications based on the Langchain framework. These attacks utilize user-input prompts to generate malicious SQL queries, thereby enabling attackers to tamper with databases or steal sensitive information. [288] introduces the Compositional Instruction Attack (CIA), unveiling the susceptibility of LLMs to attacks that utilize synthetic instructions with potentially malicious intentions. Through two transformation methods, Talking-CIA and Writing-CIA, harmful instructions are masked as conversational or writing tasks, preventing the model from recognizing potentially malicious intent and thus generating harmful content. [289] proposes a novel black-box prompt injection attack technique named HOUYI for applications integrated with LLMs. HOUYI executes attacks through three key elements: pre-constructed prompts, injection prompts, and malicious payloads. Its deployment across 36 real-world scenarios demonstrates its efficacy in discovering and exploiting vulnerabilities within LLM-integrated applications. [290] focuses on Virtual Prompt Injection (VPI) attacks against instruction-tuned LLMs, which allow attackers to manipulate model behavior by specifying virtual prompts without directly injecting into model inputs, leading to the 

22 

model disseminating biased information. [291] uses instruction-tuned models to generate datasets for specific tasks. These datasets are then utilized to fine-tune foundational models, enhancing their robustness to resist most prompt injection attacks. 

Additionally, [292] constructs an adversarial attack dataset named AttaQ in a semi-automated manner, aiming to evaluate the security of LLMs in the face of harmful or inappropriate inputs. Vulnerabilities are exposed by analyzing model responses to the AttaQ dataset, and specialized clustering techniques are further applied to identify and characterize the models’ vulnerable semantic areas. [280] conducts a comprehensive survey of various attack types targeting LLMs, encompassing both direct attacks on the models themselves and indirect attacks on applications utilizing the models. This study describes the impacts of these attacks on the privacy, security, and reliability of the models. And it underscores the critical importance of implementing proactive security measures in the development of AI models. 

**LLMs Jailbreaking.** As mentioned above, LLM is susceptible to various attacks, with jailbreaking attacks being one of the most popular. [293] studies the security issues of LLMs when facing jailbreak prompts. They collect and analyze 6,387 prompts to reveal the characteristics and attack strategies of these prompts. Despite various security measures implemented by LLMs, they found that effective jailbreak prompts still successfully induce models to generate harmful content, indicating the need for further improvements in the security of LLMs. [282] conducts a comprehensive evaluation of LLMs jailbreaking, revealing the effectiveness of these attack methods and the vulnerabilities of LLMs across various violation categories. 

There are various methods for generating adversarial prompts. [294] combines greedy search and gradient-based optimization techniques to propose a method that automatically generates adversarial suffixes to prompt models, both open-source and commercial, to produce inappropriate content. [295] introduces a novel approach to black-box jailbreak attacks using genetic algorithms, which can manipulate LLMs to produce unexpected and potentially harmful outputs without accessing the model’s internal structure and parameters by optimizing a universal adversarial prompt. [296] conceptualizes the jailbreaking process as prompt rewriting and scenario nesting. They then introduce ReNeLLM, a jailbreaking prompt generation framework that utilizes LLMs to generate effective jailbreaking prompts. Compared to existing baselines, ReNeLLM achieves high attack success rates on multiple LLMs while significantly reducing the time cost. [297] explores jailbreak attacks on LLM Chatbots and proposes a framework named MASTERKEY to automate this process. Through temporal feature analysis and automated prompt generation, MASTERKEY reveals and bypasses the defense mechanisms of LLM chatbots, offering new perspectives for LLM security research and guidance for service providers to improve their security measures. 

Research on LLMs jailbreaking can also be used for red-teaming. [298] proposes AutoDAN, an interpretable and gradient-based adversarial attack method. By combining the dual objectives of jailbreaking and readability, it generates interpretable and diverse attack prompts capable of effectively bypass perplexity filters and demonstrates robust generalization in scenarios with limited training data. This method not only offers a novel approach for red-teaming of LLMs but also helps to understand the mechanics of jailbreak attacks. [299] presents a new black-box jailbreak fuzzing framework named GPTFUZZER. By collecting human-written jailbreak templates from the internet as initial seeds, and then iterating through a process of seed selection, mutation, and evaluating the success of attacks, GPTFUZZER significantly enhances the efficiency and scalability of red team testing. [300] introduces FuzzLLM, a novel and universally applicable fuzz testing framework designed to proactively discover jailbreak vulnerabilities in LLMs. FuzzLLM employs a template-based strategy that generates a variety of jailbreak prompts and identify potential security vulnerabilities through automated testing. It demonstrates efficiency and comprehensiveness across various LLMs, effectively identifying and assessing jailbreak vulnerabilities. 

Additionally, [301] introduces the concept of a semantic firewall to describe the defense mechanisms of LLMs against malicious prompts and proposes a self-deception attack method to bypass LLMs semantic firewalls. This method designs a customizable dialogue template for experimenting with specific illegal payloads and automatically achieving LLM jailbreak. [302] develops a potential jailbreak prompt dataset embedded with malicious instructions and proposes a hierarchical annotation framework to analyze the performance of LLMs under different conditions( _e.g._ , instruction positions, word substitutions, and instruction replacements). This is aimed at evaluating the security and output robustness of LLMs when processing texts containing potential malicious instructions. [303] investigates the potential privacy threats associated with ChatGPT and the Bing search engine integrated with ChatGPT. By introducing a novel multi-step jailbreaking prompt, they successfully extract personally identifiable information from ChatGPT and demonstrate the privacy threats posed by the new Bing under direct prompts. 

**Others.** Besides the extensively researched vulnerabilities, several other LLM risks limit their application in cybersecurity. [304] highlights the dual-edged nature of generative AI and ChatGPT, revealing that while they bring convenience, they also pose cybersecurity and ethical challenges. [305] investigates the deceptive behaviors that LLMs may exhibit under specific trigger conditions and finds that these behaviors might persist even after safety alignment, posing a potential threat to the security of AI systems. [306] points out that even securely aligned LLMs can be easily 

23 

manipulated to generate harmful content with simple data tuning, highlighting the complexity of maintaining LLM security. [307] identifies critical vulnerabilities within LLM-integrated applications, which could stem from malicious app developers or external threats with the capability to control database access, manipulate, and polluting data. [308] also raises data leakage and reproducibility issues associated with the use of closed-source LLMs. 

Answer 1 to Q3: Despite the powerful capabilities of LLMs, they inherently possess certain weaknesses and vulnerabilities, making them susceptible to attacks. In particular, jailbreaking poses significant security risks to the application of LLMs. 

### **5.2 Further Research** 

Despite the significant research into LLMs within the field of cybersecurity, the exploration and application of such models remain in their initial stages and have great potential for development [18, 19]. The complexity of cybersecurity stems not only from the diversity of attack methods but also from the intricate nature of network environments, which requires the integrated application of various tools and strategies to achieve effective protection [309, 310]. Facing these challenges requires AI systems to have stronger capabilities in planning, reasoning, tool use, and memory. **Consequently, the concept of LLM Agent has emerged and attracted a lot of attention from researchers.** 

LLM Agent is “a system that can use an LLM to reason through a problem, create a plan to solve the problem, and execute the plan with the help of a set of tools [311].” By simulating complex network behaviors and attack patterns, and integrating advanced natural language processing capabilities, LLM agents introduce new perspectives and solutions to the field of cybersecurity [115, 231, 312, 313, 314, 315]. With the continuous advancement of technology and in-depth research, LLM agents are expected to play a key role in defense strategy generation, threat detection, and security policy formulation, significantly improving the efficiency and intelligence level of cybersecurity defenses. 

The AI Agents framework based on LLMs possesses the critical capabilities required to solve complex problems [316]. [317] proposes an LLM Agent architecture that includes brain, perception, and action components to provide a wide range of applications in single-agent scenarios, multi-agent environments, and human-agent collaboration. Moreover, the incorporation of Tool & API calls endows LLM agents with the capacity to interact with the real world. [318] develops the ToolBench dataset and the DFSDT algorithm to enable LLMs to successfully handle complex tasks involving numerous real-world APIs. [319] introduces a sophisticated tool invocation mechanism that enhances LLMs’ interaction with external tools by summarizing and making decisions. Additionally, [320] demonstrates that integrating code into LLMs significantly enhances its ability to perform more complex tasks as an intelligent agent. [321] proposes TaskWeaver, a code-first agent framework for seamlessly planning and executing data analytics tasks. 

LLM agents can be applied to address complex cybersecurity tasks. [312] proposes an innovative framework named LLMind, which utilizes LLM as a coordinator to perform complex tasks by integrating with IoT devices and domainspecific AI modules. The framework employs finite state machine methods to generate control scripts, thereby enhancing the accuracy and success rate of task execution. In addition, LLMind introduces a mechanism for accumulating experience, which allows the system to continually learn and progress through ongoing interactions between users and machines. [313] demonstrates the use of LLMs as agents within cybersecurity environments. Experiments show that LLM agents can achieve performance comparable to or better than extensively trained agents in sequential decisionmaking tasks, even without additional training. Furthermore, the study introduces the NetSecGame environment, a highly modular and adaptive cybersecurity environment designed to support complex multi-agent scenarios. [322] proposes ChatNet, a domain-specific network LLM framework with access to a variety of external network tools. ChatNet significantly reduces the time required for tedious network planning tasks, thereby greatly increasing efficiency. 

LLM agents can be employed to perform automated attacks. [314] reveals the potential of LLM agents in cybersecurity attacks, particularly the capability of GPT-4 to autonomously conduct complex hacker attacks on websites without prior knowledge of vulnerabilities. The study shows that LLM agents have a success rate of up to 73.3% in hacking attempts and can autonomously discover vulnerabilities in real-world websites. [231] demonstrates the potential application of LLMs in cyber threat testing, especially in automating cyber attack activities. With prompt engineering and automated agents, LLMs can understand and execute complex cyber attacks. [323] collects a dataset of 15 zero-day vulnerabilities. Based on this dataset, the study shows that LLM agents can autonomously exploit these zero-day vulnerabilities in real-world systems. [324] also shows that teams of LLM agents can exploit real-world, zero-day vulnerabilities by designing a system of agents with a planning agent that can launch subagents. 

LLM agents can also be utilized to assist in cyber defense. [315] designs a multi-agent system (Nissist) to precisely understand user queries and provide effective mitigation plans. Nissist utilizes troubleshooting guides and incident mitigation history to provide suggestions, which significantly reduces the time for event mitigation, reduces the workload of on-duty engineers, and enhances the reliability of services. Cyber Sentinel [115] is a dialogue agent based on GPT-4, 

24 

which can interpret potential cyber threats and execute security actions based on user instructions. The potential impact of Cyber Sentinel in cyber security includes improved threat detection and response capabilities, enhanced operational efficiency, real-time collaboration, and knowledge sharing. PhishAgent [325] is a multimodal agent that combines a wide range of tools, integrating both online and offline knowledge bases with Multimodal LLMs, showing strong resilience against various types of adversarial attacks. [326] develops an AI agent to replace the labor intensive repetitive tasks involved in analyzing CTI reports. By leveraging the advanced capabilities of LLMs, the AI agent can accurately extract important information from large volumes of text and generate Regex to help SOC analysts accelerate the process of establishing correlation rules. 

LLM agents enhance cybersecurity applications with their remarkable capabilities, yet the security risks inherent in agent systems [327] pose challenges for their deployment in cybersecurity environments. [328] introduces the concept of Web-based Indirect Prompt Injection (WIPI), a novel cyber threat that embeds malicious instructions in web pages to indirectly control these agents, achieving high success rates and robustness across different user inputs. [329] highlights that LLM agents integration with external tools may lead to the risk of indirect prompt injection attacks, in which attackers embed malicious commands in the content processed by LLMs to manipulate these agents to perform actions harmful to users. 

In conclusion, the application of LLM-based agents in cybersecurity opens up new avenues for dealing with cyber security threats. Although research in this area is still in its early stages, and the inherent security vulnerabilities of agents have not yet been addressed, this line of research promises to significantly enhance the capability to counter complex cyber threats and has the potential to revolutionize the working methods of security professionals, thereby unleashing greater productivity. Therefore, further research into the application of LLM agents in cybersecurity is crucial for developing adaptive, intelligent, and comprehensive cybersecurity solutions. 

Answer 2 to Q3: Extending the tool-use and API-call capabilities of LLM, coupled with the design of autonomous intelligent agents capable of understanding, planning, and executing complex tasks within cybersecurity applications, will greatly advance the utilization of AI in cybersecurity. 

## **6 Conclusion** 

This paper introduces the methodologies for constructing cybersecurity-oriented domain LLMs, detailing how existing models can be fine-tuned to meet specific needs using target data. The investigation into the applications of LLMs has shows that LLMs have great potential for a wide range of cybersecurity tasks, such as threat intelligence, vulnerability detection, secure code generation and others. However, we has also acknowledged the inherent vulnerabilities of LLMs, particularly the susceptibility to attacks such as jailbreaking, which pose significant security risks. Mitigating these vulnerabilities is crucial to securely deploying LLMs in sensitive environments. Additionally, we propose future research directions, such as extending the tool-use and API-call capabilities of LLMs, and developing autonomous intelligent agents for complex cybersecurity operations. 

In summary, we bridges the gap between LLM advancements and cybersecurity demands, laying the groundwork for researchers and practitioners. It guides them to harness the transformative potential of LLMs while addressing the unique challenges that arise in this field. Further research and exploration would open up new pathways for future cybersecurity practice, ensuring that we have more comprehensive and professional strategies in the face of increasingly complex cyber threats. 

25 

## **References** 

- [1] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ , 35:27730–27744, 2022. 

- [2] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint_ , 2023. 

- [3] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang, Yonghao Zhuang, Joseph E Gonzalez, et al. Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality. _See https://vicuna. lmsys. org (accessed 14 April 2023)_ , 2(3):6, 2023. 

- [4] Ebtesam Almazrouei, Hamza Alobeidli, Abdulaziz Alshamsi, Alessandro Cappelli, Ruxandra Cojocaru, Mérouane Debbah, Étienne Goffinet, Daniel Hesslow, Julien Launay, Quentin Malartic, et al. The falcon series of open language models. _arXiv preprint_ , 2023. 

- [5] Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, et al. Mixtral of experts. _arXiv preprint_ , 2024. 

- [6] Barret Zoph, Colin Raffel, Dale Schuurmans, Dani Yogatama, Denny Zhou, Don Metzler, Ed H Chi, Jason Wei, Jeff Dean, Liam B Fedus, et al. Emergent abilities of large language models. _TMLR_ , 2022. 

- [7] Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng Gao. Large language models: A survey. _arXiv preprint_ , 2024. 

- [8] Yingqiang Ge, Wenyue Hua, Kai Mei, Juntao Tan, Shuyuan Xu, Zelong Li, Yongfeng Zhang, et al. Openagi: When llm meets domain experts. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [9] Pravneet Kaur, Gautam Siddharth Kashyap, Ankit Kumar, Md Tabrez Nafis, Sandeep Kumar, and Vikrant Shokeen. From text to transformation: A comprehensive review of large language models’ versatility. _arXiv preprint_ , 2024. 

- [10] Xinyi Hou, Yanjie Zhao, Yue Liu, Zhou Yang, Kailong Wang, Li Li, Xiapu Luo, David Lo, John Grundy, and Haoyu Wang. Large language models for software engineering: A systematic literature review. _ACM Transactions on Software Engineering and Methodology_ , 2023. 

- [11] Jinqi Lai, Wensheng Gan, Jiayang Wu, Zhenlian Qi, and S Yu Philip. Large language models in law: A survey. _AI Open_ , 2024. 

- [12] Hongjian Zhou, Fenglin Liu, Boyang Gu, Xinyu Zou, Jinfa Huang, Jinge Wu, Yiru Li, Sam S. Chen, Peilin Zhou, Junling Liu, Yining Hua, Chengfeng Mao, Chenyu You, Xian Wu, Yefeng Zheng, Lei Clifton, Zheng Li, Jiebo Luo, and David A. Clifton. A survey of large language models in medicine: Progress, application, and challenge. _arXiv preprint_ , 2024. 

- [13] Lixiang Yan, Lele Sha, Linxuan Zhao, Yuheng Li, Roberto Martinez-Maldonado, Guanliang Chen, Xinyu Li, Yueqiao Jin, and Dragan Gaševi´c. Practical and ethical challenges of large language models in education: A systematic scoping review. _British Journal of Educational Technology_ , 55(1):90–112, 2024. 

- [14] Yinheng Li, Shaofei Wang, Han Ding, and Hang Chen. Large language models in finance: A survey. In _Proceedings of the Fourth ACM International Conference on AI in Finance_ , pages 374–382, 2023. 

- [15] Zihan Zhao, Da Ma, Lu Chen, Liangtai Sun, Zihao Li, Hongshen Xu, Zichen Zhu, Su Zhu, Shuai Fan, Guodong Shen, et al. Chemdfm: Dialogue foundation model for chemistry. _arXiv preprint_ , 2024. 

- [16] Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Zhibo Sun, and Yue Zhang. A survey on large language model (llm) security and privacy: The good, the bad, and the ugly. _High-Confidence Computing_ , page 100211, 2024. 

- [17] Badhan Chandra Das, M. Hadi Amini, and Yanzhao Wu. Security and privacy challenges of large language models: A survey. _arXiv preprint_ , 2024. 

- [18] Gabriel de Jesus Coelho da Silva and Carlos Becker Westphall. A survey of large language models in cybersecurity. _arXiv preprint_ , 2024. 

- [19] Farzad Nourmohammadzadeh Motlagh, Mehrdad Hajizadeh, Mehryar Majd, Pejman Najafi, Feng Cheng, and Christoph Meinel. Large language models in cybersecurity: State-of-the-art. _arXiv preprint_ , 2024. 

- [20] Yagmur Yigit, William J Buchanan, Madjid G Tehrani, and Leandros Maglaras. Review of generative ai methods in cybersecurity. _arXiv preprint_ , 2024. 

26 

- [21] Kutub Thakur, Meikang Qiu, Keke Gai, and Md Liakat Ali. An investigation on cyber security threats and security models. In _2015 IEEE 2nd international conference on cyber security and cloud computing_ , pages 307–311. IEEE, 2015. 

- [22] Natalie M Scala, Allison C Reilly, Paul L Goethals, and Michel Cukier. Risk and the five hard problems of cybersecurity. _Risk Analysis_ , 39(10):2119–2126, 2019. 

- [23] Diptiben Ghelani. Cyber security, cyber threats, implications and future perspectives: A review. _Authorea Preprints_ , 2022. 

- [24] Yuchong Li and Qinghui Liu. A comprehensive review study of cyber-attacks and cyber security; emerging trends and recent developments. _Energy Reports_ , 7:8176–8186, 2021. 

- [25] Ömer Aslan, Semih Serkant Aktu˘g, Merve Ozkan-Okay, Abdullah Asim Yilmaz, and Erdal Akin. A comprehensive review of cyber security vulnerabilities, threats, attacks, and solutions. _Electronics_ , 12(6):1333, 2023. 

- [26] Mohamed Amine Ferrag, Fatima Alwahedi, Ammar Battah, Bilel Cherif, Abdechakour Mechri, and Norbert Tihanyi. Generative ai and large language models for cyber security: All insights you need. _arXiv preprint_ , 2024. 

- [27] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint_ , 2023. 

- [28] André Silva, Sen Fang, and Martin Monperrus. Repairllama: Efficient representations and fine-tuned adapters for program repair. _arXiv preprint_ , 2023. 

- [29] Jie Zhang, Hui Wen, Liting Deng, Mingfeng Xin, Zhi Li, Lun Li, Hongsong Zhu, and Limin Sun. Hackmentor: Fine-tuning large language models for cybersecurity. In _2023 IEEE International Conference on Trust, Security and Privacy in Computing and Communications (TrustCom)_ . IEEE, 2023. 

- [30] Shafi Parvez Mohammed and Gahangir Hossain. Chatgpt in education, healthcare, and cybersecurity: Opportunities and challenges. In _2024 IEEE 14th Annual Computing and Communication Workshop and Conference (CCWC)_ , pages 0316–0321. IEEE, 2024. 

- [31] Rahul Pankajakshan, Sumitra Biswal, Yuvaraj Govindarajulu, and Gilad Gressel. Mapping llm security landscapes: A comprehensive stakeholder risk assessment proposal. _arXiv preprint_ , 2024. 

- [32] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

- [33] Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, and et al. Gemini: A family of highly capable multimodal models. _arXiv preprint_ , 2023. 

- [34] Baptiste Roziere, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, et al. Code llama: Open foundation models for code. _arXiv preprint_ , 2023. 

- [35] Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro, Oleh Shliazhko, Nicolas Gontier, Nicholas Meade, Armel Zebaze, Ming-Ho Yee, Logesh Kumar Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy V, Jason T. Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang, Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas, Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson, Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf, Arjun Guha, Leandro von Werra, and Harm de Vries. Starcoder: may the source be with you! _Trans. Mach. Learn. Res._ , 2023, 2023. 

- [36] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, Nouamane Tazi, Ao Tang, Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei, et al. Starcoder 2 and the stack v2: The next generation. _arXiv preprint_ , 2024. 

- [37] Ramanpreet Kaur, Dušan Gabrijelˇciˇc, and Tomaž Klobuˇcar. Artificial intelligence for cybersecurity: Literature review and future research directions. _Information Fusion_ , NA:101804, 2023. 

- [38] Sarvesh Kumar, Upasana Gupta, Arvind Kumar Singh, and Avadh Kishore Singh. Artificial intelligence: revolutionizing cyber security in the digital era. _Journal of Computers, Mechanical and Management_ , 2(3):31–42, 2023. 

27 

- [39] Maad Mijwil, Mohammad Aljanabi, et al. Towards artificial intelligence-based cybersecurity: the practices and chatgpt generated ways to combat cybercrime. _Iraqi Journal For Computer Science and Mathematics_ , 4(1):65–70, 2023. 

- [40] Norbert Tihanyi, Mohamed Amine Ferrag, Ridhi Jain, and Merouane Debbah. Cybermetric: A benchmark dataset for evaluating large language models knowledge in cybersecurity. _arXiv preprint_ , 2024. 

- [41] Manish Bhatt, Sahana Chennabasappa, Cyrus Nikolaidis, Shengye Wan, Ivan Evtimov, Dominik Gabi, Daniel Song, Faizan Ahmad, Cornelius Aschermann, Lorenzo Fontana, Sasha Frolov, Ravi Prakash Giri, Dhaval Kapil, Yiannis Kozyrakis, David LeBlanc, James Milazzo, Aleksandar Straumann, Gabriel Synnaeve, Varun Vontimitta, Spencer Whitman, and Joshua Saxe. Purple llama cyberseceval: A secure coding benchmark for language models. _arXiv preprint_ , 2023. 

- [42] Catherine Tony, Markus Mutas, Nicolás E. Díaz Ferreyra, and Riccardo Scandariato. Llmseceval: A dataset of natural language prompts for security evaluations. In _20th IEEE/ACM International Conference on Mining Software Repositories, MSR 2023, Melbourne, Australia, May 15-16, 2023_ , pages 588–592. IEEE, 2023. 

- [43] Ça˘gatay Yıldız, Nishaanth Kanna Ravichandran, Prishruit Punia, Matthias Bethge, and Beyza Ermis. Investigating continual pretraining in large language models: Insights and implications. _arXiv preprint_ , 2024. 

- [44] Tiezheng Zhang, Xiaoxi Chen, Chongyu Qu, Alan Yuille, and Zongwei Zhou. Leveraging ai predicted and expert revised annotations in interactive segmentation: Continual tuning or full training? _arXiv preprint_ , 2024. 

- [45] Shengyu Zhang, Linfeng Dong, Xiaoya Li, Sen Zhang, Xiaofei Sun, Shuhe Wang, Jiwei Li, Runyi Hu, Tianwei Zhang, Fei Wu, et al. Instruction tuning for large language models: A survey. _arXiv preprint_ , 2023. 

- [46] Guanting Dong, Hongyi Yuan, Keming Lu, Chengpeng Li, Mingfeng Xue, Dayiheng Liu, Wei Wang, Zheng Yuan, Chang Zhou, and Jingren Zhou. How abilities in large language models are affected by supervised fine-tuning data composition. _arXiv preprint_ , 2023. 

- [47] Ning Ding, Yujia Qin, Guang Yang, Fuchao Wei, Zonghan Yang, Yusheng Su, Shengding Hu, Yulin Chen, Chi-Min Chan, Weize Chen, et al. Parameter-efficient fine-tuning of large-scale pre-trained language models. _Nature Machine Intelligence_ , 5(3):220–235, 2023. 

- [48] Mohamed Amine Ferrag, Ammar Battah, Norbert Tihanyi, Merouane Debbah, Thierry Lestable, and Lucas C Cordeiro. Securefalcon: The next cyber reasoning system for cyber security. _arXiv preprint_ , 2023. 

- [49] Zefang Liu, Jialei Shi, and John F Buford. Cyberbench: A multi-task benchmark for evaluating large language models in cybersecurity. In _AAAI 2024 Workshop on Artificial Intelligence for Cyber Security_ , 2024. 

- [50] Guancheng Li, Yifeng Li, Wang Guannan, Haoyu Yang, and Yang Yu. Seceval: A comprehensive benchmark for evaluating cybersecurity knowledge of foundation models. https://github.com/XuanwuAI/SecEval, 2023. 

- [51] Zefang Liu. Secqa: A concise question-answering dataset for evaluating large language models in computer security. _arXiv preprint_ , 2023. 

- [52] Dipkamal Bhusal, Md Tanvirul Alam, Le Nguyen, Ashim Mahara, Zachary Lightcap, Rodney Frazier, Romy Fieblinger, Grace Long Torales, and Nidhi Rastogi. Secure: Benchmarking generative large language models for cybersecurity advisory. _arXiv preprint_ , 2024. 

- [53] Mohammed Latif Siddiq and Joanna C. S. Santos. Securityeval dataset: mining vulnerability examples to evaluate machine learning-based code generation techniques. In _Proceedings of the 1st International Workshop on Mining Software Repositories Applications for Privacy and Security_ , MSR4P&S 2022, page 29–33, New York, NY, USA, 2022. Association for Computing Machinery. 

- [54] Kamel Alrashedy and Abdullah Aljasser. Can llms patch security issues? _arXiv preprint_ , 2024. 

- [55] Runchu Tian, Yining Ye, Yujia Qin, Xin Cong, Yankai Lin, Yinxu Pan, Yesai Wu, Haotian Hui, Weichuan Liu, Zhiyuan Liu, and Maosong Sun. Debugbench: Evaluating debugging capability of large language models. In LunWei Ku, Andre Martins, and Vivek Srikumar, editors, _Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024_ , pages 4173–4198. Association for Computational Linguistics, 2024. 

- [56] Md Imran Hossen, Jianyi Zhang, Yinzhi Cao, and Xiali Hei. Assessing cybersecurity vulnerabilities in code large language models. _arXiv preprint_ , 2024. 

- [57] Timothee Chauvin. eyeballvul: a future-proof benchmark for vulnerability detection in the wild. _arXiv preprint_ , 2024. 

- [58] Yukai Miao, Yu Bai, Li Chen, Dan Li, Haifeng Sun, Xizheng Wang, Ziqiu Luo, Yanyu Ren, Dapeng Sun, Xiuting Xu, Qi Zhang, Chao Xiang, and Xinchi Li. An empirical study of netops capability of pre-trained large language models. _arXiv preprint_ , 2023. 

28 

- [59] Yuhe Liu, Changhua Pei, Longlong Xu, Bohan Chen, Mingze Sun, Zhirui Zhang, Yongqian Sun, Shenglin Zhang, Kun Wang, Haiming Zhang, Jianhui Li, Gaogang Xie, Xidao Wen, Xiaohui Nie, Minghua Ma, and Dan Pei. Opseval: A comprehensive it operations benchmark suite for large language models. _arXiv preprint_ , 2024. 

- [60] Denis Donadel, Francesco Marchiori, Luca Pajola, and Mauro Conti. Can llms understand computer networks? towards a virtual system administrator. _arXiv preprint_ , 2024. 

- [61] Minghao Shao, Sofija Jancheska, Meet Udeshi, Brendan Dolan-Gavitt, Haoran Xi, Kimberly Milner, Boyuan Chen, Max Yin, Siddharth Garg, Prashanth Krishnamurthy, et al. Nyu ctf dataset: A scalable open-source benchmark dataset for evaluating llms in offensive security. _arXiv preprint_ , 2024. 

- [62] Andy K Zhang, Neil Perry, Riya Dulepet, Joey Ji, Justin W Lin, Eliot Jones, Celeste Menders, Gashon Hussein, Samantha Liu, Donovan Jasper, et al. Cybench: A framework for evaluating cybersecurity capabilities and risks of language models. _arXiv preprint_ , 2024. 

- [63] Pritam Deka, Sampath Rajapaksha, Ruby Rani, Amirah Almutairi, and Erisa Karafili. Attacker: Towards enhancing cyber-attack attribution with a named entity recognition dataset. _arXiv preprint_ , 2024. 

- [64] Hangyuan Ji, Jian Yang, Linzheng Chai, Chaoren Wei, Liqun Yang, Yunlong Duan, Yunli Wang, Tianzhen Sun, Hongcheng Guo, Tongliang Li, et al. Sevenllm: Benchmarking, eliciting, and enhancing abilities of large language models in cyber threat intelligence. _arXiv preprint_ , 2024. 

- [65] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [66] Alec Radford and Karthik Narasimhan. Improving language understanding by generative pre-training. 2018. 

- [67] Aiyuan Yang, Bin Xiao, Bingning Wang, Borong Zhang, Ce Bian, Chao Yin, Chenxu Lv, Da Pan, Dian Wang, Dong Yan, et al. Baichuan 2: Open large-scale language models. _arXiv preprint_ , 2023. 

- [68] Tongtong Wu, Linhao Luo, Yuan-Fang Li, Shirui Pan, Thuy-Trang Vu, and Gholamreza Haffari. Continual learning for large language models: A survey. _arXiv preprint_ , 2024. 

- [69] Adam Ibrahim, Benjamin Thérien, Kshitij Gupta, Mats L. Richter, Quentin Anthony, Timothée Lesort, Eugene Belilovsky, and Irina Rish. Simple and scalable strategies to continually pre-train large language models. _arXiv preprint_ , 2024. 

- [70] Ruidan He, Linlin Liu, Hai Ye, Qingyu Tan, Bosheng Ding, Liying Cheng, Jia-Wei Low, Lidong Bing, and Luo Si. On the effectiveness of adapter-based tuning for pretrained language model adaptation. In Chengqing Zong, Fei Xia, Wenjie Li, and Roberto Navigli, editors, _Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021_ , pages 2208–2222. Association for Computational Linguistics, 2021. 

- [71] Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and Jie Tang. Gpt understands, too. _AI Open_ , NA, 2023. 

- [72] Xiao Liu, Kaixuan Ji, Yicheng Fu, Weng Lam Tam, Zhengxiao Du, Zhilin Yang, and Jie Tang. P-tuning v2: Prompt tuning can be comparable to fine-tuning universally across scales and tasks. _arXiv preprint_ , 2021. 

- [73] Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient prompt tuning. In Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and Scott Wen-tau Yih, editors, _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021_ , pages 3045–3059. Association for Computational Linguistics, 2021. 

- [74] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ . OpenReview.net, 2022. 

- [75] Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. Qlora: Efficient finetuning of quantized llms. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [76] Yunzhi Yao, Peng Wang, Bozhong Tian, Siyuan Cheng, Zhoubo Li, Shumin Deng, Huajun Chen, and Ningyu Zhang. Editing large language models: Problems, methods, and opportunities. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023_ , pages 10222–10240. Association for Computational Linguistics, 2023. 

- [77] Ningyu Zhang, Yunzhi Yao, Bozhong Tian, Peng Wang, Shumin Deng, Mengru Wang, Zekun Xi, Shengyu Mao, Jintian Zhang, Yuansheng Ni, Siyuan Cheng, Ziwen Xu, Xin Xu, Jia-Chen Gu, Yong Jiang, Pengjun Xie, Fei Huang, Lei Liang, Zhiqiang Zhang, Xiaowei Zhu, Jun Zhou, and Huajun Chen. A comprehensive study of knowledge editing for large language models. _arXiv preprint_ , 2024. 

29 

- [78] Aras Bozkurt and Ramesh C Sharma. Generative ai and prompt engineering: The art of whispering to let the genie out of the algorithmic world. _Asian Journal of Distance Education_ , 18(2):i–vii, 2023. 

- [79] Qinyuan Ye, Maxamed Axmed, Reid Pryzant, and Fereshte Khani. Prompt engineering a prompt engineer. _arXiv preprint_ , 2023. 

- [80] Pranab Sahoo, Ayush Kumar Singh, Sriparna Saha, Vinija Jain, Samrat Mondal, and Aman Chadha. A systematic survey of prompt engineering in large language models: Techniques and applications. _arXiv preprint_ , 2024. 

- [81] Alexey Shestov, Rodion Levichev, Ravil Mussabayev, and Anton Cheshkov. Finetuning large language models for vulnerability detection. _arXiv preprint_ , 2024. 

- [82] Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei Lin, and Daxin Jiang. Wizardcoder: Empowering code large language models with evol-instruct. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. 

- [83] Aidan ZH Yang, Claire Le Goues, Ruben Martins, and Vincent Hellendoorn. Large language models for test-free fault localization. In _Proceedings of the 46th IEEE/ACM International Conference on Software Engineering_ , pages 1–12, 2024. 

- [84] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming Xiong. Codegen: An open large language model for code with multi-turn program synthesis. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. 

- [85] Erik Nijkamp, Hiroaki Hayashi, Caiming Xiong, Silvio Savarese, and Yingbo Zhou. Codegen2: Lessons for training llms on programming and natural languages. _arXiv preprint_ , 2023. 

- [86] Peter Ince, Xiapu Luo, Jiangshan Yu, Joseph K. Liu, and Xiaoning Du. _Detect Llama - Finding Vulnerabilities in Smart Contracts Using Large Language Models_ , page 424–443. Springer Nature Singapore, 2024. 

- [87] André Storhaug, Jingyue Li, and Tianyuan Hu. Efficient avoidance of vulnerabilities in auto-completed smart contract code using vulnerability-constrained decoding. In _2023 IEEE 34th International Symposium on Software Reliability Engineering (ISSRE)_ , pages 683–693. IEEE, 2023. 

- [88] Ben Wang. Mesh-Transformer-JAX: Model-Parallel Implementation of Transformer Language Model with JAX. `https://github.com/kingoflolz/mesh-transformer-jax` , May 2021. 

- [89] Jingxuan He, Mark Vero, Gabriela Krasnopolska, and Martin T. Vechev. Instruction tuning for secure code generation. In _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. 

- [90] Guochang Li, Chen Zhi, Jialiang Chen, Junxiao Han, and Shuiguang Deng. Exploring parameter-efficient fine-tuning of large language model on automated program repair. In _Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering_ , pages 719–731, 2024. 

- [91] Nan Jiang, Chengxiao Wang, Kevin Liu, Xiangzhe Xu, Lin Tan, and Xiangyu Zhang. Nova<sup>+</sup> : Generative language models for binaries. _arXiv preprint_ , 2023. 

- [92] Hongcheng Guo, Jian Yang, Jiaheng Liu, Liqun Yang, Linzheng Chai, Jiaqi Bai, Junran Peng, Xiaorong Hu, Chao Chen, Dongfeng Zhang, Xu Shi, Tieqiao Zheng, Liangfan Zheng, Bo Zhang, Ke Xu, and Zhoujun Li. OWL: A large language model for IT operations. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. 

- [93] Matan Levi, Yair Alluouche, Daniel Ohayon, and Anton Puzanov. Cyberpal. ai: Empowering llms with expert-driven cybersecurity instructions. _arXiv preprint_ , 2024. 

- [94] Bingchang Liu, Wei Huo, Chao Zhang, Wenchao Li, Feng Li, Aihua Piao, and Wei Zou. _α_ diff: cross-version binary code similarity detection with dnn. In _Proceedings of the 33rd ACM/IEEE international conference on automated software engineering_ , pages 667–678, 2018. 

- [95] Hao Wang, Wenjie Qu, Gilad Katz, Wenyu Zhu, Zeyu Gao, Han Qiu, Jianwei Zhuge, and Chao Zhang. Jtrans: Jump-aware transformer for binary code similarity detection. In _Proceedings of the 31st ACM SIGSOFT International Symposium on Software Testing and Analysis_ , pages 1–13, 2022. 

- [96] Hao Wang, Zeyu Gao, Chao Zhang, Zihan Sha, Mingyang Sun, Yuchen Zhou, Wenyu Zhu, Wenju Sun, Han Qiu, and Xi Xiao. Clap: Learning transferable binary code representations with natural language supervision. In _Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis_ , pages 503–515, 2024. 

30 

- [97] Guangmeng Zhou, Xiongwen Guo, Zhuotao Liu, Tong Li, Qi Li, and Ke Xu. Trafficformer: An efficient pre-trained model for traffic data, 2024. 

- [98] Vanessa Clairoux-Trepanier, Isa-May Beauchamp, Estelle Ruellan, Masarah Paquet-Clouston, Serge-Olivier Paquette, and Eric Clay. The use of large language models (llm) for cyber threat intelligence (cti) in cybercrime forums. _arXiv preprint_ , 2024. 

- [99] Shaswata Mitra, Subash Neupane, Trisha Chakraborty, Sudip Mittal, Aritran Piplai, Manas Gaur, and Shahram Rahimi. Localintel: Generating organizational threat intelligence from global and local cyber knowledge. _arXiv preprint_ , 2024. 

- [100] Filippo Perrina, Francesco Marchiori, Mauro Conti, and Nino Vincenzo Verde. AGIR: automating cyber threat intelligence reporting with natural language generation. In Jingrui He, Themis Palpanas, Xiaohua Hu, Alfredo Cuzzocrea, Dejing Dou, Dominik Slezak, Wei Wang, Aleksandra Gruca, Jerry Chun-Wei Lin, and Rakesh Agrawal, editors, _IEEE International Conference on Big Data, BigData 2023, Sorrento, Italy, December 15-18, 2023_ , pages 3053–3062. IEEE, 2023. 

- [101] Reza Fayyazi and Shanchieh Jay Yang. On the uses of large language models to interpret ambiguous cyberattack descriptions. _arXiv preprint_ , 2023. 

- [102] Reza Fayyazi, Rozhina Taghdimi, and Shanchieh Jay Yang. Advancing ttp analysis: Harnessing the power of encoder-only and decoder-only language models with retrieval augmented generation. _arXiv preprint_ , 2024. 

- [103] Yuval Schwartz, Lavi Benshimol, Dudu Mimran, Yuval Elovici, and Asaf Shabtai. Llmcloudhunter: Harnessing llms for automated extraction of detection rules from cloud-based cti. _arXiv preprint_ , 2024. 

- [104] Tanmay Singla, Dharun Anandayuvaraj, Kelechi G. Kalu, Taylor R. Schorlemmer, and James C. Davis. An empirical study on using large language models to analyze software supply chain security failures. In _Proceedings of the 2023 Workshop on Software Supply Chain Offensive Research and Ecosystem Defenses_ , SCORED ’23, page 5–15, New York, NY, USA, 2023. Association for Computing Machinery. 

- [105] Samaneh Shafee, Alysson Bessani, and Pedro M. Ferreira. Evaluation of llm-based chatbots for osint-based cyber threat awareness. _Expert Syst. Appl._ , 261:125509, 2025. 

- [106] Gaëtan Michelet and Frank Breitinger. Chatgpt, llama, can you write my report? an experiment on assisted digital forensics reports written using (local) large language models. _Forensic Sci. Int. Digit. Investig._ , 48:301683, 2024. 

- [107] Giuseppe Siracusano, Davide Sanvito, Roberto Gonzalez, Manikantan Srinivasan, Sivakaman Kamatchi, Wataru Takahashi, Masaru Kawakita, Takahiro Kakumaru, and Roberto Bifulco. Time for action: Automated analysis of cyber threat intelligence in the wild. _arXiv preprint_ , 2023. 

- [108] Yuelin Hu, Futai Zou, Jiajia Han, Xin Sun, and Yilei Wang. LLM-TIKG: threat intelligence knowledge graph construction utilizing large language model. _Comput. Secur._ , 145:103999, 2024. 

- [109] Sean Barnum. Standardizing cyber threat intelligence information with the structured threat information expression (stix). _Mitre Corporation_ , 11:1–22, 2012. 

- [110] Yongheng Zhang, Tingwen Du, Yunshan Ma, Xiang Wang, Yi Xie, Guozheng Yang, Yuliang Lu, and Ee-Chien Chang. Attackg+: Boosting attack knowledge graph construction with large language models. _arXiv preprint_ , 2024. 

- [111] Romy Fieblinger, Md Tanvirul Alam, and Nidhi Rastogi. Actionable cyber threat intelligence using knowledge graphs and large language models. In _2024 IEEE European Symposium on Security and Privacy Workshops (EuroS&PW)_ , pages 100–111. IEEE, 2024. 

- [112] Ting Zhang, Ivana Clairine Irsan, Ferdian Thung, and David Lo. Cupid: Leveraging chatgpt for more accurate duplicate bug report detection. _arXiv preprint_ , 2023. 

- [113] Chengnian Sun, David Lo, Siau-Cheng Khoo, and Jing Jiang. Towards more accurate retrieval of duplicate bug reports. In Perry Alexander, Corina S. Pasareanu, and John G. Hosking, editors, _26th IEEE/ACM International Conference on Automated Software Engineering (ASE 2011), Lawrence, KS, USA, November 6-10, 2011_ , pages 253–262. IEEE Computer Society, 2011. 

- [114] Yu-Zheng Lin, Muntasir Mamun, Muhtasim Alam Chowdhury, Shuyu Cai, Mingyu Zhu, Banafsheh Saber Latibari, Kevin Immanuel Gubbi, Najmeh Nazari Bavarsad, Arjun Caputo, Avesta Sasan, Houman Homayoun, Setareh Rafatirad, Pratik Satam, and Soheil Salehi. Hw-v2w-map: Hardware vulnerability to weakness mapping framework for root cause analysis with gpt-assisted mitigation suggestion. _arXiv preprint_ , 2023. 

- [115] Mehrdad Kaheh, Danial Khosh Kholgh, and Panos Kostakos. Cyber sentinel: Exploring conversational agents in streamlining security tasks with gpt-4. _arXiv preprint_ , 2023. 

31 

- [116] Jiandong Jin, Bowen Tang, Mingxuan Ma, Xiao Liu, Yunfei Wang, Qingnan Lai, Jia Yang, and Changling Zhou. Crimson: Empowering strategic reasoning in cybersecurity through large language models. _arXiv preprint_ , 2024. 

- [117] PeiYu Tseng, ZihDwo Yeh, Xushu Dai, and Peng Liu. Using llms to automate threat intelligence analysis workflows in security operation centers. _arXiv preprint_ , 2024. 

- [118] Sampath Rajapaksha, Ruby Rani, and Erisa Karafili. A rag-based question-answering solution for cyber-attack investigation and attribution. _arXiv preprint_ , 2024. 

- [119] Zongzong Wu, Fengxiao Tang, Ming Zhao, and Yufeng Li. Kgv: Integrating large language models with knowledge graphs for cyber threat intelligence credibility assessment. _arXiv preprint_ , 2024. 

- [120] Xin Zhou, Sicong Cao, Xiaobing Sun, and David Lo. Large language model for vulnerability detection and repair: Literature review and roadmap. _arXiv preprint_ , 2024. 

- [121] Karl Tamberg and Hayretdin Bahsi. Harnessing large language models for software vulnerability detection: A comprehensive benchmarking study. _arXiv preprint_ , 2024. 

- [122] Xin Zhou, Duc-Manh Tran, Thanh Le-Cong, Ting Zhang, Ivana Clairine Irsan, Joshua Sumarlin, Bach Le, and David Lo. Comparison of static application security testing tools and large language models for repo-level vulnerability detection. _arXiv preprint_ , 2024. 

- [123] Andrew A Mahyari. 

   - _arXiv preprint_ , 2024. 

- [124] Qiheng Mao, Zhenhao Li, Xing Hu, Kui Liu, Xin Xia, and Jianling Sun. Towards effectively detecting and explaining vulnerabilities using large language models. _arXiv preprint_ , 2024. 

- [125] Anton Cheshkov, Pavel Zadorozhny, and Rodion Levichev. Evaluation of chatgpt model for vulnerability detection. _arXiv preprint_ , 2023. 

- [126] Moumita Das Purba, Arpita Ghosh, Benjamin J. Radford, and Bill Chu. Software vulnerability detection using large language models. In _2023 IEEE 34th International Symposium on Software Reliability Engineering Workshops (ISSREW)_ , pages 112–119, 2023. 

- [127] Marwan Omar and Stavros Shiaeles. Vuldetect: A novel technique for detecting software vulnerabilities using language models. In _IEEE International Conference on Cyber Security and Resilience, CSR 2023, Venice, Italy, July 31 - Aug. 2, 2023_ , pages 105–110. IEEE, 2023. 

- [128] Avishree Khare, Saikat Dutta, Ziyang Li, Alaia Solko-Breslin, Rajeev Alur, and Mayur Naik. Understanding the effectiveness of large language models in detecting security vulnerabilities. _arXiv preprint_ , 2023. 

- [129] Rasmus Ingemann Tuffveson Jensen, Vali Tawosi, and Salwa Alamir. Software vulnerability and functionality assessment using llms. _arXiv preprint_ , 2024. 

- [130] Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian. The hitchhiker’s guide to program analysis: A journey with large language models. _arXiv preprint_ , 2023. 

- [131] Vasileios Kouliaridis, Georgios Karopoulos, and Georgios Kambourakis. Assessing the effectiveness of llms in android application vulnerability analysis. _arXiv preprint_ , 2024. 

- [132] Yuejun Guo, Constantinos Patsakis, Qiang Hu, Qiang Tang, and Fran Casino. Outside the comfort zone: Analysing llm capabilities in software vulnerability detection. In _European symposium on research in computer security_ , pages 271–289. Springer, 2024. 

- [133] Jin Wang, Zishan Huang, Hengli Liu, Nianyi Yang, and Yinhao Xiao. Defecthunter: A novel llm-driven boosted-conformer-based code vulnerability detection mechanism. _arXiv preprint_ , 2023. 

- [134] Anmol Gulati, James Qin, Chung-Cheng Chiu, Niki Parmar, Yu Zhang, Jiahui Yu, Wei Han, Shibo Wang, Zhengdong Zhang, Yonghui Wu, and Ruoming Pang. Conformer: Convolution-augmented transformer for speech recognition. In Helen Meng, Bo Xu, and Thomas Fang Zheng, editors, _21st Annual Conference of the International Speech Communication Association, Interspeech 2020, Virtual Event, Shanghai, China, October 25-29, 2020_ , pages 5036–5040. ISCA, 2020. 

- [135] Chenyuan Zhang, Hao Liu, Jiutian Zeng, Kejing Yang, Yuhong Li, and Hui Li. Prompt-enhanced software vulnerability detection using chatgpt. In _Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings, ICSE Companion 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 276–277. ACM, 2024. 

- [136] Atieh Bakhshandeh, Abdalsamad Keramatfar, Amir Norouzi, and Mohammad Mahdi Chekidehkhoun. Using chatgpt as a static application security testing tool. _arXiv preprint_ , 2023. 

- [137] Noble Saji Mathews, Yelizaveta Brus, Yousra Aafer, Mei Nagappan, and Shane McIntosh. Llbezpeky: Leveraging large language models for vulnerability detection. _arXiv preprint_ , 2024. 

32 

- [138] Yu-Tsung Lee, Hayawardh Vijayakumar, Zhiyun Qian, and Trent Jaeger. Static detection of filesystem vulnerabilities in android systems. _arXiv preprint_ , 2024. 

- [139] Yanjing Yang, Xin Zhou, Runfeng Mao, Jinwei Xu, Lanxin Yang, Yu Zhang, Haifeng Shen, and He Zhang. Dlap: A deep learning augmented large language model prompting framework for software vulnerability detection. _Journal of Systems and Software_ , 219:112234, 2025. 

- [140] Weizhou Wang, Eric Liu, Xiangyu Guo, and David Lie. Anvil: Anomaly-based vulnerability identification without labelled training data. _arXiv preprint_ , 2024. 

- [141] Xu Yang, Gopi Krishnan Rajbahadur, Dayi Lin, Shaowei Wang, and Zhen Ming (Jack) Jiang. Simclone: Detecting tabular data clones using value similarity. _ACM Transactions on Software Engineering and Methodology_ , July 2024. 

- [142] Xueying Du, Geng Zheng, Kaixin Wang, Jiayi Feng, Wentai Deng, Mingwei Liu, Bihuan Chen, Xin Peng, Tao Ma, and Yiling Lou. Vul-rag: Enhancing llm-based vulnerability detection via knowledge-level rag. _arXiv preprint_ , 2024. 

- [143] Sihao Hu, Tiansheng Huang, Fatih Ilhan, Selim Furkan Tekin, and Ling Liu. Large language model-powered smart contract vulnerability detection: New perspectives. In _5th IEEE International Conference on Trust, Privacy and Security in Intelligent Systems and Applications, TPS-ISA 2023, Atlanta, GA, USA, November 1-4, 2023_ , pages 297–306. IEEE, 2023. 

- [144] Zhihong Liu, Qing Liao, Wenchao Gu, and Cuiyun Gao. Software vulnerability detection with gpt and in-context learning. In _2023 8th International Conference on Data Science in Cyberspace (DSC)_ , pages 229–236, 2023. 

- [145] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Haijun Wang, Zhengzi Xu, Xiaofei Xie, and Yang Liu. Gptscan: Detecting logic vulnerabilities in smart contracts by combining GPT with program analysis. In _Proceedings of the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 166:1–166:13. ACM, 2024. 

- [146] Xiaohu Du, Ming Wen, Jiahao Zhu, Zifan Xie, Bin Ji, Huijun Liu, Xuanhua Shi, and Hai Jin. Generalizationenhanced code vulnerability detection via multi-task instruction fine-tuning. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024_ , pages 10507–10521. Association for Computational Linguistics, 2024. 

- [147] Yuqiang Sun, Daoyuan Wu, Yue Xue, Han Liu, Wei Ma, Lyuye Zhang, Miaolei Shi, and Yang Liu. Llm4vuln: A unified evaluation framework for decoupling and enhancing llms’ vulnerability reasoning. _arXiv preprint_ , 2024. 

- [148] Zhenyu Mao, Jialong Li, Munan Li, and Kenji Tei. Multi-role consensus through llms discussions for vulnerability detection. _arXiv preprint_ , 2024. 

- [149] Ziyang Li, Saikat Dutta, and Mayur Naik. Llm-assisted static analysis for detecting security vulnerabilities. _arXiv preprint_ , 2024. 

- [150] Tianyu Chen, Lin Li, Liuchuan Zhu, Zongyang Li, Guangtai Liang, Ding Li, Qianxiang Wang, and Tao Xie. Vullibgen: Identifying vulnerable third-party libraries via generative pre-trained model. _arXiv preprint_ , 2023. 

- [151] Peiyu Liu, Junming Liu, Lirong Fu, Kangjie Lu, Yifan Xia, Xuhong Zhang, Wenzhi Chen, Haiqin Weng, Shouling Ji, and Wenhai Wang. How chatgpt is solving vulnerability management problem. _arXiv preprint_ , 2023. 

- [152] Yizheng Chen, Zhoujie Ding, Lamya Alowain, Xinyun Chen, and David Wagner. Diversevul: A new vulnerable source code dataset for deep learning based vulnerability detection. In _Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses_ , RAID ’23, page 654–668, New York, NY, USA, 2023. Association for Computing Machinery. 

- [153] Zeyu Gao, Hao Wang, Yuchen Zhou, Wenyu Zhu, and Chao Zhang. How far have we gone in vulnerability detection using large language models. _arXiv preprint_ , 2023. 

- [154] Norbert Tihanyi, Tamas Bisztray, Ridhi Jain, Mohamed Amine Ferrag, Lucas C. Cordeiro, and Vasileios Mavroeidis. The formai dataset: Generative ai in software security through the lens of formal verification. In _Proceedings of the 19th International Conference on Predictive Models and Data Analytics in Software Engineering_ , PROMISE 2023, page 33–43, New York, NY, USA, 2023. Association for Computing Machinery. 

- [155] José Gonçalves, Tiago Dias, Eva Maia, and Isabel Praça. Scope: Evaluating llms for software vulnerability detection. _arXiv preprint_ , 2024. 

- [156] Hammond Pearce, Benjamin Tan, Prashanth Krishnamurthy, Farshad Khorrami, Ramesh Karri, and Brendan Dolan-Gavitt. Pop quiz! can a large language model help with reverse engineering? _arXiv preprint_ , 2022. 

33 

- [157] Hanzhuo Tan, Qi Luo, Jing Li, and Yuqun Zhang. Llm4decompile: Decompiling binary code with large language models. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16, 2024_ , pages 3473–3487. Association for Computational Linguistics, 2024. 

- [158] Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu, Ruoyu Zhang, Ruijie Fang, Asmita, Ryan Tsang, Najmeh Nazari, Han Wang, and Houman Homayoun. Large language models for code analysis: Do llms really do their job? In Davide Balzarotti and Wenyuan Xu, editors, _33rd USENIX Security Symposium, USENIX Security 2024, Philadelphia, PA, USA, August 14-16, 2024_ . USENIX Association, 2024. 

- [159] Jianyu Zhao, Yuyang Rong, Yiwen Guo, Yifeng He, and Hao Chen. Understanding programs by exploiting (fuzzing) test cases. In Anna Rogers, Jordan L. Boyd-Graber, and Naoaki Okazaki, editors, _Findings of the Association for Computational Linguistics: ACL 2023, Toronto, Canada, July 9-14, 2023_ , pages 10667–10679. Association for Computational Linguistics, 2023. 

- [160] David N Palacio, Alejandro Velasco, Daniel Rodriguez-Cardenas, Kevin Moran, and Denys Poshyvanyk. Evaluating and explaining large language models for code using syntactic structures. _arXiv preprint_ , 2023. 

- [161] Pei Yan, Shunquan Tan, Miaohui Wang, and Jiwu Huang. Prompt engineering-assisted malware dynamic analysis using gpt-4. _arXiv preprint_ , 2023. 

- [162] Himari Fujima, Takako Kumamoto, and Yunko Yoshida. Using chatgpt to analyze ransomware messages and to predict ransomware threats, 2023. 

- [163] Fang Wang. Using large language models to mitigate ransomware threats. _Preprints_ , 2023. 

- [164] Nusrat Zahan, Philipp Burckhardt, Mikola Lysenko, Feross Aboukhadijeh, and Laurie Williams. Shifting the lens: Detecting malware in npm ecosystem with large language models. _arXiv preprint_ , 2024. 

- [165] Haolang Lu, Hongrui Peng, Guoshun Nan, Jiaoyang Cui, Cheng Wang, Weifei Jin, Songtao Wang, Shengli Pan, and Xiaofeng Tao. Malsight: Exploring malicious source code and benign pseudocode for iterative binary malware summarization. _arXiv preprint_ , 2024. 

- [166] Zhe Liu, Chunyang Chen, Junjie Wang, Mengzhuo Chen, Boyu Wu, Xing Che, Dandan Wang, and Qing Wang. Make LLM a testing expert: Bringing human-like interaction to mobile GUI testing via functionality-aware decisions. In _Proceedings of the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 100:1–100:13. ACM, 2024. 

- [167] Baleegh Ahmad, Benjamin Tan, Ramesh Karri, and Hammond Pearce. Flag: Finding line anomalies (in code) with generative ai. _arXiv preprint_ , 2023. 

- [168] Egil Karlsen, Xiao Luo, Nur Zincir-Heywood, and Malcolm I. Heywood. Benchmarking large language models for log analysis, security, and interpretation. _J. Netw. Syst. Manag._ , 32(3):59, 2024. 

- [169] Jinyang Liu, Junjie Huang, Yintong Huo, Zhihan Jiang, Jiazhen Gu, Zhuangbin Chen, Cong Feng, Minzhi Yan, and Michael R. Lyu. Log-based anomaly detection based on evt theory with feedback. _arXiv preprint_ , 2023. 

- [170] Jiaxing Qi, Shaohan Huang, Zhongzhi Luan, Shu Yang, Carol J. Fung, Hailong Yang, Depei Qian, Jing Shang, Zhiwen Xiao, and Zhihui Wu. Loggpt: Exploring chatgpt for log-based anomaly detection. In _IEEE International Conference on High Performance Computing & Communications, Data Science & Systems, Smart City & Dependability in Sensor, Cloud & Big Data Systems & Application, HPCC/DSS/SmartCity/DependSys 2023, Melbourne, Australia, December 17-21, 2023_ , pages 273–280. IEEE, 2023. 

- [171] Xiao Han, Shuhan Yuan, and Mohamed Trabelsi. Loggpt: Log anomaly detection via GPT. In Jingrui He, Themis Palpanas, Xiaohua Hu, Alfredo Cuzzocrea, Dejing Dou, Dominik Slezak, Wei Wang, Aleksandra Gruca, Jerry Chun-Wei Lin, and Rakesh Agrawal, editors, _IEEE International Conference on Big Data, BigData 2023, Sorrento, Italy, December 15-18, 2023_ , pages 1117–1122. IEEE, 2023. 

- [172] Yilun Liu, Shimin Tao, Weibin Meng, Jingyu Wang, Wenbing Ma, Yuhang Chen, Yanqing Zhao, Hao Yang, and Yanfei Jiang. Interpretable online log analysis using large language models with prompt strategies. In Igor Steinmacher, Mario Linares-Vásquez, Kevin Patrick Moran, and Olga Baysal, editors, _Proceedings of the 32nd IEEE/ACM International Conference on Program Comprehension, ICPC 2024, Lisbon, Portugal, April 15-16, 2024_ , pages 35–46. ACM, 2024. 

- [173] Wei Zhang, Hongcheng Guo, Anjie Le, Jian Yang, Jiaheng Liu, Zhoujun Li, Tieqiao Zheng, Shi Xu, Runqiang Zang, Liangfan Zheng, and Bo Zhang. Lemur: Log parsing with entropy sampling and chain-of-thought merging. _arXiv preprint_ , 2024. 

- [174] Suhaima Jamal and Hayden Wimmer. An improved transformer-based model for detecting phishing, spam, and ham: A large language model approach. _arXiv preprint_ , 2023. 

34 

- [175] Yuwei Wu, Shijing Si, Yugui Zhang, Jiawen Gu, and Jedrek Wosik. Evaluating the performance of chatgpt for spam email detection. _arXiv preprint_ , 2024. 

- [176] Daniel Nahmias, Gal Engelberg, Dan Klein, and Asaf Shabtai. Prompted contextual vectors for spear-phishing detection. _arXiv preprint_ , 2024. 

- [177] Fredrik Heiding, Bruce Schneier, Arun Vishwanath, Jeremy Bernstein, and Peter S. Park. Devising and detecting phishing: Large language models vs. smaller human models. _arXiv preprint_ , 2023. 

- [178] Tamás Vörös, Sean Paul Bergeron, and Konstantin Berlin. Web content filtering through knowledge distillation of large language models. In _IEEE International Conference on Web Intelligence and Intelligent Agent Technology, WI-IAT 2023, Venice, Italy, October 26-29, 2023_ , pages 357–361. IEEE, 2023. 

- [179] Michael Guastalla, Yiyi Li, Arvin Hekmati, and Bhaskar Krishnamachari. Application of large language models to ddos attack detection. In _International Conference on Security and Privacy in Cyber-Physical Systems and Smart Vehicles_ , pages 83–99. Springer, 2023. 

- [180] Mohamed Amine Ferrag, Mthandazo Ndhlovu, Norbert Tihanyi, Lucas C. Cordeiro, Mérouane Debbah, Thierry Lestable, and Narinderjit Singh Thandi. Revolutionizing cyber threat detection with large language models: A privacy-preserving bert-based lightweight model for iot/iiot devices. _IEEE Access_ , 12:23733–23750, 2024. 

- [181] Noah Ziems, Gang Liu, John Flanagan, and Meng Jiang. Explaining tree model decisions in natural language for network intrusion detection. _arXiv preprint_ , 2023. 

- [182] Tarek Ali and Panos Kostakos. Huntgpt: Integrating machine learning-based anomaly detection and explainable ai with large language models (llms). _arXiv preprint_ , 2023. 

- [183] Mark Scanlon, Frank Breitinger, Christopher Hargreaves, Jan-Niclas Hilgert, and John Sheppard. Chatgpt for digital forensic investigation: The good, the bad, and the unknown. _Forensic Science International: Digital Investigation_ , 46:301609, 2023. 

- [184] Yu Jiang, Jie Liang, Fuchen Ma, Yuanliang Chen, Chijin Zhou, Yuheng Shen, Zhiyong Wu, Jingzhou Fu, Mingzhe Wang, Shanshan Li, et al. When fuzzing meets llms: Challenges and opportunities. In _Companion Proceedings of the 32nd ACM International Conference on the Foundations of Software Engineering_ , pages 492–496, 2024. 

- [185] Bo Wang, Mingda Chen, Youfang Lin, Mike Papadakis, and Jie M Zhang. An exploratory study on using large language models for mutation testing. _arXiv preprint_ , 2024. 

- [186] Ying Zhang, Wenjia Song, Zhengjie Ji, Danfeng, Yao, and Na Meng. How well does llm generate security tests? _arXiv preprint_ , 2023. 

- [187] Jie Hu, Qian Zhang, and Heng Yin. Augmenting greybox fuzzing with generative ai. _arXiv preprint_ , 2023. 

- [188] Chunqiu Steven Xia, Matteo Paltenghi, Jia Le Tian, Michael Pradel, and Lingming Zhang. Fuzz4all: Universal fuzzing with large language models. In _Proceedings of the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 126:1–126:13. ACM, 2024. 

- [189] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K. Lahiri, and Siddhartha Sen. Codamosa: Escaping coverage plateaus in test generation ·with pre-trained large language models. In _2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE)_ , pages 919–931, 2023. 

- [190] Cen Zhang, Mingqiang Bai, Yaowen Zheng, Yeting Li, Xiaofei Xie, Yuekang Li, Wei Ma, Limin Sun, and Yang Liu. Understanding large language model based fuzz driver generation. _arXiv preprint_ , 2023. 

- [191] Yinlin Deng, Chunqiu Steven Xia, Haoran Peng, Chenyuan Yang, and Lingming Zhang. Large language models are zero-shot fuzzers: Fuzzing deep-learning libraries via large language models. In _Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis_ , ISSTA 2023, page 423–435, New York, NY, USA, 2023. Association for Computing Machinery. 

- [192] Yinlin Deng, Chunqiu Steven Xia, Chenyuan Yang, Shizhuo Dylan Zhang, Shujing Yang, and Lingming Zhang. Large language models are edge-case fuzzers: Testing deep learning libraries via fuzzgpt. _arXiv preprint_ , 2023. 

- [193] Ruijie Meng, Martin Mirchev, Marcel Böhme, and Abhik Roychoudhury. Large language model guided protocol fuzzing. In _31st Annual Network and Distributed System Security Symposium, NDSS 2024, San Diego, California, USA, February 26 - March 1, 2024_ . The Internet Society, 2024. 

- [194] Asmita, Yaroslav Oliinyk, Michael Scott, Ryan Tsang, Chongzhou Fang, and Houman Homayoun. Fuzzing busybox: Leveraging LLM and crash reuse for embedded bug unearthing. In Davide Balzarotti and Wenyuan Xu, editors, _33rd USENIX Security Symposium, USENIX Security 2024, Philadelphia, PA, USA, August 14-16, 2024_ . USENIX Association, 2024. 

35 

- [195] Quanjun Zhang, Chunrong Fang, Yang Xie, YuXiang Ma, Weisong Sun, Yun Yang, and Zhenyu Chen. A systematic literature review on large language models for automated program repair. _arXiv preprint_ , 2024. 

- [196] Julian Aron Prenner and Romain Robbes. Automatic program repair with openai’s codex: Evaluating quixbugs. _arXiv preprint_ , 2021. 

- [197] Dominik Sobania, Martin Briesch, Carol Hanna, and Justyna Petke. An analysis of the automatic bug fixing performance of chatgpt. In _IEEE/ACM International Workshop on Automated Program Repair, APR@ICSE 2023, Melbourne, Australia, May 16, 2023_ , pages 23–30. IEEE, 2023. 

- [198] Jan Keller and Jan Nowakowski. Ai-powered patching: the future of automated vulnerability fixes. Technical report, google, 2024. 

- [199] Jiaxin Yu, Peng Liang, Yujia Fu, Amjed Tahir, Mojtaba Shahin, Chong Wang, and Yangxiao Cai. Security code review by llms: A deep dive into responses. _arXiv preprint_ , 2024. 

- [200] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. Practical program repair in the era of large pre-trained language models. _arXiv preprint_ , 2022. 

- [201] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Brendan Dolan-Gavitt. Examining zero-shot vulnerability repair with large language models. In _2023 IEEE Symposium on Security and Privacy (SP)_ , pages 2339–2356, 2023. 

- [202] Yi Wu, Nan Jiang, Hung Viet Pham, Thibaud Lutellier, Jordan Davis, Lin Tan, Petr Babkin, and Sameena Shah. How effective are neural networks for fixing security vulnerabilities. In _Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis_ , ISSTA ’23. ACM, July 2023. 

- [203] Jiahong Xiang, Xiaoyang Xu, Fanchu Kong, Mingyuan Wu, Zizheng Zhang, Haotian Zhang, and Yuqun Zhang. How far can we go with practical function-level program repair? _arXiv preprint_ , 2024. 

- [204] Matthew Jin, Syed Shahriar, Michele Tufano, Xin Shi, Shuai Lu, Neel Sundaresan, and Alexey Svyatkovskiy. Inferfix: End-to-end program repair with llms. In Satish Chandra, Kelly Blincoe, and Paolo Tonella, editors, _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering, ESEC/FSE 2023, San Francisco, CA, USA, December 3-9, 2023_ , pages 1646–1656. ACM, 2023. 

- [205] Junjielong Xu, Ying Fu, Shin Hwei Tan, and Pinjia He. Aligning llms for fl-free program repair. _arXiv preprint_ , 2024. 

- [206] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. Teaching large language models to self-debug. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. 

- [207] Toufique Ahmed and Premkumar Devanbu. Better patching using llm prompting, via self-consistency. In _2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)_ , pages 1742–1746, 2023. 

- [208] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023. 

- [209] Ummay Kulsum, Haotian Zhu, Bowen Xu, and Marcelo d’Amorim. A case study of llm for automated vulnerability repair: Assessing impact of reasoning and patch validation feedback. In _Proceedings of the 1st ACM International Conference on AI-Powered Software_ , pages 103–111, 2024. 

- [210] Jiuang Zhao, Donghao Yang, Li Zhang, Xiaoli Lian, Zitian Yang, and Fang Liu. Enhancing automated program repair with solution design. In _Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering_ , pages 1706–1718, 2024. 

- [211] Aidan Z. H. Yang, Sophia Kolak, Vincent J. Hellendoorn, Ruben Martins, and Claire Le Goues. Revisiting unnaturalness for automated program repair in the era of large language models. _arXiv preprint_ , 2024. 

- [212] Xin Yin, Chao Ni, Shaohua Wang, Zhenhao Li, Limin Zeng, and Xiaohu Yang. Thinkrepair: Self-directed automated program repair. In _Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis_ , pages 1274–1286, 2024. 

- [213] Yuxiang Wei, Chunqiu Steven Xia, and Lingming Zhang. Copiloting the copilots: Fusing large language models with completion engines for automated program repair. In _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , ESEC/FSE 2023, page 172–184, New York, NY, USA, 2023. Association for Computing Machinery. 

36 

- [214] Nafis Tanveer Islam, Joseph Khoury, Andrew Seong, Mohammad Bahrami Karkevandi, Gonzalo De La Torre Parra, Elias Bou-Harb, and Peyman Najafirad. Llm-powered code vulnerability repair with reinforcement learning and semantic reward. _arXiv preprint_ , 2024. 

- [215] Yunan Wang, Tingyu Guo, Zilong Huang, and Yuan Yuan. Revisiting evolutionary program repair via code language model. _arXiv preprint_ , 2024. 

- [216] Jiaolong Kong, Mingfei Cheng, Xiaofei Xie, Shangqing Liu, Xiaoning Du, and Qi Guo. Contrastrepair: Enhancing conversation-based automated program repair via contrastive test case pairs. _arXiv preprint_ , 2024. 

- [217] Yuxiao Chen, Jingzheng Wu, Xiang Ling, Changjiang Li, Zhiqing Rui, Tianyue Luo, and Yanjun Wu. When large language models confront repository-level automatic program repair: How well they done? In _Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings, ICSE Companion 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 459–471. ACM, 2024. 

- [218] Boyang Yang, Haoye Tian, Jiadong Ren, Hongyu Zhang, Jacques Klein, Tegawendé F. Bissyandé, Claire Le Goues, and Shunfu Jin. Multi-objective fine-tuning for enhanced program repair with llms. _arXiv preprint_ , 2024. 

- [219] David de-Fitero-Dominguez, Eva García-López, Antonio García-Cabot, and José Javier Martínez-Herráiz. Enhanced automated code vulnerability repair using large language models. _Eng. Appl. Artif. Intell._ , 138:109291, 2024. 

- [220] Yuze Zhao, Zhenya Huang, Yixiao Ma, Rui Li, Kai Zhang, Hao Jiang, Qi Liu, Linbo Zhu, and Yu Su. Repair: Automated program repair with process-based feedback. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024_ , pages 16415–16429. Association for Computational Linguistics, 2024. 

- [221] Meghdad Dehghan, Jie JW Wu, Fatemeh H. Fard, and Ali Ouni. Mergerepair: An exploratory study on merging task-specific adapters in code llms for automated program repair. _arXiv preprint_ , 2024. 

- [222] M. Caner Tol and Berk Sunar. Zeroleak: Using llms for scalable and cost effective side-channel patching. _arXiv preprint_ , 2023. 

- [223] Sudipta Paria, Aritra Dasgupta, and Swarup Bhunia. Divas: An llm-based end-to-end framework for soc security analysis and policy-based protection. _arXiv preprint_ , 2023. 

- [224] Baleegh Ahmad, Shailja Thakur, Benjamin Tan, Ramesh Karri, and Hammond Pearce. Fixing hardware security bugs with large language models. _arXiv preprint_ , 2023. 

- [225] Yiannis Charalambous, Edoardo Manino, and Lucas C. Cordeiro. Automated repair of ai code with large language models and formal verification. _arXiv preprint_ , 2024. 

- [226] Tan Khang Le, Saba Alimadadi, and Steven Y. Ko. A study of vulnerability repair in javascript programs with large language models. In Tat-Seng Chua, Chong-Wah Ngo, Roy Ka-Wei Lee, Ravi Kumar, and Hady W. Lauw, editors, _Companion Proceedings of the ACM on Web Conference 2024, WWW 2024, Singapore, Singapore, May 13-17, 2024_ , pages 666–669. ACM, 2024. 

- [227] Kangwei Xu, Grace Li Zhang, Xunzhao Yin, Cheng Zhuo, Ulf Schlichtmann, and Bing Li. Automated c/c++ program repair for high-level synthesis via large language models. In _Proceedings of the 2024 ACM/IEEE International Symposium on Machine Learning for CAD_ , pages 1–9, 2024. 

- [228] Clark Barrett, Brad Boyd, Elie Bursztein, Nicholas Carlini, Brad Chen, Jihye Choi, Amrita Roy Chowdhury, Mihai Christodorescu, Anupam Datta, Soheil Feizi, et al. Identifying and mitigating the security risks of generative ai. _Foundations and Trends® in Privacy and Security_ , 6(1):1–52, 2023. 

- [229] Pawankumar Sharma and Bibhu Dash. Impact of big data analytics and chatgpt on cybersecurity. In _2023 4th International Conference on Computing and Communication Systems (I3CS)_ , pages 1–6, 2023. 

- [230] Maanak Gupta, Charankumar Akiri, Kshitiz Aryal, Eli Parker, and Lopamudra Praharaj. From chatgpt to threatgpt: Impact of generative ai in cybersecurity and privacy. _IEEE Access_ , 11:80218–80245, 2023. 

- [231] Stephen Moskal, Sam Laney, Erik Hemberg, and Una-May O’Reilly. Llms killed the script kiddie: How agents supported by large language models change the landscape of network threat testing. _arXiv preprint_ , 2023. 

- [232] Zilong Lin, Jian Cui, Xiaojing Liao, and XiaoFeng Wang. Malla: Demystifying real-world large language model integrated malicious services. In Davide Balzarotti and Wenyuan Xu, editors, _33rd USENIX Security Symposium, USENIX Security 2024, Philadelphia, PA, USA, August 14-16, 2024_ . USENIX Association, 2024. 

- [233] Gelei Deng, Yi Liu, Víctor Mayoral-Vilches, Peng Liu, Yuekang Li, Yuan Xu, Tianwei Zhang, Yang Liu, Martin Pinzger, and Stefan Rass. Pentestgpt: An llm-empowered automatic penetration testing tool. _arXiv preprint_ , 2023. 

37 

- [234] Andreas Happe and Jürgen Cito. Getting pwn’d by ai: Penetration testing with large language models. In _Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , ESEC/FSE 2023, page 2082–2086, New York, NY, USA, 2023. Association for Computing Machinery. 

- [235] Junjie Huang and Quanyan Zhu. Penheal: A two-stage llm framework for automated pentesting and optimal remediation. In _Proceedings of the Workshop on Autonomous Cybersecurity_ , pages 11–22, 2023. 

- [236] Derry Pratama, Naufal Suryanto, Andro Aprila Adiputra, Thi-Thu-Huong Le, Ahmada Yusril Kadiptya, Muhammad Iqbal, and Howon Kim. Cipher: Cybersecurity intelligent penetration-testing helper for ethical researcher. _Sensors_ , 24(21):6878, October 2024. 

- [237] Jiacen Xu, Jack W. Stokes, Geoff McDonald, Xuesong Bai, David Marshall, Siyue Wang, Adith Swaminathan, and Zhou Li. Autoattacker: A large language model guided system to implement automatic cyber-attacks. _arXiv preprint_ , 2024. 

- [238] Lingzhi Wang, Jiahui Wang, Kyle Jung, Kedar Thiagarajan, Emily Wei, Xiangmin Shen, Yan Chen, and Zhenyuan Li. From sands to mansions: Enabling automatic full-life-cycle cyberattack construction with llm. _arXiv preprint_ , 2024. 

- [239] Yusuf Usman, Aadesh Upadhyay, Prashnna Gyawali, and Robin Chataut. Is generative ai the next tactical cyber weapon for threat actors? unforeseen implications of ai generated cyber attacks. _arXiv preprint_ , 2024. 

- [240] Nils Begou, Jérémy Vinoy, Andrzej Duda, and Maciej Korczy´nski. Exploring the dark side of ai: Advanced phishing attack design and deployment using chatgpt. In _2023 IEEE Conference on Communications and Network Security (CNS)_ , pages 1–6, 2023. 

- 

- [241] Sayak Saha Roy, Poojitha Thota, Krishna Vamsi Naragam, and Shirin Nilizadeh. From chatbots to phishbots? preventing phishing scams created using chatgpt, google bard and claude. _arXiv preprint_ , 2024. 

- [242] Jerson Francia, Derek Hansen, Ben Schooley, Matthew Taylor, Shydra Murray, and Greg Snow. Assessing ai vs human-authored spear phishing sms attacks: An empirical study using the trapd method. _arXiv preprint_ , 2024. 

- [243] Andreas Happe, Aaron Kaplan, and Jürgen Cito. Evaluating llms for privilege-escalation scenarios. _arXiv preprint_ , 2023. 

- [244] P. V. Sai Charan, Hrushikesh Chunduri, P. Mohan Anand, and Sandeep K Shukla. From text to mitre techniques: Exploring the malicious use of large language models for generating cyber attack payloads. _arXiv preprint_ , 2023. 

- [245] Renascence Tarafder Prapty, Ashish Kundu, and Arun Iyengar. Using retriever augmented large language models for attack graph generation. _arXiv preprint_ , 2024. 

- [246] Wesley Tann, Yuancheng Liu, Jun Heng Sim, Choon Meng Seah, and Ee-Chien Chang. Using large language models for cybersecurity capture-the-flag challenges and certification questions. _arXiv preprint_ , 2023. 

- [247] Mika Beckerich, Laura Plein, and Sergio Coronado. Ratgpt: Turning online llms into proxies for malware attacks. _arXiv preprint_ , 2023. 

- [248] Gustavo Sandoval, Hammond Pearce, Teo Nys, Ramesh Karri, Siddharth Garg, and Brendan Dolan-Gavitt. Lost at c: A user study on the security implications of large language model code assistants. In _32nd USENIX Security Symposium (USENIX Security 23)_ , pages 2205–2222, Anaheim, CA, August 2023. USENIX Association. 

- [249] Florian Tambon, Arghavan Moradi Dakhel, Amin Nikanjam, Foutse Khomh, Michel C. Desmarais, and Giuliano Antoniol. Bugs in large language models generated code: An empirical study. _arXiv preprint_ , 2024. 

- [250] Norbert Tihanyi, Tamas Bisztray, Mohamed Amine Ferrag, Ridhi Jain, and Lucas C. Cordeiro. Do neutral prompts produce insecure code? formai-v2 dataset: Labelling vulnerabilities in code generated by large language models. _arXiv preprint_ , 2024. 

- [251] Hammond Pearce, Baleegh Ahmad, Benjamin Tan, Brendan Dolan-Gavitt, and Ramesh Karri. Asleep at the keyboard? assessing the security of github copilot’s code contributions. In _2022 IEEE Symposium on Security and Privacy (SP)_ , pages 754–768, 2022. 

- [252] Jiexin Wang, Xitong Luo, Liuwen Cao, Hongkui He, Hailin Huang, Jiayuan Xie, Adam Jatowt, and Yi Cai. Is your ai-generated code really safe? evaluating large language models on secure code generation with codeseceval. _arXiv preprint_ , 2024. 

- [253] Zhilong Wang, Lan Zhang, Chen Cao, and Peng Liu. The effectiveness of large language models (chatgpt and codebert) for security-oriented code analysis. _Available at SSRN 4567887_ , 2023. 

- [254] Zhijie Liu, Yutian Tang, Xiapu Luo, Yuming Zhou, and Liang Feng Zhang. No need to lift a finger anymore? assessing the quality of code generation by chatgpt. _IEEE Trans. Software Eng._ , 50(6):1548–1584, 2024. 

38 

- [255] Mohammed Latif Siddiq and Joanna C. S. Santos. Generate and pray: Using sallms to evaluate the security of llm generated code. _arXiv preprint_ , 2023. 

- [256] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code generated by chatgpt really correct? rigorous evaluation of large language models for code generation. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [257] Saad Ullah, Mingji Han, Saurabh Pujar, Hammond Pearce, Ayse Coskun, and Gianluca Stringhini. Can large language models identify and reason about security vulnerabilities? not yet. _arXiv preprint_ , 2023. 

- [258] Alessio Buscemi. A comparative study of code generation using chatgpt 3.5 across 10 programming languages. _arXiv preprint_ , 2023. 

- [259] Raphaël Khoury, Anderson R. Avila, Jacob Brunelle, and Baba Mamadou Camara. How secure is code generated by chatgpt? In _IEEE International Conference on Systems, Man, and Cybernetics, SMC 2023, Honolulu, Oahu, HI, USA, October 1-4, 2023_ , pages 2445–2451. IEEE, 2023. 

- [260] Arya Kavian, Mohammad Mehdi Pourhashem Kallehbasti, Sajjad Kazemi, Ehsan Firouzi, and Mohammad Ghafari. Llm security guard for code. In _Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering_ , pages 600–603, 2024. 

- [261] Jingxuan He and Martin Vechev. Large language models for code: Security hardening and adversarial testing. In _Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security_ , CCS ’23. ACM, November 2023. 

- [262] Junjie Li, Fazle Rabbi, Cheng Cheng, Aseem Sangalay, Yuan Tian, and Jinqiu Yang. An exploratory study on fine-tuning large language models for secure code generation. _arXiv preprint_ , 2024. 

- [263] Hao Tang, Keya Hu, Jin Peng Zhou, Sicheng Zhong, Wei-Long Zheng, Xujie Si, and Kevin Ellis. Code repair with llms gives an exploration-exploitation tradeoff. _arXiv preprint_ , 2024. 

- [264] Kyle Wong, Alfonso Amayuelas, Liangming Pan, and William Yang Wang. Investigating the transferability of code repair for low-resource programming languages. _arXiv preprint_ , 2024. 

- [265] Armin Sarabi, Tongxin Yin, and Mingyan Liu. An llm-based framework for fingerprinting internet-connected devices. In _Proceedings of the 2023 ACM on Internet Measurement Conference_ , IMC ’23, page 478–484, New York, NY, USA, 2023. Association for Computing Machinery. 

- [266] Kai-Cheng Yang and Filippo Menczer. Anatomy of an ai-powered malicious social botnet. _arXiv preprint_ , 2023. 

- [267] Xunzhu Tang, Zhenghan Chen, Kisub Kim, Haoye Tian, Saad Ezzini, and Jacques Klein. Just-in-time security patch detection – llm at the rescue for data augmentation. _arXiv preprint_ , 2023. 

- [268] Dipayan Saha, Shams Tarek, Katayoon Yahyaei, Sujan Kumar Saha, Jingbo Zhou, Mark M. Tehranipoor, and Farimah Farahmandi. LLM for soc security: A paradigm shift. _IEEE Access_ , 12:155498–155521, 2024. 

- [269] Puzhuo Liu, Chengnian Sun, Yaowen Zheng, Xuan Feng, Chuan Qin, Yuncheng Wang, Zhi Li, and Limin Sun. Harnessing the power of llm to support binary taint analysis. _arXiv preprint_ , 2023. 

- [270] Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, and Madian Khabsa. Llama guard: Llm-based input-output safeguard for human-ai conversations. _arXiv preprint_ , 2023. 

- [271] Muris Sladic, Veronica Valeros, Carlos Adrián Catania, and Sebastian García. LLM in the shell: Generative honeypots. In _IEEE European Symposium on Security and Privacy Workshops, EuroS&PW 2024, Vienna, Austria, July 8-12, 2024_ , pages 430–435. IEEE, 2024. 

- [272] Daniel Reti, Norman Becker, Tillmann Angeli, Anasuya Chattopadhyay, Daniel Schneider, Sebastian Vollmer, and Hans D. Schotten. Act as a honeytoken generator! an investigation into honeytoken generation with large language models. _arXiv preprint_ , 2024. 

- [273] Christoforos Vasilatos, Dunia J. Mahboobeh, Hithem Lamri, Manaar Alam, and Michail Maniatakos. Llmpot: Automated llm-based industrial protocol and physical process emulation for ics honeypots. _arXiv preprint_ , 2024. 

- [274] Sam Hays and Dr. Jules White. Employing llms for incident response planning and review. _arXiv preprint_ , 2024. 

- [275] Sathiya Kumaran Mani, Yajie Zhou, Kevin Hsieh, Santiago Segarra, Trevor Eberl, Eliran Azulai, Ido Frizler, Ranveer Chandra, and Srikanth Kandula. Enhancing network management using code generated by large language models. In _Proceedings of the 22nd ACM Workshop on Hot Topics in Networks_ , HotNets ’23, page 196–204, New York, NY, USA, 2023. Association for Computing Machinery. 

39 

- [276] Sidong Feng and Chunyang Chen. Prompting is all you need: Automated android bug replay with large language models. In _Proceedings of the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 67:1–67:13. ACM, 2024. 

- [277] Samia Kabir, David N. Udo-Imeh, Bonan Kou, and Tianyi Zhang. Is stack overflow obsolete? an empirical study of the characteristics of chatgpt answers to stack overflow questions. In Florian ’Floyd’ Mueller, Penny Kyburz, Julie R. Williamson, Corina Sas, Max L. Wilson, Phoebe O. Toups Dugas, and Irina Shklovski, editors, _Proceedings of the CHI Conference on Human Factors in Computing Systems, CHI 2024, Honolulu, HI, USA, May 11-16, 2024_ , pages 935:1–935:17. ACM, 2024. 

- [278] Xuandong Zhao, Xianjun Yang, Tianyu Pang, Chao Du, Lei Li, Yu-Xiang Wang, and William Yang Wang. Weak-to-strong jailbreaking on large language models. _arXiv preprint_ , 2024. 

- [279] Surender Suresh Kumar, ML Cummings, and Alexander Stimpson. Strengthening llm trust boundaries: A survey of prompt injection attacks surender suresh kumar dr. ml cummings dr. alexander stimpson. In _2024 IEEE 4th International Conference on Human-Machine Systems (ICHMS)_ , pages 1–6. IEEE, 2024. 

- [280] Aysan Esmradi, Daniel Wankit Yip, and Chun-Fai Chan. A comprehensive survey of attack techniques, implementation, and mitigation strategies in large language models. In Guojun Wang, Haozhe Wang, Geyong Min, Nektarios Georgalas, and Weizhi Meng, editors, _Ubiquitous Security - Third International Conference, UbiSec 2023, Exeter, UK, November 1-3, 2023, Revised Selected Papers_ , volume 2034 of _Communications in Computer and Information Science_ , pages 76–95. Springer, 2023. 

- [281] Fangzhou Wu, Ning Zhang, Somesh Jha, Patrick McDaniel, and Chaowei Xiao. A new era in llm security: Exploring security concerns in real-world llm-based systems. _arXiv preprint_ , 2024. 

- [282] Junjie Chu, Yugeng Liu, Ziqing Yang, Xinyue Shen, Michael Backes, and Yang Zhang. Comprehensive assessment of jailbreak attacks against llms. _arXiv preprint_ , 2024. 

- [283] Zihao Xu, Yi Liu, Gelei Deng, Yuekang Li, and Stjepan Picek. Llm jailbreak attack versus defense techniques–a comprehensive study. _arXiv preprint_ , 2024. 

- [284] Jiawen Shi, Yixin Liu, Pan Zhou, and Lichao Sun. Badgpt: Exploring security vulnerabilities of chatgpt via backdoor attacks to instructgpt. _arXiv preprint_ , 2023. 

- [285] Shuai Zhao, Meihuizi Jia, Anh Tuan Luu, Fengjun Pan, and Jinming Wen. Universal vulnerabilities in large language models: Backdoor attacks for in-context learning. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16, 2024_ , pages 11507–11522. Association for Computational Linguistics, 2024. 

- [286] Hongwei Yao, Jian Lou, and Zhan Qin. Poisonprompt: Backdoor attack on prompt-based large language models. In _IEEE International Conference on Acoustics, Speech and Signal Processing, ICASSP 2024, Seoul, Republic of Korea, April 14-19, 2024_ , pages 7745–7749. IEEE, 2024. 

- [287] Rodrigo Pedro, Daniel Castro, Paulo Carreira, and Nuno Santos. From prompt injections to sql injection attacks: How protected is your llm-integrated web application? _arXiv preprint_ , 2023. 

- [288] Shuyu Jiang, Xingshu Chen, and Rui Tang. Prompt packer: Deceiving llms through compositional instruction with hidden attacks. _arXiv preprint_ , 2023. 

- [289] Yupei Liu, Yuqi Jia, Runpeng Geng, Jinyuan Jia, and Neil Zhenqiang Gong. Prompt injection attacks and defenses in llm-integrated applications. _arXiv preprint_ , 2023. 

- [290] Jun Yan, Vikas Yadav, Shiyang Li, Lichang Chen, Zheng Tang, Hai Wang, Vijay Srinivasan, Xiang Ren, and Hongxia Jin. Backdooring instruction-tuned large language models with virtual prompt injection. In Kevin Duh, Helena Gómez-Adorno, and Steven Bethard, editors, _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), NAACL 2024, Mexico City, Mexico, June 16-21, 2024_ , pages 6065–6086. Association for Computational Linguistics, 2024. 

- [291] Julien Piet, Maha Alrashed, Chawin Sitawarin, Sizhe Chen, Zeming Wei, Elizabeth Sun, Basel Alomair, and David A. Wagner. Jatmo: Prompt injection defense by task-specific finetuning. In Joaquín García-Alfaro, Rafal Kozik, Michal Choras, and Sokratis K. Katsikas, editors, _Computer Security - ESORICS 2024 - 29th European Symposium on Research in Computer Security, Bydgoszcz, Poland, September 16-20, 2024, Proceedings, Part I_ , volume 14982 of _Lecture Notes in Computer Science_ , pages 105–124. Springer, 2024. 

- [292] George Kour, Marcel Zalmanovici, Naama Zwerdling, Esther Goldbraich, Ora Nova Fandina, Ateret AnabyTavor, Orna Raz, and Eitan Farchi. Unveiling safety vulnerabilities of large language models. _arXiv preprint_ , 2023. 

40 

- [293] Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, and Yang Zhang. "do anything now": Characterizing and evaluating in-the-wild jailbreak prompts on large language models. _arXiv preprint_ , 2023. 

- [294] Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, and Matt Fredrikson. Universal and transferable adversarial attacks on aligned language models. _arXiv preprint_ , 2023. 

- [295] Raz Lapid, Ron Langberg, and Moshe Sipper. Open sesame! universal black box jailbreaking of large language models. _arXiv preprint_ , 2023. 

- [296] Peng Ding, Jun Kuang, Dan Ma, Xuezhi Cao, Yunsen Xian, Jiajun Chen, and Shujian Huang. A wolf in sheep’s clothing: Generalized nested jailbreak prompts can fool large language models easily. In Kevin Duh, Helena Gómez-Adorno, and Steven Bethard, editors, _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), NAACL 2024, Mexico City, Mexico, June 16-21, 2024_ , pages 2136–2153. Association for Computational Linguistics, 2024. 

- [297] Gelei Deng, Yi Liu, Yuekang Li, Kailong Wang, Ying Zhang, Zefeng Li, Haoyu Wang, Tianwei Zhang, and Yang Liu. Masterkey: Automated jailbreaking of large language model chatbots. In _Proceedings 2024 Network and Distributed System Security Symposium_ , NDSS 2024. Internet Society, 2024. 

- [298] Sicheng Zhu, Ruiyi Zhang, Bang An, Gang Wu, Joe Barrow, Zichao Wang, Furong Huang, Ani Nenkova, and Tong Sun. Autodan: interpretable gradient-based adversarial attacks on large language models. In _First Conference on Language Modeling_ , 2024. 

- [299] Jiahao Yu, Xingwei Lin, Zheng Yu, and Xinyu Xing. Gptfuzzer: Red teaming large language models with auto-generated jailbreak prompts. _arXiv preprint_ , 2023. 

- [300] Dongyu Yao, Jianshu Zhang, Ian G. Harris, and Marcel Carlsson. Fuzzllm: A novel and universal fuzzing framework for proactively discovering jailbreak vulnerabilities in large language models. _arXiv preprint_ , 2023. 

- [301] Zhenhua Wang, Wei Xie, Kai Chen, Baosheng Wang, Zhiwen Gui, and Enze Wang. Self-deception: Reverse penetrating the semantic firewall of large language models. _arXiv preprint_ , 2023. 

- [302] Huachuan Qiu, Shuai Zhang, Anqi Li, Hongliang He, and Zhenzhong Lan. Latent jailbreak: A benchmark for evaluating text safety and output robustness of large language models. _arXiv preprint_ , 2023. 

- [303] Haoran Li, Dadi Guo, Wei Fan, Mingshi Xu, Jie Huang, Fanpu Meng, and Yangqiu Song. Multi-step jailbreaking privacy attacks on chatgpt. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, _Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023_ , pages 4138–4153. Association for Computational Linguistics, 2023. 

- [304] Rajesh Pasupuleti, Ravi Vadapalli, and Christopher Mader. Cyber security issues and challenges related to generative ai and chatgpt. In _2023 Tenth International Conference on Social Networks Analysis, Management and Security (SNAMS)_ , pages 1–5, 2023. 

- [305] Evan Hubinger, Carson Denison, Jesse Mu, Mike Lambert, Meg Tong, Monte MacDiarmid, Tamera Lanham, Daniel M. Ziegler, Tim Maxwell, Newton Cheng, Adam Jermyn, Amanda Askell, Ansh Radhakrishnan, Cem Anil, David Duvenaud, Deep Ganguli, Fazl Barez, Jack Clark, Kamal Ndousse, Kshitij Sachan, Michael Sellitto, Mrinank Sharma, Nova DasSarma, Roger Grosse, Shauna Kravec, Yuntao Bai, Zachary Witten, Marina Favaro, Jan Brauner, Holden Karnofsky, Paul Christiano, Samuel R. Bowman, Logan Graham, Jared Kaplan, Sören Mindermann, Ryan Greenblatt, Buck Shlegeris, Nicholas Schiefer, and Ethan Perez. Sleeper agents: Training deceptive llms that persist through safety training. _arXiv preprint_ , 2024. 

- [306] Xianjun Yang, Xiao Wang, Qi Zhang, Linda Petzold, William Yang Wang, Xun Zhao, and Dahua Lin. Shadow alignment: The ease of subverting safely-aligned language models. _arXiv preprint_ , 2023. 

- [307] Fengqing Jiang, Zhangchen Xu, Luyao Niu, Boxin Wang, Jinyuan Jia, Bo Li, and Radha Poovendran. POSTER: identifying and mitigating vulnerabilities in llm-integrated applications. In Jianying Zhou, Tony Q. S. Quek, Debin Gao, and Alvaro A. Cárdenas, editors, _Proceedings of the 19th ACM Asia Conference on Computer and Communications Security, ASIA CCS 2024, Singapore, July 1-5, 2024_ . ACM, 2024. 

- [308] June Sallou, Thomas Durieux, and Annibale Panichella. Breaking the silence: the threats of using llms in software engineering. In _Proceedings of the 2024 ACM/IEEE 44th International Conference on Software Engineering: New Ideas and Emerging Results, NIER@ICSE 2024, Lisbon, Portugal, April 14-20, 2024_ , pages 102–106. ACM, 2024. 

- [309] Neda Azizi and Omid Haass. Cybersecurity issues and challenges. In _Handbook of research on cybersecurity issues and challenges for business and FinTech applications_ , pages 21–48. IGI Global, 2023. 

41 

- [310] Jabu Mtsweni, Noluxolo Gcaza, and Mphahlele Thaba. A unified cybersecurity framework for complex environments. In _Proceedings of the Annual Conference of the South African Institute of Computer Scientists and Information Technologists_ , pages 1–9, 2018. 

- [311] Tanay Varshney. Introduction to llm agents, 2023. 

- [312] Hongwei Cui, Yuyang Du, Qun Yang, Yulin Shao, and Soung Chang Liew. Llmind: Orchestrating ai and iot with llm for complex task execution. _arXiv preprint_ , 2024. 

- [313] Maria Rigaki, Ondrej Lukás, Carlos Adrián Catania, and Sebastian García. Out of the cage: How stochastic parrots win in cyber security environments. In Ana Paula Rocha, Luc Steels, and H. Jaap van den Herik, editors, _Proceedings of the 16th International Conference on Agents and Artificial Intelligence, ICAART 2024, Volume 3, Rome, Italy, February 24-26, 2024_ , pages 774–781. SCITEPRESS, 2024. 

- [314] Richard Fang, Rohan Bindu, Akul Gupta, Qiusi Zhan, and Daniel Kang. Llm agents can autonomously hack websites. _arXiv preprint_ , 2024. 

- [315] Kaikai An, Fangkai Yang, Junting Lu, Liqun Li, Zhixing Ren, Hao Huang, Lu Wang, Pu Zhao, Yu Kang, Hua Ding, Qingwei Lin, Saravan Rajmohan, Dongmei Zhang, and Qi Zhang. Nissist: An incident mitigation copilot based on troubleshooting guides. In Ulle Endriss, Francisco S. Melo, Kerstin Bach, Alberto José Bugarín Diz, Jose Maria Alonso-Moral, Senén Barro, and Fredrik Heintz, editors, _ECAI 2024 - 27th European Conference on Artificial Intelligence, 19-24 October 2024, Santiago de Compostela, Spain - Including 13th Conference on Prestigious Applications of Intelligent Systems (PAIS 2024)_ , volume 392 of _Frontiers in Artificial Intelligence and Applications_ , pages 4471–4474. IOS Press, 2024. 

- [316] Jingqing Ruan, Yihong Chen, Bin Zhang, Zhiwei Xu, Tianpeng Bao, Guoqing Du, Shiwei Shi, Hangyu Mao, Ziyue Li, Xingyu Zeng, and Rui Zhao. Tptu: Large language model-based ai agents for task planning and tool usage. _arXiv preprint_ , 2023. 

- [317] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, Rui Zheng, Xiaoran Fan, Xiao Wang, Limao Xiong, Yuhao Zhou, Weiran Wang, Changhao Jiang, Yicheng Zou, Xiangyang Liu, Zhangyue Yin, Shihan Dou, Rongxiang Weng, Wensen Cheng, Qi Zhang, Wenjuan Qin, Yongyan Zheng, Xipeng Qiu, Xuanjing Huang, and Tao Gui. The rise and potential of large language model based agents: A survey. _arXiv preprint_ , 2023. 

- [318] Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun. Toolllm: Facilitating large language models to master 16000+ real-world apis. In _The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024_ . OpenReview.net, 2024. 

- [319] Yulong Liu, Yunlong Yuan, Chunwei Wang, Jianhua Han, Yongqiang Ma, Li Zhang, Nanning Zheng, and Hang Xu. From summary to action: Enhancing large language models for complex tasks with open world apis. _arXiv preprint_ , 2024. 

- [320] Ke Yang, Jiateng Liu, John Wu, Chaoqi Yang, Yi R. Fung, Sha Li, Zixuan Huang, Xu Cao, Xingyao Wang, Yiquan Wang, Heng Ji, and Chengxiang Zhai. If llm is the wizard, then code is the wand: A survey on how code empowers large language models to serve as intelligent agents. _arXiv preprint_ , 2024. 

- [321] Bo Qiao, Liqun Li, Xu Zhang, Shilin He, Yu Kang, Chaoyun Zhang, Fangkai Yang, Hang Dong, Jue Zhang, Lu Wang, Minghua Ma, Pu Zhao, Si Qin, Xiaoting Qin, Chao Du, Yong Xu, Qingwei Lin, Saravan Rajmohan, and Dongmei Zhang. Taskweaver: A code-first agent framework. _arXiv preprint_ , 2023. 

- [322] Yudong Huang, Hongyang Du, Xinyuan Zhang, Dusit Niyato, Jiawen Kang, Zehui Xiong, Shuo Wang, and Tao Huang. Large language models for networking: Applications, enabling techniques, and challenges. _arXiv preprint_ , 2023. 

- [323] Richard Fang, Rohan Bindu, Akul Gupta, and Daniel Kang. Llm agents can autonomously exploit one-day vulnerabilities. _arXiv preprint_ , 2024. 

- [324] Richard Fang, Rohan Bindu, Akul Gupta, Qiusi Zhan, and Daniel Kang. Teams of llm agents can exploit zero-day vulnerabilities. _arXiv preprint_ , 2024. 

- [325] Tri Cao, Chengyu Huang, Yuexin Li, Huilin Wang, Amy He, Nay Oo, and Bryan Hooi. Phishagent: A robust multimodal agent for phishing webpage detection. _arXiv preprint_ , 2024. 

- [326] PeiYu Tseng, ZihDwo Yeh, Xushu Dai, and Peng Liu. Using llms to automate threat intelligence analysis workflows in security operation centers. _arXiv preprint_ , 2024. 

42 

- [327] Tongxin Yuan, Zhiwei He, Lingzhong Dong, Yiming Wang, Ruijie Zhao, Tian Xia, Lizhen Xu, Binglin Zhou, Fangqi Li, Zhuosheng Zhang, Rui Wang, and Gongshen Liu. R-judge: Benchmarking safety risk awareness for LLM agents. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, _Findings of the Association for Computational Linguistics: EMNLP 2024, Miami, Florida, USA, November 12-16, 2024_ , pages 1467–1490. Association for Computational Linguistics, 2024. 

- [328] Fangzhou Wu, Shutong Wu, Yulong Cao, and Chaowei Xiao. Wipi: A new web threat for llm-driven web agents. _arXiv preprint_ , 2024. 

- [329] Qiusi Zhan, Zhixiang Liang, Zifan Ying, and Daniel Kang. Injecagent: Benchmarking indirect prompt injections in tool-integrated large language model agents. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Findings of the Association for Computational Linguistics, ACL 2024, Bangkok, Thailand and virtual meeting, August 11-16, 2024_ , pages 10471–10506. Association for Computational Linguistics, 2024. 

43 

