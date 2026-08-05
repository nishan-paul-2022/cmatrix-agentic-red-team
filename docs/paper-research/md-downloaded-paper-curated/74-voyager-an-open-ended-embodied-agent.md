Title: [2305.16291] Voyager: An Open-Ended Embodied Agent with Large Language Models

Description: We introduce Voyager, the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention. Voyager c…

Source: https://ar5iv.labs.arxiv.org/html/2305.16291

---

[https://voyager.minedojo.org](https://voyager.minedojo.org)

###### Abstract
We introduce Voyager, the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention. Voyager consists of three key components: 1) an automatic curriculum that maximizes exploration, 2) an ever-growing skill library of executable code for storing and retrieving complex behaviors, and 3) a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification for program improvement. Voyager interacts with GPT-4 via blackbox queries, which bypasses the need for model parameter fine-tuning. The skills developed by Voyager are temporally extended, interpretable, and compositional, which compounds the agent’s abilities rapidly and alleviates catastrophic forgetting. Empirically, Voyager shows strong in-context lifelong learning capability and exhibits exceptional proficiency in playing Minecraft. It obtains 3.3×3.3\times more unique items, travels 2.3×2.3\times longer distances, and unlocks key tech tree milestones up to 15.3×15.3\times faster than prior SOTA. Voyager is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch, while other techniques struggle to generalize.

Building generally capable embodied agents that continuously explore, plan, and develop new skills in open-ended worlds is a grand challenge for the AI community [[1](https://ar[5](https://ar5iv.labs.arxiv.org/html/[23](https://ar5iv.labs.arxiv.org/html/2[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)5.16[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)1#bib.bib23)05.1[6](https://ar5iv.labs.arxiv.org/html/2305.[[16](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib16)](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib16)2[9](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib9)1#bib.bib6)291#bib.bib5)iv.labs.arxiv.org/html/[2](https://ar5iv.labs.arxiv.org/html/2[3](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib3)05.16291#bib.bib2)305.16291#bib.bib1), 2, 3, [4](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib4), 5]. Classical approaches employ reinforcement learning (RL) [6, [7](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib7)] and imitation learning [[8](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib8), 9, [10](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib10)] that operate on primitive actions, which could be challenging for systematic exploration [[11](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib11), [12](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib12), [13](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib13), [14](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib14), [15](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib15)], interpretability [16, [17](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib17), [18](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib18)], and generalization [[[19](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib19)](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib19), [20](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib20), [21](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib21)]. Recent advances in large language model (LLM) based agents harness the world knowledge encapsulated in pre-trained LLMs to generate consistent action plans or executable policies [16, [22](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib22), 19]. They are applied to embodied tasks like games and robotics [23, [24](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib24), [25](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib25), [26](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib26), [27](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib27)], as well as NLP tasks without embodiment [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28), 29, 30]. However, these agents are not lifelong learners that can progressively acquire, update, accumulate, and transfer knowledge over extended time spans [[31](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib31), [32](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib32)].
Let us consider Minecraft as an example. Unlike most other games studied in AI [[33](https://ar5iv.labs.arxiv.org/html/[23](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib23)05.16291#bib.bib33), [34](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib34), [10](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib10)], Minecraft does not impose a predefined end goal or a fixed storyline but rather provides a unique playground with endless possibilities [23]. Minecraft requires players to explore vast, procedurally generated 3D terrains and unlock a tech tree using gathered resources. Human players typically start by learning the basics, such as mining wood and cooking food, before advancing to more complex tasks like combating monsters and crafting diamond tools. We argue that an effective lifelong learning agent should have similar capabilities as human players: (1) propose suitable tasks based on its current skill level and world state, e.g., learn to harvest sand and cactus before iron if it finds itself in a desert rather than a forest; (2) refine skills based on environmental feedback and commit mastered skills to memory for future reuse in similar situations (e.g. fighting zombies is similar to fighting spiders); (3) continually explore the world and seek out new tasks in a self-driven manner.

Towards these goals, we introduce Voyager, the first LLM-powered embodied lifelong learning agent to drive exploration, master a wide range of skills, and make new discoveries continually without human intervention in Minecraft. Voyager is made possible through three key modules (Fig. [2](https://ar5iv.labs.arxiv.org/html/2305.[16](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib16)291#S1.F2)): 1) an automatic curriculum that maximizes exploration; 2) a skill library for storing and retrieving complex behaviors; and 3) a new iterative prompting mechanism that generates executable code for embodied control. We opt to use code as the action space instead of low-level motor commands because programs can naturally represent temporally extended and compositional actions [16, [22](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib22)], which are essential for many long-horizon tasks in Minecraft. Voyager interacts with a blackbox LLM (GPT-4 [[35](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib35)]) through prompting and in-context learning [[36](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib36), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37), [38](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib38)]. Our approach bypasses the need for model parameter access and explicit gradient-based training or finetuning.
More specifically, Voyager attempts to solve progressively harder tasks proposed by the automatic curriculum, which takes into account the exploration progress and the agent’s state. The curriculum is generated by GPT-4 based on the overarching goal of “discovering as many diverse things as possible”. This approach can be perceived as an in-context form of novelty search [[39](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib39), [40](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib40)]. Voyager incrementally builds a skill library by storing the action programs that help solve a task successfully. Each program is indexed by the embedding of its description, which can be retrieved in similar situations in the future. Complex skills can be synthesized by composing simpler programs, which compounds Voyager’s capabilities rapidly over time and alleviates catastrophic forgetting in other continual learning methods [[31](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib31), [32](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib32)].
However, LLMs struggle to produce the correct action code consistently in one shot [[41](https://ar5iv.labs.arxiv.org/html/[2](https://ar5iv.labs.arxiv.org/html/2305.16291#S1.F2)305.16291#bib.bib41)]. To address this challenge, we propose an iterative prompting mechanism that: (1) executes the generated program to obtain observations from the Minecraft simulation (such as inventory listing and nearby creatures) and error trace from the code interpreter (if any); (2) incorporates the feedback into GPT-4’s prompt for another round of code refinement; and (3) repeats the process until a self-verification module confirms the task completion, at which point we commit the program to the skill library (e.g., craftStoneShovel() and combatZombieWithSword()) and query the automatic curriculum for the next milestone (Fig. 2).
Empirically, Voyager demonstrates strong in-context lifelong learning capabilities. It can construct an ever-growing skill library of action programs that are reusable, interpretable, and generalizable to novel tasks. We evaluate Voyager systematically against other LLM-based agent techniques (e.g., ReAct [[29](https://ar5iv.labs.arxiv.org/html/2[30](https://ar5iv.labs.arxiv.org/html/[23](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib23)05.16291#bib.bib30)5.16291#bib.bib29)], Reflexion [30], AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)]) in MineDojo [23], an open-source Minecraft AI framework. Voyager outperforms prior SOTA by obtaining 3.3×3.3\times more unique items, unlocking key tech tree milestones up to 15.3×15.3\times faster, and traversing 2.3×2.3\times longer distances. We further demonstrate that Voyager is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch, while other methods struggle to generalize.

Voyager consists of three novel components: (1) an automatic curriculum (Sec. [2.1](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.SS1)) that suggests objectives for open-ended exploration, (2) a skill library (Sec. [2.2](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.SS2)) for developing increasingly complex behaviors, and (3) an iterative prompting mechanism (Sec. [2.3](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.SS3)) that generates executable code for embodied control. Full prompts are presented in [A](https://ar5iv.labs.arxiv.org/html/2305.16291#A1)ppendix, Sec. A.

[A.3](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3)
Embodied agents encounter a variety of objectives with different complexity levels in open-ended environments. An automatic curriculum offers numerous benefits for open-ended exploration, ensuring a challenging but manageable learning process, fostering curiosity-driven intrinsic motivation for agents to learn and explore, and encouraging the development of general and flexible problem-solving strategies [[42](https://ar5iv.labs.arxiv.org/html/2[3](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F3)05.16291#bib.bib42), [43](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib43), [44](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib44)]. Our automatic curriculum capitalizes on the internet-scale knowledge contained within GPT-4 by prompting it to provide a steady stream of new tasks or challenges. The curriculum unfolds in a bottom-up fashion, allowing for considerable adaptability and responsiveness to the exploration progress and the agent’s current state (Fig. 3). As Voyager progresses to harder self-driven goals, it naturally learns a variety of skills, such as “mining a diamond”.
The input prompt to GPT-4 consists of several components:
1. 
(1) 

Directives encouraging diverse behaviors and imposing constraints, such as “My ultimate goal is to discover as many diverse things as possible ... The next task should not be too hard since I may not have the necessary resources or have learned enough skills to complete it yet.”;


2. 
(2) 

The agent’s current state, including inventory, equipment, nearby blocks and entities, biome, time, health and hunger bars, and position;


3. 
(3) 

Previously completed and failed tasks, reflecting the agent’s current exploration progress and capabilities frontier;


4. 
(4) 

Additional context: We also leverage GPT-3.5 to self-ask questions based on the agent’s current state and exploration progress and self-answer questions. We opt to use GPT-3.5 instead of GPT-4 for standard NLP tasks due to budgetary considerations.


Directives encouraging diverse behaviors and imposing constraints, such as “My ultimate goal is to discover as many diverse things as possible ... The next task should not be too hard since I may not have the necessary resources or have learned enough skills to complete it yet.”;
The agent’s current state, including inventory, equipment, nearby blocks and entities, biome, time, health and hunger bars, and position;
Previously completed and failed tasks, reflecting the agent’s current exploration progress and capabilities frontier;
Additional context: We also leverage GPT-3.5 to self-ask questions based on the agent’s current state and exploration progress and self-answer questions. We opt to use GPT-3.5 instead of GPT-4 for standard NLP tasks due to budgetary considerations.

With the automatic curriculum consistently proposing increasingly complex tasks, it is essential to have a skill library that serves as a basis for learning and evolution. Inspired by the generality, interpretability, and universality of programs [[45](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib45)], we represent each skill with executable code that scaffolds temporally extended actions for completing a specific task proposed by the automatic curriculum.
The input prompt to GPT-4 consists of the following components:
1. 
(1) 

Guidelines for code generation, such as “Your function will be reused for building more complex functions. Therefore, you should make it generic and reusable.”;


2. 
(2) 

Control primitive APIs, and relevant skills retrieved from the skill library, which are crucial for in-context learning [[36](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib36), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37), [38](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib38)] to work well;


3. 
(3) 

The generated code from the last round, environment feedback, execution errors, and critique, based on which GPT-4 can self-improve (Sec. [2.3](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.SS3));


4. 
(4) 

The agent’s current state, including inventory, equipment, nearby blocks and entities, biome, time, health and hunger bars, and position;


5. 
(5) 

Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] to do reasoning before code generation.


Guidelines for code generation, such as “Your function will be reused for building more complex functions. Therefore, you should make it generic and reusable.”;
Control primitive APIs, and relevant skills retrieved from the skill library, which are crucial for in-context learning [[36](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib36), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37), [38](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib38)] to work well;
The generated code from the last round, environment feedback, execution errors, and critique, based on which GPT-4 can self-improve (Sec. [2.3](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.SS3));
The agent’s current state, including inventory, equipment, nearby blocks and entities, biome, time, health and hunger bars, and position;
Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] to do reasoning before code generation.
We iteratively refine the program through a novel iterative prompting mechanism (Sec. [2.3](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.SS3)), incorporate it into the skill library as a new skill, and index it by the embedding of its description (Fig. [[4](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F4)](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F4), top). For skill retrieval, we query the skill library with the embedding of self-generated task plans and environment feedback (Fig. 4, bottom). By continuously expanding and refining the skill library, Voyager can learn, adapt, and excel in a wide spectrum of tasks, consistently pushing the boundaries of its capabilities in the open world.

[A.4](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS4)
We introduce an iterative prompting mechanism for self-improvement through three types of feedback:
1. 
(1) 

Environment feedback, which illustrates the intermediate progress of program execution (Fig. [5](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F5), left). For example, “I cannot make an iron chestplate because I need: 7 more iron ingots” highlights the cause of failure in crafting an iron chestplate. We use bot.chat() inside control primitive APIs to generate environment feedback and prompt GPT-4 to use this function as well during code generation;


2. 
(2) 

Execution errors from the program interpreter that reveal any invalid operations or syntax errors in programs, which are valuable for bug fixing (Fig. [5](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F5), right);


3. 
(3) 

Self-verification for checking task success. Instead of manually coding success checkers for each new task proposed by the automatic curriculum, we instantiate another GPT-4 agent for self-verification. By providing Voyager’s current state and the task to GPT-4, we ask it to act as a critic [[47](https://ar5iv.labs.arxiv.org/html/2[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)5.1[6](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F6)291#bib.bib47), [48](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib48), [49](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib49)] and inform us whether the program achieves the task. In addition, if the task fails, it provides a critique by suggesting how to complete the task (Fig. 6). Hence, our self-verification is more comprehensive than self-reflection [30] by both checking success and reflecting on mistakes.


Environment feedback, which illustrates the intermediate progress of program execution (Fig. [5](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F5), left). For example, “I cannot make an iron chestplate because I need: 7 more iron ingots” highlights the cause of failure in crafting an iron chestplate. We use bot.chat() inside control primitive APIs to generate environment feedback and prompt GPT-4 to use this function as well during code generation;
Execution errors from the program interpreter that reveal any invalid operations or syntax errors in programs, which are valuable for bug fixing (Fig. [5](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F5), right);
Self-verification for checking task success. Instead of manually coding success checkers for each new task proposed by the automatic curriculum, we instantiate another GPT-4 agent for self-verification. By providing Voyager’s current state and the task to GPT-4, we ask it to act as a critic [[47](https://ar5iv.labs.arxiv.org/html/2[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)5.1[6](https://ar5iv.labs.arxiv.org/html/2305.16291#S2.F6)291#bib.bib47), [48](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib48), [49](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib49)] and inform us whether the program achieves the task. In addition, if the task fails, it provides a critique by suggesting how to complete the task (Fig. 6). Hence, our self-verification is more comprehensive than self-reflection [30] by both checking success and reflecting on mistakes.
During each round of code generation, we execute the generated program to obtain environment feedback and execution errors from the code interpreter, which are incorporated into GPT-4’s prompt for the next round of code refinement. This iterative process repeats until self-verification validates the task’s completion, at which point we add this new skill to the skill library and ask the automatic curriculum for a new objective (Fig. [2](https://ar5iv.labs.arxiv.org/html/2305.16291#S1.F2)). If the agent gets stuck after 4 rounds of code generation, then we query the curriculum for another task. This iterative prompting approach significantly improves program synthesis for embodied control, enabling Voyager to continuously acquire diverse skills without human intervention.
[A.5](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS5)

### 3.1 Experimental Setup
We leverage OpenAI’s gpt-4-0314 [[35](https://ar5iv.labs.arxiv.org/html/[23](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib23)05.16291#bib.bib35)] and gpt-3.5-turbo-0301 [[50](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib50)] APIs for text completion, along with text-embedding-ada-002 [[51](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib51)] API for text embedding. We set all temperatures to 0 except for the automatic curriculum, which uses temperature == 0.1 to encourage task diversity. Our simulation environment is built on top of MineDojo [23] and leverages Mineflayer [[52](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib52)] JavaScript APIs for motor controls. See Appendix, Sec. [B.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.SS1) for more details.

### 3.2 Baselines
Because there is no LLM-based agents that work out of the box for Minecraft, we make our best effort to select a number of representative algorithms as baselines. These methods are originally designed only for NLP tasks without embodiment, therefore we have to re-interpret them to be executable in MineDojo and compatible with our experimental setting:
ReAct [[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)] uses chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] by generating both reasoning traces and action plans with LLMs. We provide it with our environment feedback and the agent states as observations.
Reflexion [[30](https://ar5iv.labs.arxiv.org/html/2305.16[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)1#bib.bib30)] is built on top of ReAct [29] with self-reflection to infer more intuitive future actions. We provide it with execution errors and our self-verification module.
AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)] is a popular software tool that automates NLP tasks by decomposing a high-level goal into multiple subgoals and executing them in a ReAct-style loop. We re-implement AutoGPT by using GPT-4 to do task decomposition and provide it with the agent states, environment feedback, and execution errors as observations for subgoal execution. Compared with Voyager, AutoGPT lacks the skill library for accumulating knowledge, self-verification for assessing task success, and automatic curriculum for open-ended exploration.
Note that we do not directly compare with prior methods that take Minecraft screen pixels as input and output low-level controls [[53](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib53), [54](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib54), [55](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib55)]. It would not be an apple-to-apple comparison, because we rely on the high-level Mineflayer [[52](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib52)] API to control the agent. Our work’s focus is on pushing the limits of GPT-4 for lifelong embodied agent learning, rather than solving the 3D perception or sensorimotor control problems. Voyager is orthogonal and can be combined with gradient-based approaches like VPT [[8](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib8)] as long as the controller provides a code API. We make a system-level comparison between Voyager and prior Minecraft agents in Table. [A.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.T2).

We systematically evaluate Voyager and baselines on their exploration performance, tech tree mastery, map coverage, and zero-shot generalization capability to novel tasks in a new world.
Significantly better exploration. Results of exploration performance are shown in Fig. [1](https://ar5iv.labs.arxiv.org/html/2305.16291#S0.F1). Voyager’s superiority is evident in its ability to consistently make new strides, discovering 63 unique items within 160 prompting iterations, 3.3×3.3\times many novel items compared to its counterparts. On the other hand, AutoGPT lags considerably in discovering new items, while ReAct and Reflexion struggle to make significant progress, given the abstract nature of the open-ended exploration goal that is challenging to execute without an appropriate curriculum.
Consistent tech tree mastery. The Minecraft tech tree tests the agent’s ability to craft and use a hierarchy of tools. Progressing through this tree (wooden tool →→\rightarrow stone tool →→\rightarrow iron tool →→\rightarrow diamond tool) requires the agent to master systematic and compositional skills. Compared with baselines, Voyager unlocks the wooden level [1](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.T1)5.3×15.3\times faster (in terms of the prompting iterations), the stone level 8.5×8.5\times faster, the iron level 6.4×6.4\times faster, and Voyager is the only one to unlock the diamond level of the tech tree (Fig. [2](https://ar5iv.labs.arxiv.org/html/2305.16291#S1.F2) and Table. 1). This underscores the effectiveness of the automatic curriculum, which consistently presents challenges of suitable complexity to facilitate the agent’s progress.
Extensive map traversal. Voyager is able to navigate distances 2.3×2.3\times longer compared to baselines by traversing a variety of terrains, while the baseline agents often find themselves confined to local areas, which significantly hampers their capacity to discover new knowledge (Fig. [7](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F7)).
[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)
[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)
[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)
Efficient zero-shot generalization to unseen tasks. To evaluate zero-shot generalization, we clear the agent’s inventory, reset it to a newly instantiated world, and test it with unseen tasks. For both Voyager and AutoGPT, we utilize GPT-4 to break down the task into a series of subgoals. Table. [2](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.T2) and Fig. [8](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F8) show Voyager can consistently solve all the tasks, while baselines cannot solve any task within 50 prompting iterations. What’s interesting to note is that our skill library constructed from lifelong learning not only enhances Voyager’s performance but also gives a boost to AutoGPT. This demonstrates that the skill library serves as a versatile tool that can be readily employed by other methods, effectively acting as a plug-and-play asset to enhance performance.
[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)
[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)
[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)
[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)
[A.3](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.F3)

We ablate 6 design choices (automatic curriculum, skill library, environment feedback, execution errors, self-verification, and GPT-4 for code generation) in Voyager and study their impact on exploration performance (see Appendix, Sec. [B.3](https://ar5iv.labs.arxiv.org/html/2305.162[9](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F9)1#A2.SS3) for details of each ablated variant). Results are shown in Fig. 9. We highlight the key findings below:
- 
• 

Automatic curriculum is crucial for the agent’s consistent progress. The discovered item count drops by 93%percent9393\% if the curriculum is replaced with a random one, because certain tasks may be too challenging if attempted out of order. On the other hand, a manually designed curriculum requires significant Minecraft-specific expertise, and does not take into account the agent’s live situation. It falls short in the experimental results compared to our automatic curriculum.


- 
• 

Voyager w/o skill library exhibits a tendency to plateau in the later stages. This underscores the pivotal role that the skill library plays in Voyager. It helps create more complex actions and steadily pushes the agent’s boundaries by encouraging new skills to be built upon older ones.


- 
• 

Self-verification is the most important among all the feedback types. Removing the module leads to a significant drop (−73%percent73-73\%) in the discovered item count. Self-verification serves as a critical mechanism to decide when to move on to a new task or reattempt a previously unsuccessful task.


- 
• 

GPT-4 significantly outperforms GPT-3.5 in code generation and obtains 5.7×5.7\times more unique items, as GPT-4 exhibits a quantum leap in coding abilities. This finding corroborates recent studies in the literature  [[56](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib56), [57](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib57)].


Automatic curriculum is crucial for the agent’s consistent progress. The discovered item count drops by 93%percent9393\% if the curriculum is replaced with a random one, because certain tasks may be too challenging if attempted out of order. On the other hand, a manually designed curriculum requires significant Minecraft-specific expertise, and does not take into account the agent’s live situation. It falls short in the experimental results compared to our automatic curriculum.
Voyager w/o skill library exhibits a tendency to plateau in the later stages. This underscores the pivotal role that the skill library plays in Voyager. It helps create more complex actions and steadily pushes the agent’s boundaries by encouraging new skills to be built upon older ones.
Self-verification is the most important among all the feedback types. Removing the module leads to a significant drop (−73%percent73-73\%) in the discovered item count. Self-verification serves as a critical mechanism to decide when to move on to a new task or reattempt a previously unsuccessful task.
GPT-4 significantly outperforms GPT-3.5 in code generation and obtains 5.7×5.7\times more unique items, as GPT-4 exhibits a quantum leap in coding abilities. This finding corroborates recent studies in the literature  [[56](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib56), [57](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib57)].

Voyager does not currently support visual perception, because the available version of GPT-4 API is text-only at the time of this writing. However, Voyager has the potential to be augmented by multimodal perception models [[58](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib58), [59](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib59)] to achieve more impressive tasks. We demonstrate that given human feedback, Voyager is able to construct complex 3D structures in Minecraft, such as a Nether Portal and a house (Fig. [10](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F10)). There are two ways to integrate human feedback:
1. 
(1) 

Human as a critic (equivalent to Voyager’s self-verification module): humans provide visual critique to Voyager, allowing it to modify the code from the previous round. This feedback is essential for correcting certain errors in the spatial details of a 3D structure that Voyager cannot perceive directly.


2. 
(2) 

Human as a curriculum (equivalent to Voyager’s automatic curriculum module): humans break down a complex building task into smaller steps, guiding Voyager to complete them incrementally. This approach improves Voyager’s ability to handle more sophisticated 3D construction tasks.


Human as a critic (equivalent to Voyager’s self-verification module): humans provide visual critique to Voyager, allowing it to modify the code from the previous round. This feedback is essential for correcting certain errors in the spatial details of a 3D structure that Voyager cannot perceive directly.
Human as a curriculum (equivalent to Voyager’s automatic curriculum module): humans break down a complex building task into smaller steps, guiding Voyager to complete them incrementally. This approach improves Voyager’s ability to handle more sophisticated 3D construction tasks.

## 4 Limitations and Future Work
Cost. The GPT-4 API incurs significant costs. It is 15×15\times more expensive than GPT-3.5. Nevertheless, Voyager requires the quantum leap in code generation quality from GPT-4 (Fig. [9](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F9)), which GPT-3.5 and open-source LLMs cannot provide [[60](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib60)].
Inaccuracies. Despite the iterative prompting mechanism, there are still cases where the agent gets stuck and fails to generate the correct skill. The automatic curriculum has the flexibility to reattempt this task at a later time. Occasionally, self-verification module may also fail, such as not recognizing spider string as a success signal of beating a spider.
Hallucinations. The automatic curriculum occasionally proposes unachievable tasks. For example, it may ask the agent to craft a “copper sword" or “copper chestplate", which are items that do not exist within the game. Hallucinations also occur during the code generation process. For instance, GPT-4 tends to use cobblestone as a fuel input, despite being an invalid fuel source in the game. Additionally, it may call functions absent in the provided control primitive APIs, leading to code execution errors.
We are confident that improvements in the GPT API models as well as novel techniques for finetuning open-source LLMs will overcome these limitations in the future.

## 5 Related work
##### Decision-making Agents in Minecraft.
Minecraft is an open-ended 3D world with incredibly flexible game mechanics supporting a broad spectrum of activities. Built upon notable Minecraft benchmarks [[[23](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib23)](https://ar5iv.labs.arxiv.org/html/2305.1[62](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib62)91#bib.bib23), [61](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib61), 62, [63](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib63), [64](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib64), [65](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib65)], Minecraft learning algorithms can be divided into two categories: 1) Low-level controller: Many prior efforts leverage hierarchical reinforcement learning to learn from human demonstrations [[66](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib66), [67](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib67), [6[8](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib8)](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib68)]. Kanitscheider et al. [[14](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib14)] design a curriculum based on success rates, but its objectives are limited to curated items. MineDojo [23] and VPT [8] utilize YouTube videos for large-scale pre-training. DreamerV3 [[69](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib69)], on the other hand, learns a world model to explore the environment and collect diamonds. 2) High-level planner: Volum et al. [[[70](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib70)](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib70)] leverage few-shot prompting with Codex [[41](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib41)] to generate executable policies, but they require additional human interaction. Recent works leverage LLMs as a high-level planner in Minecraft by decomposing a high-level task into several subgoals following Minecraft recipes [[55](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib55), [53](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib53), [71](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib71)], thus lacking full exploration flexibility. Like these latter works, Voyager also uses LLMs as a high-level planner by prompting GPT-4 and utilizes Mineflayer [[52](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib52)] as a low-level controller following Volum et al. [70]. Unlike prior works, Voyager employs an automatic curriculum that unfolds in a bottom-up manner, driven by curiosity, and therefore enables open-ended exploration.

##### Large Language Models for Agent Planning.

Inspired by the strong emergent capabilities of LLMs, such as zero-shot prompting and complex reasoning [[72](https://ar5iv.labs.arxiv.org/html/2[30](https://ar5iv.labs.arxiv.org/html/2305.16[[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)1#bib.bib30)5.[16](https://ar5iv.labs.arxiv.org/html/2305.16[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)1#bib.bib16)291#bib.bib72), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37), [38](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib38), [36](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib36), [73](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib73), [74](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib74)], embodied agent research [[75](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib75), [76](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib76), [77](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib77), [78](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib78)] has witnessed a significant increase in the utilization of LLMs for planning purposes. Recent efforts can be roughly classified into two groups. 1) Large language models for robot learning: Many prior works apply LLMs to generate subgoals for robot planning [[[27](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib27)](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib27), 27, [25](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib25), [79](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib79), [80](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib80)]. Inner Monologue [[26](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib26)] incorporates environment feedback for robot planning with LLMs. Code as Policies [16] and ProgPrompt [[22](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib22)] directly leverage LLMs to generate executable robot policies. VIMA [[19](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib19)] and PaLM-E [[59](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib59)] fine-tune pre-trained LLMs to support multimodal prompts. 2) Large language models for text agents: ReAct [29] leverages chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] and generates both reasoning traces and task-specific actions with LLMs. Reflexion [30] is built upon ReAct [29] with self-reflection to enhance reasoning. AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)] is a popular tool that automates NLP tasks by crafting a curriculum of multiple subgoals for completing a high-level goal while incorporating ReAct [29]’s reasoning and acting loops. DERA [[81](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib81)] frames a task as a dialogue between two GPT-4 [[35](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib35)] agents. Generative Agents [[82](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib82)] leverages ChatGPT [[50](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib50)] to simulate human behaviors by storing agents’ experiences as memories and retrieving those for planning, but its agent actions are not executable. SPRING [[83](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib83)] is a concurrent work that uses GPT-4 to extract game mechanics from game manuals, based on which it answers questions arranged in a directed acyclic graph and predicts the next action. All these works lack a skill library for developing more complex behaviors, which are crucial components for the success of Voyager in lifelong learning.

##### Code Generation with Execution.

## 5 Related work
Code generation has been a longstanding challenge in NLP [[41](https://ar5iv.labs.arxiv.org/html/2305.162[91](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib91)#bib.bib41), [84](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib84), [85](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib85), [73](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib73), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37)], with various works leveraging execution results to improve program synthesis. Execution-guided approaches leverage intermediate execution outcomes to guide program search [[86](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib86), [87](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib87), [88](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib88)]. Another line of research utilizes majority voting to choose candidates based on their execution performance [[89](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib89), [90](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib90)]. Additionally, LEVER [91] trains a verifier to distinguish and reject incorrect programs based on execution results. CLAIRIFY [[92](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib92)], on the other hand, generates code for planning chemistry experiments and makes use of a rule-based verifier to iteratively provide error feedback to LLMs. Voyager distinguishes itself from these works by integrating environment feedback, execution errors, and self-verification (to assess task success) into an iterative prompting mechanism for embodied control.

## 6 Conclusion
In this work, we introduce Voyager, the first LLM-powered embodied lifelong learning agent, which leverages GPT-4 to explore the world continuously, develop increasingly sophisticated skills, and make new discoveries consistently without human intervention. Voyager exhibits superior performance in discovering novel items, unlocking the Minecraft tech tree, traversing diverse terrains, and applying its learned skill library to unseen tasks in a newly instantiated world. Voyager serves as a starting point to develop powerful generalist agents without tuning the model parameters.

## 7 Broader Impacts
Our research is conducted within Minecraft, a safe and harmless 3D video game environment. While Voyager is designed to be generally applicable to other domains, such as robotics, its application to physical robots would require additional attention and the implementation of safety constraints by humans to ensure responsible and secure deployment.

## 8 Acknowledgements
We are extremely grateful to Ziming Zhu, Kaiyu Yang, Rafał Kocielnik, Colin White, Or Sharir, Sahin Lale, De-An Huang, Jean Kossaifi, Yuncong Yang, Charles Zhang, Minchao Huang, and many other colleagues and friends for their helpful feedback and insightful discussions. This work is done during Guanzhi Wang’s internship at NVIDIA. Guanzhi Wang is supported by the Kortschak fellowship in Computing and Mathematical Sciences at Caltech.

- 
[1]

Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro
Herrasti, Daniel Gordon, Yuke Zhu, Abhinav Gupta, and Ali Farhadi.


Ai2-thor: An interactive 3d environment for visual ai.


arXiv preprint arXiv: Arxiv-1712.05474, 2017.



- 
[2]

Manolis Savva, Jitendra Malik, Devi Parikh, Dhruv Batra, Abhishek Kadian,
Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub,
Jia Liu, and Vladlen Koltun.


Habitat: A platform for embodied AI research.


In 2019 IEEE/CVF International Conference on Computer Vision,
ICCV 2019, Seoul, Korea (South), October 27 - November 2, 2019, pages
9338–9346. IEEE, 2019.



- 
[3]

Yuke Zhu, Josiah Wong, Ajay Mandlekar, and Roberto Martín-Martín.


robosuite: A modular simulation framework and benchmark for robot
learning.


arXiv preprint arXiv: Arxiv-2009.12293, 2020.



- 
[4]

Fei Xia, William B. Shen, Chengshu Li, Priya Kasimbeg, Micael Tchapmi,
Alexander Toshev, Li Fei-Fei, Roberto Martín-Martín, and Silvio Savarese.


Interactive gibson benchmark (igibson 0.5): A benchmark for
interactive navigation in cluttered environments.


arXiv preprint arXiv: Arxiv-1910.14442, 2019.



- 
[5]

Bokui Shen, Fei Xia, Chengshu Li, Roberto Martín-Martín, Linxi Fan, Guanzhi
Wang, Claudia Pérez-D’Arpino, Shyamal Buch, Sanjana Srivastava, Lyne P.
Tchapmi, Micael E. Tchapmi, Kent Vainio, Josiah Wong, Li Fei-Fei, and Silvio
Savarese.


igibson 1.0: a simulation environment for interactive tasks in large
realistic scenes.


arXiv preprint arXiv: Arxiv-2012.02924, 2020.



- 
[6]

Jens Kober, J Andrew Bagnell, and Jan Peters.


Reinforcement learning in robotics: A survey.


The International Journal of Robotics Research,
32(11):1238–1274, 2013.



- 
[7]

Kai Arulkumaran, Marc Peter Deisenroth, Miles Brundage, and Anil Anthony
Bharath.


Deep reinforcement learning: A brief survey.


IEEE Signal Processing Magazine, 34(6):26–38, 2017.



- 
[8]

Bowen Baker, Ilge Akkaya, Peter Zhokhov, Joost Huizinga, Jie Tang, Adrien
Ecoffet, Brandon Houghton, Raul Sampedro, and Jeff Clune.


Video pretraining (vpt): Learning to act by watching unlabeled online
videos.


arXiv preprint arXiv: Arxiv-2206.11795, 2022.



- 
[9]

DeepMind Interactive Agents Team, Josh Abramson, Arun Ahuja, Arthur Brussee,
Federico Carnevale, Mary Cassin, Felix Fischer, Petko Georgiev, Alex Goldin,
Mansi Gupta, Tim Harley, Felix Hill, Peter C Humphreys, Alden Hung, Jessica
Landon, Timothy Lillicrap, Hamza Merzic, Alistair Muldal, Adam Santoro, Guy
Scully, Tamara von Glehn, Greg Wayne, Nathaniel Wong, Chen Yan, and Rui Zhu.


Creating multimodal interactive agents with imitation and
self-supervised learning.


arXiv preprint arXiv: Arxiv-2112.03763, 2021.



- 
[10]

Oriol Vinyals, Igor Babuschkin, Junyoung Chung, Michael Mathieu, Max Jaderberg,
Wojciech M Czarnecki, Andrew Dudzik, Aja Huang, Petko Georgiev, Richard
Powell, et al.


Alphastar: Mastering the real-time strategy game starcraft ii.


DeepMind blog, 2, 2019.



- 
[11]

Adrien Ecoffet, Joost Huizinga, Joel Lehman, Kenneth O. Stanley, and Jeff
Clune.


Go-explore: a new approach for hard-exploration problems.


arXiv preprint arXiv: Arxiv-1901.10995, 2019.



- 
[12]

Joost Huizinga and Jeff Clune.


Evolving multimodal robot behavior via many stepping stones with the
combinatorial multiobjective evolutionary algorithm.


Evolutionary computation, 30(2):131–164, 2022.



- 
[13]

Rui Wang, Joel Lehman, Aditya Rawal, Jiale Zhi, Yulun Li, Jeffrey Clune, and
Kenneth O. Stanley.


Enhanced POET: open-ended reinforcement learning through unbounded
invention of learning challenges and their solutions.


In Proceedings of the 37th International Conference on Machine
Learning, ICML 2020, 13-18 July 2020, Virtual Event, volume 119 of Proceedings of Machine Learning Research, pages 9940–9951. PMLR, 2020.



- 
[14]

Ingmar Kanitscheider, Joost Huizinga, David Farhi, William Hebgen Guss, Brandon
Houghton, Raul Sampedro, Peter Zhokhov, Bowen Baker, Adrien Ecoffet, Jie
Tang, Oleg Klimov, and Jeff Clune.


Multi-task curriculum learning in a complex, visual, hard-exploration
domain: Minecraft.


arXiv preprint arXiv: Arxiv-2106.14876, 2021.



- 
[15]

Michael Dennis, Natasha Jaques, Eugene Vinitsky, Alexandre M. Bayen, Stuart
Russell, Andrew Critch, and Sergey Levine.


Emergent complexity and zero-shot transfer via unsupervised
environment design.


In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell,

Maria-Florina Balcan, and Hsuan-Tien Lin, editors, Advances in
Neural Information Processing Systems 33: Annual Conference on Neural
Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020,
virtual, 2020.



- 
[16]

Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete
Florence, and Andy Zeng.


Code as policies: Language model programs for embodied control.


arXiv preprint arXiv: Arxiv-2209.07753, 2022.



- 
[17]

Shao-Hua Sun, Te-Lin Wu, and Joseph J. Lim.


Program guided agent.


In 8th International Conference on Learning Representations,
ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020. OpenReview.net, 2020.



- 
[18]

Zelin Zhao, Karan Samel, Binghong Chen, and Le Song.


Proto: Program-guided transformer for program-guided tasks.


In Marc’Aurelio Ranzato, Alina Beygelzimer, Yann N. Dauphin, Percy
Liang, and Jennifer Wortman Vaughan, editors, Advances in Neural
Information Processing Systems 34: Annual Conference on Neural Information
Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual, pages
17021–17036, 2021.



- 
[19]

Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun
Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi (Jim) Fan.


Vima: General robot manipulation with multimodal prompts.


ARXIV.ORG, 2022.



- 
[20]

Mohit Shridhar, Lucas Manuelli, and Dieter Fox.


Cliport: What and where pathways for robotic manipulation.


arXiv preprint arXiv: Arxiv-2109.12098, 2021.



- 
[21]

Linxi Fan, Guanzhi Wang, De-An Huang, Zhiding Yu, Li Fei-Fei, Yuke Zhu, and
Animashree Anandkumar.


SECANT: self-expert cloning for zero-shot generalization of visual
policies.


In Marina Meila and Tong Zhang, editors, Proceedings of the 38th
International Conference on Machine Learning, ICML 2021, 18-24 July 2021,
Virtual Event, volume 139 of Proceedings of Machine Learning Research,
pages 3088–3099. PMLR, 2021.



- 
[22]

Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan
Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg.


Progprompt: Generating situated robot task plans using large language
models.


arXiv preprint arXiv: Arxiv-2209.11302, 2022.



- 
[23]

Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu,
Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar.


Minedojo: Building open-ended embodied agents with internet-scale
knowledge.


arXiv preprint arXiv: Arxiv-2206.08853, 2022.



- 
[24]

Andy Zeng, Adrian Wong, Stefan Welker, Krzysztof Choromanski, Federico Tombari,
Aveek Purohit, Michael Ryoo, Vikas Sindhwani, Johnny Lee, Vincent Vanhoucke,
and Pete Florence.


Socratic models: Composing zero-shot multimodal reasoning with
language.


arXiv preprint arXiv: Arxiv-2204.00598, 2022.



- 
[25]

Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron
David, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog,
Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang,
Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan
Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao
Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao,
Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton
Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun
Xu, and Mengyuan Yan.


Do as i can, not as i say: Grounding language in robotic affordances.


arXiv preprint arXiv: Arxiv-2204.01691, 2022.



- 
[26]

Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy
Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah
Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, and Brian
Ichter.


Inner monologue: Embodied reasoning through planning with language
models.


arXiv preprint arXiv: Arxiv-2207.05608, 2022.



- 
[27]

Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch.


Language models as zero-shot planners: Extracting actionable
knowledge for embodied agents.


In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba
Szepesvári, Gang Niu, and Sivan Sabato, editors, International
Conference on Machine Learning, ICML 2022, 17-23 July 2022, Baltimore,
Maryland, USA, volume 162 of Proceedings of Machine Learning
Research, pages 9118–9147. PMLR, 2022.



- 
[28]

Significant-gravitas/auto-gpt: An experimental open-source attempt to make
gpt-4 fully autonomous., 2023.



- 
[29]

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
and Yuan Cao.


React: Synergizing reasoning and acting in language models.


arXiv preprint arXiv: Arxiv-2210.03629, 2022.



- 
[30]

Noah Shinn, Beck Labash, and Ashwin Gopinath.


Reflexion: an autonomous agent with dynamic memory and
self-reflection.


arXiv preprint arXiv: Arxiv-2303.11366, 2023.



- 
[31]

German Ignacio Parisi, Ronald Kemker, Jose L. Part, Christopher Kanan, and
Stefan Wermter.


Continual lifelong learning with neural networks: A review.


Neural Networks, 113:54–71, 2019.



- 
[32]

Liyuan Wang, Xingxing Zhang, Hang Su, and Jun Zhu.


A comprehensive survey of continual learning: Theory, method and
application.


arXiv preprint arXiv: Arxiv-2302.00487, 2023.



- 
[33]

Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Alex Graves, Ioannis
Antonoglou, Daan Wierstra, and Martin Riedmiller.


Playing atari with deep reinforcement learning.


arXiv preprint arXiv: Arxiv-1312.5602, 2013.



- 
[34]

OpenAI, :, Christopher Berner, Greg Brockman, Brooke Chan, Vicki Cheung,
Przemysław Dębiak, Christy Dennison, David Farhi, Quirin Fischer, Shariq
Hashme, Chris Hesse, Rafal Józefowicz, Scott Gray, Catherine Olsson, Jakub
Pachocki, Michael Petrov, Henrique P. d. O. Pinto, Jonathan Raiman, Tim
Salimans, Jeremy Schlatter, Jonas Schneider, Szymon Sidor, Ilya Sutskever,
Jie Tang, Filip Wolski, and Susan Zhang.


Dota 2 with large scale deep reinforcement learning.


arXiv preprint arXiv: Arxiv-1912.06680, 2019.



- 
[35]

OpenAI.


Gpt-4 technical report.


arXiv preprint arXiv: Arxiv-2303.08774, 2023.



- 
[36]

Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian
Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H.
Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William
Fedus.


Emergent abilities of large language models.


arXiv preprint arXiv: Arxiv-2206.07682, 2022.



- 
[37]

Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan,
Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom
Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens
Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott
Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec
Radford, Ilya Sutskever, and Dario Amodei.


Language models are few-shot learners.


In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell,
Maria-Florina Balcan, and Hsuan-Tien Lin, editors, Advances in
Neural Information Processing Systems 33: Annual Conference on Neural
Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020,
virtual, 2020.



- 
[38]

Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael
Matena, Yanqi Zhou, Wei Li, and Peter J. Liu.


Exploring the limits of transfer learning with a unified text-to-text
transformer.


J. Mach. Learn. Res., 21:140:1–140:67, 2020.



- 
[39]

Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine.


Diversity is all you need: Learning skills without a reward function.


In 7th International Conference on Learning Representations,
ICLR 2019, New Orleans, LA, USA, May 6-9, 2019. OpenReview.net, 2019.



- 
[40]

Edoardo Conti, Vashisht Madhavan, Felipe Petroski Such, Joel Lehman, Kenneth O.
Stanley, and Jeff Clune.


Improving exploration in evolution strategies for deep reinforcement
learning via a population of novelty-seeking agents.


In Samy Bengio, Hanna M. Wallach, Hugo Larochelle, Kristen Grauman,
Nicolò Cesa-Bianchi, and Roman Garnett, editors, Advances in
Neural Information Processing Systems 31: Annual Conference on Neural
Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018,
Montréal, Canada, pages 5032–5043, 2018.



- 
[41]

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde
de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph,
Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy
Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder,
Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens
Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias

Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss,
William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor
Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher
Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa,
Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter
Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and
Wojciech Zaremba.


Evaluating large language models trained on code.


arXiv preprint arXiv: Arxiv-2107.03374, 2021.



- 
[42]

Rui Wang, Joel Lehman, Jeff Clune, and Kenneth O. Stanley.


Paired open-ended trailblazer (poet): Endlessly generating
increasingly complex and diverse learning environments and their solutions.


arXiv preprint arXiv: Arxiv-1901.01753, 2019.



- 
[43]

Rémy Portelas, Cédric Colas, Lilian Weng, Katja Hofmann, and
Pierre-Yves Oudeyer.


Automatic curriculum learning for deep RL: A short survey.


In Christian Bessiere, editor, Proceedings of the Twenty-Ninth
International Joint Conference on Artificial Intelligence, IJCAI 2020,
pages 4819–4825. ijcai.org, 2020.



- 
[44]

Sébastien Forestier, Rémy Portelas, Yoan Mollard, and Pierre-Yves
Oudeyer.


Intrinsically motivated goal exploration processes with automatic
curriculum learning.


The Journal of Machine Learning Research, 23(1):6818–6858,
2022.



- 
[45]

Kevin Ellis, Catherine Wong, Maxwell Nye, Mathias Sable-Meyer, Luc Cary, Lucas
Morales, Luke Hewitt, Armando Solar-Lezama, and Joshua B. Tenenbaum.


Dreamcoder: Growing generalizable, interpretable knowledge with
wake-sleep bayesian program learning.


arXiv preprint arXiv: Arxiv-2006.08381, 2020.



- 
[46]

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and
Denny Zhou.


Chain of thought prompting elicits reasoning in large language
models.


arXiv preprint arXiv: Arxiv-2201.11903, 2022.



- 
[47]

Volodymyr Mnih, Adrià Puigdomènech Badia, Mehdi Mirza, Alex Graves,
Timothy P. Lillicrap, Tim Harley, David Silver, and Koray Kavukcuoglu.


Asynchronous methods for deep reinforcement learning.


In Maria-Florina Balcan and Kilian Q. Weinberger, editors, Proceedings of the 33nd International Conference on Machine Learning, ICML
2016, New York City, NY, USA, June 19-24, 2016, volume 48 of JMLR
Workshop and Conference Proceedings, pages 1928–1937. JMLR.org, 2016.



- 
[48]

John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.


Proximal policy optimization algorithms.


arXiv preprint arXiv: Arxiv-1707.06347, 2017.



- 
[49]

Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom
Erez, Yuval Tassa, David Silver, and Daan Wierstra.


Continuous control with deep reinforcement learning.


In Yoshua Bengio and Yann LeCun, editors, 4th International
Conference on Learning Representations, ICLR 2016, San Juan, Puerto Rico,
May 2-4, 2016, Conference Track Proceedings, 2016.



- 
[50]

Introducing chatgpt, 2022.



- 
[51]

New and improved embedding model, 2022.



- 
[52]

PrismarineJS.


Prismarinejs/mineflayer: Create minecraft bots with a powerful,
stable, and high level javascript api., 2013.



- 
[53]

Kolby Nottingham, Prithviraj Ammanabrolu, Alane Suhr, Yejin Choi, Hanna
Hajishirzi, Sameer Singh, and Roy Fox.


Do embodied agents dream of pixelated sheep?: Embodied decision
making using language guided world modelling.


ARXIV.ORG, 2023.



- 
[54]

Shaofei Cai, Zihao Wang, Xiaojian Ma, Anji Liu, and Yitao Liang.


Open-world multi-task control through goal-aware representation
learning and adaptive horizon prediction.


arXiv preprint arXiv: Arxiv-2301.10034, 2023.



- 
[55]

Zihao Wang, Shaofei Cai, Anji Liu, Xiaojian Ma, and Yitao Liang.


Describe, explain, plan and select: Interactive planning with large
language models enables open-world multi-task agents.


arXiv preprint arXiv: Arxiv-2302.01560, 2023.



- 
[56]

Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric
Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg,
Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro, and Yi Zhang.


Sparks of artificial general intelligence: Early experiments with
gpt-4.


arXiv preprint arXiv: Arxiv-2303.12712, 2023.



- 
[57]

Yiheng Liu, Tianle Han, Siyuan Ma, Jiayue Zhang, Yuanyuan Yang, Jiaming Tian,
Hao He, Antong Li, Mengshen He, Zhengliang Liu, Zihao Wu, Dajiang Zhu, Xiang

Li, Ning Qiang, Dingang Shen, Tianming Liu, and Bao Ge.


Summary of chatgpt/gpt-4 research and perspective towards the future
of large language models.


arXiv preprint arXiv: Arxiv-2304.01852, 2023.



- 
[58]

Shikun Liu, Linxi Fan, Edward Johns, Zhiding Yu, Chaowei Xiao, and Anima
Anandkumar.


Prismer: A vision-language model with an ensemble of experts.


arXiv preprint arXiv: Arxiv-2303.02506, 2023.



- 
[59]

Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery,
Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong
Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine,
Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng,
Igor Mordatch, and Pete Florence.


Palm-e: An embodied multimodal language model.


arXiv preprint arXiv: Arxiv-2303.03378, 2023.



- 
[60]

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne
Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro,
Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume
Lample.


Llama: Open and efficient foundation language models.


arXiv preprint arXiv: Arxiv-2302.13971, 2023.



- 
[61]

William H. Guss, Brandon Houghton, Nicholay Topin, Phillip Wang, Cayden Codel,
Manuela Veloso, and Ruslan Salakhutdinov.


Minerl: A large-scale dataset of minecraft demonstrations.


In Sarit Kraus, editor, Proceedings of the Twenty-Eighth
International Joint Conference on Artificial Intelligence, IJCAI 2019,
Macao, China, August 10-16, 2019, pages 2442–2448. ijcai.org, 2019.



- 
[62]

William H. Guss, Cayden Codel, Katja Hofmann, Brandon Houghton, Noboru Kuno,
Stephanie Milani, Sharada Mohanty, Diego Perez Liebana, Ruslan Salakhutdinov,
Nicholay Topin, Manuela Veloso, and Phillip Wang.


The minerl 2019 competition on sample efficient reinforcement
learning using human priors.


arXiv preprint arXiv: Arxiv-1904.10079, 2019.



- 
[63]

William H. Guss, Mario Ynocente Castro, Sam Devlin, Brandon Houghton,
Noboru Sean Kuno, Crissman Loomis, Stephanie Milani, Sharada Mohanty, Keisuke
Nakata, Ruslan Salakhutdinov, John Schulman, Shinya Shiroshita, Nicholay
Topin, Avinash Ummadisingu, and Oriol Vinyals.


The minerl 2020 competition on sample efficient reinforcement
learning using human priors.


arXiv preprint arXiv: Arxiv-2101.11071, 2021.



- 
[64]

Anssi Kanervisto, Stephanie Milani, Karolis Ramanauskas, Nicholay Topin,
Zichuan Lin, Junyou Li, Jianing Shi, Deheng Ye, Qiang Fu, Wei Yang, Weijun
Hong, Zhongyue Huang, Haicheng Chen, Guangjun Zeng, Yue Lin, Vincent Micheli,
Eloi Alonso, François Fleuret, Alexander Nikulin, Yury Belousov, Oleg
Svidchenko, and Aleksei Shpilman.


Minerl diamond 2021 competition: Overview, results, and lessons
learned.


arXiv preprint arXiv: Arxiv-2202.10583, 2022.



- 
[65]

Matthew Johnson, Katja Hofmann, Tim Hutton, and David Bignell.


The malmo platform for artificial intelligence experimentation.


In Subbarao Kambhampati, editor, Proceedings of the Twenty-Fifth
International Joint Conference on Artificial Intelligence, IJCAI 2016, New
York, NY, USA, 9-15 July 2016, pages 4246–4247. IJCAI/AAAI Press, 2016.



- 
[66]

Zichuan Lin, Junyou Li, Jianing Shi, Deheng Ye, Qiang Fu, and Wei Yang.


Juewu-mc: Playing minecraft with sample-efficient hierarchical
reinforcement learning.


arXiv preprint arXiv: Arxiv-2112.04907, 2021.



- 
[67]

Hangyu Mao, Chao Wang, Xiaotian Hao, Yihuan Mao, Yiming Lu, Chengjie Wu, Jianye
Hao, Dong Li, and Pingzhong Tang.


Seihai: A sample-efficient hierarchical ai for the minerl
competition.


arXiv preprint arXiv: Arxiv-2111.08857, 2021.



- 
[68]

Alexey Skrynnik, Aleksey Staroverov, Ermek Aitygulov, Kirill Aksenov, Vasilii
Davydov, and Aleksandr I. Panov.


Hierarchical deep q-network from imperfect demonstrations in
minecraft.


Cogn. Syst. Res., 65:74–78, 2021.



- 
[69]

Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap.


Mastering diverse domains through world models.


arXiv preprint arXiv: Arxiv-2301.04104, 2023.



- 
[70]

Ryan Volum, Sudha Rao, Michael Xu, Gabriel DesGarennes, Chris Brockett,
Benjamin Van Durme, Olivia Deng, Akanksha Malhotra, and Bill Dolan.


Craft an iron sword: Dynamically generating interactive game
characters by prompting large language models tuned on code.


In Proceedings of the 3rd Wordplay: When Language Meets Games

Workshop (Wordplay 2022), pages 25–43, Seattle, United States, 2022.
Association for Computational Linguistics.



- 
[71]

Haoqi Yuan, Chi Zhang, Hongcheng Wang, Feiyang Xie, Penglin Cai, Hao Dong, and
Zongqing Lu.


Plan4mc: Skill reinforcement learning and planning for open-world
minecraft tasks.


arXiv preprint arXiv: 2303.16563, 2023.



- 
[72]

Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney
von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma
Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon,
Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora
Demszky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John
Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren
Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori
Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu,
Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri,
Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar Khattab, Pang Wei
Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal
Ladhak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li,
Xuechen Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani,
Eric Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak
Narayanan, Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan,
Julian Nyarko, Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung Park,
Chris Piech, Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich,
Hongyu Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher
Ré, Dorsa Sadigh, Shiori Sagawa, Keshav Santhanam, Andy Shih, Krishnan
Srinivasan, Alex Tamkin, Rohan Taori, Armin W. Thomas, Florian Tramèr,
Rose E. Wang, William Wang, Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie,
Michihiro Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi Zhang,
Xikun Zhang, Yuhui Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang.


On the opportunities and risks of foundation models.


arXiv preprint arXiv: Arxiv-2108.07258, 2021.



- 
[73]

Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra,
Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian
Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez,
Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran,
Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob
Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm
Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia,
Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David
Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David
Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai,
Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica
Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi
Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei,
Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel.


Palm: Scaling language modeling with pathways.


arXiv preprint arXiv: Arxiv-2204.02311, 2022.



- 
[74]

Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus,
Eric Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, Albert Webson,
Shixiang Shane Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha
Chowdhery, Sharan Narang, Gaurav Mishra, Adams Yu, Vincent Zhao, Yanping
Huang, Andrew Dai, Hongkun Yu, Slav Petrov, Ed H. Chi, Jeff Dean, Jacob
Devlin, Adam Roberts, Denny Zhou, Quoc V. Le, and Jason Wei.


Scaling instruction-finetuned language models.


arXiv preprint arXiv: Arxiv-2210.11416, 2022.



- 
[75]

Jiafei Duan, Samson Yu, Hui Li Tan, Hongyuan Zhu, and Cheston Tan.


A survey of embodied AI: from simulators to research tasks.


IEEE Trans. Emerg. Top. Comput. Intell., 6(2):230–244, 2022.



- 
[76]

Dhruv Batra, Angel X. Chang, Sonia Chernova, Andrew J. Davison, Jia Deng,
Vladlen Koltun, Sergey Levine, Jitendra Malik, Igor Mordatch, Roozbeh
Mottaghi, Manolis Savva, and Hao Su.


Rearrangement: A challenge for embodied ai.


arXiv preprint arXiv: Arxiv-2011.01975, 2020.



- 
[77]

Harish Ravichandar, Athanasios S Polydoros, Sonia Chernova, and Aude Billard.

Recent advances in robot learning from demonstration.


Annual review of control, robotics, and autonomous systems,
3:297–330, 2020.



- 
[78]

Jack Collins, Shelvin Chand, Anthony Vanderkop, and David Howard.


A review of physics simulators for robotic applications.


IEEE Access, 9:51416–51431, 2021.



- 
[79]

So Yeon Min, Devendra Singh Chaplot, Pradeep Ravikumar, Yonatan Bisk, and
R. Salakhutdinov.


Film: Following instructions in language with modular methods.


International Conference on Learning Representations, 2021.



- 
[80]

Valts Blukis, Chris Paxton, Dieter Fox, Animesh Garg, and Yoav Artzi.


A persistent spatial semantic representation for high-level natural
language instruction execution.


In 5th Annual Conference on Robot Learning, 2021.



- 
[81]

Varun Nair, Elliot Schumacher, Geoffrey Tso, and Anitha Kannan.


Dera: Enhancing large language model completions with dialog-enabled
resolving agents.


arXiv preprint arXiv: Arxiv-2303.17071, 2023.



- 
[82]

Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy
Liang, and Michael S. Bernstein.


Generative agents: Interactive simulacra of human behavior.


arXiv preprint arXiv: Arxiv-2304.03442, 2023.



- 
[83]

Yue Wu, Shrimai Prabhumoye, So Yeon Min, Yonatan Bisk, Ruslan Salakhutdinov,
Amos Azaria, Tom Mitchell, and Yuanzhi Li.


Spring: Gpt-4 out-performs rl algorithms by studying papers and
reasoning.


arXiv preprint arXiv: 2305.15486, 2023.



- 
[84]

Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio
Savarese, and Caiming Xiong.


A conversational paradigm for program synthesis.


arXiv preprint arXiv: Arxiv-2203.13474, 2022.



- 
[85]

Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H.
Hoi.


Coderl: Mastering code generation through pretrained models and deep
reinforcement learning.


arXiv preprint arXiv: Arxiv-2207.01780, 2022.



- 
[86]

Xinyun Chen, Chang Liu, and Dawn Song.


Execution-guided neural program synthesis.


In 7th International Conference on Learning Representations,
ICLR 2019, New Orleans, LA, USA, May 6-9, 2019. OpenReview.net, 2019.



- 
[87]

Xinyun Chen, Dawn Song, and Yuandong Tian.


Latent execution for neural program synthesis.


arXiv preprint arXiv: Arxiv-2107.00101, 2021.



- 
[88]

Kevin Ellis, Maxwell I. Nye, Yewen Pu, Felix Sosa, Josh Tenenbaum, and Armando
Solar-Lezama.


Write, execute, assess: Program synthesis with a REPL.


In Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence
d’Alché-Buc, Emily B. Fox, and Roman Garnett, editors, Advances
in Neural Information Processing Systems 32: Annual Conference on Neural
Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019,
Vancouver, BC, Canada, pages 9165–9174, 2019.



- 
[89]

Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi
Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas
Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen,
Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy,
Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando
de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.


Competition-level code generation with alphacode.


arXiv preprint arXiv: Arxiv-2203.07814, 2022.



- 
[90]

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz
Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano,
Christopher Hesse, and John Schulman.


Training verifiers to solve math word problems.


arXiv preprint arXiv: Arxiv-2110.14168, 2021.



- 
[91]

Ansong Ni, Srini Iyer, Dragomir Radev, Ves Stoyanov, Wen tau Yih, Sida I. Wang,
and Xi Victoria Lin.


Lever: Learning to verify language-to-code generation with execution.


arXiv preprint arXiv: Arxiv-2302.08468, 2023.



- 
[92]

Marta Skreta, Naruki Yoshikawa, Sebastian Arellano-Rubach, Zhi Ji, Lasse Bjørn
Kristensen, Kourosh Darvish, Alán Aspuru-Guzik, Florian Shkurti, and Animesh
Garg.


Errors are useful prompts: Instruction guided task programming with
verifier-assisted iterative prompting.


arXiv preprint arXiv: Arxiv-2303.14100, 2023.

### A.1 Voyager Algorithm
[⬇](data:text/plain;base64,ZGVmIHZveWFnZXIoCiAgICBlbnZpcm9ubWVudCwgICMgZW52aXJvbm1lbnQgdGhhdCB1c2VzIGNvZGUgYXMgYWN0aW9uIHNwYWNlCiAgICBjdXJyaWN1bHVtX2FnZW50LCAgIyBjdXJyaWN1bHVtIGFnZW50IGZvciBwcm9wb3NpbmcgdGhlIG5leHQgdGFzawogICAgYWN0aW9uX2FnZW50LCAgIyBhY3Rpb24gYWdlbnQgZm9yIGNvZGUgZ2VuZXJhdGlvbgogICAgY3JpdGljX2FnZW50LCAgIyBjcml0aWMgYWdlbnQgZm9yIHNlbGYtdmVyaWZpY2F0aW9uCiAgICBza2lsbF9tYW5hZ2VyLCAgIyBza2lsbCBtYW5hZ2VyIGZvciBhZGRpbmcgbmV3IHNraWxscyBhbmQgc2tpbGwgcmV0cmlldmFsCik6CiAgICBhZ2VudF9zdGF0ZSA9IGVudmlyb25tZW50LnJlc2V0KCkKICAgIHdoaWxlIFRydWU6CiAgICAgICAgZXhwbG9yYXRpb25fcHJvZ3Jlc3MgPSAoCiAgICAgICAgICAgIGN1cnJpY3VsdW1fYWdlbnQuZ2V0X2V4cGxvcmF0aW9uX3Byb2dyZXNzKAogICAgICAgICAgICAgICAgY3VycmljdWx1bV9hZ2VudC5nZXRfY29tcGxldGVkX3Rhc2tzKCksCiAgICAgICAgICAgICAgICBjdXJyaWN1bHVtX2FnZW50LmdldF9mYWlsZWRfdGFza3MoKSwKICAgICAgICAgICAgKQogICAgICAgICkKICAgICAgICB0YXNrID0gY3VycmljdWx1bV9hZ2VudC5wcm9wb3NlX25leHRfdGFzaygKICAgICAgICAgICAgYWdlbnRfc3RhdGUsIGV4cGxvcmF0aW9uX3Byb2dyZXNzCiAgICAgICAgKQogICAgICAgIGNvZGUgPSBOb25lCiAgICAgICAgZW52aXJvbm1lbnRfZmVlZGJhY2sgPSBOb25lCiAgICAgICAgZXhlY3V0aW9uX2Vycm9ycyA9IE5vbmUKICAgICAgICBjcml0aXF1ZSA9IE5vbmUKICAgICAgICBzdWNjZXNzID0gRmFsc2UKICAgICAgICAjIHRyeSBhdCBtb3N0IDQgcm91bmRzIGJlZm9yZSBtb3Zpbmcgb24gdG8gdGhlIG5leHQgdGFzawogICAgICAgIGZvciBpIGluIHJhbmdlKDQpOgogICAgICAgICAgICBza2lsbHMgPSBza2lsbF9tYW5hZ2VyLnJldHJpZXZlX3NraWxscygKICAgICAgICAgICAgICAgIHRhc2ssIGVudmlyb25tZW50X2ZlZWRiYWNrCiAgICAgICAgICAgICkKICAgICAgICAgICAgY29kZSA9IGFjdGlvbl9hZ2VudC5nZW5lcmF0ZV9jb2RlKAogICAgICAgICAgICAgICAgdGFzaywKICAgICAgICAgICAgICAgIGNvZGUsCiAgICAgICAgICAgICAgICBlbnZpcm9ubWVudF9mZWVkYmFjaywKICAgICAgICAgICAgICAgIGV4ZWN1dGlvbl9lcnJvcnMsCiAgICAgICAgICAgICAgICBjcml0aXF1ZSwKICAgICAgICAgICAgICAgIHNraWxscywKICAgICAgICAgICAgKQogICAgICAgICAgICAoCiAgICAgICAgICAgICAgICBhZ2VudF9zdGF0ZSwKICAgICAgICAgICAgICAgIGVudmlyb25tZW50X2ZlZWRiYWNrLAogICAgICAgICAgICAgICAgZXhlY3V0aW9uX2Vycm9ycywKICAgICAgICAgICAgKSA9IGVudmlyb25tZW50LnN0ZXAoY29kZSkKICAgICAgICAgICAgc3VjY2VzcywgY3JpdGlxdWUgPSBjcml0aWNfYWdlbnQuY2hlY2tfdGFza19zdWNjZXNzKAogICAgICAgICAgICAgICAgdGFzaywgYWdlbnRfc3RhdGUKICAgICAgICAgICAgKQogICAgICAgICAgICBpZiBzdWNjZXNzOgogICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICBpZiBzdWNjZXNzOgogICAgICAgICAgICBza2lsbF9tYW5hZ2VyLmFkZF9za2lsbChjb2RlKQogICAgICAgICAgICBjdXJyaWN1bHVtX2FnZW50LmFkZF9jb21wbGV0ZWRfdGFzayh0YXNrKQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGN1cnJpY3VsdW1fYWdlbnQuYWRkX2ZhaWxlZF90YXNrKHRhc2spCg==)

### A.2 Prompting
GPT-4 and GPT-3.5 offer users the ability to designate the role of each prompt message among three options:
- 
• 

System: A high-level instruction that guides the model behavior throughout the conversation. It sets the overall tone and objective for the interaction.


- 
• 

User: A detailed instruction that guides the assistant for the next immediate response.


- 
• 

Assistant: A response message generated the model.


System: A high-level instruction that guides the model behavior throughout the conversation. It sets the overall tone and objective for the interaction.
User: A detailed instruction that guides the assistant for the next immediate response.
Assistant: A response message generated the model.
See [https://platform.openai.com/docs/guides/chat/introduction](https://platform.openai.com/docs/guides/chat/introduction) for more details.
To save token usage, instead of engaging in multi-round conversations, we concatenate a system prompt and a user prompt to obtain each assistant’s response.

#### A.3.1 Components in the Prompt
The input prompt to GPT-4 consists of several components:
1. 
(1) 

Directives encouraging diverse behaviors and imposing constraints (so that the proposed task is achievable and verifiable): See Sec. [A.3.4](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS4) for the full prompt;


2. 
(2) 

The agent’s current state:


• 

Inventory: A dictionary of items with counts, for example, {‘cobblestone’: 4, ‘furnace’: 1, ‘stone_pickaxe’: 1, ‘oak_planks’: 7, ‘dirt’: 6, ‘wooden_pickaxe’: 1, ‘crafting_table’: 1, ‘raw_iron’: 4, ‘coal’: 1};



• 

Equipment: Armors or weapons equipped by the agents;



• 

Nearby blocks: A set of block names within a 32-block distance to the agent, for example, ‘dirt’, ‘water’, ‘spruce_planks’, ‘grass_block’, ‘dirt_path’, ‘sugar_cane’, ‘fern’;



• 

Other blocks that are recently seen: Blocks that are not nearby or in the inventory;



• 

Nearby entities: A set of entity names within a 32-block distance to the agent, for example, ‘pig’, ‘cat’, ‘villager’, ‘zombie’;



• 

A list of chests that are seen by the agent: Chests are external containers where the agent can deposit items. If a chest is not opened before, its content is “Unknown”. Otherwise, the items inside each chest are shown to the agent.



• 

Biome: For example, ‘plains’, ‘flower_forest’, ‘meadow’, ‘river’, ‘beach’, ‘forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘old_growth_birch_forest’, ‘ocean’, ‘sunflower_plains’, ‘stony_shore’;



• 

Time: One of ‘sunrise’, ‘day’, ‘noon’, ‘sunset’, ‘night’, ‘midnight’;



• 

Health and hunger bars: The max value is 20;



• 

Position: 3D coordinate (x,y,z)𝑥𝑦𝑧(x,y,z) of the agent’s position in the Minecraft world;





3. 
• 

Inventory: A dictionary of items with counts, for example, {‘cobblestone’: 4, ‘furnace’: 1, ‘stone_pickaxe’: 1, ‘oak_planks’: 7, ‘dirt’: 6, ‘wooden_pickaxe’: 1, ‘crafting_table’: 1, ‘raw_iron’: 4, ‘coal’: 1};


4. 
• 

Equipment: Armors or weapons equipped by the agents;


5. 
• 

Nearby blocks: A set of block names within a 32-block distance to the agent, for example, ‘dirt’, ‘water’, ‘spruce_planks’, ‘grass_block’, ‘dirt_path’, ‘sugar_cane’, ‘fern’;


6. 
• 

Other blocks that are recently seen: Blocks that are not nearby or in the inventory;


7. 
• 

Nearby entities: A set of entity names within a 32-block distance to the agent, for example, ‘pig’, ‘cat’, ‘villager’, ‘zombie’;


8. 
• 

A list of chests that are seen by the agent: Chests are external containers where the agent can deposit items. If a chest is not opened before, its content is “Unknown”. Otherwise, the items inside each chest are shown to the agent.


9. 
• 

Biome: For example, ‘plains’, ‘flower_forest’, ‘meadow’, ‘river’, ‘beach’, ‘forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘old_growth_birch_forest’, ‘ocean’, ‘sunflower_plains’, ‘stony_shore’;


10. 
• 

Time: One of ‘sunrise’, ‘day’, ‘noon’, ‘sunset’, ‘night’, ‘midnight’;


11. 
• 

Health and hunger bars: The max value is 20;


12. 
• 

Position: 3D coordinate (x,y,z)𝑥𝑦𝑧(x,y,z) of the agent’s position in the Minecraft world;


13. 
(3) 

Previously completed and failed tasks;


14. 
(4) 

Additional context: See Sec. [A.3.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS2);


15. 
(5) 

Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] in response: We request GPT-4 to first reason about the current progress and then suggest the next task.


Directives encouraging diverse behaviors and imposing constraints (so that the proposed task is achievable and verifiable): See Sec. [A.3.4](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS4) for the full prompt;
The agent’s current state:
- 
• 

Inventory: A dictionary of items with counts, for example, {‘cobblestone’: 4, ‘furnace’: 1, ‘stone_pickaxe’: 1, ‘oak_planks’: 7, ‘dirt’: 6, ‘wooden_pickaxe’: 1, ‘crafting_table’: 1, ‘raw_iron’: 4, ‘coal’: 1};


- 
• 

Equipment: Armors or weapons equipped by the agents;


- 
•

Nearby blocks: A set of block names within a 32-block distance to the agent, for example, ‘dirt’, ‘water’, ‘spruce_planks’, ‘grass_block’, ‘dirt_path’, ‘sugar_cane’, ‘fern’;


- 
• 

Other blocks that are recently seen: Blocks that are not nearby or in the inventory;


- 
• 

Nearby entities: A set of entity names within a 32-block distance to the agent, for example, ‘pig’, ‘cat’, ‘villager’, ‘zombie’;


- 
• 

A list of chests that are seen by the agent: Chests are external containers where the agent can deposit items. If a chest is not opened before, its content is “Unknown”. Otherwise, the items inside each chest are shown to the agent.


- 
• 

Biome: For example, ‘plains’, ‘flower_forest’, ‘meadow’, ‘river’, ‘beach’, ‘forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘old_growth_birch_forest’, ‘ocean’, ‘sunflower_plains’, ‘stony_shore’;


- 
• 

Time: One of ‘sunrise’, ‘day’, ‘noon’, ‘sunset’, ‘night’, ‘midnight’;


- 
• 

Health and hunger bars: The max value is 20;


- 
• 

Position: 3D coordinate (x,y,z)𝑥𝑦𝑧(x,y,z) of the agent’s position in the Minecraft world;


Inventory: A dictionary of items with counts, for example, {‘cobblestone’: 4, ‘furnace’: 1, ‘stone_pickaxe’: 1, ‘oak_planks’: 7, ‘dirt’: 6, ‘wooden_pickaxe’: 1, ‘crafting_table’: 1, ‘raw_iron’: 4, ‘coal’: 1};
Equipment: Armors or weapons equipped by the agents;
Nearby blocks: A set of block names within a 32-block distance to the agent, for example, ‘dirt’, ‘water’, ‘spruce_planks’, ‘grass_block’, ‘dirt_path’, ‘sugar_cane’, ‘fern’;
Other blocks that are recently seen: Blocks that are not nearby or in the inventory;
Nearby entities: A set of entity names within a 32-block distance to the agent, for example, ‘pig’, ‘cat’, ‘villager’, ‘zombie’;
A list of chests that are seen by the agent: Chests are external containers where the agent can deposit items. If a chest is not opened before, its content is “Unknown”. Otherwise, the items inside each chest are shown to the agent.
Biome: For example, ‘plains’, ‘flower_forest’, ‘meadow’, ‘river’, ‘beach’, ‘forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘old_growth_birch_forest’, ‘ocean’, ‘sunflower_plains’, ‘stony_shore’;
Time: One of ‘sunrise’, ‘day’, ‘noon’, ‘sunset’, ‘night’, ‘midnight’;
Health and hunger bars: The max value is 20;
Position: 3D coordinate (x,y,z)𝑥𝑦𝑧(x,y,z) of the agent’s position in the Minecraft world;
Previously completed and failed tasks;
Additional context: See Sec. [A.3.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS2);
Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] in response: We request GPT-4 to first reason about the current progress and then suggest the next task.

#### A.3.2 Additional Context
We leverage GPT-3.5 to self-ask questions to provide additional context. Each question is paired with a concept that is used for retrieving the most relevant document from the wiki knowledge base [[23](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib23)]. We feed the document content to GPT-3.5 for self-answering questions. In practice, using a wiki knowledge base is optional since GPT-3.5 already possesses a good understanding of Minecraft game mechanics. However, the external knowledge base becomes advantageous if GPT-3.5 is not pre-trained in that specific domain. See Sec. [A.3.4](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS4) for the full prompt.

#### A.3.3 Warm-up Schedule
In practice, we adopt a warm-up schedule to gradually incorporate the agent’s state and the additional context into the prompt based on how many tasks the agent has completed. This ensures that the prompt is exposed to increasing amounts of information over the exploration progress and therefore begins with basic skills and progressively advances towards more intricate and diverse ones. The warm-up setting that we use across all the experiments is shown in Table. [A.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.T1).

#### A.3.4 Full Prompt

[⬇](data:text/plain;base64,WW91IGFyZSBhIGhlbHBmdWwgYXNzaXN0YW50IHRoYXQgdGVsbHMgbWUgdGhlIG5leHQgaW1tZWRpYXRlIHRhc2sgdG8gZG8gaW4gTWluZWNyYWZ0LiBNeSB1bHRpbWF0ZSBnb2FsIGlzIHRvIGRpc2NvdmVyIGFzIG1hbnkgZGl2ZXJzZSB0aGluZ3MgYXMgcG9zc2libGUsIGFjY29tcGxpc2ggYXMgbWFueSBkaXZlcnNlIHRhc2tzIGFzIHBvc3NpYmxlIGFuZCBiZWNvbWUgdGhlIGJlc3QgTWluZWNyYWZ0IHBsYXllciBpbiB0aGUgd29ybGQuCgpJIHdpbGwgZ2l2ZSB5b3UgdGhlIGZvbGxvd2luZyBpbmZvcm1hdGlvbjoKUXVlc3Rpb24gMTogLi4uCkFuc3dlcjogLi4uClF1ZXN0aW9uIDI6IC4uLgpBbnN3ZXI6IC4uLgpRdWVzdGlvbiAzOiAuLi4KQW5zd2VyOiAuLi4KLi4uCkJpb21lOiAuLi4KVGltZTogLi4uCk5lYXJieSBibG9ja3M6IC4uLgpPdGhlciBibG9ja3MgdGhhdCBhcmUgcmVjZW50bHkgc2VlbjogLi4uCk5lYXJieSBlbnRpdGllcyAobmVhcmVzdCB0byBmYXJ0aGVzdCk6IC4uLgpIZWFsdGg6IEhpZ2hlciB0aGFuIDE1IG1lYW5zIEknbSBoZWFsdGh5LgpIdW5nZXI6IEhpZ2hlciB0aGFuIDE1IG1lYW5zIEknbSBub3QgaHVuZ3J5LgpQb3NpdGlvbjogLi4uCkVxdWlwbWVudDogSWYgSSBoYXZlIGJldHRlciBhcm1vciBpbiBteSBpbnZlbnRvcnksIHlvdSBzaG91bGQgYXNrIG1lIHRvIGVxdWlwIGl0LgpJbnZlbnRvcnkgKHh4LzM2KTogLi4uCkNoZXN0czogWW91IGNhbiBhc2sgbWUgdG8gZGVwb3NpdCBvciB0YWtlIGl0ZW1zIGZyb20gdGhlc2UgY2hlc3RzLiBUaGVyZSBhbHNvIG1pZ2h0IGJlIHNvbWUgdW5rbm93biBjaGVzdCwgeW91IHNob3VsZCBhc2sgbWUgdG8gb3BlbiBhbmQgY2hlY2sgaXRlbXMgaW5zaWRlIHRoZSB1bmtub3duIGNoZXN0LgpDb21wbGV0ZWQgdGFza3Mgc28gZmFyOiAuLi4KRmFpbGVkIHRhc2tzIHRoYXQgYXJlIHRvbyBoYXJkOiAuLi4KCllvdSBtdXN0IGZvbGxvdyB0aGUgZm9sbG93aW5nIGNyaXRlcmlhOgoxKSBZb3Ugc2hvdWxkIGFjdCBhcyBhIG1lbnRvciBhbmQgZ3VpZGUgbWUgdG8gdGhlIG5leHQgdGFzayBiYXNlZCBvbiBteSBjdXJyZW50IGxlYXJuaW5nIHByb2dyZXNzLgoyKSBQbGVhc2UgYmUgdmVyeSBzcGVjaWZpYyBhYm91dCB3aGF0IHJlc291cmNlcyBJIG5lZWQgdG8gY29sbGVjdCwgd2hhdCBJIG5lZWQgdG8gY3JhZnQsIG9yIHdoYXQgbW9icyBJIG5lZWQgdG8ga2lsbC4KMykgVGhlIG5leHQgdGFzayBzaG91bGQgZm9sbG93IGEgY29uY2lzZSBmb3JtYXQsIHN1Y2ggYXMgIk1pbmUgW3F1YW50aXR5XSBbYmxvY2tdIiwgIkNyYWZ0IFtxdWFudGl0eV0gW2l0ZW1dIiwgIlNtZWx0IFtxdWFudGl0eV0gW2l0ZW1dIiwgIktpbGwgW3F1YW50aXR5XSBbbW9iXSIsICJDb29rIFtxdWFudGl0eV0gW2Zvb2RdIiwgIkVxdWlwIFtpdGVtXSIgZXRjLiBJdCBzaG91bGQgYmUgYSBzaW5nbGUgcGhyYXNlLiBEbyBub3QgcHJvcG9zZSBtdWx0aXBsZSB0YXNrcyBhdCB0aGUgc2FtZSB0aW1lLiBEbyBub3QgbWVudGlvbiBhbnl0aGluZyBlbHNlLgo0KSBUaGUgbmV4dCB0YXNrIHNob3VsZCBub3QgYmUgdG9vIGhhcmQgc2luY2UgSSBtYXkgbm90IGhhdmUgdGhlIG5lY2Vzc2FyeSByZXNvdXJjZXMgb3IgaGF2ZSBsZWFybmVkIGVub3VnaCBza2lsbHMgdG8gY29tcGxldGUgaXQgeWV0Lgo1KSBUaGUgbmV4dCB0YXNrIHNob3VsZCBiZSBub3ZlbCBhbmQgaW50ZXJlc3RpbmcuIEkgc2hvdWxkIGxvb2sgZm9yIHJhcmUgcmVzb3VyY2VzLCB1cGdyYWRlIG15IGVxdWlwbWVudCBhbmQgdG9vbHMgdXNpbmcgYmV0dGVyIG1hdGVyaWFscywgYW5kIGRpc2NvdmVyIG5ldyB0aGluZ3MuIEkgc2hvdWxkIG5vdCBiZSBkb2luZyB0aGUgc2FtZSB0aGluZyBvdmVyIGFuZCBvdmVyIGFnYWluLgo2KSBJIG1heSBzb21ldGltZXMgbmVlZCB0byByZXBlYXQgc29tZSB0YXNrcyBpZiBJIG5lZWQgdG8gY29sbGVjdCBtb3JlIHJlc291cmNlcyB0byBjb21wbGV0ZSBtb3JlIGRpZmZpY3VsdCB0YXNrcy4gT25seSByZXBlYXQgdGFza3MgaWYgbmVjZXNzYXJ5Lgo3KSBEbyBub3QgYXNrIG1lIHRvIGJ1aWxkIG9yIGRpZyBzaGVsdGVyIGV2ZW4gaWYgaXQncyBhdCBuaWdodC4gSSB3YW50IHRvIGV4cGxvcmUgdGhlIHdvcmxkIGFuZCBkaXNjb3ZlciBuZXcgdGhpbmdzLiBJIGRvbid0IHdhbnQgdG8gc3RheSBpbiBvbmUgcGxhY2UuCjgpIFRhc2tzIHRoYXQgcmVxdWlyZSBpbmZvcm1hdGlvbiBiZXlvbmQgdGhlIHBsYXllcidzIHN0YXR1cyB0byB2ZXJpZnkgc2hvdWxkIGJlIGF2b2lkZWQuIEZvciBpbnN0YW5jZSwgIlBsYWNpbmcgNCB0b3JjaGVzIiBhbmQgIkRpZyBhIDJ4MXgyIGhvbGUiIGFyZSBub3QgaWRlYWwgc2luY2UgdGhleSByZXF1aXJlIHZpc3VhbCBjb25maXJtYXRpb24gZnJvbSB0aGUgc2NyZWVuLiBBbGwgdGhlIHBsYWNpbmcsIGJ1aWxkaW5nLCBwbGFudGluZywgYW5kIHRyYWRpbmcgdGFza3Mgc2hvdWxkIGJlIGF2b2lkZWQuIERvIG5vdCBwcm9wb3NlIHRhc2sgc3RhcnRpbmcgd2l0aCB0aGVzZSBrZXl3b3Jkcy4KCllvdSBzaG91bGQgb25seSByZXNwb25kIGluIHRoZSBmb3JtYXQgYXMgZGVzY3JpYmVkIGJlbG93OgpSRVNQT05TRSBGT1JNQVQ6ClJlYXNvbmluZzogQmFzZWQgb24gdGhlIGluZm9ybWF0aW9uIEkgbGlzdGVkIGFib3ZlLCBkbyByZWFzb25pbmcgYWJvdXQgd2hhdCB0aGUgbmV4dCB0YXNrIHNob3VsZCBiZS4KVGFzazogVGhlIG5leHQgdGFzay4KCkhlcmUncyBhbiBleGFtcGxlIHJlc3BvbnNlOgpSZWFzb25pbmc6IFRoZSBpbnZlbnRvcnkgaXMgZW1wdHkgbm93LCBjaG9wIGRvd24gYSB0cmVlIHRvIGdldCBzb21lIHdvb2QuClRhc2s6IE9idGFpbiBhIHdvb2QgbG9nLg==)

[⬇](data:text/plain;base64,WW91IGFyZSBhIGhlbHBmdWwgYXNzaXN0YW50IHRoYXQgYXNrcyBxdWVzdGlvbnMgdG8gaGVscCBtZSBkZWNpZGUgdGhlIG5leHQgaW1tZWRpYXRlIHRhc2sgdG8gZG8gaW4gTWluZWNyYWZ0LiBNeSB1bHRpbWF0ZSBnb2FsIGlzIHRvIGRpc2NvdmVyIGFzIG1hbnkgdGhpbmdzIGFzIHBvc3NpYmxlLCBhY2NvbXBsaXNoIGFzIG1hbnkgdGFza3MgYXMgcG9zc2libGUgYW5kIGJlY29tZSB0aGUgYmVzdCBNaW5lY3JhZnQgcGxheWVyIGluIHRoZSB3b3JsZC4KCkkgd2lsbCBnaXZlIHlvdSB0aGUgZm9sbG93aW5nIGluZm9ybWF0aW9uOgpCaW9tZTogLi4uClRpbWU6IC4uLgpOZWFyYnkgYmxvY2tzOiAuLi4KT3RoZXIgYmxvY2tzIHRoYXQgYXJlIHJlY2VudGx5IHNlZW46IC4uLgpOZWFyYnkgZW50aXRpZXMgKG5lYXJlc3QgdG8gZmFydGhlc3QpOiAuLi4KSGVhbHRoOiAuLi4KSHVuZ2VyOiAuLi4KUG9zaXRpb246IC4uLgpFcXVpcG1lbnQ6IC4uLgpJbnZlbnRvcnkgKHh4LzM2KTogLi4uCkNoZXN0czogLi4uCkNvbXBsZXRlZCB0YXNrcyBzbyBmYXI6IC4uLgpGYWlsZWQgdGFza3MgdGhhdCBhcmUgdG9vIGhhcmQ6IC4uLgoKWW91IG11c3QgZm9sbG93IHRoZSBmb2xsb3dpbmcgY3JpdGVyaWE6CjEpIFlvdSBzaG91bGQgYXNrIGF0IGxlYXN0IDUgcXVlc3Rpb25zIChidXQgbm8gbW9yZSB0aGFuIDEwIHF1ZXN0aW9ucykgdG8gaGVscCBtZSBkZWNpZGUgdGhlIG5leHQgaW1tZWRpYXRlIHRhc2sgdG8gZG8uIEVhY2ggcXVlc3Rpb24gc2hvdWxkIGJlIGZvbGxvd2VkIGJ5IHRoZSBjb25jZXB0IHRoYXQgdGhlIHF1ZXN0aW9uIGlzIGFib3V0LgoyKSBZb3VyIHF1ZXN0aW9uIHNob3VsZCBiZSBzcGVjaWZpYyB0byBhIGNvbmNlcHQgaW4gTWluZWNyYWZ0LgogIEJhZCBleGFtcGxlICh0aGUgcXVlc3Rpb24gaXMgdG9vIGdlbmVyYWwpOgogICAgUXVlc3Rpb246IFdoYXQgaXMgdGhlIGJlc3Qgd2F5IHRvIHBsYXkgTWluZWNyYWZ0PwogICAgQ29uY2VwdDogdW5rbm93bgogIEJhZCBleGFtcGxlIChheGUgaXMgc3RpbGwgZ2VuZXJhbCwgeW91IHNob3VsZCBzcGVjaWZ5IHRoZSB0eXBlIG9mIGF4ZSBzdWNoIGFzIHdvb2RlbiBheGUpOgogICAgV2hhdCBhcmUgdGhlIGJlbmVmaXRzIG9mIHVzaW5nIGFuIGF4ZSB0byBnYXRoZXIgcmVzb3VyY2VzPwogICAgQ29uY2VwdDogYXhlCiAgR29vZCBleGFtcGxlOgogICAgUXVlc3Rpb246IEhvdyB0byBtYWtlIGEgd29vZGVuIHBpY2theGU/CiAgICBDb25jZXB0OiB3b29kZW4gcGlja2F4ZQozKSBZb3VyIHF1ZXN0aW9ucyBzaG91bGQgYmUgc2VsZi1jb250YWluZWQgYW5kIG5vdCByZXF1aXJlIGFueSBjb250ZXh0LgogIEJhZCBleGFtcGxlICh0aGUgcXVlc3Rpb24gcmVxdWlyZXMgdGhlIGNvbnRleHQgb2YgbXkgY3VycmVudCBiaW9tZSk6CiAgICBRdWVzdGlvbjogV2hhdCBhcmUgdGhlIGJsb2NrcyB0aGF0IEkgY2FuIGZpbmQgaW4gbXkgY3VycmVudCBiaW9tZT8KICAgIENvbmNlcHQ6IHVua25vd24KICBCYWQgZXhhbXBsZSAodGhlIHF1ZXN0aW9uIHJlcXVpcmVzIHRoZSBjb250ZXh0IG9mIG15IGN1cnJlbnQgaW52ZW50b3J5KToKICAgIFF1ZXN0aW9uOiBXaGF0IGFyZSB0aGUgcmVzb3VyY2VzIHlvdSBuZWVkIHRoZSBtb3N0IGN1cnJlbnRseT8KICAgIENvbmNlcHQ6IHVua25vd24KICBCYWQgZXhhbXBsZSAodGhlIHF1ZXN0aW9uIHJlcXVpcmVzIHRoZSBjb250ZXh0IG9mIG15IGN1cnJlbnQgaW52ZW50b3J5KToKICAgIFF1ZXN0aW9uOiBEbyB5b3UgaGF2ZSBhbnkgZ29sZCBvciBlbWVyYWxkIHJlc291cmNlcz8KICAgIENvbmNlcHQ6IGdvbGQKICBCYWQgZXhhbXBsZSAodGhlIHF1ZXN0aW9uIHJlcXVpcmVzIHRoZSBjb250ZXh0IG9mIG15IG5lYXJieSBlbnRpdGllcyk6CiAgICBRdWVzdGlvbjogQ2FuIHlvdSBzZWUgYW55IGFuaW1hbHMgbmVhcmJ5IHRoYXQgeW91IGNhbiBraWxsIGZvciBmb29kPwogICAgQ29uY2VwdDogZm9vZAogIEJhZCBleGFtcGxlICh0aGUgcXVlc3Rpb24gcmVxdWlyZXMgdGhlIGNvbnRleHQgb2YgbXkgbmVhcmJ5IGJsb2Nrcyk6CiAgICBRdWVzdGlvbjogSXMgdGhlcmUgYW55IHdhdGVyIHNvdXJjZSBuZWFyYnk/CiAgICBDb25jZXB0OiB3YXRlcgogIEdvb2QgZXhhbXBsZToKICAgIFF1ZXN0aW9uOiBXaGF0IGFyZSB0aGUgYmxvY2tzIHRoYXQgSSBjYW4gZmluZCBpbiB0aGUgc3BhcnNlIGp1bmdsZT8KICAgIENvbmNlcHQ6IHNwYXJzZSBqdW5nbGUKNCkgRG8gbm90IGFzayBxdWVzdGlvbnMgYWJvdXQgYnVpbGRpbmcgdGFza3MgKHN1Y2ggYXMgYnVpbGRpbmcgYSBzaGVsdGVyKSBzaW5jZSB0aGV5IGFyZSB0b28gaGFyZCBmb3IgbWUgdG8gZG8uCgpMZXQncyBzYXkgeW91ciBjdXJyZW50IGJpb21lIGlzIHNwYXJzZSBqdW5nbGUuIFlvdSBjYW4gYXNrIHF1ZXN0aW9ucyBsaWtlOgpRdWVzdGlvbjogV2hhdCBhcmUgdGhlIGl0ZW1zIHRoYXQgSSBjYW4gZmluZCBpbiB0aGUgc3BhcnNlIGp1bmdsZT8KQ29uY2VwdDogc3BhcnNlIGp1bmdsZQpRdWVzdGlvbjogV2hhdCBhcmUgdGhlIG1vYnMgdGhhdCBJIGNhbiBmaW5kIGluIHRoZSBzcGFyc2UganVuZ2xlPwpDb25jZXB0OiBzcGFyc2UganVuZ2xlCgpMZXQncyBzYXkgeW91IHNlZSBhIGNyZWVwZXIgbmVhcmJ5LCBhbmQgeW91IGhhdmUgbm90IGRlZmVhdGVkIGEgY3JlZXBlciBiZWZvcmUuIFlvdSBjYW4gYXNrIGEgcXVlc3Rpb24gbGlrZToKUXVlc3Rpb246IEhvdyB0byBkZWZlYXQgdGhlIGNyZWVwZXI/CkNvbmNlcHQ6IGNyZWVwZXIKCkxldCdzIHNheSB5b3UgbGFzdCBjb21wbGV0ZWQgdGFzayBpcyAiQ3JhZnQgYSB3b29kZW4gcGlja2F4ZSIuIFlvdSBjYW4gYXNrIGEgcXVlc3Rpb24gbGlrZToKUXVlc3Rpb246IFdoYXQgYXJlIHRoZSBzdWdnZXN0ZWQgdGFza3MgdGhhdCBJIGNhbiBkbyBhZnRlciBjcmFmdGluZyBhIHdvb2RlbiBwaWNrYXhlPwpDb25jZXB0OiB3b29kZW4gcGlja2F4ZQoKSGVyZSBhcmUgc29tZSBtb3JlIHF1ZXN0aW9uIGFuZCBjb25jZXB0IGV4YW1wbGVzOgpRdWVzdGlvbjogV2hhdCBhcmUgdGhlIG9yZXMgdGhhdCBJIGNhbiBmaW5kIGluIHRoZSBzcGFyc2UganVuZ2xlPwpDb25jZXB0OiBzcGFyc2UganVuZ2xlCih0aGUgYWJvdmUgY29uY2VwdCBzaG91bGQgbm90IGJlICJvcmUiIGJlY2F1c2UgSSBuZWVkIHRvIGxvb2sgdXAgdGhlIHBhZ2Ugb2YgInNwYXJzZSBqdW5nbGUiIHRvIGZpbmQgb3V0IHdoYXQgb3JlcyBJIGNhbiBmaW5kIGluIHRoZSBzcGFyc2UganVuZ2xlKQpRdWVzdGlvbjogSG93IGNhbiB5b3Ugb2J0YWluIGZvb2QgaW4gdGhlIHNwYXJzZSBqdW5nbGU/CkNvbmNlcHQ6IHNwYXJzZSBqdW5nbGUKKHRoZSBhYm92ZSBjb25jZXB0IHNob3VsZCBub3QgYmUgImZvb2QiIGJlY2F1c2UgSSBuZWVkIHRvIGxvb2sgdXAgdGhlIHBhZ2Ugb2YgInNwYXJzZSBqdW5nbGUiIHRvIGZpbmQgb3V0IHdoYXQgZm9vZCBJIGNhbiBvYnRhaW4gaW4gdGhlIHNwYXJzZSBqdW5nbGUpClF1ZXN0aW9uOiBIb3cgY2FuIHlvdSB1c2UgdGhlIGZ1cm5hY2UgdG8gdXBncmFkZSB5b3VyIGVxdWlwbWVudCBhbmQgbWFrZSB1c2VmdWwgaXRlbXM/CkNvbmNlcHQ6IGZ1cm5hY2UKUXVlc3Rpb246IEhvdyB0byBvYnRhaW4gYSBkaWFtb25kIG9yZT8KQ29uY2VwdDogZGlhbW9uZCBvcmUKUXVlc3Rpb246IFdoYXQgYXJlIHRoZSBiZW5lZml0cyBvZiB1c2luZyBhIHN0b25lIHBpY2theGUgb3ZlciBhIHdvb2RlbiBwaWNrYXhlPwpDb25jZXB0OiBzdG9uZSBwaWNrYXhlClF1ZXN0aW9uOiBXaGF0IGFyZSB0aGUgdG9vbHMgdGhhdCB5b3UgY2FuIGNyYWZ0IHVzaW5nIHdvb2QgcGxhbmtzIGFuZCBzdGlja3M/CkNvbmNlcHQ6IHdvb2QgcGxhbmtzCgpZb3Ugc2hvdWxkIG9ubHkgcmVzcG9uZCBpbiB0aGUgZm9ybWF0IGFzIGRlc2NyaWJlZCBiZWxvdzoKUkVTUE9OU0UgRk9STUFUOgpSZWFzb25pbmc6IC4uLgpRdWVzdGlvbiAxOiAuLi4KQ29uY2VwdCAxOiAuLi4KUXVlc3Rpb24gMjogLi4uCkNvbmNlcHQgMjogLi4uClF1ZXN0aW9uIDM6IC4uLgpDb25jZXB0IDM6IC4uLgpRdWVzdGlvbiA0OiAuLi4KQ29uY2VwdCA0OiAuLi4KUXVlc3Rpb24gNTogLi4uCkNvbmNlcHQgNTogLi4uCi4uLg==)

[⬇](data:text/plain;base64,WW91IGFyZSBhIGhlbHBmdWwgYXNzaXN0YW50IHRoYXQgYW5zd2VyIG15IHF1ZXN0aW9uIGFib3V0IE1pbmVjcmFmdC4KCkkgd2lsbCBnaXZlIHlvdSB0aGUgZm9sbG93aW5nIGluZm9ybWF0aW9uOgpRdWVzdGlvbjogLi4uCgpZb3Ugd2lsbCBhbnN3ZXIgdGhlIHF1ZXN0aW9uIGJhc2VkIG9uIHRoZSBjb250ZXh0IChvbmx5IGlmIGF2YWlsYWJsZSBhbmQgaGVscGZ1bCkgYW5kIHlvdXIgb3duIGtub3dsZWRnZSBvZiBNaW5lY3JhZnQuCjEpIFN0YXJ0IHlvdXIgYW5zd2VyIHdpdGggIkFuc3dlcjogIi4KMikgQW5zd2VyICJBbnN3ZXI6IFVua25vd24iIGlmIHlvdSBkb24ndCBrbm93IHRoZSBhbnN3ZXIu)

#### A.4.1 Components in the Prompt
The input prompt to GPT-4 consists of the following components:
1. 
(1) 

Guidelines for code generation: See Sec [A.4.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS4.SSS2) for the full prompt;


2. 
(2) 

Control primitive APIs implemented by us: These APIs serve a dual purpose: they demonstrate the usage of Mineflayer APIs, and they can be directly called by GPT-4.


• 

exploreUntil(bot, direction, maxTime = 60, callback): Allow the agent to explore in a fixed direction for maxTime. The callback is the stopping condition implemented by the agent to determine when to stop exploring;



• 

mineBlock(bot, name, count = 1): Mine and collect the specified number of blocks within a 32-block distance;



• 

craftItem(bot, name, count = 1): Craft the item with a crafting table nearby;



• 

placeItem(bot, name, position): Place the block at the specified position;



• 

smeltItem(bot, itemName, fuelName, count = 1): Smelt the item with the specified fuel. There must be a furnace nearby;



• 

killMob(bot, mobName, timeout = 300): Attack the mob and collect its dropped item;



• 

getItemFromChest(bot, chestPosition, itemsToGet): Move to the chest at the specified position and get items from the chest;



• 

depositItemIntoChest(bot, chestPosition, itemsToDeposit): Move to the chest at the specified position and deposit items into the chest;





3. 
• 

exploreUntil(bot, direction, maxTime = 60, callback): Allow the agent to explore in a fixed direction for maxTime. The callback is the stopping condition implemented by the agent to determine when to stop exploring;


4. 
• 

mineBlock(bot, name, count = 1): Mine and collect the specified number of blocks within a 32-block distance;


5. 
• 

craftItem(bot, name, count = 1): Craft the item with a crafting table nearby;


6. 
• 

placeItem(bot, name, position): Place the block at the specified position;


7. 
• 

smeltItem(bot, itemName, fuelName, count = 1): Smelt the item with the specified fuel. There must be a furnace nearby;


8. 
• 

killMob(bot, mobName, timeout = 300): Attack the mob and collect its dropped item;


9. 
• 

getItemFromChest(bot, chestPosition, itemsToGet): Move to the chest at the specified position and get items from the chest;


10. 
• 

depositItemIntoChest(bot, chestPosition, itemsToDeposit): Move to the chest at the specified position and deposit items into the chest;


11. 
(3) 

Control primitive APIs provided by Mineflayer:


• 

await bot.pathfinder.goto(goal): Go to a specific position. See below for how to set the goal;



• 

new GoalNear(x, y, z, range): Move the bot to a block within the specified range of the specified block;



• 

new GoalXZ(x, z): For long-range goals that don’t have a specific Y level;



• 

new GoalGetToBlock(x, y, z): Not get into the block, but get directly adjacent to it. Useful for fishing, farming, filling a bucket, and using a bed.;



• 

new GoalFollow(entity, range): Follow the specified entity within the specified range;



• 

new GoalPlaceBlock(position, bot.world, {}): Position the bot in order to place a block;



• 

new GoalLookAtBlock(position, bot.world, {}): Path towards a position where a face of the block at position is visible;



• 

bot.isABed(bedBlock): Return true if bedBlock is a bed;



• 

bot.blockAt(position): Return the block at position;



• 

await bot.equip(item, destination): Equip the item in the specified destination. destination must be one of “hand”, “head”, “torso”, “legs”, “feet”, “off-hand”;



• 

await bot.consume(): Consume the item in the bot’s hand. You must equip the item to consume first. Useful for eating food, drinking potions, etc.;



• 

await bot.fish(): Let bot fish. Before calling this function, you must first get to a water block and then equip a fishing rod. The bot will automatically stop fishing when it catches a fish;



• 

await bot.sleep(bedBlock): Sleep until sunrise. You must get to a bed block first;



• 

await bot.activateBlock(block): This is the same as right-clicking a block in the game. Useful for buttons, doors, etc. You must get to the block first;



• 

await bot.lookAt(position): Look at the specified position. You must go near the position before you look at it. To fill a bucket with water, you must look at it first;



•

await bot.activateItem(): This is the same as right-clicking to use the item in the bot’s hand. Useful for using a bucket, etc. You must equip the item to activate first;



• 

await bot.useOn(entity): This is the same as right-clicking an entity in the game. Useful for shearing a sheep. You must get to the entity first;





12. 
• 

await bot.pathfinder.goto(goal): Go to a specific position. See below for how to set the goal;


13. 
• 

new GoalNear(x, y, z, range): Move the bot to a block within the specified range of the specified block;


14. 
• 

new GoalXZ(x, z): For long-range goals that don’t have a specific Y level;


15. 
• 

new GoalGetToBlock(x, y, z): Not get into the block, but get directly adjacent to it. Useful for fishing, farming, filling a bucket, and using a bed.;


16. 
• 

new GoalFollow(entity, range): Follow the specified entity within the specified range;


17. 
• 

new GoalPlaceBlock(position, bot.world, {}): Position the bot in order to place a block;


18. 
• 

new GoalLookAtBlock(position, bot.world, {}): Path towards a position where a face of the block at position is visible;


19. 
• 

bot.isABed(bedBlock): Return true if bedBlock is a bed;


20. 
• 

bot.blockAt(position): Return the block at position;


21. 
• 

await bot.equip(item, destination): Equip the item in the specified destination. destination must be one of “hand”, “head”, “torso”, “legs”, “feet”, “off-hand”;


22. 
• 

await bot.consume(): Consume the item in the bot’s hand. You must equip the item to consume first. Useful for eating food, drinking potions, etc.;


23. 
• 

await bot.fish(): Let bot fish. Before calling this function, you must first get to a water block and then equip a fishing rod. The bot will automatically stop fishing when it catches a fish;


24. 
• 

await bot.sleep(bedBlock): Sleep until sunrise. You must get to a bed block first;


25. 
• 

await bot.activateBlock(block): This is the same as right-clicking a block in the game. Useful for buttons, doors, etc. You must get to the block first;


26. 
• 

await bot.lookAt(position): Look at the specified position. You must go near the position before you look at it. To fill a bucket with water, you must look at it first;


27. 
• 

await bot.activateItem(): This is the same as right-clicking to use the item in the bot’s hand. Useful for using a bucket, etc. You must equip the item to activate first;


28. 
• 

await bot.useOn(entity): This is the same as right-clicking an entity in the game. Useful for shearing a sheep. You must get to the entity first;


29. 
(4) 

Retrieved skills from the skill library;


30. 
(5) 

Generated code from the last round;


31. 
(6) 

Environment feedback: The chat log in the prompt;


32. 
(7) 

Execution errors;


33. 
(8) 

Critique from the self-verification module;


34. 
(9) 

The agent’s current state: See Sec. [A.3.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS1) for each element of the agent’s state;


35. 
(10) 

Task proposed by the automatic curriculum;


36. 
(11) 

Task context: We prompt GPT-3.5 to ask for general suggestions about how to solve the task. In practice, this part is handled by the automatic curriculum since it has a systematic mechanism for question-answering (Sec. [A.3.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS2));


37. 
(12) 

Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] in response: We ask GPT-4 to first explain the reason why the code from the last round fails, then give step-by-step plans to finish the task, and finally generate code. See Sec. [A.4.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS4.SSS2) for the full prompt.


Guidelines for code generation: See Sec [A.4.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS4.SSS2) for the full prompt;
Control primitive APIs implemented by us: These APIs serve a dual purpose: they demonstrate the usage of Mineflayer APIs, and they can be directly called by GPT-4.
- 
• 

exploreUntil(bot, direction, maxTime = 60, callback): Allow the agent to explore in a fixed direction for maxTime. The callback is the stopping condition implemented by the agent to determine when to stop exploring;


- 
• 

mineBlock(bot, name, count = 1): Mine and collect the specified number of blocks within a 32-block distance;


- 
•

craftItem(bot, name, count = 1): Craft the item with a crafting table nearby;


- 
• 

placeItem(bot, name, position): Place the block at the specified position;


- 
• 

smeltItem(bot, itemName, fuelName, count = 1): Smelt the item with the specified fuel. There must be a furnace nearby;


- 
• 

killMob(bot, mobName, timeout = 300): Attack the mob and collect its dropped item;


- 
• 

getItemFromChest(bot, chestPosition, itemsToGet): Move to the chest at the specified position and get items from the chest;


- 
• 

depositItemIntoChest(bot, chestPosition, itemsToDeposit): Move to the chest at the specified position and deposit items into the chest;


exploreUntil(bot, direction, maxTime = 60, callback): Allow the agent to explore in a fixed direction for maxTime. The callback is the stopping condition implemented by the agent to determine when to stop exploring;
mineBlock(bot, name, count = 1): Mine and collect the specified number of blocks within a 32-block distance;
craftItem(bot, name, count = 1): Craft the item with a crafting table nearby;
placeItem(bot, name, position): Place the block at the specified position;
smeltItem(bot, itemName, fuelName, count = 1): Smelt the item with the specified fuel. There must be a furnace nearby;
killMob(bot, mobName, timeout = 300): Attack the mob and collect its dropped item;
getItemFromChest(bot, chestPosition, itemsToGet): Move to the chest at the specified position and get items from the chest;
depositItemIntoChest(bot, chestPosition, itemsToDeposit): Move to the chest at the specified position and deposit items into the chest;
Control primitive APIs provided by Mineflayer:
- 
• 

await bot.pathfinder.goto(goal): Go to a specific position. See below for how to set the goal;


- 
• 

new GoalNear(x, y, z, range): Move the bot to a block within the specified range of the specified block;


- 
• 

new GoalXZ(x, z): For long-range goals that don’t have a specific Y level;


- 
• 

new GoalGetToBlock(x, y, z): Not get into the block, but get directly adjacent to it. Useful for fishing, farming, filling a bucket, and using a bed.;


- 
• 

new GoalFollow(entity, range): Follow the specified entity within the specified range;


- 
• 

new GoalPlaceBlock(position, bot.world, {}): Position the bot in order to place a block;


- 
• 

new GoalLookAtBlock(position, bot.world, {}): Path towards a position where a face of the block at position is visible;


- 
• 

bot.isABed(bedBlock): Return true if bedBlock is a bed;


- 
• 

bot.blockAt(position): Return the block at position;


- 
• 

await bot.equip(item, destination): Equip the item in the specified destination. destination must be one of “hand”, “head”, “torso”, “legs”, “feet”, “off-hand”;


- 
• 

await bot.consume(): Consume the item in the bot’s hand. You must equip the item to consume first. Useful for eating food, drinking potions, etc.;


- 
• 

await bot.fish(): Let bot fish. Before calling this function, you must first get to a water block and then equip a fishing rod. The bot will automatically stop fishing when it catches a fish;


- 
• 

await bot.sleep(bedBlock): Sleep until sunrise. You must get to a bed block first;


- 
• 

await bot.activateBlock(block): This is the same as right-clicking a block in the game. Useful for buttons, doors, etc. You must get to the block first;


- 
• 

await bot.lookAt(position): Look at the specified position. You must go near the position before you look at it. To fill a bucket with water, you must look at it first;


- 
• 

await bot.activateItem(): This is the same as right-clicking to use the item in the bot’s hand. Useful for using a bucket, etc. You must equip the item to activate first;


- 
• 

await bot.useOn(entity): This is the same as right-clicking an entity in the game. Useful for shearing a sheep. You must get to the entity first;


await bot.pathfinder.goto(goal): Go to a specific position. See below for how to set the goal;
new GoalNear(x, y, z, range): Move the bot to a block within the specified range of the specified block;
new GoalXZ(x, z): For long-range goals that don’t have a specific Y level;
new GoalGetToBlock(x, y, z): Not get into the block, but get directly adjacent to it. Useful for fishing, farming, filling a bucket, and using a bed.;
new GoalFollow(entity, range): Follow the specified entity within the specified range;

new GoalPlaceBlock(position, bot.world, {}): Position the bot in order to place a block;
new GoalLookAtBlock(position, bot.world, {}): Path towards a position where a face of the block at position is visible;
bot.isABed(bedBlock): Return true if bedBlock is a bed;
bot.blockAt(position): Return the block at position;
await bot.equip(item, destination): Equip the item in the specified destination. destination must be one of “hand”, “head”, “torso”, “legs”, “feet”, “off-hand”;
await bot.consume(): Consume the item in the bot’s hand. You must equip the item to consume first. Useful for eating food, drinking potions, etc.;
await bot.fish(): Let bot fish. Before calling this function, you must first get to a water block and then equip a fishing rod. The bot will automatically stop fishing when it catches a fish;
await bot.sleep(bedBlock): Sleep until sunrise. You must get to a bed block first;
await bot.activateBlock(block): This is the same as right-clicking a block in the game. Useful for buttons, doors, etc. You must get to the block first;
await bot.lookAt(position): Look at the specified position. You must go near the position before you look at it. To fill a bucket with water, you must look at it first;
await bot.activateItem(): This is the same as right-clicking to use the item in the bot’s hand. Useful for using a bucket, etc. You must equip the item to activate first;
await bot.useOn(entity): This is the same as right-clicking an entity in the game. Useful for shearing a sheep. You must get to the entity first;
Retrieved skills from the skill library;
Generated code from the last round;
Environment feedback: The chat log in the prompt;
Execution errors;
Critique from the self-verification module;
The agent’s current state: See Sec. [A.3.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS1) for each element of the agent’s state;
Task proposed by the automatic curriculum;
Task context: We prompt GPT-3.5 to ask for general suggestions about how to solve the task. In practice, this part is handled by the automatic curriculum since it has a systematic mechanism for question-answering (Sec. [A.3.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS2));
Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] in response: We ask GPT-4 to first explain the reason why the code from the last round fails, then give step-by-step plans to finish the task, and finally generate code. See Sec. [A.4.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS4.SSS2) for the full prompt.

#### A.4.2 Full Prompt

[⬇](data:text/plain;base64,WW91IGFyZSBhIGhlbHBmdWwgYXNzaXN0YW50IHRoYXQgd3JpdGVzIE1pbmVmbGF5ZXIgamF2YXNjcmlwdCBjb2RlIHRvIGNvbXBsZXRlIGFueSBNaW5lY3JhZnQgdGFzayBzcGVjaWZpZWQgYnkgbWUuCgpIZXJlIGFyZSBzb21lIHVzZWZ1bCBwcm9ncmFtcyB3cml0dGVuIHdpdGggTWluZWZsYXllciBBUElzLgoKLyoKRXhwbG9yZSB1bnRpbCBmaW5kIGFuIGlyb25fb3JlLCB1c2UgVmVjMygwLCAtMSwgMCkgYmVjYXVzZSBpcm9uIG9yZXMgYXJlIHVzdWFsbHkgdW5kZXJncm91bmQKYXdhaXQgZXhwbG9yZVVudGlsKGJvdCwgbmV3IFZlYzMoMCwgLTEsIDApLCA2MCwgKCkgPT4gewogICAgY29uc3QgaXJvbl9vcmUgPSBib3QuZmluZEJsb2NrKHsKICAgICAgICBtYXRjaGluZzogbWNEYXRhLmJsb2Nrc0J5TmFtZVsiaXJvbl9vcmUiXS5pZCwKICAgICAgICBtYXhEaXN0YW5jZTogMzIsCiAgICB9KTsKICAgIHJldHVybiBpcm9uX29yZTsKfSk7CgpFeHBsb3JlIHVudGlsIGZpbmQgYSBwaWcsIHVzZSBWZWMzKDEsIDAsIDEpIGJlY2F1c2UgcGlncyBhcmUgdXN1YWxseSBvbiB0aGUgc3VyZmFjZQpsZXQgcGlnID0gYXdhaXQgZXhwbG9yZVVudGlsKGJvdCwgbmV3IFZlYzMoMSwgMCwgMSksIDYwLCAoKSA9PiB7CiAgICBjb25zdCBwaWcgPSBib3QubmVhcmVzdEVudGl0eSgoZW50aXR5KSA9PiB7CiAgICAgICAgcmV0dXJuICgKICAgICAgICAgICAgZW50aXR5Lm5hbWUgPT09ICJwaWciICYmCiAgICAgICAgICAgIGVudGl0eS5wb3NpdGlvbi5kaXN0YW5jZVRvKGJvdC5lbnRpdHkucG9zaXRpb24pIDwgMzIKICAgICAgICApOwogICAgfSk7CiAgICByZXR1cm4gcGlnOwp9KTsKKi8KYXN5bmMgZnVuY3Rpb24gZXhwbG9yZVVudGlsKGJvdCwgZGlyZWN0aW9uLCBtYXhUaW1lID0gNjAsIGNhbGxiYWNrKSB7CiAgICAvKgogICAgSW1wbGVtZW50YXRpb24gb2YgdGhpcyBmdW5jdGlvbiBpcyBvbWl0dGVkLgogICAgZGlyZWN0aW9uOiBWZWMzLCBjYW4gb25seSBjb250YWluIHZhbHVlIG9mIC0xLCAwIG9yIDEKICAgIG1heFRpbWU6IG51bWJlciwgdGhlIG1heCB0aW1lIGZvciBleHBsb3JhdGlvbgogICAgY2FsbGJhY2s6IGZ1bmN0aW9uLCBlYXJseSBzdG9wIGNvbmRpdGlvbiwgd2lsbCBiZSBjYWxsZWQgZWFjaCBzZWNvbmQsIGV4cGxvcmF0aW9uIHdpbGwgc3RvcCBpZiByZXR1cm4gdmFsdWUgaXMgbm90IG51bGwKCiAgICBSZXR1cm46IG51bGwgaWYgZXhwbG9yZSB0aW1lb3V0LCBvdGhlcndpc2UgcmV0dXJuIHRoZSByZXR1cm4gdmFsdWUgb2YgY2FsbGJhY2sKICAgICovCn0KCgovLyBNaW5lIDMgY29iYmxlc3RvbmU6IG1pbmVCbG9jayhib3QsICJzdG9uZSIsIDMpOwphc3luYyBmdW5jdGlvbiBtaW5lQmxvY2soYm90LCBuYW1lLCBjb3VudCA9IDEpIHsKICAgIGNvbnN0IGJsb2NrcyA9IGJvdC5maW5kQmxvY2tzKHsKICAgICAgICBtYXRjaGluZzogKGJsb2NrKSA9PiB7CiAgICAgICAgICAgIHJldHVybiBibG9jay5uYW1lID09PSBuYW1lOwogICAgICAgIH0sCiAgICAgICAgbWF4RGlzdGFuY2U6IDMyLAogICAgICAgIGNvdW50OiBjb3VudCwKICAgIH0pOwogICAgY29uc3QgdGFyZ2V0cyA9IFtdOwogICAgZm9yIChsZXQgaSA9IDA7IGkgPCBNYXRoLm1pbihibG9ja3MubGVuZ3RoLCBjb3VudCk7IGkrKykgewogICAgICAgIHRhcmdldHMucHVzaChib3QuYmxvY2tBdChibG9ja3NbaV0pKTsKICAgIH0KICAgIGF3YWl0IGJvdC5jb2xsZWN0QmxvY2suY29sbGVjdCh0YXJnZXRzLCB7IGlnbm9yZU5vUGF0aDogdHJ1ZSB9KTsKfQoKCi8vIENyYWZ0IDggb2FrX3BsYW5rcyBmcm9tIDIgb2FrX2xvZyAoZG8gdGhlIHJlY2lwZSAyIHRpbWVzKTogY3JhZnRJdGVtKGJvdCwgIm9ha19wbGFua3MiLCAyKTsKLy8gWW91IG11c3QgcGxhY2UgYSBjcmFmdGluZyB0YWJsZSBiZWZvcmUgY2FsbGluZyB0aGlzIGZ1bmN0aW9uCmFzeW5jIGZ1bmN0aW9uIGNyYWZ0SXRlbShib3QsIG5hbWUsIGNvdW50ID0gMSkgewogICAgY29uc3QgaXRlbSA9IG1jRGF0YS5pdGVtc0J5TmFtZVtuYW1lXTsKICAgIGNvbnN0IGNyYWZ0aW5nVGFibGUgPSBib3QuZmluZEJsb2NrKHsKICAgICAgICBtYXRjaGluZzogbWNEYXRhLmJsb2Nrc0J5TmFtZS5jcmFmdGluZ190YWJsZS5pZCwKICAgICAgICBtYXhEaXN0YW5jZTogMzIsCiAgICB9KTsKICAgIGF3YWl0IGJvdC5wYXRoZmluZGVyLmdvdG8oCiAgICAgICAgbmV3IEdvYWxMb29rQXRCbG9jayhjcmFmdGluZ1RhYmxlLnBvc2l0aW9uLCBib3Qud29ybGQpCiAgICApOwogICAgY29uc3QgcmVjaXBlID0gYm90LnJlY2lwZXNGb3IoaXRlbS5pZCwgbnVsbCwgMSwgY3JhZnRpbmdUYWJsZSlbMF07CiAgICBhd2FpdCBib3QuY3JhZnQocmVjaXBlLCBjb3VudCwgY3JhZnRpbmdUYWJsZSk7Cn0KCgovLyBQbGFjZSBhIGNyYWZ0aW5nX3RhYmxlIG5lYXIgdGhlIHBsYXllciwgVmVjMygxLCAwLCAwKSBpcyBqdXN0IGFuIGV4YW1wbGUsIHlvdSBzaG91bGRuJ3QgYWx3YXlzIHVzZSB0aGF0OiBwbGFjZUl0ZW0oYm90LCAiY3JhZnRpbmdfdGFibGUiLCBib3QuZW50aXR5LnBvc2l0aW9uLm9mZnNldCgxLCAwLCAwKSk7CmFzeW5jIGZ1bmN0aW9uIHBsYWNlSXRlbShib3QsIG5hbWUsIHBvc2l0aW9uKSB7CiAgICBjb25zdCBpdGVtID0gYm90LmludmVudG9yeS5maW5kSW52ZW50b3J5SXRlbShtY0RhdGEuaXRlbXNCeU5hbWVbbmFtZV0uaWQpOwogICAgLy8gZmluZCBhIHJlZmVyZW5jZSBibG9jawogICAgY29uc3QgZmFjZVZlY3RvcnMgPSBbCiAgICAgICAgbmV3IFZlYzMoMCwgMSwgMCksCiAgICAgICAgbmV3IFZlYzMoMCwgLTEsIDApLAogICAgICAgIG5ldyBWZWMzKDEsIDAsIDApLAogICAgICAgIG5ldyBWZWMzKC0xLCAwLCAwKSwKICAgICAgICBuZXcgVmVjMygwLCAwLCAxKSwKICAgICAgICBuZXcgVmVjMygwLCAwLCAtMSksCiAgICBdOwogICAgbGV0IHJlZmVyZW5jZUJsb2NrID0gbnVsbDsKICAgIGxldCBmYWNlVmVjdG9yID0gbnVsbDsKICAgIGZvciAoY29uc3QgdmVjdG9yIG9mIGZhY2VWZWN0b3JzKSB7CiAgICAgICAgY29uc3QgYmxvY2sgPSBib3QuYmxvY2tBdChwb3NpdGlvbi5taW51cyh2ZWN0b3IpKTsKICAgICAgICBpZiAoYmxvY2s/Lm5hbWUgIT09ICJhaXIiKSB7CiAgICAgICAgICAgIHJlZmVyZW5jZUJsb2NrID0gYmxvY2s7CiAgICAgICAgICAgIGZhY2VWZWN0b3IgPSB2ZWN0b3I7CiAgICAgICAgICAgIGJyZWFrOwogICAgICAgIH0KICAgIH0KICAgIC8vIFlvdSBtdXN0IGZpcnN0IGdvIHRvIHRoZSBibG9jayBwb3NpdGlvbiB5b3Ugd2FudCB0byBwbGFjZQogICAgYXdhaXQgYm90LnBhdGhmaW5kZXIuZ290byhuZXcgR29hbFBsYWNlQmxvY2socG9zaXRpb24sIGJvdC53b3JsZCwge30pKTsKICAgIC8vIFlvdSBtdXN0IGVxdWlwIHRoZSBpdGVtIHJpZ2h0IGJlZm9yZSBjYWxsaW5nIHBsYWNlQmxvY2sKICAgIGF3YWl0IGJvdC5lcXVpcChpdGVtLCAiaGFuZCIpOwogICAgYXdhaXQgYm90LnBsYWNlQmxvY2socmVmZXJlbmNlQmxvY2ssIGZhY2VWZWN0b3IpOwp9CgoKLy8gU21lbHQgMSByYXdfaXJvbiBpbnRvIDEgaXJvbl9pbmdvdCB1c2luZyAxIG9ha19wbGFua3MgYXMgZnVlbDogc21lbHRJdGVtKGJvdCwgInJhd19pcm9uIiwgIm9ha19wbGFua3MiKTsKLy8gWW91IG11c3QgcGxhY2UgYSBmdXJuYWNlIGJlZm9yZSBjYWxsaW5nIHRoaXMgZnVuY3Rpb24KYXN5bmMgZnVuY3Rpb24gc21lbHRJdGVtKGJvdCwgaXRlbU5hbWUsIGZ1ZWxOYW1lLCBjb3VudCA9IDEpIHsKICAgIGNvbnN0IGl0ZW0gPSBtY0RhdGEuaXRlbXNCeU5hbWVbaXRlbU5hbWVdOwogICAgY29uc3QgZnVlbCA9IG1jRGF0YS5pdGVtc0J5TmFtZVtmdWVsTmFtZV07CiAgICBjb25zdCBmdXJuYWNlQmxvY2sgPSBib3QuZmluZEJsb2NrKHsKICAgICAgICBtYXRjaGluZzogbWNEYXRhLmJsb2Nrc0J5TmFtZS5mdXJuYWNlLmlkLAogICAgICAgIG1heERpc3RhbmNlOiAzMiwKICAgIH0pOwogICAgYXdhaXQgYm90LnBhdGhmaW5kZXIuZ290bygKICAgICAgICBuZXcgR29hbExvb2tBdEJsb2NrKGZ1cm5hY2VCbG9jay5wb3NpdGlvbiwgYm90LndvcmxkKQogICAgKTsKICAgIGNvbnN0IGZ1cm5hY2UgPSBhd2FpdCBib3Qub3BlbkZ1cm5hY2UoZnVybmFjZUJsb2NrKTsKICAgIGZvciAobGV0IGkgPSAwOyBpIDwgY291bnQ7IGkrKykgewogICAgICAgIGF3YWl0IGZ1cm5hY2UucHV0RnVlbChmdWVsLmlkLCBudWxsLCAxKTsKICAgICAgICBhd2FpdCBmdXJuYWNlLnB1dElucHV0KGl0ZW0uaWQsIG51bGwsIDEpOwogICAgICAgIC8vIFdhaXQgMTIgc2Vjb25kcyBmb3IgdGhlIGZ1cm5hY2UgdG8gc21lbHQgdGhlIGl0ZW0KICAgICAgICBhd2FpdCBib3Qud2FpdEZvclRpY2tzKDEyICogMjApOwogICAgICAgIGF3YWl0IGZ1cm5hY2UudGFrZU91dHB1dCgpOwogICAgfQogICAgYXdhaXQgZnVybmFjZS5jbG9zZSgpOwp9CgoKLy8gS2lsbCBhIHBpZyBhbmQgY29sbGVjdCB0aGUgZHJvcHBlZCBpdGVtOiBraWxsTW9iKGJvdCwgInBpZyIsIDMwMCk7CmFzeW5jIGZ1bmN0aW9uIGtpbGxNb2IoYm90LCBtb2JOYW1lLCB0aW1lb3V0ID0gMzAwKSB7CiAgICBjb25zdCBlbnRpdHkgPSBib3QubmVhcmVzdEVudGl0eSgKICAgICAgICAoZW50aXR5KSA9PgogICAgICAgICAgICBlbnRpdHkubmFtZSA9PT0gbW9iTmFtZSAmJgogICAgICAgICAgICBlbnRpdHkucG9zaXRpb24uZGlzdGFuY2VUbyhib3QuZW50aXR5LnBvc2l0aW9uKSA8IDMyCiAgICApOwogICAgYXdhaXQgYm90LnB2cC5hdHRhY2soZW50aXR5KTsKICAgIGF3YWl0IGJvdC5wYXRoZmluZGVyLmdvdG8oCiAgICAgICAgbmV3IEdvYWxCbG9jayhlbnRpdHkucG9zaXRpb24ueCwgZW50aXR5LnBvc2l0aW9uLnksIGVudGl0eS5wb3NpdGlvbi56KQogICAgKTsKfQoKCi8vIEdldCBhIHRvcmNoIGZyb20gY2hlc3QgYXQgKDMwLCA2NSwgMTAwKTogZ2V0SXRlbUZyb21DaGVzdChib3QsIG5ldyBWZWMzKDMwLCA2NSwgMTAwKSwgeyJ0b3JjaCI6IDF9KTsKLy8gVGhpcyBmdW5jdGlvbiB3aWxsIHdvcmsgbm8gbWF0dGVyIGhvdyBmYXIgdGhlIGJvdCBpcyBmcm9tIHRoZSBjaGVzdC4KYXN5bmMgZnVuY3Rpb24gZ2V0SXRlbUZyb21DaGVzdChib3QsIGNoZXN0UG9zaXRpb24sIGl0ZW1zVG9HZXQpIHsKICAgIGF3YWl0IG1vdmVUb0NoZXN0KGJvdCwgY2hlc3RQb3NpdGlvbik7CiAgICBjb25zdCBjaGVzdEJsb2NrID0gYm90LmJsb2NrQXQoY2hlc3RQb3NpdGlvbik7CiAgICBjb25zdCBjaGVzdCA9IGF3YWl0IGJvdC5vcGVuQ29udGFpbmVyKGNoZXN0QmxvY2spOwogICAgZm9yIChjb25zdCBuYW1lIGluIGl0ZW1zVG9HZXQpIHsKICAgICAgICBjb25zdCBpdGVtQnlOYW1lID0gbWNEYXRhLml0ZW1zQnlOYW1lW25hbWVdOwogICAgICAgIGNvbnN0IGl0ZW0gPSBjaGVzdC5maW5kQ29udGFpbmVySXRlbShpdGVtQnlOYW1lLmlkKTsKICAgICAgICBhd2FpdCBjaGVzdC53aXRoZHJhdyhpdGVtLnR5cGUsIG51bGwsIGl0ZW1zVG9HZXRbbmFtZV0pOwogICAgfQogICAgYXdhaXQgY2xvc2VDaGVzdChib3QsIGNoZXN0QmxvY2spOwp9Ci8vIERlcG9zaXQgYSB0b3JjaCBpbnRvIGNoZXN0IGF0ICgzMCwgNjUsIDEwMCk6IGRlcG9zaXRJdGVtSW50b0NoZXN0KGJvdCwgbmV3IFZlYzMoMzAsIDY1LCAxMDApLCB7InRvcmNoIjogMX0pOwovLyBUaGlzIGZ1bmN0aW9uIHdpbGwgd29yayBubyBtYXR0ZXIgaG93IGZhciB0aGUgYm90IGlzIGZyb20gdGhlIGNoZXN0Lgphc3luYyBmdW5jdGlvbiBkZXBvc2l0SXRlbUludG9DaGVzdChib3QsIGNoZXN0UG9zaXRpb24sIGl0ZW1zVG9EZXBvc2l0KSB7CiAgICBhd2FpdCBtb3ZlVG9DaGVzdChib3QsIGNoZXN0UG9zaXRpb24pOwogICAgY29uc3QgY2hlc3RCbG9jayA9IGJvdC5ibG9ja0F0KGNoZXN0UG9zaXRpb24pOwogICAgY29uc3QgY2hlc3QgPSBhd2FpdCBib3Qub3BlbkNvbnRhaW5lcihjaGVzdEJsb2NrKTsKICAgIGZvciAoY29uc3QgbmFtZSBpbiBpdGVtc1RvRGVwb3NpdCkgewogICAgICAgIGNvbnN0IGl0ZW1CeU5hbWUgPSBtY0RhdGEuaXRlbXNCeU5hbWVbbmFtZV07CiAgICAgICAgY29uc3QgaXRlbSA9IGJvdC5pbnZlbnRvcnkuZmluZEludmVudG9yeUl0ZW0oaXRlbUJ5TmFtZS5pZCk7CiAgICAgICAgYXdhaXQgY2hlc3QuZGVwb3NpdChpdGVtLnR5cGUsIG51bGwsIGl0ZW1zVG9EZXBvc2l0W25hbWVdKTsKICAgIH0KICAgIGF3YWl0IGNsb3NlQ2hlc3QoYm90LCBjaGVzdEJsb2NrKTsKfQovLyBDaGVjayB0aGUgaXRlbXMgaW5zaWRlIHRoZSBjaGVzdCBhdCAoMzAsIDY1LCAxMDApOiBjaGVja0l0ZW1JbnNpZGVDaGVzdChib3QsIG5ldyBWZWMzKDMwLCA2NSwgMTAwKSk7Ci8vIFlvdSBvbmx5IG5lZWQgdG8gY2FsbCB0aGlzIGZ1bmN0aW9uIG9uY2Ugd2l0aG91dCBhbnkgYWN0aW9uIHRvIGZpbmlzaCB0YXNrIG9mIGNoZWNraW5nIGl0ZW1zIGluc2lkZSB0aGUgY2hlc3QuCmFzeW5jIGZ1bmN0aW9uIGNoZWNrSXRlbUluc2lkZUNoZXN0KGJvdCwgY2hlc3RQb3NpdGlvbikgewogICAgYXdhaXQgbW92ZVRvQ2hlc3QoYm90LCBjaGVzdFBvc2l0aW9uKTsKICAgIGNvbnN0IGNoZXN0QmxvY2sgPSBib3QuYmxvY2tBdChjaGVzdFBvc2l0aW9uKTsKICAgIGF3YWl0IGJvdC5vcGVuQ29udGFpbmVyKGNoZXN0QmxvY2spOwogICAgLy8gWW91IG11c3QgY2xvc2UgdGhlIGNoZXN0IGFmdGVyIG9wZW5pbmcgaXQgaWYgeW91IGFyZSBhc2tlZCB0byBvcGVuIGEgY2hlc3QKICAgIGF3YWl0IGNsb3NlQ2hlc3QoYm90LCBjaGVzdEJsb2NrKTsKfQoKCmF3YWl0IGJvdC5wYXRoZmluZGVyLmdvdG8oZ29hbCk7IC8vIEEgdmVyeSB1c2VmdWwgZnVuY3Rpb24uIFRoaXMgZnVuY3Rpb24gbWF5IGNoYW5nZSB5b3VyIG1haW4taGFuZCBlcXVpcG1lbnQuCi8vIEZvbGxvd2luZyBhcmUgc29tZSBHb2FscyB5b3UgY2FuIHVzZToKbmV3IEdvYWxOZWFyKHgsIHksIHosIHJhbmdlKTsgLy8gTW92ZSB0aGUgYm90IHRvIGEgYmxvY2sgd2l0aGluIHRoZSBzcGVjaWZpZWQgcmFuZ2Ugb2YgdGhlIHNwZWNpZmllZCBibG9jay4gYHhgLCBgeWAsIGB6YCwgYW5kIGByYW5nZWAgYXJlIGBudW1iZXJgCm5ldyBHb2FsWFooeCwgeik7IC8vIFVzZWZ1bCBmb3IgbG9uZy1yYW5nZSBnb2FscyB0aGF0IGRvbid0IGhhdmUgYSBzcGVjaWZpYyBZIGxldmVsLiBgeGAgYW5kIGB6YCBhcmUgYG51bWJlcmAKbmV3IEdvYWxHZXRUb0Jsb2NrKHgsIHksIHopOyAvLyBOb3QgZ2V0IGludG8gdGhlIGJsb2NrLCBidXQgZ2V0IGRpcmVjdGx5IGFkamFjZW50IHRvIGl0LiBVc2VmdWwgZm9yIGZpc2hpbmcsIGZhcm1pbmcsIGZpbGxpbmcgYnVja2V0LCBhbmQgYmVkcy4gYHhgLCBgeWAsIGFuZCBgemAgYXJlIGBudW1iZXJgCm5ldyBHb2FsRm9sbG93KGVudGl0eSwgcmFuZ2UpOyAvLyBGb2xsb3cgdGhlIHNwZWNpZmllZCBlbnRpdHkgd2l0aGluIHRoZSBzcGVjaWZpZWQgcmFuZ2UuIGBlbnRpdHlgIGlzIGBFbnRpdHlgLCBgcmFuZ2VgIGlzIGBudW1iZXJgCm5ldyBHb2FsUGxhY2VCbG9jayhwb3NpdGlvbiwgYm90LndvcmxkLCB7fSk7IC8vIFBvc2l0aW9uIHRoZSBib3QgaW4gb3JkZXIgdG8gcGxhY2UgYSBibG9jay4gYHBvc2l0aW9uYCBpcyBgVmVjM2AKbmV3IEdvYWxMb29rQXRCbG9jayhwb3NpdGlvbiwgYm90LndvcmxkLCB7fSk7IC8vIFBhdGggaW50byBhIHBvc2l0aW9uIHdoZXJlIGEgYmxvY2tmYWNlIG9mIHRoZSBibG9jayBhdCBwb3NpdGlvbiBpcyB2aXNpYmxlLiBgcG9zaXRpb25gIGlzIGBWZWMzYAoKLy8gVGhlc2UgYXJlIG90aGVyIE1pbmVmbGF5ZXIgZnVuY3Rpb25zIHlvdSBjYW4gdXNlOgpib3QuaXNBQmVkKGJlZEJsb2NrKTsgLy8gUmV0dXJuIHRydWUgaWYgYGJlZEJsb2NrYCBpcyBhIGJlZApib3QuYmxvY2tBdChwb3NpdGlvbik7IC8vIFJldHVybiB0aGUgYmxvY2sgYXQgYHBvc2l0aW9uYC4gYHBvc2l0aW9uYCBpcyBgVmVjM2AKCi8vIFRoZXNlIGFyZSBvdGhlciBNaW5lZmxheWVyIGFzeW5jIGZ1bmN0aW9ucyB5b3UgY2FuIHVzZToKYXdhaXQgYm90LmVxdWlwKGl0ZW0sIGRlc3RpbmF0aW9uKTsgLy8gRXF1aXAgdGhlIGl0ZW0gaW4gdGhlIHNwZWNpZmllZCBkZXN0aW5hdGlvbi4gYGl0ZW1gIGlzIGBJdGVtYCwgYGRlc3RpbmF0aW9uYCBjYW4gb25seSBiZSAiaGFuZCIsICJoZWFkIiwgInRvcnNvIiwgImxlZ3MiLCAiZmVldCIsICJvZmYtaGFuZCIKYXdhaXQgYm90LmNvbnN1bWUoKTsgLy8gQ29uc3VtZSB0aGUgaXRlbSBpbiB0aGUgYm90J3MgaGFuZC4gWW91IG11c3QgZXF1aXAgdGhlIGl0ZW0gdG8gY29uc3VtZSBmaXJzdC4gVXNlZnVsIGZvciBlYXRpbmcgZm9vZCwgZHJpbmtpbmcgcG90aW9ucywgZXRjLgphd2FpdCBib3QuZmlzaCgpOyAvLyBMZXQgYm90IGZpc2guIEJlZm9yZSBjYWxsaW5nIHRoaXMgZnVuY3Rpb24sIHlvdSBtdXN0IGZpcnN0IGdldCB0byBhIHdhdGVyIGJsb2NrIGFuZCB0aGVuIGVxdWlwIGEgZmlzaGluZyByb2QuIFRoZSBib3Qgd2lsbCBhdXRvbWF0aWNhbGx5IHN0b3AgZmlzaGluZyB3aGVuIGl0IGNhdGNoZXMgYSBmaXNoCmF3YWl0IGJvdC5zbGVlcChiZWRCbG9jayk7IC8vIFNsZWVwIHVudGlsIHN1bnJpc2UuIFlvdSBtdXN0IGdldCB0byBhIGJlZCBibG9jayBmaXJzdAphd2FpdCBib3QuYWN0aXZhdGVCbG9jayhibG9jayk7IC8vIFRoaXMgaXMgdGhlIHNhbWUgYXMgcmlnaHQtY2xpY2tpbmcgYSBibG9jayBpbiB0aGUgZ2FtZS4gVXNlZnVsIGZvciBidXR0b25zLCBkb29ycywgdXNpbmcgaG9lcywgZXRjLiBZb3UgbXVzdCBnZXQgdG8gdGhlIGJsb2NrIGZpcnN0CmF3YWl0IGJvdC5sb29rQXQocG9zaXRpb24pOyAvLyBMb29rIGF0IHRoZSBzcGVjaWZpZWQgcG9zaXRpb24uIFlvdSBtdXN0IGdvIG5lYXIgdGhlIHBvc2l0aW9uIGJlZm9yZSB5b3UgbG9vayBhdCBpdC4gVG8gZmlsbCBidWNrZXQgd2l0aCB3YXRlciwgeW91IG11c3QgbG9va0F0IGZpcnN0LiBgcG9zaXRpb25gIGlzIGBWZWMzYAphd2FpdCBib3QuYWN0aXZhdGVJdGVtKCk7IC8vIFRoaXMgaXMgdGhlIHNhbWUgYXMgcmlnaHQtY2xpY2tpbmcgdG8gdXNlIHRoZSBpdGVtIGluIHRoZSBib3QncyBoYW5kLiBVc2VmdWwgZm9yIHVzaW5nIGJ1Y2tldHMsIGV0Yy4gWW91IG11c3QgZXF1aXAgdGhlIGl0ZW0gdG8gYWN0aXZhdGUgZmlyc3QKYXdhaXQgYm90LnVzZU9uKGVudGl0eSk7IC8vIFRoaXMgaXMgdGhlIHNhbWUgYXMgcmlnaHQtY2xpY2tpbmcgYW4gZW50aXR5IGluIHRoZSBnYW1lLiBVc2VmdWwgZm9yIHNoZWFyaW5nIHNoZWVwLCBlcXVpcHBpbmcgaGFybmVzc2VzLCBldGMuIFlvdSBtdXN0IGdldCB0byB0aGUgZW50aXR5IGZpcnN0Cgp7cmV0cmlldmVkX3NraWxsc30KCgpBdCBlYWNoIHJvdW5kIG9mIGNvbnZlcnNhdGlvbiwgSSB3aWxsIGdpdmUgeW91CkNvZGUgZnJvbSB0aGUgbGFzdCByb3VuZDogLi4uCkV4ZWN1dGlvbiBlcnJvcjogLi4uCkNoYXQgbG9nOiAuLi4KQmlvbWU6IC4uLgpUaW1lOiAuLi4KTmVhcmJ5IGJsb2NrczogLi4uCk5lYXJieSBlbnRpdGllcyAobmVhcmVzdCB0byBmYXJ0aGVzdCk6CkhlYWx0aDogLi4uCkh1bmdlcjogLi4uClBvc2l0aW9uOiAuLi4KRXF1aXBtZW50OiAuLi4KSW52ZW50b3J5ICh4eC8zNik6IC4uLgpDaGVzdHM6IC4uLgpUYXNrOiAuLi4KQ29udGV4dDogLi4uCkNyaXRpcXVlOiAuLi4KCllvdSBzaG91bGQgdGhlbiByZXNwb25kIHRvIG1lIHdpdGgKRXhwbGFpbiAoaWYgYXBwbGljYWJsZSk6IEFyZSB0aGVyZSBhbnkgc3RlcHMgbWlzc2luZyBpbiB5b3VyIHBsYW4/IFdoeSBkb2VzIHRoZSBjb2RlIG5vdCBjb21wbGV0ZSB0aGUgdGFzaz8gV2hhdCBkb2VzIHRoZSBjaGF0IGxvZyBhbmQgZXhlY3V0aW9uIGVycm9yIGltcGx5PwpQbGFuOiBIb3cgdG8gY29tcGxldGUgdGhlIHRhc2sgc3RlcCBieSBzdGVwLiBZb3Ugc2hvdWxkIHBheSBhdHRlbnRpb24gdG8gSW52ZW50b3J5IHNpbmNlIGl0IHRlbGxzIHdoYXQgeW91IGhhdmUuIFRoZSB0YXNrIGNvbXBsZXRlbmVzcyBjaGVjayBpcyBhbHNvIGJhc2VkIG9uIHlvdXIgZmluYWwgaW52ZW50b3J5LgpDb2RlOgogICAgMSkgV3JpdGUgYW4gYXN5bmMgZnVuY3Rpb24gdGFraW5nIHRoZSBib3QgYXMgdGhlIG9ubHkgYXJndW1lbnQuCiAgICAyKSBSZXVzZSB0aGUgYWJvdmUgdXNlZnVsIHByb2dyYW1zIGFzIG11Y2ggYXMgcG9zc2libGUuCiAgICAgICAgLSBVc2UgYG1pbmVCbG9jayhib3QsIG5hbWUsIGNvdW50KWAgdG8gY29sbGVjdCBibG9ja3MuIERvIG5vdCB1c2UgYGJvdC5kaWdgIGRpcmVjdGx5LgogICAgICAgIC0gVXNlIGBjcmFmdEl0ZW0oYm90LCBuYW1lLCBjb3VudClgIHRvIGNyYWZ0IGl0ZW1zLiBEbyBub3QgdXNlIGBib3QuY3JhZnRgIGRpcmVjdGx5LgogICAgICAgIC0gVXNlIGBzbWVsdEl0ZW0oYm90LCBuYW1lIGNvdW50KWAgdG8gc21lbHQgaXRlbXMuIERvIG5vdCB1c2UgYGJvdC5vcGVuRnVybmFjZWAgZGlyZWN0bHkuCiAgICAgICAgLSBVc2UgYHBsYWNlSXRlbShib3QsIG5hbWUsIHBvc2l0aW9uKWAgdG8gcGxhY2UgYmxvY2tzLiBEbyBub3QgdXNlIGBib3QucGxhY2VCbG9ja2AgZGlyZWN0bHkuCiAgICAgICAgLSBVc2UgYGtpbGxNb2IoYm90LCBuYW1lLCB0aW1lb3V0KWAgdG8ga2lsbCBtb2JzLiBEbyBub3QgdXNlIGBib3QuYXR0YWNrYCBkaXJlY3RseS4KICAgIDMpIFlvdXIgZnVuY3Rpb24gd2lsbCBiZSByZXVzZWQgZm9yIGJ1aWxkaW5nIG1vcmUgY29tcGxleCBmdW5jdGlvbnMuIFRoZXJlZm9yZSwgeW91IHNob3VsZCBtYWtlIGl0IGdlbmVyaWMgYW5kIHJldXNhYmxlLiBZb3Ugc2hvdWxkIG5vdCBtYWtlIHN0cm9uZyBhc3N1bXB0aW9uIGFib3V0IHRoZSBpbnZlbnRvcnkgKGFzIGl0IG1heSBiZSBjaGFuZ2VkIGF0IGEgbGF0ZXIgdGltZSksIGFuZCB0aGVyZWZvcmUgeW91IHNob3VsZCBhbHdheXMgY2hlY2sgd2hldGhlciB5b3UgaGF2ZSB0aGUgcmVxdWlyZWQgaXRlbXMgYmVmb3JlIHVzaW5nIHRoZW0uIElmIG5vdCwgeW91IHNob3VsZCBmaXJzdCBjb2xsZWN0IHRoZSByZXF1aXJlZCBpdGVtcyBhbmQgcmV1c2UgdGhlIGFib3ZlIHVzZWZ1bCBwcm9ncmFtcy4KICAgIDQpIEZ1bmN0aW9ucyBpbiB0aGUgIkNvZGUgZnJvbSB0aGUgbGFzdCByb3VuZCIgc2VjdGlvbiB3aWxsIG5vdCBiZSBzYXZlZCBvciBleGVjdXRlZC4gRG8gbm90IHJldXNlIGZ1bmN0aW9ucyBsaXN0ZWQgdGhlcmUuCiAgICA1KSBBbnl0aGluZyBkZWZpbmVkIG91dHNpZGUgYSBmdW5jdGlvbiB3aWxsIGJlIGlnbm9yZWQsIGRlZmluZSBhbGwgeW91ciB2YXJpYWJsZXMgaW5zaWRlIHlvdXIgZnVuY3Rpb25zLgogICAgNikgQ2FsbCBgYm90LmNoYXRgIHRvIHNob3cgdGhlIGludGVybWVkaWF0ZSBwcm9ncmVzcy4KICAgIDcpIFVzZSBgZXhwbG9yZVVudGlsKGJvdCwgZGlyZWN0aW9uLCBtYXhEaXN0YW5jZSwgY2FsbGJhY2spYCB3aGVuIHlvdSBjYW5ub3QgZmluZCBzb21ldGhpbmcuIFlvdSBzaG91bGQgZnJlcXVlbnRseSBjYWxsIHRoaXMgYmVmb3JlIG1pbmluZyBibG9ja3Mgb3Iga2lsbGluZyBtb2JzLiBZb3Ugc2hvdWxkIHNlbGVjdCBhIGRpcmVjdGlvbiBhdCByYW5kb20gZXZlcnkgdGltZSBpbnN0ZWFkIG9mIGNvbnN0YW50bHkgdXNpbmcgKDEsIDAsIDEpLgogICAgOCkgYG1heERpc3RhbmNlYCBzaG91bGQgYWx3YXlzIGJlIDMyIGZvciBgYm90LmZpbmRCbG9ja3NgIGFuZCBgYm90LmZpbmRCbG9ja2AuIERvIG5vdCBjaGVhdC4KICAgIDkpIERvIG5vdCB3cml0ZSBpbmZpbml0ZSBsb29wcyBvciByZWN1cnNpdmUgZnVuY3Rpb25zLgogICAgMTApIERvIG5vdCB1c2UgYGJvdC5vbmAgb3IgYGJvdC5vbmNlYCB0byByZWdpc3RlciBldmVudCBsaXN0ZW5lcnMuIFlvdSBkZWZpbml0ZWx5IGRvIG5vdCBuZWVkIHRoZW0uCiAgICAxMSkgTmFtZSB5b3VyIGZ1bmN0aW9uIGluIGEgbWVhbmluZ2Z1bCB3YXkgKGNhbiBpbmZlciB0aGUgdGFzayBmcm9tIHRoZSBuYW1lKS4KCllvdSBzaG91bGQgb25seSByZXNwb25kIGluIHRoZSBmb3JtYXQgYXMgZGVzY3JpYmVkIGJlbG93OgpSRVNQT05TRSBGT1JNQVQ6CkV4cGxhaW46IC4uLgpQbGFuOgoxKSAuLi4KMikgLi4uCjMpIC4uLgouLi4KQ29kZToKYGBgamF2YXNjcmlwdAovLyBoZWxwZXIgZnVuY3Rpb25zIChvbmx5IGlmIG5lZWRlZCwgdHJ5IHRvIGF2b2lkIHRoZW0pCi4uLgovLyBtYWluIGZ1bmN0aW9uIGFmdGVyIHRoZSBoZWxwZXIgZnVuY3Rpb25zCmFzeW5jIGZ1bmN0aW9uIHlvdXJNYWluRnVuY3Rpb25OYW1lKGJvdCkgewogIC8vIC4uLgp9CmBgYA==)

[⬇](data:text/plain;base64,WW91IGFyZSBhIGhlbHBmdWwgYXNzaXN0YW50IHRoYXQgd3JpdGVzIGEgZGVzY3JpcHRpb24gb2YgdGhlIGdpdmVuIGZ1bmN0aW9uIHdyaXR0ZW4gaW4gTWluZWZsYXllciBqYXZhc2NyaXB0IGNvZGUuCgoxKSBEbyBub3QgbWVudGlvbiB0aGUgZnVuY3Rpb24gbmFtZS4KMikgRG8gbm90IG1lbnRpb24gYW55dGhpbmcgYWJvdXQgYGJvdC5jaGF0YCBvciBoZWxwZXIgZnVuY3Rpb25zLgozKSBUaGVyZSBtaWdodCBiZSBzb21lIGhlbHBlciBmdW5jdGlvbnMgYmVmb3JlIHRoZSBtYWluIGZ1bmN0aW9uLCBidXQgeW91IG9ubHkgbmVlZCB0byBkZXNjcmliZSB0aGUgbWFpbiBmdW5jdGlvbi4KNCkgVHJ5IHRvIHN1bW1hcml6ZSB0aGUgZnVuY3Rpb24gaW4gbm8gbW9yZSB0aGFuIDYgc2VudGVuY2VzLgo1KSBZb3VyIHJlc3BvbnNlIHNob3VsZCBiZSBhIHNpbmdsZSBsaW5lIG9mIHRleHQuCgpGb3IgZXhhbXBsZSwgaWYgdGhlIGZ1bmN0aW9uIGlzOgoKYXN5bmMgZnVuY3Rpb24gbWluZUNvYmJsZXN0b25lKGJvdCkgewogIC8vIENoZWNrIGlmIHRoZSB3b29kZW4gcGlja2F4ZSBpcyBpbiB0aGUgaW52ZW50b3J5LCBpZiBub3QsIGNyYWZ0IG9uZQogIGxldCB3b29kZW5QaWNrYXhlID0gYm90LmludmVudG9yeS5maW5kSW52ZW50b3J5SXRlbShtY0RhdGEuaXRlbXNCeU5hbWVbIndvb2Rlbl9waWNrYXhlIl0uaWQpOwogIGlmICghd29vZGVuUGlja2F4ZSkgewogICAgYm90LmNoYXQoIkNyYWZ0aW5nIGEgd29vZGVuIHBpY2theGUuIik7CiAgICBhd2FpdCBjcmFmdFdvb2RlblBpY2theGUoYm90KTsKICAgIHdvb2RlblBpY2theGUgPSBib3QuaW52ZW50b3J5LmZpbmRJbnZlbnRvcnlJdGVtKG1jRGF0YS5pdGVtc0J5TmFtZVsid29vZGVuX3BpY2theGUiXS5pZCk7CiAgfQoKICAvLyBFcXVpcCB0aGUgd29vZGVuIHBpY2theGUgaWYgaXQgZXhpc3RzCiAgaWYgKHdvb2RlblBpY2theGUpIHsKICAgIGF3YWl0IGJvdC5lcXVpcCh3b29kZW5QaWNrYXhlLCAiaGFuZCIpOwoKICAgIC8vIEV4cGxvcmUgdW50aWwgd2UgZmluZCBhIHN0b25lIGJsb2NrCiAgICBhd2FpdCBleHBsb3JlVW50aWwoYm90LCBuZXcgVmVjMygxLCAtMSwgMSksIDYwLCAoKSA9PiB7CiAgICAgIGNvbnN0IHN0b25lID0gYm90LmZpbmRCbG9jayh7CiAgICAgICAgbWF0Y2hpbmc6IG1jRGF0YS5ibG9ja3NCeU5hbWVbInN0b25lIl0uaWQsCiAgICAgICAgbWF4RGlzdGFuY2U6IDMyCiAgICAgIH0pOwogICAgICBpZiAoc3RvbmUpIHsKICAgICAgICByZXR1cm4gdHJ1ZTsKICAgICAgfQogICAgfSk7CgogICAgLy8gTWluZSA4IGNvYmJsZXN0b25lIGJsb2NrcyB1c2luZyB0aGUgd29vZGVuIHBpY2theGUKICAgIGJvdC5jaGF0KCJGb3VuZCBhIHN0b25lIGJsb2NrLiBNaW5pbmcgOCBjb2JibGVzdG9uZSBibG9ja3MuIik7CiAgICBhd2FpdCBtaW5lQmxvY2soYm90LCAic3RvbmUiLCA4KTsKICAgIGJvdC5jaGF0KCJTdWNjZXNzZnVsbHkgbWluZWQgOCBjb2JibGVzdG9uZSBibG9ja3MuIik7CgogICAgLy8gU2F2ZSB0aGUgZXZlbnQgb2YgbWluaW5nIDggY29iYmxlc3RvbmUKICAgIGJvdC5zYXZlKCJjb2JibGVzdG9uZV9taW5lZCIpOwogIH0gZWxzZSB7CiAgICBib3QuY2hhdCgiRmFpbGVkIHRvIGNyYWZ0IGEgd29vZGVuIHBpY2theGUuIENhbm5vdCBtaW5lIGNvYmJsZXN0b25lLiIpOwogIH0KfQoKVGhlIG1haW4gZnVuY3Rpb24gaXMgYG1pbmVDb2JibGVzdG9uZWAuCgpUaGVuIHlvdSB3b3VsZCB3cml0ZToKClRoZSBmdW5jdGlvbiBpcyBhYm91dCBtaW5pbmcgOCBjb2JibGVzdG9uZXMgdXNpbmcgYSB3b29kZW4gcGlja2F4ZS4gRmlyc3QgY2hlY2sgaWYgYSB3b29kZW4gcGlja2F4ZSBpcyBpbiB0aGUgaW52ZW50b3J5LiBJZiBub3QsIGNyYWZ0IG9uZS4gSWYgdGhlIHdvb2RlbiBwaWNrYXhlIGlzIGF2YWlsYWJsZSwgZXF1aXAgdGhlIHdvb2RlbiBwaWNrYXhlIGluIHRoZSBoYW5kLiBOZXh0LCBleHBsb3JlIHRoZSBlbnZpcm9ubWVudCB1bnRpbCBmaW5kaW5nIGEgc3RvbmUgYmxvY2suIE9uY2UgYSBzdG9uZSBibG9jayBpcyBmb3VuZCwgbWluZSBhIHRvdGFsIG9mIDggY29iYmxlc3RvbmUgYmxvY2tzIHVzaW5nIHRoZSB3b29kZW4gcGlja2F4ZS4=)

#### A.4.3 Examples
[⬇](data:text/plain;base64,YXN5bmMgZnVuY3Rpb24gY3JhZnRXb29kZW5QbGFua3MoYm90KSB7DQogIGNvbnN0IGxvZ05hbWVzID0gWyJvYWtfbG9nIiwgImJpcmNoX2xvZyIsICJzcHJ1Y2VfbG9nIiwgImp1bmdsZV9sb2ciLCAiYWNhY2lhX2xvZyIsICJkYXJrX29ha19sb2ciLCAibWFuZ3JvdmVfbG9nIl07DQogIGNvbnN0IHBsYW5rTmFtZXMgPSBbIm9ha19wbGFua3MiLCAiYmlyY2hfcGxhbmtzIiwgInNwcnVjZV9wbGFua3MiLCAianVuZ2xlX3BsYW5rcyIsICJhY2FjaWFfcGxhbmtzIiwgImRhcmtfb2FrX3BsYW5rcyIsICJtYW5ncm92ZV9wbGFua3MiXTsNCiAgY29uc3QgbG9nSW5JbnZlbnRvcnkgPSBsb2dOYW1lcy5maW5kKGxvZ05hbWUgPT4gYm90LmludmVudG9yeS5jb3VudChtY0RhdGEuaXRlbXNCeU5hbWVbbG9nTmFtZV0uaWQpID4gMCk7DQogIGlmICghbG9nSW5JbnZlbnRvcnkpIHsNCiAgICBib3QuY2hhdCgiTm8gd29vZGVuIGxvZyBpbiBpbnZlbnRvcnkuIE1pbmluZyBhIHdvb2RlbiBsb2cuLi4iKTsNCiAgICBhd2FpdCBtaW5lV29vZExvZyhib3QpOw0KICB9DQogIGNvbnN0IGxvZ0luZGV4ID0gbG9nTmFtZXMuaW5kZXhPZihsb2dJbkludmVudG9yeSk7DQogIGNvbnN0IHBsYW5rTmFtZSA9IHBsYW5rTmFtZXNbbG9nSW5kZXhdOw0KICBib3QuY2hhdChgQ3JhZnRpbmcgNCAke3BsYW5rTmFtZX0uLi5gKTsNCiAgYXdhaXQgY3JhZnRJdGVtKGJvdCwgcGxhbmtOYW1lLCAxKTsNCiAgYm90LmNoYXQoYDQgJHtwbGFua05hbWV9IGNyYWZ0ZWQuYCk7DQp9)

[⬇](data:text/plain;base64,YXN5bmMgZnVuY3Rpb24gbWluZVRlbkNvYmJsZWREZWVwc2xhdGVCZWxvd1kwKGJvdCkgew0KICAvLyBFcXVpcCB0aGUgaXJvbiBwaWNrYXhlDQogIGNvbnN0IGlyb25QaWNrYXhlID0gYm90LmludmVudG9yeS5maW5kSW52ZW50b3J5SXRlbShtY0RhdGEuaXRlbXNCeU5hbWVbImlyb25fcGlja2F4ZSJdLmlkKTsNCiAgYXdhaXQgYm90LmVxdWlwKGlyb25QaWNrYXhlLCAiaGFuZCIpOw0KDQogIC8vIEZpbmQgY29iYmxlZF9kZWVwc2xhdGUgYmxvY2tzIGJlbG93IFk9MA0KICBjb25zdCBjb2JibGVkRGVlcHNsYXRlQmxvY2tzID0gYXdhaXQgZXhwbG9yZVVudGlsKGJvdCwgbmV3IFZlYzMoMSwgLTEsIDEpLCA2MCwgKCkgPT4gew0KICAgIGNvbnN0IGNvYmJsZWREZWVwc2xhdGUgPSBib3QuZmluZEJsb2NrKHsNCiAgICAgIG1hdGNoaW5nOiBtY0RhdGEuYmxvY2tzQnlOYW1lWyJjb2JibGVkX2RlZXBzbGF0ZSJdLmlkLA0KICAgICAgbWF4RGlzdGFuY2U6IDMyLA0KICAgICAgcG9zaXRpb246IHBvcyA9PiBwb3MueSA8IDANCiAgICB9KTsNCiAgICByZXR1cm4gY29iYmxlZERlZXBzbGF0ZTsNCiAgfSk7DQoNCiAgLy8gTWluZSAxMCBjb2JibGVkX2RlZXBzbGF0ZSBibG9ja3MNCiAgYXdhaXQgbWluZUJsb2NrKGJvdCwgImNvYmJsZWRfZGVlcHNsYXRlIiwgMTApOw0KICBib3QuY2hhdCgiMTAgY29iYmxlZF9kZWVwc2xhdGUgbWluZWQgYmVsb3cgWT0wLiIpOw0KfQ==)
[⬇](data:text/plain;base64,YXN5bmMgZnVuY3Rpb24gZmluZFN1aXRhYmxlUG9zaXRpb24oYm90KSB7DQogIGNvbnN0IG9mZnNldHMgPSBbbmV3IFZlYzMoMSwgMCwgMCksIG5ldyBWZWMzKC0xLCAwLCAwKSwgbmV3IFZlYzMoMCwgMCwgMSksIG5ldyBWZWMzKDAsIDAsIC0xKV07DQogIGZvciAoY29uc3Qgb2Zmc2V0IG9mIG9mZnNldHMpIHsNCiAgICBjb25zdCBwb3NpdGlvbiA9IGJvdC5lbnRpdHkucG9zaXRpb24ub2Zmc2V0KG9mZnNldC54LCBvZmZzZXQueSwgb2Zmc2V0LnopOw0KICAgIGNvbnN0IGJsb2NrID0gYm90LmJsb2NrQXQocG9zaXRpb24pOw0KICAgIGlmIChibG9jay5uYW1lID09PSAiYWlyIikgew0KICAgICAgcmV0dXJuIHBvc2l0aW9uOw0KICAgIH0NCiAgfQ0KICByZXR1cm4gbnVsbDsNCn0NCg0KYXN5bmMgZnVuY3Rpb24gc21lbHRGaXZlUmF3SXJvbihib3QpIHsNCiAgLy8gQ2hlY2sgaWYgdGhlcmUgaXMgYSBmdXJuYWNlIGluIHRoZSBpbnZlbnRvcnkNCiAgY29uc3QgZnVybmFjZUl0ZW0gPSBib3QuaW52ZW50b3J5LmZpbmRJbnZlbnRvcnlJdGVtKG1jRGF0YS5pdGVtc0J5TmFtZS5mdXJuYWNlLmlkKTsNCg0KICAvLyBJZiBub3QsIGNyYWZ0IGEgZnVybmFjZSB1c2luZyB0aGUgYXZhaWxhYmxlIGNvYmJsZXN0b25lDQogIGlmICghZnVybmFjZUl0ZW0pIHsNCiAgICBhd2FpdCBjcmFmdEZ1cm5hY2UoYm90KTsNCiAgfQ0KDQogIC8vIEZpbmQgYSBzdWl0YWJsZSBwb3NpdGlvbiB0byBwbGFjZSB0aGUgZnVybmFjZQ0KICBjb25zdCBmdXJuYWNlUG9zaXRpb24gPSBhd2FpdCBmaW5kU3VpdGFibGVQb3NpdGlvbihib3QpOw0KICBpZiAoIWZ1cm5hY2VQb3NpdGlvbikgew0KICAgIGJvdC5jaGF0KCJDb3VsZCBub3QgZmluZCBhIHN1aXRhYmxlIHBvc2l0aW9uIHRvIHBsYWNlIHRoZSBmdXJuYWNlLiIpOw0KICAgIHJldHVybjsNCiAgfQ0KDQogIC8vIFBsYWNlIHRoZSBmdXJuYWNlIGF0IHRoZSBzdWl0YWJsZSBwb3NpdGlvbg0KICBhd2FpdCBwbGFjZUl0ZW0oYm90LCAiZnVybmFjZSIsIGZ1cm5hY2VQb3NpdGlvbik7DQoNCiAgLy8gU21lbHQgNSByYXcgaXJvbiB1c2luZyB0aGUgYXZhaWxhYmxlIGNvYWwgYXMgZnVlbA0KICBhd2FpdCBzbWVsdEl0ZW0oYm90LCAicmF3X2lyb24iLCAiY29hbCIsIDUpOw0KICBib3QuY2hhdCgiNSByYXcgaXJvbiBzbWVsdGVkLiIpOw0KfQ==)
[⬇](data:text/plain;base64,YXN5bmMgZnVuY3Rpb24gZmlsbEJ1Y2tldFdpdGhXYXRlcihib3QpIHsNCi8vIEZpbmQgYSB3YXRlciBibG9jayBuZWFyYnkNCiAgY29uc3Qgd2F0ZXJCbG9jayA9IGF3YWl0IGV4cGxvcmVVbnRpbChib3QsIG5ldyBWZWMzKDEsIDAsIDEpLCA2MCwgKCkgPT4gew0KICAgIGNvbnN0IHdhdGVyID0gYm90LmZpbmRCbG9jayh7DQogICAgICBtYXRjaGluZzogbWNEYXRhLmJsb2Nrc0J5TmFtZS53YXRlci5pZCwNCiAgICAgIG1heERpc3RhbmNlOiAzMg0KICAgIH0pOw0KICAgIHJldHVybiB3YXRlcjsNCiAgfSk7DQogIGlmICghd2F0ZXJCbG9jaykgew0KICAgIGJvdC5jaGF0KCJDb3VsZCBub3QgZmluZCB3YXRlci4iKTsNCiAgICByZXR1cm47DQogIH0NCg0KICAvLyBHbyB0byB0aGUgd2F0ZXIgYmxvY2sNCiAgY29uc3QgYWRqYWNlbnRCbG9jaz0gd2F0ZXJCbG9jay5wb3NpdGlvbi5vZmZzZXQoMCwgMSwgMCk7DQogIGF3YWl0IGJvdC5wYXRoZmluZGVyLmdvdG8oDQogICAgICBuZXcgR29hbEdldFRvQmxvY2soYWRqYWNlbnRCbG9jay54LCBhZGphY2VudEJsb2NrLnksIGFkamFjZW50QmxvY2sueikNCiAgKTsNCg0KICAvLyBMb29rIGF0IHRoZSB3YXRlciBibG9jaw0KICBhd2FpdCBib3QubG9va0F0KHdhdGVyQmxvY2sucG9zaXRpb24sIHRydWUpOw0KDQogIC8vIEVxdWlwIHRoZSBidWNrZXQNCiAgY29uc3QgYnVja2V0ID0gYm90LmludmVudG9yeS5maW5kSW52ZW50b3J5SXRlbShtY0RhdGEuaXRlbXNCeU5hbWUuYnVja2V0LmlkKTsNCiAgYXdhaXQgYm90LmVxdWlwKGJ1Y2tldCwgImhhbmQiKTsNCg0KICAvLyBBY3RpdmF0ZSB0aGUgYnVja2V0IHRvIGNvbGxlY3Qgd2F0ZXINCiAgYXdhaXQgYm90LmFjdGl2YXRlSXRlbSgpOw0KICBib3QuY2hhdCgiRmlsbGVkIHRoZSBidWNrZXQgd2l0aCB3YXRlci4iKTsNCn0=)

[⬇](data:text/plain;base64,YXN5bmMgZnVuY3Rpb24gY2F0Y2hGaXZlRmlzaFNhZmVseShib3QpIHsNCiAgLy8gQ2hlY2sgaWYgdGhlIGJvdCBoYXMgYSBmaXNoaW5nIHJvZCBpbiBpdHMgaW52ZW50b3J5DQogIGxldCBmaXNoaW5nUm9kID0gYm90LmludmVudG9yeS5maW5kSW52ZW50b3J5SXRlbShtY0RhdGEuaXRlbXNCeU5hbWUuZmlzaGluZ19yb2QuaWQpOw0KICBpZiAoIWZpc2hpbmdSb2QpIHsNCiAgICBhd2FpdCBjcmFmdEZpc2hpbmdSb2QoYm90KTsNCiAgICBmaXNoaW5nUm9kID0gYm90LmludmVudG9yeS5maW5kSW52ZW50b3J5SXRlbShtY0RhdGEuaXRlbXNCeU5hbWUuZmlzaGluZ19yb2QuaWQpOw0KICB9DQoNCiAgLy8gRmluZCBhIG5lYXJieSB3YXRlciBibG9jaw0KICBsZXQgd2F0ZXJCbG9jazsNCiAgd2hpbGUgKCF3YXRlckJsb2NrKSB7DQogICAgd2F0ZXJCbG9jayA9IGF3YWl0IGV4cGxvcmVVbnRpbChib3QsIG5ldyBWZWMzKDEsIDAsIDEpLCA2MCwgKCkgPT4gew0KICAgICAgY29uc3QgZm91bmRXYXRlckJsb2NrID0gYm90LmZpbmRCbG9jayh7DQogICAgICAgIG1hdGNoaW5nOiBtY0RhdGEuYmxvY2tzQnlOYW1lLndhdGVyLmlkLA0KICAgICAgICBtYXhEaXN0YW5jZTogMzINCiAgICAgIH0pOw0KICAgICAgcmV0dXJuIGZvdW5kV2F0ZXJCbG9jazsNCiAgICB9KTsNCiAgICBpZiAoIXdhdGVyQmxvY2spIHsNCiAgICAgIGJvdC5jaGF0KCJObyBwYXRoIHRvIHRoZSB3YXRlciBibG9jay4gVHJ5aW5nIHRvIGZpbmQgYW5vdGhlciB3YXRlciBibG9jay4uLiIpOw0KICAgIH0NCiAgfQ0KDQogIC8vIE1vdmUgdG8gYSBibG9jayBhZGphY2VudCB0byB0aGUgd2F0ZXIgYmxvY2sNCiAgY29uc3QgYWRqYWNlbnRCbG9jayA9IHdhdGVyQmxvY2sucG9zaXRpb24ub2Zmc2V0KDAsIDEsIDApOw0KICBhd2FpdCBib3QucGF0aGZpbmRlci5nb3RvKG5ldyBHb2FsQmxvY2soYWRqYWNlbnRCbG9jay54LCBhZGphY2VudEJsb2NrLnksIGFkamFjZW50QmxvY2sueikpOw0KDQogIC8vIExvb2sgYXQgdGhlIHdhdGVyIGJsb2NrDQogIGF3YWl0IGJvdC5sb29rQXQod2F0ZXJCbG9jay5wb3NpdGlvbik7DQoNCiAgLy8gRXF1aXAgdGhlIGZpc2hpbmcgcm9kDQogIGF3YWl0IGJvdC5lcXVpcChmaXNoaW5nUm9kLCAiaGFuZCIpOw0KDQogIC8vIEZpc2ggaW4gdGhlIHdhdGVyIDUgdGltZXMNCiAgZm9yIChsZXQgaSA9IDA7IGkgPCA1OyBpKyspIHsNCiAgICB0cnkgew0KICAgICAgYXdhaXQgYm90LmZpc2goKTsNCiAgICAgIGJvdC5jaGF0KGBGaXNoICR7aSArIDF9IGNhdWdodC5gKTsNCiAgICB9IGNhdGNoIChlcnJvcikgew0KICAgICAgaWYgKGVycm9yLm1lc3NhZ2UgPT09ICJGaXNoaW5nIGNhbmNlbGxlZCIpIHsNCiAgICAgICAgYm90LmNoYXQoIkZpc2hpbmcgd2FzIGNhbmNlbGxlZC4gVHJ5aW5nIGFnYWluLi4uIik7DQogICAgICAgIGktLTsgLy8gUmV0cnkgdGhlIHNhbWUgaXRlcmF0aW9uDQogICAgICB9IGVsc2Ugew0KICAgICAgICB0aHJvdyBlcnJvcjsNCiAgICAgIH0NCiAgICB9DQogIH0NCn0=)

#### A.5.1 Components in the Prompt
The input prompt to GPT-4 consists of the following components:
1. 
(1) 

The agent’s state: We exclude other blocks that are recently seen and nearby entities from the agent’s state since they are not useful for assessing the task’s completeness. See Sec. [A.3.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS1) for each element of the agent’s state;


2. 
(2) 

Task proposed by the automatic curriculum;


3. 
(3) 

Task context: We prompt GPT-3.5 to ask for general suggestions about how to solve the task. In practice, this part is handled by the automatic curriculum since it has a systematic mechanism for question-answering (Sec. [A.3.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS2));


4. 
(4) 

Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] in response: We request GPT-4 to initially reason about the task’s success or failure, then output a boolean variable indicating the task’s outcome, and finally provide a critique to the agent if the task fails.


5. 
(5) 

Few-shot examples for in-context learning [[36](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib36), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37), [38](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib38)].


The agent’s state: We exclude other blocks that are recently seen and nearby entities from the agent’s state since they are not useful for assessing the task’s completeness. See Sec. [A.3.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS1) for each element of the agent’s state;
Task proposed by the automatic curriculum;
Task context: We prompt GPT-3.5 to ask for general suggestions about how to solve the task. In practice, this part is handled by the automatic curriculum since it has a systematic mechanism for question-answering (Sec. [A.3.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS3.SSS2));
Chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] in response: We request GPT-4 to initially reason about the task’s success or failure, then output a boolean variable indicating the task’s outcome, and finally provide a critique to the agent if the task fails.
Few-shot examples for in-context learning [[36](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib36), [37](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib37), [38](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib38)].

#### A.5.2 Full Prompt

[⬇](data:text/plain;base64,WW91IGFyZSBhbiBhc3Npc3RhbnQgdGhhdCBhc3Nlc3NlcyBteSBwcm9ncmVzcyBvZiBwbGF5aW5nIE1pbmVjcmFmdCBhbmQgcHJvdmlkZXMgdXNlZnVsIGd1aWRhbmNlLgoKWW91IGFyZSByZXF1aXJlZCB0byBldmFsdWF0ZSBpZiBJIGhhdmUgbWV0IHRoZSB0YXNrIHJlcXVpcmVtZW50cy4gRXhjZWVkaW5nIHRoZSB0YXNrIHJlcXVpcmVtZW50cyBpcyBhbHNvIGNvbnNpZGVyZWQgYSBzdWNjZXNzIHdoaWxlIGZhaWxpbmcgdG8gbWVldCB0aGVtIHJlcXVpcmVzIHlvdSB0byBwcm92aWRlIGNyaXRpcXVlIHRvIGhlbHAgbWUgaW1wcm92ZS4KCkkgd2lsbCBnaXZlIHlvdSB0aGUgZm9sbG93aW5nIGluZm9ybWF0aW9uOgoKQmlvbWU6IFRoZSBiaW9tZSBhZnRlciB0aGUgdGFzayBleGVjdXRpb24uClRpbWU6IFRoZSBjdXJyZW50IHRpbWUuCk5lYXJieSBibG9ja3M6IFRoZSBzdXJyb3VuZGluZyBibG9ja3MuIFRoZXNlIGJsb2NrcyBhcmUgbm90IGNvbGxlY3RlZCB5ZXQuIEhvd2V2ZXIsIHRoaXMgaXMgdXNlZnVsIGZvciBzb21lIHBsYWNpbmcgb3IgcGxhbnRpbmcgdGFza3MuCkhlYWx0aDogTXkgY3VycmVudCBoZWFsdGguCkh1bmdlcjogTXkgY3VycmVudCBodW5nZXIgbGV2ZWwuIEZvciBlYXRpbmcgdGFzaywgaWYgbXkgaHVuZ2VyIGxldmVsIGlzIDIwLjAsIHRoZW4gSSBzdWNjZXNzZnVsbHkgYXRlIHRoZSBmb29kLgpQb3NpdGlvbjogTXkgY3VycmVudCBwb3NpdGlvbi4KRXF1aXBtZW50OiBNeSBmaW5hbCBlcXVpcG1lbnQuIEZvciBjcmFmdGluZyB0YXNrcywgSSBzb21ldGltZXMgZXF1aXAgdGhlIGNyYWZ0ZWQgaXRlbS4KSW52ZW50b3J5ICh4eC8zNik6IE15IGZpbmFsIGludmVudG9yeS4gRm9yIG1pbmluZyBhbmQgc21lbHRpbmcgdGFza3MsIHlvdSBvbmx5IG5lZWQgdG8gY2hlY2sgaW52ZW50b3J5LgpDaGVzdHM6IElmIHRoZSB0YXNrIHJlcXVpcmVzIG1lIHRvIHBsYWNlIGl0ZW1zIGluIGEgY2hlc3QsIHlvdSBjYW4gZmluZCBjaGVzdCBpbmZvcm1hdGlvbiBoZXJlLgpUYXNrOiBUaGUgb2JqZWN0aXZlIEkgbmVlZCB0byBhY2NvbXBsaXNoLgpDb250ZXh0OiBUaGUgY29udGV4dCBvZiB0aGUgdGFzay4KCllvdSBzaG91bGQgb25seSByZXNwb25kIGluIEpTT04gZm9ybWF0IGFzIGRlc2NyaWJlZCBiZWxvdzoKewogICAgInJlYXNvbmluZyI6ICJyZWFzb25pbmciLAogICAgInN1Y2Nlc3MiOiBib29sZWFuLAogICAgImNyaXRpcXVlIjogImNyaXRpcXVlIiwKfQpFbnN1cmUgdGhlIHJlc3BvbnNlIGNhbiBiZSBwYXJzZWQgYnkgUHl0aG9uIGBqc29uLmxvYWRzYCwgZS5nLjogbm8gdHJhaWxpbmcgY29tbWFzLCBubyBzaW5nbGUgcXVvdGVzLCBldGMuCgpIZXJlIGFyZSBzb21lIGV4YW1wbGVzOgpJTlBVVDoKSW52ZW50b3J5ICgyLzM2KTogeydvYWtfbG9nJzoyLCAnc3BydWNlX2xvZyc6Mn0KClRhc2s6IE1pbmUgMyB3b29kIGxvZ3MKClJFU1BPTlNFOgp7CiAgICAicmVhc29uaW5nIjogIllvdSBuZWVkIHRvIG1pbmUgMyB3b29kIGxvZ3MuIFlvdSBoYXZlIDIgb2FrIGxvZ3MgYW5kIDIgc3BydWNlIGxvZ3MsIHdoaWNoIGFkZCB1cCB0byA0IHdvb2QgbG9ncy4iLAogICAgInN1Y2Nlc3MiOiB0cnVlLAogICAgImNyaXRpcXVlIjogIiIKfQoKSU5QVVQ6CkludmVudG9yeSAoMy8zNik6IHsnY3JhZnRpbmdfdGFibGUnOiAxLCAnc3BydWNlX3BsYW5rcyc6IDYsICdzdGljayc6IDR9CgpUYXNrOiBDcmFmdCBhIHdvb2RlbiBwaWNrYXhlCgpSRVNQT05TRToKewogICAgInJlYXNvbmluZyI6ICJZb3UgaGF2ZSBlbm91Z2ggbWF0ZXJpYWxzIHRvIGNyYWZ0IGEgd29vZGVuIHBpY2theGUsIGJ1dCB5b3UgZGlkbid0IGNyYWZ0IGl0LiIsCiAgICAic3VjY2VzcyI6IGZhbHNlLAogICAgImNyaXRpcXVlIjogIkNyYWZ0IGEgd29vZGVuIHBpY2theGUgd2l0aCBhIGNyYWZ0aW5nIHRhYmxlIHVzaW5nIDMgc3BydWNlIHBsYW5rcyBhbmQgMiBzdGlja3MuIgp9CgpJTlBVVDoKSW52ZW50b3J5ICgyLzM2KTogeydyYXdfaXJvbic6IDUsICdzdG9uZV9waWNrYXhlJzogMX0KClRhc2s6IE1pbmUgNSBpcm9uX29yZQoKUkVTUE9OU0U6CnsKICAgICJyZWFzb25pbmciOiAiTWluaW5nIGlyb25fb3JlIGluIE1pbmVjcmFmdCB3aWxsIGdldCByYXdfaXJvbi4gWW91IGhhdmUgNSByYXdfaXJvbiBpbiB5b3VyIGludmVudG9yeS4iLAogICAgInN1Y2Nlc3MiOiB0cnVlLAogICAgImNyaXRpcXVlIjogIiIKfQoKSU5QVVQ6CkJpb21lOiBwbGFpbnMKCk5lYXJieSBibG9ja3M6IHN0b25lLCBkaXJ0LCBncmFzc19ibG9jaywgZ3Jhc3MsIGZhcm1sYW5kLCB3aGVhdAoKSW52ZW50b3J5ICgyNi8zNik6IC4uLgoKVGFzazogIFBsYW50IDEgd2hlYXQgc2VlZC4KClJFU1BPTlNFOgp7CiAgICAicmVhc29uaW5nIjogIkZvciBwbGFudGluZyB0YXNrcywgaW52ZW50b3J5IGluZm9ybWF0aW9uIGlzIHVzZWxlc3MuIEluIG5lYXJieSBibG9ja3MsIHRoZXJlIGlzIGZhcm1sYW5kIGFuZCB3aGVhdCwgd2hpY2ggbWVhbnMgeW91IHN1Y2NlZWQgdG8gcGxhbnQgdGhlIHdoZWF0IHNlZWQuIiwKICAgICJzdWNjZXNzIjogdHJ1ZSwKICAgICJjcml0aXF1ZSI6ICIiCn0KCklOUFVUOgpJbnZlbnRvcnkgKDExLzM2KTogey4uLiAsJ3JvdHRlbl9mbGVzaCc6IDF9CgpUYXNrOiBLaWxsIDEgem9tYmllCgpDb250ZXh0OiAuLi4KClJFU1BPTlNFCnsKICAgICJyZWFzb25pbmciOiAiWW91IGhhdmUgcm90dGVuIGZsZXNoIGluIHlvdXIgaW52ZW50b3J5LCB3aGljaCBtZWFucyB5b3Ugc3VjY2Vzc2Z1bGx5IGtpbGxlZCBvbmUgem9tYmllLiIsCiAgICAic3VjY2VzcyI6IHRydWUsCiAgICAiY3JpdGlxdWUiOiAiIgp9CgpJTlBVVDoKSHVuZ2VyOiAyMC4wLzIwLjAKCkludmVudG9yeSAoMTEvMzYpOiAuLi4KClRhc2s6IEVhdCAxIC4uLgoKQ29udGV4dDogLi4uCgpSRVNQT05TRQp7CiAgICAicmVhc29uaW5nIjogIkZvciBhbGwgZWF0aW5nIHRhc2ssIGlmIHRoZSBwbGF5ZXIncyBodW5nZXIgaXMgMjAuMCwgdGhlbiB0aGUgcGxheWVyIHN1Y2Nlc3NmdWxseSBhdGUgdGhlIGZvb2QuIiwKICAgICJzdWNjZXNzIjogdHJ1ZSwKICAgICJjcml0aXF1ZSI6ICIiCn0KCklOUFVUOgpOZWFyYnkgYmxvY2tzOiBjaGVzdAoKSW52ZW50b3J5ICgyOC8zNik6IHsncmFpbCc6IDEsICdjb2FsJzogMiwgJ29ha19wbGFua3MnOiAxMywgJ2NvcHBlcl9ibG9jayc6IDEsICdkaW9yaXRlJzogNywgJ2Nvb2tlZF9iZWVmJzogNCwgJ2dyYW5pdGUnOiAyMiwgJ2NvYmJsZWRfZGVlcHNsYXRlJzogMjMsICdmZWF0aGVyJzogNCwgJ2xlYXRoZXInOiAyLCAnY29va2VkX2NoaWNrZW4nOiAzLCAnd2hpdGVfd29vbCc6IDIsICdzdGljayc6IDMsICdibGFja193b29sJzogMSwgJ3N0b25lX3N3b3JkJzogMiwgJ3N0b25lX2hvZSc6IDEsICdzdG9uZV9heGUnOiAyLCAnc3RvbmVfc2hvdmVsJzogMiwgJ2Nvb2tlZF9tdXR0b24nOiA0LCAnY29iYmxlc3RvbmVfd2FsbCc6IDE4LCAnY3JhZnRpbmdfdGFibGUnOiAxLCAnZnVybmFjZSc6IDEsICdpcm9uX3BpY2theGUnOiAxLCAnc3RvbmVfcGlja2F4ZSc6IDEsICdyYXdfY29wcGVyJzogMTJ9CgpDaGVzdHM6Cig4MSwgMTMxLCAxNik6IHsnYW5kZXNpdGUnOiAyLCAnZGlydCc6IDIsICdjb2JibGVzdG9uZSc6IDc1LCAnd29vZGVuX3BpY2theGUnOiAxLCAnd29vZGVuX3N3b3JkJzogMX0KClRhc2s6IERlcG9zaXQgdXNlbGVzcyBpdGVtcyBpbnRvIHRoZSBjaGVzdCBhdCAoODEsIDEzMSwgMTYpCgpDb250ZXh0OiAuLi4KClJFU1BPTlNFCnsKICAgICJyZWFzb25pbmciOiAiWW91IGhhdmUgMjggaXRlbXMgaW4geW91ciBpbnZlbnRvcnkgYWZ0ZXIgZGVwb3NpdGluZywgd2hpY2ggaXMgbW9yZSB0aGFuIDIwLiBZb3UgbmVlZCB0byBkZXBvc2l0IG1vcmUgaXRlbXMgZnJvbSB5b3VyIGludmVudG9yeSB0byB0aGUgY2hlc3QuIiwKICAgICJzdWNjZXNzIjogZmFsc2UsCiAgICAiY3JpdGlxdWUiOiAiRGVwb3NpdCBtb3JlIHVzZWxlc3MgaXRlbXMgc3VjaCBhcyBjb3BwZXJfYmxvY2ssIGRpb3JpdGUsIGdyYW5pdGUsIGNvYmJsZWRfZGVlcHNsYXRlLCBmZWF0aGVyLCBhbmQgbGVhdGhlciB0byBtZWV0IHRoZSByZXF1aXJlbWVudCBvZiBoYXZpbmcgb25seSAyMCBvY2N1cGllZCBzbG90cyBpbiB5b3VyIGludmVudG9yeS4iCn0=)

We make a system-level comparison in Table. [A.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.T2). Voyager stands out as the only method featuring a combination of automatic curriculum, iterative planning, and a skill library. Moreover, it learns to play Minecraft without the need for any gradient update.
[8](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib8)
[69](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib69)
[53](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib53)
[55](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib55)
[71](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib71)

### B.1 Experimental Setup
Our simulation environment is built upon MineDojo [[23](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib23)] and utilizes Mineflayer [[52](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib52)] JavaScript APIs for motor controls (Sec. [A.4.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A1.SS4.SSS2)). Additionally, we incorporate many bot.chat() into Mineflayer functions to provide abundant environment feedback and implement various condition checks along with try-catch exceptions for continuous execution. If the bot dies, it is resurrected near the closest ground, and its inventory is preserved for uninterrupted exploration. The bot recycles its crafting table and furnace after program execution. For detailed implementations, please refer to our codebase.

### B.2 Baselines
ReAct [[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)] uses chain-of-thought prompting [[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)] by generating both reasoning traces and action plans with LLMs. We provide it with our environment feedback and the agent states as observations. ReAct undergoes one round of code generation from scratch, followed by three rounds of code refinement. This process is then repeated until the maximum prompting iteration is reached.
Reflexion [[30](https://ar5iv.labs.arxiv.org/html/2305.16[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)1#bib.bib30)] is built on top of ReAct [29] with self-reflection to infer more intuitive future actions. We provide it with environment feedback, the agent states, execution errors, and our self-verification module. Similar to ReAct, Reflexion undergoes one round of code generation from scratch, followed by three rounds of code refinement. This process is then repeated until the maximum prompting iteration is reached.
AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)] is a popular software tool that automates NLP tasks by decomposing a high-level goal into multiple subgoals and executing them in a ReAct-style loop. We re-implement AutoGPT by using GPT-4 to do task decomposition and provide it with the agent states, environment feedback, and execution errors as observations for subgoal execution. Compared with Voyager, AutoGPT lacks the skill library for accumulating knowledge, self-verification for assessing task success, and automatic curriculum for open-ended exploration. During each subgoal execution, if no execution error occurs, we consider the subgoal completed and proceed to the next one. Otherwise, we refine the program until three rounds of code refinement (equivalent to four rounds of code generation) are completed, and then move on to the next subgoal. If three consecutive subgoals do not result in acquiring a new item, we replan by rerunning the task decomposition.
The task is “explore the world and get as many items as possible” for all baselines.
[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)
[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)
[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)
[46](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib46)

We ablate 6 design choices (automatic curriculum, skill library, environment feedback, execution errors, self-verification, and GPT-4 for code generation) in Voyager and study their impact on exploration performance.
- 
• 

Manual Curriculum: We substitute the automatic curriculum with a manually designed curriculum for mining a diamond: “Mine 3 wood log”, “Craft 1 crafting table”, “Craft 1 wooden pickaxe”, “Mine 11 cobblestone”, “Craft 1 stone pickaxe”, “Craft 1 furnace”, “Mine 3 iron ore”, “Smelt 3 iron ore”, “Craft 1 iron pickaxe”, “Mine 1 diamond”. A manual curriculum requires human effort to design and is not scalable for open-ended exploration.


- 
• 

Random Curriculum: We curate 101 items obtained by Voyager and create a random curriculum by randomly selecting one item as the next task.


- 
• 

w/o Skill Library: We remove the skill library, eliminating skill retrieval for code generation.


- 
• 

w/o Environment Feedback: We exclude environment feedback (chat log) from the prompt for code generation.


- 
• 

w/o Execution Errors: We exclude execution errors from the prompt for code generation.


- 
• 

w/o Self-Verification: For each task, we generate code without self-verification and iteratively refine the program for 3 rounds (equivalent to 4 rounds of code generation in total).


- 
• 

GPT-3.5: We replace GPT-4 with GPT-3.5 for code generation. We retain GPT-4 for the automatic curriculum and the self-verification module.


Manual Curriculum: We substitute the automatic curriculum with a manually designed curriculum for mining a diamond: “Mine 3 wood log”, “Craft 1 crafting table”, “Craft 1 wooden pickaxe”, “Mine 11 cobblestone”, “Craft 1 stone pickaxe”, “Craft 1 furnace”, “Mine 3 iron ore”, “Smelt 3 iron ore”, “Craft 1 iron pickaxe”, “Mine 1 diamond”. A manual curriculum requires human effort to design and is not scalable for open-ended exploration.
Random Curriculum: We curate 101 items obtained by Voyager and create a random curriculum by randomly selecting one item as the next task.
w/o Skill Library: We remove the skill library, eliminating skill retrieval for code generation.
w/o Environment Feedback: We exclude environment feedback (chat log) from the prompt for code generation.
w/o Execution Errors: We exclude execution errors from the prompt for code generation.
w/o Self-Verification: For each task, we generate code without self-verification and iteratively refine the program for 3 rounds (equivalent to 4 rounds of code generation in total).
GPT-3.5: We replace GPT-4 with GPT-3.5 for code generation. We retain GPT-4 for the automatic curriculum and the self-verification module.

#### B.4.1 Significantly Better Exploration
The meaning of each icon in Fig. [1](https://ar5iv.labs.arxiv.org/html/2305.16291#S0.F1) is shown in Fig. [A.1](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.F1).
We run three trials for each method. The items collected by Voyager in each trial is
- 
• 

Trial 1: ‘iron_ingot’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘pufferfish’, ‘oak_log’, ‘cooked_mutton’, ‘green_dye’, ‘flint’, ‘chest’, ‘iron_sword’, ‘string’, ‘ender_pearl’, ‘raw_copper’, ‘crafting_table’, ‘cactus’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘copper_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘scaffolding’, ‘stick’, ‘porkchop’, ‘copper_block’, ‘gravel’, ‘grass_block’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘oak_sapling’, ‘coal’, ‘bamboo’, ‘wooden_pickaxe’, ‘rotten_flesh’, ‘cooked_porkchop’, ‘cod’, ‘iron_boots’, ‘lightning_rod’, ‘diorite’, ‘water_bucket’, ‘shears’, ‘furnace’, ‘andesite’, ‘granite’, ‘bucket’, ‘wooden_sword’, ‘sandstone’, ‘iron_helmet’, ‘raw_iron’, ‘sand’, ‘acacia_log’, ‘cooked_cod’, ‘oak_planks’, ‘azure_bluet’, ‘iron_shovel’, ‘acacia_planks’, ‘shield’, ‘iron_axe’, ‘iron_chestplate’, ‘cobblestone’;


- 
• 

Trial 2: ‘iron_ingot’, ‘tuff’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘cooked_mutton’, ‘spruce_planks’, ‘gunpowder’, ‘amethyst_shard’, ‘chest’, ‘string’, ‘cooked_salmon’, ‘iron_sword’, ‘raw_copper’, ‘crafting_table’, ‘torch’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘copper_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘stick’, ‘amethyst_block’, ‘salmon’, ‘calcite’, ‘gravel’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘spyglass’, ‘coal’, ‘wooden_pickaxe’, ‘cod’, ‘iron_boots’, ‘lily_pad’, ‘cobbled_deepslate’, ‘lightning_rod’, ‘snowball’, ‘stone_axe’, ‘smooth_basalt’, ‘diorite’, ‘water_bucket’, ‘furnace’, ‘andesite’, ‘bucket’, ‘granite’, ‘shield’, ‘iron_helmet’, ‘raw_iron’, ‘cobblestone’, ‘spruce_log’, ‘cooked_cod’, ‘tripwire_hook’, ‘stone_hoe’, ‘iron_chestplate’, ‘stone_sword’;


- 
• 

Trial 3: ‘spruce_planks’, ‘dirt’, ‘shield’, ‘redstone’, ‘clock’, ‘diamond_sword’, ‘iron_chestplate’, ‘stone_pickaxe’, ‘leather’, ‘string’, ‘chicken’, ‘chest’, ‘diorite’, ‘iron_leggings’, ‘black_wool’, ‘cobblestone_wall’, ‘cobblestone’, ‘cooked_chicken’, ‘feather’, ‘stone_sword’, ‘raw_gold’, ‘gravel’, ‘birch_planks’, ‘coal’, ‘cobbled_deepslate’, ‘oak_planks’, ‘iron_pickaxe’, ‘granite’, ‘tuff’, ‘crafting_table’, ‘iron_helmet’, ‘stone_hoe’, ‘iron_ingot’, ‘stone_axe’, ‘birch_boat’, ‘stick’, ‘sand’, ‘bone’, ‘raw_iron’, ‘beef’, ‘rail’, ‘oak_sapling’, ‘kelp’, ‘gold_ingot’, ‘birch_log’, ‘wheat_seeds’, ‘cooked_mutton’, ‘furnace’, ‘arrow’, ‘stone_shovel’, ‘white_wool’, ‘andesite’, ‘jungle_slab’, ‘mutton’, ‘iron_sword’, ‘copper_ingot’, ‘diamond’, ‘torch’, ‘oak_log’, ‘cooked_beef’, ‘copper_block’, ‘flint’, ‘bone_meal’, ‘raw_copper’, ‘wooden_pickaxe’, ‘iron_boots’, ‘wooden_sword’.

Trial 1: ‘iron_ingot’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘pufferfish’, ‘oak_log’, ‘cooked_mutton’, ‘green_dye’, ‘flint’, ‘chest’, ‘iron_sword’, ‘string’, ‘ender_pearl’, ‘raw_copper’, ‘crafting_table’, ‘cactus’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘copper_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘scaffolding’, ‘stick’, ‘porkchop’, ‘copper_block’, ‘gravel’, ‘grass_block’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘oak_sapling’, ‘coal’, ‘bamboo’, ‘wooden_pickaxe’, ‘rotten_flesh’, ‘cooked_porkchop’, ‘cod’, ‘iron_boots’, ‘lightning_rod’, ‘diorite’, ‘water_bucket’, ‘shears’, ‘furnace’, ‘andesite’, ‘granite’, ‘bucket’, ‘wooden_sword’, ‘sandstone’, ‘iron_helmet’, ‘raw_iron’, ‘sand’, ‘acacia_log’, ‘cooked_cod’, ‘oak_planks’, ‘azure_bluet’, ‘iron_shovel’, ‘acacia_planks’, ‘shield’, ‘iron_axe’, ‘iron_chestplate’, ‘cobblestone’;
Trial 2: ‘iron_ingot’, ‘tuff’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘cooked_mutton’, ‘spruce_planks’, ‘gunpowder’, ‘amethyst_shard’, ‘chest’, ‘string’, ‘cooked_salmon’, ‘iron_sword’, ‘raw_copper’, ‘crafting_table’, ‘torch’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘copper_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘stick’, ‘amethyst_block’, ‘salmon’, ‘calcite’, ‘gravel’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘spyglass’, ‘coal’, ‘wooden_pickaxe’, ‘cod’, ‘iron_boots’, ‘lily_pad’, ‘cobbled_deepslate’, ‘lightning_rod’, ‘snowball’, ‘stone_axe’, ‘smooth_basalt’, ‘diorite’, ‘water_bucket’, ‘furnace’, ‘andesite’, ‘bucket’, ‘granite’, ‘shield’, ‘iron_helmet’, ‘raw_iron’, ‘cobblestone’, ‘spruce_log’, ‘cooked_cod’, ‘tripwire_hook’, ‘stone_hoe’, ‘iron_chestplate’, ‘stone_sword’;
Trial 3: ‘spruce_planks’, ‘dirt’, ‘shield’, ‘redstone’, ‘clock’, ‘diamond_sword’, ‘iron_chestplate’, ‘stone_pickaxe’, ‘leather’, ‘string’, ‘chicken’, ‘chest’, ‘diorite’, ‘iron_leggings’, ‘black_wool’, ‘cobblestone_wall’, ‘cobblestone’, ‘cooked_chicken’, ‘feather’, ‘stone_sword’, ‘raw_gold’, ‘gravel’, ‘birch_planks’, ‘coal’, ‘cobbled_deepslate’, ‘oak_planks’, ‘iron_pickaxe’, ‘granite’, ‘tuff’, ‘crafting_table’, ‘iron_helmet’, ‘stone_hoe’, ‘iron_ingot’, ‘stone_axe’, ‘birch_boat’, ‘stick’, ‘sand’, ‘bone’, ‘raw_iron’, ‘beef’, ‘rail’, ‘oak_sapling’, ‘kelp’, ‘gold_ingot’, ‘birch_log’, ‘wheat_seeds’, ‘cooked_mutton’, ‘furnace’, ‘arrow’, ‘stone_shovel’, ‘white_wool’, ‘andesite’, ‘jungle_slab’, ‘mutton’, ‘iron_sword’, ‘copper_ingot’, ‘diamond’, ‘torch’, ‘oak_log’, ‘cooked_beef’, ‘copper_block’, ‘flint’, ‘bone_meal’, ‘raw_copper’, ‘wooden_pickaxe’, ‘iron_boots’, ‘wooden_sword’.
The items collected by ReAct [[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)] in each trial is
- 
• 

Trial 1: ‘bamboo’, ‘dirt’, ‘sand’, ‘wheat_seeds’;


- 
• 

Trial 2: ‘dirt’, ‘rabbit’, ‘spruce_log’, ‘spruce_sapling’;


- 
• 

Trial 3: ‘dirt’, ‘pointed_dripstone’;


Trial 1: ‘bamboo’, ‘dirt’, ‘sand’, ‘wheat_seeds’;
Trial 2: ‘dirt’, ‘rabbit’, ‘spruce_log’, ‘spruce_sapling’;
Trial 3: ‘dirt’, ‘pointed_dripstone’;
The items collected by Reflexion [[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)] in each trial is
- 
• 

Trial 1: ‘crafting_table’, ‘orange_tulip’, ‘oak_planks’, ‘oak_log’, ‘dirt’;


- 
• 

Trial 2: ‘spruce_log’, ‘dirt’, ‘clay_ball’, ‘sand’, ‘gravel’;


- 
• 

Trial 3: ‘wheat_seeds’, ‘oak_log’, ‘dirt’, ‘birch_log’, ‘sand’.


Trial 1: ‘crafting_table’, ‘orange_tulip’, ‘oak_planks’, ‘oak_log’, ‘dirt’;
Trial 2: ‘spruce_log’, ‘dirt’, ‘clay_ball’, ‘sand’, ‘gravel’;
Trial 3: ‘wheat_seeds’, ‘oak_log’, ‘dirt’, ‘birch_log’, ‘sand’.

The items collected by AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)] in each trial is
- 
• 

Trial 1: ‘feather’, ‘oak_log’, ‘leather’, ‘stick’, ‘porkchop’, ‘chicken’, ‘crafting_table’, ‘wheat_seeds’, ‘oak_planks’, ‘dirt’, ‘mutton’;


- 
• 

Trial 2: ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘coal’, ‘spruce_planks’, ‘string’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘andesite’, ‘furnace’, ‘torch’, ‘spruce_sapling’, ‘granite’, ‘iron_pickaxe’, ‘stone_pickaxe’, ‘wooden_axe’, ‘raw_iron’, ‘stick’, ‘spruce_log’, ‘dirt’, ‘cobblestone’;


- 
• 

Trial 3: ‘wooden_shovel’, ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘cod’, ‘coal’, ‘oak_log’, ‘flint’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘furnace’, ‘andesite’, ‘torch’, ‘granite’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘stone_pickaxe’, ‘raw_iron’, ‘stick’, ‘gravel’, ‘oak_planks’, ‘dirt’, ‘iron_axe’, ‘cobblestone’.


Trial 1: ‘feather’, ‘oak_log’, ‘leather’, ‘stick’, ‘porkchop’, ‘chicken’, ‘crafting_table’, ‘wheat_seeds’, ‘oak_planks’, ‘dirt’, ‘mutton’;
Trial 2: ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘coal’, ‘spruce_planks’, ‘string’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘andesite’, ‘furnace’, ‘torch’, ‘spruce_sapling’, ‘granite’, ‘iron_pickaxe’, ‘stone_pickaxe’, ‘wooden_axe’, ‘raw_iron’, ‘stick’, ‘spruce_log’, ‘dirt’, ‘cobblestone’;
Trial 3: ‘wooden_shovel’, ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘cod’, ‘coal’, ‘oak_log’, ‘flint’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘furnace’, ‘andesite’, ‘torch’, ‘granite’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘stone_pickaxe’, ‘raw_iron’, ‘stick’, ‘gravel’, ‘oak_planks’, ‘dirt’, ‘iron_axe’, ‘cobblestone’.

#### B.4.2 Extensive Map Traversal
Agent trajectories for map coverage are displayed in Fig. [[A.2](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.F2)](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.F2). Fig. [7](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F7) is plotted based on Fig. A.2 by drawing the smallest circle enclosing each trajectory. The terrains traversed by Voyager in each trial is
- 
• 

Trial 1: ‘meadow’, ‘desert’, ‘river’, ‘savanna’, ‘forest’, ‘plains’, ‘bamboo_jungle’, ‘dripstone_caves’;


- 
• 

Trial 2: ‘snowy_plains’, ‘frozen_river’, ‘dripstone_caves’, ‘snowy_taiga’, ‘beach’;


- 
• 

Trial 3: ‘flower_forest’, ‘meadow’, ‘old_growth_birch_forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘forest’, ‘river’, ‘beach’, ‘ocean’, ‘sunflower_plains’, ‘plains’, ‘stony_shore’.


Trial 1: ‘meadow’, ‘desert’, ‘river’, ‘savanna’, ‘forest’, ‘plains’, ‘bamboo_jungle’, ‘dripstone_caves’;
Trial 2: ‘snowy_plains’, ‘frozen_river’, ‘dripstone_caves’, ‘snowy_taiga’, ‘beach’;
Trial 3: ‘flower_forest’, ‘meadow’, ‘old_growth_birch_forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘forest’, ‘river’, ‘beach’, ‘ocean’, ‘sunflower_plains’, ‘plains’, ‘stony_shore’.
The terrains traversed by ReAct [[29](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib29)] in each trial is
- 
• 

Trial 1: ‘plains’, ‘desert’, ‘jungle’;


- 
• 

Trial 2: ‘snowy_plains’, ‘snowy_taiga’, ‘snowy_slopes’;


- 
• 

Trial 3: ‘dark_forest’, ‘dripstone_caves’, ‘grove’, ‘jagged_peaks’.


Trial 1: ‘plains’, ‘desert’, ‘jungle’;
Trial 2: ‘snowy_plains’, ‘snowy_taiga’, ‘snowy_slopes’;
Trial 3: ‘dark_forest’, ‘dripstone_caves’, ‘grove’, ‘jagged_peaks’.
The terrains traversed by Reflexion [[30](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib30)] in each trial is
- 
• 

Trial 1: ‘plains’, ‘flower_forest’;


- 
• 

Trial 2: ‘snowy_taiga’;


- 
• 

Trial 3: ‘old_growth_birch_forest’, ‘river’, ‘ocean’, ‘beach’, ‘plains’.


Trial 1: ‘plains’, ‘flower_forest’;
Trial 2: ‘snowy_taiga’;

Trial 3: ‘old_growth_birch_forest’, ‘river’, ‘ocean’, ‘beach’, ‘plains’.
The terrains traversed by AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)] in each trial is
- 
• 

Trial 1: ‘plains’, ‘dripstone_caves’, ‘savanna’, ‘meadow’;


- 
• 

Trial 2: ‘snowy_taiga’;


- 
• 

Trial 3: ‘plains’, ‘stony_shore’, ‘forest’, ‘ocean’.


Trial 1: ‘plains’, ‘dripstone_caves’, ‘savanna’, ‘meadow’;
Trial 2: ‘snowy_taiga’;
Trial 3: ‘plains’, ‘stony_shore’, ‘forest’, ‘ocean’.

#### B.4.3 Efficient Zero-Shot Generalization to Unseen Tasks
The results of zero-shot generalization to unseen tasks for the other two tasks are presented in Fig. [A.3](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.F3). Similar to Fig. [8](https://ar5iv.labs.arxiv.org/html/2305.16291#S3.F8), Voyager consistently solves all tasks, while the baselines are unable to solve any task within 50 prompting iterations. Our skill library, constructed from lifelong learning, not only enhances Voyager’s performance but also provides a boost to AutoGPT [[28](https://ar5iv.labs.arxiv.org/html/2305.16291#bib.bib28)].

#### B.4.4 Accurate Skill Retrieval
We conduct an evaluation of our skill retrieval (309 samples in total) and the results are in Table. [A.4](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.T4). The top-5 accuracy standing at 96.5% suggests our retrieval process is reliable (note that we include the top-5 relevant skills in the prompt for synthesizing a new skill).

#### B.4.5 Robust to Model Variations
In the main paper, all of Voyager’s experiments are conducted with gpt-4-0314. We additionally run new experiments with gpt-4-0613 and find that the performance is roughly the same (Fig. [A.4](https://ar5iv.labs.arxiv.org/html/2305.16291#A2.F4)). It demonstrates that Voyager is robust to model variations.
[◄](https://ar5iv.labs.arxiv.org/html/2305.16290)
[Feelinglucky?](https://ar5iv.labs.arxiv.org/feeling_lucky)
[Conversionreport](https://ar5iv.labs.arxiv.org/log/2305.16291)
[Reportan issue](https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+2305.16291)
[View originalon arXiv](https://arxiv.org/abs/2305.16291)
[►](https://ar5iv.labs.arxiv.org/html/2305.16292)
[Copyright](https://arxiv.org/help/license)
[Privacy Policy](https://arxiv.org/help/policies/privacy_policy)
[LaTeXML](http://dlmf.nist.gov/LaTeXML/)

