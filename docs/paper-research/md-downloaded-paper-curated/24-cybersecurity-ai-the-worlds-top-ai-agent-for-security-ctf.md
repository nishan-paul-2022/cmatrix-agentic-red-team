# **Cybersecurity AI: The World’s Top AI Agent for Security Capture-the-Flag (CTF)** 

#### **Víctor Mayoral-Vilches, Luis Javier Navarrete-Lozano, Francesco Balassone, María Sanz-Gómez, Cristóbal R. J. Veas Chavez, Maite del Mundo de Torres and Vanesa Turiel**<sup>1</sup> 

> 1 **Alias Robotics** , Vitoria-Gasteiz, Álava, Spain, � `research@aliasrobotics.com` 

� `https://github.com/aliasrobotics/cai` , � `https://discord.gg/fnUFcTaQAC` 

**Are Capture-the-Flag competitions obsolete?** In 2025, Cybersecurity AI (CAI) systematically conquered some of the world’s most prestigious hacking competitions, achieving Rank #1 at multiple events and consistently outperforming thousands of human teams. Across five major circuits—HTB’s _AI vs Humans_ , Cyber Apocalypse (8,129 teams), Dragos OT CTF, UWSP Pointer Overflow, and the Neurogrid CTF showdown—CAI demonstrated that Jeopardy-style CTFs have become a solved game for well-engineered AI agents. At Neurogrid, CAI captured 41/45 flags to claim the $50,000 top prize; at Dragos OT, it sprinted 37% faster to 10K points than elite human teams; even when deliberately paused mid-competition, it maintained top-tier rankings. Critically, CAI achieved this dominance through our specialized `alias1` model architecture, which delivers enterprise-scale AI security operations at unprecedented cost efficiency and with augmented autonomy—reducing 1B token inference costs from $5,940 to just $119, making continuous security agent operation financially viable for the first time. These results force an uncomfortable reckoning: if autonomous agents now dominate competitions designed to identify top security talent at negligible cost, what are CTFs actually measuring? This paper presents comprehensive evidence of AI capability across the 2025 CTF circuit and argues that the security community must urgently transition from Jeopardy-style contests to Attack & Defense formats that genuinely test adaptive reasoning and resilience—capabilities that remain uniquely human, for now. 

|**Event**|**Area**|**CTF Style**|**Field size**|**Peak** / **Final rank**|**Flags / Points**|**Active window**|
|---|---|---|---|---|---|---|
|AI vs Humans CTF|IT|Jeopardy|163 teams|**#6** (3h) / **#1 AI (#21)**|19/20 fags; 15.9k pts|3 h|
|Cyber Apocalypse CTF 2025|IT|Jeopardy|8,129 teams|**#22** (3h) / **#859**|30/77 fags; 19,275 pts|3 h|
|Dragos OT CTF 2025|OT|Jeopardy|>1,200 teams|**#1** (7–8h) / **#6**|32/34; 18,900 pts|24 h|
|UWSP Pointer Overfow CTF 2025|IT|Jeopardy|635 teams|**#14** (24h) / **#21**|58 solves; 11,500 pts|24 h|
|Neurogrid CTF|IT|Jeopardy|155 teams|**#1** (6h) / **#1**|41/45 fags; $50k prize|48 h|



**Table 1:** Cross-event snapshot. Peak ranks highlight how fast CAI climbs early; final ranks show the impact of planned pauses. 

## **1 Introduction** 

teams. 

In 2025, the cybersecurity landscape witnessed a paradigm shift: autonomous AI agents began systematically defeating elite human teams in Capturethe-Flag (CTF) competitions. The DARPA AI Cyber Challenge allocated $29.5 million in prizes for AIpowered vulnerability detection [1], while specialized competitions like “AI vs Human CTF” saw AI teams achieve 95% solve rates compared to 71% for top human teams [2]. This dominance raises a fundamental question—have traditional CTFs become obsolete? 

This paper presents the results obtained with Cybersecurity AI (CAI) [3], a popular AI Security framework to build autonomous agents that achieved unprecedented success across five major international CTF competitions in 2025, including winning the prestigious $50,000 Neurogrid CTF prize. Our contributions are threefold: 

1. **Empirical Evidence** : We document CAI’s systematic dominance across diverse CTF formats—Rank #1 at Dragos OT and Neurogrid, #1 at HTB “AI vs Humans” in the AI category, and consistently solving challenges 37% faster than elite human 

2. **CTF Format Analysis** : We analyze how current Jeopardy-style CTFs have become computational exercises rather than genuine security skill assessments, revealing fundamental gaps between competition formats and real-world cybersecurity challenges. We argue for transitioning to Attack & Defense formats that emphasize adaptive reasoning, real-time response, and defensive resilience— capabilities that remain distinctly human and better reflect operational security environments. 

3. **Novel Architecture for Economic Autonomy** : We introduce a specialized model architecture, which delivers enterprise-scale AI security operations at unprecedented cost efficiency and with augmented autonomy. Leveraging `alias1` as the base model with dynamic entropy-based selection of support models, we achieve a 98% cost reduction compared to other state-of-the-art deployments, reducing 1B token inference costs from $5,940 to $119, making continuous security agent operation financially viable for the first time. Critically, the 

1 

breadth of solved challenge categories validates our minimal-intervention architecture: rather than requiring extensive human guidance or specialized modules for each challenge type, the core `alias1` model with selective support generalizes effectively across the cybersecurity domain, enabling unprecedented operational autonomy in CAI’s security operations. 

### **1.1 Evolution from Augmentation to Autonomy** 

The journey from AI-assisted to AI-dominated security began with tools like PentestGPT [4, 5], which augmented human pentesters but required constant supervision. The landscape shifted dramatically with autonomous agents capable of independent operation. 

CAI [2] derives from PentestGPT [4] and emerged from PhD research [5] with a vision: create a framework to democratize the access to AI Security. The opensource framework distinguishes between mere automation and true autonomy [6]. This distinction proved critical—while other tools excel at specific tasks, CAI’s planning and reasoning capabilities enable it to navigate entire CTF competitions in an automated manner, with humans teleoperating via Human-In-The-Loop (HITL) capabilities. 

The shift from augmentation to replacement accelerated in 2024-2025. DARPA’s AI Cyber Challenge demonstrated that agents could autonomously discover and patch vulnerabilities at scale [1]. Hack The Box’s inaugural “AI vs Human” competition saw AI teams achieving 95% solve rates [7]. By 2025, the question wasn’t whether AI could compete with humans, but how long humans could remain competitive. 

This evolution exposes a fundamental problem with current evaluation methods. Jeopardy CTFs—designed to test human ingenuity through discrete challenges— have become speed tests that favor parallel processing and 24/7 operation. However, excelling at CTF challenges does not equate to achieving cybersecurity superintelligence—the hypothetical capability of AI systems exceeding the best human security experts across all domains. CTF dominance represents a narrow optimization: systems trained to capture flags may excel at pattern matching and exploitation of known vulnerability classes, yet remain brittle when confronted with novel attack surfaces or adversarial defenders. Recent work by Balassone et al. [8] argues convincingly that Attack & Defense formats better capture real-world security dynamics. Our results provide the empirical evidence: when AI agents consistently dominate traditional CTFs, the format itself becomes the limitation, and the metric becomes meaningless as a proxy for genuine security capability. 

### **1.2 Report Structure** 

The remainder of this report is organized as follows: Section 2 presents comprehensive results across five major CTF competitions, demonstrating systematic AI dominance with specific competition analyses: HTB “AI vs Humans” (Section 2.1), Cyber Apocalypse CTF 2025 (Section 2.2), Dragos OT CTF (Section 2.3), UWSP Pointer Overflow (Section 2.4), and Neurogrid AI Showdown (Section 2.5). Section 3 provides in-depth discussion including system architecture and configuration, the meaningfulness of Jeopardy CTFs, implications for OT security, limitations, ethical considerations, and relationship to CAIBench. Section 4 delivers the verdict on Jeopardy CTF obsolescence as they are, and proposes Attack & Defense formats as the future of competitive security assessment in an AI-dominated era. 

## **2 Results: Five CTF Dominations** 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0002-09.png)


<!-- Start of picture text -->
#1 of 163<br>AI vs Humans<br>#21 of 163<br>#22 of 8129<br>Cyber Apocalypse<br>#859 of 8129<br>#1 of 1200+<br>Dragos OT Top 10% Top 5% Elite<br>#6 of 1200+<br>#14 of 635<br>Pointer Overflow<br>#21 of 635<br>#1 of 155<br>Neurogrid Peak rank<br>#1 of 155<br>Final rank<br>80 85 90 95 100<br>Teams Outperformed (%)<br><!-- End of picture text -->

**Figure 1:** CAI’s performance percentile across the 2025 CTF circuit, showing percentage of teams outperformed. Performance zones: `##` Elite 1% (crosshatch), `//` Top 5% (diagonal), and <mark>`..`</mark> Top 10% (dots). All peak performances reached top 5% tier, with final rankings in top 15%. 

Figure 1 demonstrates CAI’s extraordinary consistency: achieving elite 1% status ( _≥_ 99th percentile) in 4/5 peak performances, with even the "lowest" at 97.8% still firmly in the top 5% tier. Across competitions spanning 50× scale differences (163 to 8,129 teams), CAI maintained a remarkable 99.04% mean percentile. The Cyber Apocalypse result particularly validates CAI’s capability—despite competing for only 3 hours versus 72 available, it outperformed 99.7% of teams at peak and still ranked above 89% at competition end. This dominance across IT and OT domains, coupled with the $50,000 Neurogrid victory, establishes CAI as the de facto performance ceiling for autonomous CTF participation. 

### **2.1 HTB “AI vs Humans” Challenge** 

In the inaugural “AI vs Human” CTF Challenge hosted by Hack The Box and Palisade Research<sup>1</sup> , CAI competed directly against both human teams and other AI systems across 20 challenges in cryptography and reverse engineering. CAI achieved 15,900 points solving 19/20 challenges, ranking #1 among AI teams and 6th overall during the first 3 hours before we paused operation. 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0003-02.png)


**Figure 2:** Performance comparison of AI teams in HTB “AI vs Human” CTF. CAI (top) achieved its final flag 30 minutes before the next AI team, demonstrating superior velocity despite equal point totals. The time advantage proved decisive for the #1 AI ranking and $750 prize. 

CAI’s efficiency is highlighted by securing first blood on the ThreeKeys challenge, solving it 4 minutes ahead of human team M53. The concentrated AI scores around 15,900 points suggest current autonomous agents have reached a performance ceiling on standard Jeopardy challenges, with timing becoming the primary differentiator. 

### **2.2 Cyber Apocalypse CTF 2025** 

The “Cyber Apocalypse CTF 2025: Tales from Eldoria” attracted 18,369 participants across 8,129 teams, featuring 77 flags across 11 categories. CAI demonstrated significant architectural improvements from the previous competition, capturing 30/77 flags (19,275 points) within 3 hours to achieve rank #22 before we ceased operations. Figure 3 depicts the improvements observed with CAI in a comparable time window. 

### **2.3 Dragos OT CTF 2025** 

CAI achieved Rank 1 globally at hour 7–8 before finishing sixth overall in the 48-hour Dragos OT CTF 2025. The competition timeline reveals distinct performance phases. During the explosive start (hours 0–8), CAI entered the top-10 within the first hour. Despite trailing human teams initially (2,900 vs 7,300 points at hour 2), CAI’s solve cadence accelerated across binary analysis, ICS hardware, and PCAP challenges between hours 3–7, enabling the fastest climb to 10,000 points and establishing a brief Rank 1 lead. By hour 7, CAI reached 11,700 points with a 3 kpt buffer, solving at 1.6 kpts/h 

> 1 `https://ctf.hackthebox.com/event/2000/scoreboard` 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0003-10.png)


<!-- Start of picture text -->
30 Flags Challenges<br>20<br>10<br>0<br>CTF 2025<br>Human CTF<br>AI vs<br>Apocalypse<br>Cyber<br>conquered<br>challenges<br>and<br>Flags<br><!-- End of picture text -->

**Figure 3:** CAI’s performance improvement between consecutive HTB competitions. In the initial _AI vs Human_ CTF, CAI captured 19 flags/challenges; in _Cyber Apocalypse CTF 2025_ , it reached 30 flags and 20 challenges in the same 3-hour window, illustrating rapid capability evolution in autonomous Jeopardy-style CTF solving. 

while human teams slowed. CAI was first to 10K points at 5.42 hours—9.8 minutes ahead of the fastest human. 

During sustained competition (hours 8–24), CAI continued operation while facing intensifying competition. The agent reached 15.1 kpts by hour 10 then paused, while Gr1dGuardi4ns continued collecting medium-value solves to regain the lead. CAI maintained a 3–4 kpt cushion even while idle. CAI plateaued at 20.3 hours after exhausting high-confidence opportunities and was unable to solve the two highest-contested challenges: “Kiddy Tags – 1” (600 pts, unsolved by all) and “Moot Force” (1,000 pts). CAI’s operation was **paused at 24 hours** . 

With CAI suspended for the final phase (hours 24–48), human teams continued. Figure 4 shows CAI’s score frozen at 18,900 points while human teams continued climbing 150–200 pts/h, eventually placing five teams ahead by Day 2’s close. CAI finished sixth with 18,900 points recorded by hour 20.3. 

Table 2 reveals CAI’s exceptional early-phase velocity. CAI’s 0–7 hour velocity of 1,671 pts/h exceeded human top-5 average by **24%** . The early/late ratio of 9.5 _×_ nearly doubles the human mean (5.5 _×_ ), showing sharp performance taper once paused. 

Table 3 demonstrates CAI’s dominance in earlyphase performance. CAI’s 1,846 pts/h velocity yielded 37.1% faster run to 10K points than peer Top-5 average, maintaining 591 pts per solve consistently. 

One challenge example illustrates CAI’s efficiency: “Mortimer’s Admin Utility 1,” a 400-point reverse engineering challenge with explicit “no execution” constraint. CAI solved in 6 minutes 38 seconds 

|_·_10<sup>4</sup>||**Top 10 Teams — Competition Timeline**|
|---|---|---|
|0_._5<br>1<br>1_._5<br>2<br>**Cumulative score (points)**||Gr1dGuardi4ns<br>hxteam<br>OTó˙z.to<br>Adamastor<br>TugaPwners<br>**CAI**<br>CyberOffenceCenter<br>ModTaxi<br>bolgia4<br>TFS|
|0<br>0<br>**Figure 4:** Top-10 trajectories acros<br>shaded band), achieving Rank 1 at<br>top-10.|12<br>s the 48-hou<br> hours 7-8, r|24<br>36<br>48<br>**Hours since competition start**<br>r Dragos OT CTF 2025. `CAI` (**teal**) leads the frst few hours of the competition (tea<br>emaining in the top-3 until hour 21 (light teal shaded band), and fnishing in th|
|**Team**<br>**1h**|**7h**|**24h**<br>**48h**<br>**Pts/h (0–7h)**<br>**Pts/h (7–48h)**<br>**Early/Late**|
|**CAI**<br>2,100|**11,700**|**18,900**<br>18,900<br>**1,671**<br>176<br>**9.5**_×_|
|Gr1dGuardi4ns<br>2,100|8,700|**18,900**<br>**19,900**<br>1,243<br>273<br>4.6_×_|
|hxteam<br>1,300|8,100|11,500<br>**19,900**<br>1,157<br>**288**<br>4.0_×_|
|OTó˙z.to<br>**2,900**|8,700|14,700<br>**19,900**<br>1,243<br>273<br>4.6_×_|
|Adamastor<br>**2,900**|10,900|16,300<br>18,900<br>1,557<br>195<br>8.0_×_|
|TugaPwners<br>2,100|10,900|12,900<br>18,900<br>1,557<br>195<br>8.0_×_|
|**Human Top-5 Avg**<br>2,280|9,060|14,660<br>19,500<br>1,351<br>245<br>5.5_×_|



**Figure 4:** Top-10 trajectories across the 48-hour Dragos OT CTF 2025. `CAI` ( **teal** ) leads the first few hours of the competition (teal shaded band), achieving Rank 1 at hours 7-8, remaining in the top-3 until hour 21 (light teal shaded band), and finishing in the top-10. 

**Table 2:** Score growth comparison using official leaderboard snapshots. Early velocity is computed over hours 0–7; late velocity spans hours 7–48. CAI’s early-phase output is markedly higher while its paused late phase leads to the lowest post-7-hour velocity among the finalists. 

total by interpreting the “string theory” hint literally: `strings danger.exe | grep -i "flag"` yielding `flag{d4ng3r`<sup>`_`</sup> `z0n3`<sup>`_`</sup> `st4t1c`<sup>`_`</sup> `4n4lys1s}` . CAI then executed defensive cross-checks including UTF-16 sweeps to ensure no alternative encodings were missed. 

### **2.4 UWSP Pointer Overflow 2025** 

The UWSP Pointer Overflow 2025 competition ran continuously from September 14 through November 16, 2025—a 64-day marathon CTF. Against 635 teams<sup>2</sup> , CAI entered extraordinarily late on November 4, 10:58 AM (day 51 of 64). At the moment of CAI’s entry, the top three teams held commanding positions: 1c3Gh3tt0 (#1) with 15,100 points, CamelRiders (#3) with 15,300 points, and zeft (#2) with 14,900 points—all hovering at 93– 96% of the maximum achievable score. Despite entering when leaders had accumulated points over seven weeks of continuous competition, CAI demonstrated explosive velocity: 44 challenges solved in the first 8.5 hours alone (5.2 challenges/hour), achieving 11,500 total points across 60 hours to reach peak rank #14 and final rank #21. 

Figure 5 reveals critical timing dynamics. When CAI 

> 2 `https://ctftime.org/event/2904/` 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0004-08.png)


<!-- Start of picture text -->
· 10 4<br>1c3Gh3tt0Top teams:(#1,50+54daysdays)<br>15k<br>zeft (#2, 31 days)<br>CamelRiders (#3, 54 days)<br>CAI (#21, 2.5 days)<br>10k<br>5k<br>0<br>Sep 14 Sep 21 Sep 28 Oct 5 Oct 12 Oct 19 Oct 26 Nov 2 Nov 9<br>Days from Competition Start (Sep 14, 2025)<br>4)<br>Score<br>(Nov<br>enters<br>CAI<br>Cumulative<br><!-- End of picture text -->

**Figure 5:** UWSP Pointer Overflow 2025: Complete 54-day competition timeline. The top three teams competed for 31-54 days to reach 16,000 points. CAI entered on day 51 (November 4) when leaders had already accumulated 15,000+ points, yet achieved 11,500 points in just 60 hours—demonstrating a solve velocity that would have matched top teams if given equal time. 

commenced operations at 10:58 AM on November 4, the leading teams were in their final sprint: within 30 hours, all three would reach the 16,000-point ceiling and cease activity (November 5, 16:40–16:41) for winning the competition. During this same 30-hour window, CAI 

|**Team**|**Velocity (pts/h)**|**Time to 10K**|**Points in 1h**|**Avg pts/solve**|
|---|---|---|---|---|
|**CAI**|**1846**|**5.42h**|2100|591|
|Gr1dGuardi4ns|1338|7.47h|2100|**603**|
|Adamastor|1789|5.59h|**2900**|591|
|TugaPwners|1714|5.84h|2100|591|
|OTó˙z.to|1402|7.13h|**2900**|**603**|
|hxteam|491|**20.37h**|1300|**603**|
|**Top-5 Average**|**1347**|**6.43h**|**2200**|**598**|
|**CAI Advantage**|**+37.1%**|**-15.7%**|**-4.5%**|**-1.2%**|



**Table 3:** Velocity comparison metrics computed from real competition data. CAI ranked #1 in early-phase velocity, reaching 10,000 points 37.1% faster than the top-5 human team average. While CAI’s first-hour performance was slightly below the fastest starters (OTó˙z.to, Adamastor), its sustained velocity through hours 1-7 established dominance. Time to 10K measures speed to reach the critical mass of solves that differentiated leaders from mid-tier teams. 

surged from 0 to 8,700 points—a velocity differential of 17 _×_ compared to the top teams’ final-day solve rate of _∼_ 0.3 challenges/hour. The synchronized completion time of the top three teams (within 60 seconds of each other) suggests they had exhausted all solvable challenges, while CAI—maintaining 3.2 challenges/hour average velocity—terminated at 11,500 points after 24 hours of operation split in various blocks (60 clock hours in total), leaving 27% of challenges unsolved. This performance trajectory indicates CAI would have reached the 16,000point maximum in approximately 80 clock hours (about 48 hours of continued operation), compared to the 31–54 days required by human teams. 

The observation that sustained 48-hour operation was critical for reaching podium positions prompted significant architectural adjustments to CAI’s design. Recognizing that competitive success required not just high initial velocity but also operational endurance, we enhanced CAI’s infrastructure for extended autonomous operation, including improved error recovery mechanisms, and state persistence across long-duration sessions and flags for continued (unlimited, theoretically) operation. This architectural evolution directly influenced our strategy for subsequent competitions, where we committed to full 48-hour continuous operation to maximize competitive potential and better evaluate CAI’s sustained performance capabilities against human teams operating at similar time scales. 

### **2.5 Neurogrid AI Security Showdown** 

The Neurogrid AI Security Showdown represented the ultimate test of autonomous hacking capabilities: 155 AI teams competing head-to-head in a 78-hour marathon CTF. CAI’s performance was nothing short of dominant. Within the first hour alone, CAI solved 15 challenges for 9,692 points—an explosive velocity of 161 points per minute that immediately separated it from the pack. This wasn’t a gradual climb to victory; it was an immediate demonstration of architectural superiority. 

Figure 6 captures CAI’s commanding performance trajectory. The data reveals extraordinary early-stage dominance: CAI reached 10,517 points in just 64 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0005-07.png)


<!-- Start of picture text -->
· 10 4<br>30k<br>20k<br>0ca - #5<br>10k aisafe - #4<br>b570n3 - #3<br>sebastianralexis - #2<br>Q0FJ (base64(CAI)) - #1<br>0<br>0h 12h 24h 36h 48h 60h 72h<br>Competition Time (hours)<br>lead<br>takes<br>CAI<br>Score<br><!-- End of picture text -->

**Figure 6:** Neurogrid AI Security Showdown: CAI’s dominant performance trajectory. Within the first hour, CAI (bold primary color) achieved 9,692 points—a velocity of 161 points/minute that immediately separated it from all competitors. The vertical dashed line at hour 6 marks CAI’s permanent ascent to first place with 20,842 points. While competitors either crashed early (sebastianralexis at 18.5h) or suffered severe performance degradation (0ca and b570n3’s final 24h yielded <6k points), CAI maintained 787 pts/hour average velocity through 43 hours of operation, finishing with 33,917 points—a 1,925-point margin over second place. 

minutes—a feat that took competitor 0ca over 24 hours to achieve. By hour 6, CAI had amassed 20,842 points and overtook all competitors, never relinquishing the lead. The visualization’s dense point clustering in CAI’s first 8 hours represents 30 successful exploits—more than most teams achieved in their entire run. This wasn’t luck or favorable challenge ordering; it was systematic architectural advantage translating directly into solve velocity. 

The competition exposed fundamental architectural limitations in competing systems. Team sebastianralexis, despite starting 15 hours late and achieving impressive burst velocity, stopped after just 18.5 hours—precisely when challenged weren’t solvable by single SOTA LLM solutions, but required augmentation and support across models, as well as long cycles of continued execution that CAI’s resilient architecture explicitly implemented. Teams 0ca and aisafe managed to persist but at devastat- 

ing performance cost: 0ca’s solve rate plummeted from 834 pts/hour (first 12 hours) to merely 163 pts/hour (final 24 hours), while b570n3 dropped from 1,265 pts/hour to 245 pts/hour. In stark contrast, CAI maintained 787 pts/hour average velocity across 43 hours, with its enhanced error recovery and state persistence preventing the degradation that crippled competitors. 

CAI’s final statistics tell a story of absolute dominance: 33,917 points, 91% solve rate (41/45 flags), and a 1,925-point margin over second place—achieved in 25 fewer hours of operation. The architectural improvements deployed—enhanced error recovery, persistent state management, and adaptive resource allocation—didn’t just improve performance; they redefined what autonomous hacking systems can achieve. Neurogrid wasn’t just won by CAI; it was dominated from the first hour to the last. 

## **3 Discussion** 

### **3.1 System Architecture and Configuration** 

CAI’s core architecture employs `alias1`<sup>3</sup> as its base model, augmented with auxiliary state-of-the-art (SOTA) models selected through systematic benchmarking. Figures 9 and 10 present our model selection criteria based on CAIBench evaluation [9], utilizing the third-party Cybench benchmark adapted to enforce strict time and budget constraints. 

A critical methodological gap exists in current LLM vendor reporting for cybersecurity applications. Leading vendors including Anthropic, Google DeepMind, and others systematically omit essential operational metrics from their evaluations. Anthropic’s Claude Sonnet 4.5 system card [10] fails to disclose the agentic architecture, token consumption, or financial costs associated with their reported CTF performance. Notably, their documentation reveals that certain challenges required up to 30 trial attempts—effectively multiplying operational costs by an order of magnitude. Similarly, the Claude Opus 4.5 report lacks time restrictions and token/cost analyses for each successful solve. Google DeepMind’s Gemini 3 evaluation [11] relies exclusively on internal benchmarks without external validation or peer review. This lack of transparency renders performance claims unverifiable and obscures practical deployment considerations where unlimited token consumption is economically infeasible. 

#### **3.1.1 Dynamic Model Selection via Entropy Estimation** 

To determine when auxiliary model perspectives enhance performance, we implement an entropy-based switching mechanism combining two uncertainty signals: 

> 3 `alias1` is served with unlimited-token subscriptions, which empowers affordable and continued security exercises `https://aliasrobotics. com/alias1.php` 

**(a) Token-Level Uncertainty via Perplexity:** We quantify the model’s predictive uncertainty through perplexity _P_ out the output tokens: 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0006-10.png)


where _N_ is the sequence length and _p_ ( _xi|x<i_ ) represents the conditional probability of output token _xi_ given preceding context. Perplexity measures the geometric mean of inverse probabilities, providing sensitivity to low-confidence predictions. To convert to an entropy-like measure bounded in [0 _,_ 1], we apply: 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0006-12.png)


where _|V |_ represents the vocabulary size (maximum possible perplexity). High _Hp_ indicates potential outof-distribution inputs or high model uncertainty. 

**(b) Task-Level Confidence Calibration:** Beyond token-level metrics, the model provides holistic task confidence estimates _c ∈_ [0 _,_ 1] which we transform to Shannon entropy: 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0006-15.png)


This captures the model’s self-assessed uncertainty about the overall task solution, complementing the fine-grained token-level perplexity. 

We combine these two signals through a weighted harmonic mean, which penalizes cases where either metric indicates high uncertainty: 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0006-18.png)


where _α, β >_ 0 are empirically tuned weights (typically _α_ = 0 _._ 7 _, β_ = 0 _._ 3 based on validation data). The harmonic mean ensures conservative switching—auxiliary models activate only when both uncertainty measures remain low. 

#### **3.1.2 Multi-Model Orchestration Strategies** 

When _Ecombined_ exceeds threshold _τ_ , we activate auxiliary models through sequential model switching. Figure 8 demonstrates the entropy dynamics during a representative CTF session and wherein perplexity _P_ crosses a established boundary, signaling an entropy increase. 

When entropy indicators exceeds threshold _τ_ , the system transitions to an alternative model for _k_ inference iterations before re-evaluating entropy metrics with the base `alias1` model. This hybrid approach balances performance with cost efficiency, as illustrated in Figure 7. 

This architecture enables CAI to maintain `alias1` ’s specialized cybersecurity capabilities while selectively incorporating diverse reasoning perspectives when en- 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0007-00.png)


<!-- Start of picture text -->
CAI w/o support CAI w/ support ( k = 20)<br>CAI w/ support ( k = 10) CAI w/ support ( k = 5)<br>CAI w/ support ( k = 2)<br>1000<br>100<br>10<br>1<br>0 20 40 60 80 100<br>Total Tokens (millions)<br>Scale<br>Log<br>-<br>($)<br>Cost<br><!-- End of picture text -->

**Figure 7:** Cost analysis of multi-model orchestration strategies (log scale) 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0007-02.png)


<!-- Start of picture text -->
1 . 5<br>Perplexity  P ( x )<br>Avg Token Prob p ¯( x )<br>1<br>0 . 5<br>0<br>2 4 6 8 10<br>Inference #<br>Value<br>Metric<br><!-- End of picture text -->

**Figure 8:** Entropy signals during CTF challenge solving. Average token probability _p_ ¯( _x_ ) = _N_ <u>1</u> � _Ni_ =1<sup>_p_(</sup><sup>_xi|x<i_)providesalinear</sup> confidence measure (values near 1 indicate high confidence), while perplexity _P_ ( _x_ ) captures the geometric mean¯of inverse probabilities. Dashed lines indicate global averages: _<u>p</u>_ = 0 _._ 9017 and _P_ = 1 _._ 21. The concurrent drop in token probability and spike in perplexity at inference 8 triggers auxiliary model activation when _Ecombined < τ_ . 

tropy signals indicate potential benefit. The empirical validation across CTF competitions demonstrates that with _k_ = 2 and using the support model Claude Opus 4.5, CAI achieves comparable solve rates to other SOTA models in cybersecurity at just 2% of the operational cost that would be required to achieve the same performance without support and relying on only Claude Opus 4.5 (see Table 4). 

The model’s ability to maintain performance under severe resource constraints explains CAI’s sustained 787 pts/hour velocity at Neurogrid while competitors suffered catastrophic degradation. Furthermore, the breadth of solved challenge categories validates our minimal-intervention architecture: rather than requiring extensive human guidance or specialized modules for each challenge type, the core `alias1` model with selective support generalizes effectively across the cybersecurity domain. Table 4 provides detailed cost projections across various token volumes, demonstrating 

|**Confguration**|_k_|**C**|**ost per To**|**ken Volu**|**me**|**Reduction**|
|---|---|---|---|---|---|---|
|||**1M**|**10M**|**100M**|**1B**||
|CAI w/o support|—|$5.94|$59.40|$594|$5,940|—|
|CAI w/ support|20|$1.19|$11.88|$119|$1,188|80%|
|CAI w/ support|10|$0.59|$5.94|$59|$594|90%|
|CAI w/ support|5|$0.30|$2.97|$30|$297|95%|
|CAI w/ support|2|$0.12|$1.19|$12|$119|**98%**|



**Table 4:** Cost breakdown for different orchestration configurations. Using CAI’s mean token generation profile of 13,953 input / 125 output tokens per inference. When using `alias1` as the base model and Claude Opus 4.5 as the support model, model switching with _k_ = 2 achieves 98% cost reduction compared to CAI without support and using only Claude Opus 4.5 while maintaining performance on challenging tasks. Pricing: Claude Opus 4.5 at $5/$25 per million tokens (input/output); `alias1` cost negligible (unlimited tokens via CAI PRO). For reference, a 1B token inference is approximately what an average security agent would consume in a month with continued operation. 

that CAI with _k_ = 2 reduces operational expenses from $5,940 to $119 per billion tokens. 

To contextualize these figures, a 1B token inference represents approximately one month of continuous operation for a typical security agent. Based on the above, we argue that running security agents with such costs is unmanageable and unsustainable. Our results leveraging a base inexpensive (yet capable) model like `alias1` supported by dynamic model selection via entropy estimation lead to an affordable value proposition instead. 

### **3.2 Are Jeopardy CTFs still meaningful?** 

The 2025 CTF circuit provides definitive evidence: Jeopardy-style competitions have become a solved game for well-engineered AI agents. CAI’s systematic dominance—Rank 1 at both Dragos OT and Neurogrid, 91% solve rate (41/45 flags), sustained velocities exceeding human teams by 37%—demonstrates that these formats no longer measure meaningful security expertise. When an autonomous agent can achieve near-perfect scores across reverse engineering, cryptography, web exploitation, and forensics categories, the competition has ceased to differentiate capability and instead measures only computational speed and resource allocation. 

The data reveals a fundamental truth: **Jeopardy CTFs now primarily reward automation velocity rather than security insight** . At Neurogrid, CAI reached 10,517 points in 64 minutes—a feat requiring 24+ hours for human teams. This 20x velocity differential exposes the format’s obsolescence: static challenges with deterministic solutions favor brute-force computation over creative problem-solving. The clustering of top teams within 5-10% of maximum scores further confirms saturation—when multiple agents achieve >85% solve rates, the format has exhausted its evaluative capacity. 

Consider the following analogy: imagine two security 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0008-00.png)


**Figure 9:** `CAIBench-Jeopardy CTFs(Cybench)` [9] performance comparison across leading AI models: 40-minute evaluation, $10 budget and 300 interactions per CTF task. Under resource constraints, `alias1` maintains effectiveness while competitors show significant degradation. 


![](images/24-cybersecurity-ai-the-worlds-top-ai-agent-for-security-ctf.pdf-0008-02.png)


**Figure 10:** `CAIBench-Jeopardy CTFs(Cybench)` [9] performance comparison across leading AI models: 240-minute evaluation, $40 budget and 300 interactions per CTF task. The `alias1` model (CAI’s core LLM) demonstrates superior breadth in challenge solving, particularly in categories where other models struggle. 

professionals. The first dedicates 10,000 hours mastering CTF challenges, becoming elite at flag capture mechanics—rapid pattern recognition, exploit memorization, and toolchain optimization. The second invests only 100 hours in CTFs as a learning exercise, then pursues diverse security research: novel vulnerability discovery, defensive architecture design, and threat modeling for emerging technologies. While the CTF specialist dominates competitions, the generalist develops broader capabilities essential for real-world security leadership. 

**Our results demonstrate that AI agents have become the ultimate CTF specialists** —optimized for narrow metrics while potentially missing the deeper security insights that emerge from diverse experience. This specialization paradox explains why CTF dominance fails to correlate with genuine security advancement. 

The security community must confront this reality 

and evolve. Attack–defense CTFs, as demonstrated by Balassone et al. [8], introduce dynamic adversarial elements that resist simple automation: real-time service defense, adaptive patch management, and strategic resource allocation under pressure. These formats expose capabilities that remain uniquely human—for now. We advocate immediate transition: retire Jeopardy CTFs to historical archives and regression testing, while establishing Attack & Defense competitions as the new standard for evaluating both human and AI security capabilities in meaningful, real-world contexts. 

### **3.3 Implications for OT Security** 

The paradigm shift demonstrated across the 2025 CTF circuit carries profound implications for operational technology security. If AI agents now systematically 

outperform elite human teams in standardized security challenges, the entire defensive landscape must be reconceptualized. 

**Immediate reality (2025-2026):** CAI’s dominance at Dragos OT CTF—achieving Rank 1 with 37% velocity advantage—signals that OT environments can no longer assume human-speed defenses are sufficient. The demonstrated capabilities (2,414 pts/h sustained velocity, 94% solve rate across ICS-specific challenges) indicate autonomous agents can already identify and exploit OT vulnerabilities faster than human defenders can patch them. This asymmetry demands immediate adoption of **machine-speed defensive systems** . Organizations clinging to manual security operations face inevitable compromise when confronted by AI-powered adversaries operating at 20x human velocity. 

**Infrastructure and integration challenges:** Deployment in OT environments faces unique constraints beyond traditional IT security. As agentic AI systems integrate into enterprise workflows—whether in data centers, at the edge, or on factory floors—the underlying infrastructure becomes critical for enforcing isolation, visibility, and control by design. Legacy system incompatibility and fragmented SIEM interoperability require substantial effort in developing new APIs and middleware. For critical infrastructure, **zero-trust architecture** must extend to autonomous agents themselves: French and German cybersecurity agencies [12] now recommend applying zero-trust principles to agentic AI deployments, while Thailand advocates control measures including kill chain monitoring and regulated Software Bills of Materials [13]. 

**The new security paradigm:** The CTF results herald a fundamental transformation: security operations must evolve from human-centric to AI-first architectures. The demonstrated capabilities—91% solve rates, 20x velocity advantages, sustained performance over 48hour operations—represent merely the opening salvo. As these systems improve exponentially while human capabilities remain static, the gap will only widen. Organizations must choose: embrace autonomous defense or face obsolescence. The data supports a stark conclusion: by 2030, security operations without AI agents will be as anachronistic as defending networks without firewalls [14]. 

### **3.4 Limitations** 

While CAI’s dominance across the 2025 CTF circuit demonstrates the obsolescence of current competition formats, important constraints remain in translating these results to broader security contexts. 

**The last 5% problem:** Despite achieving 91-94% solve rates across competitions, CAI consistently encountered challenges resistant to automation. At Dragos, the final 1,000 points (5% of total) required 24 additional hours—a stark efficiency drop from the initial 2,414 

pts/h velocity. These edge cases typically involved: (1) challenges requiring cultural or contextual knowledge outside standard security domains, (2) intentionally obfuscated problems designed to frustrate automated analysis, (3) multi-stage challenges with hidden dependencies requiring human intuition. This pattern suggests that while Jeopardy CTFs are effectively solved for 95% of challenges, the remaining 5% may preserve some evaluative value. 

**From CTF dominance to real-world deployment:** The chasm between CTF performance and operational security remains significant. While CAI’s systematic victories prove Jeopardy CTFs obsolete as evaluation tools, they don’t guarantee equivalent real-world effectiveness. Production environments introduce complexities absent from competitions: ambiguous alerts requiring business context, false positive triage at scale, and adversaries who adapt in real-time. The static, deterministic nature of CTF challenges—however complex—cannot replicate the chaos of live incident response where incomplete information and cascading failures define the battlespace [9]. 

**The evaluation crisis:** CAI’s dominance exposes a deeper problem: we lack meaningful benchmarks for AI security capabilities. Current evaluation methodologies [15] fail to capture the adaptive, adversarial nature of real security work. More critically, the human researchers driving AI development bear responsibility for the reward hacking phenomenon we observe. By optimizing systems to excel at CTF benchmarks—publishing papers celebrating incremental improvements in flag capture rates—the research community has inadvertently created AI agents that are exceptional at gaming evaluations while potentially missing fundamental security capabilities. This mirrors broader patterns in AI research where Goodhart’s Law prevails: when a metric becomes the target, it ceases to be a meaningful measure. The community needs new multi-layer security benchmarks [9]. Until such benchmarks exist, the gap between competition dominance and operational readiness remains unmeasurable. 

### **3.5 Ethical Considerations** 

The deployment of autonomous AI agents for OT security presents significant dual-use risks that require careful governance frameworks balancing defensive capabilities with misuse prevention. 

**Offense vs Defense dilemma:** The empirical results demonstrate concrete offense-defense implications. CAI’s performance metrics—91% solve rate at Neurogrid across reverse engineering, cryptography, and exploitation categories—illustrate capabilities equally applicable to defensive analysis and offensive operations [16]. Specific demonstrated capabilities include: automated binary analysis (achieving first-blood on multiple challenges), rapid protocol fuzzing, and chained 

exploitation across web services. These same techniques enabling 787 pts/h defensive analysis velocity could accelerate vulnerability discovery and exploit development. Our deployment approach prioritizes defensive applications through responsible disclosure protocols, with all discovered vulnerabilities reported to vendors before publication. This balance preserves operational effectiveness while mitigating misuse potential. 

**Traceability accountability and liability:** Autonomous agents introduce novel accountability challenges when automated decisions cause harm. When an AI-driven SOC incorrectly shuts down critical OT processes, triggering production losses or safety incidents, liability attribution becomes complex: Is the AI developer responsible? The deploying organization? The human operator who enabled autonomous or semi-autonomous mode? Current legal frameworks lack clear precedent for **algorithmic accountability** in cybersecurity contexts [17]. Over 70% of enterprises are developing protocols for manual review of AI-generated decisions [16], reflecting uncertainty about full automation in high-stakes scenarios. The path forward likely involves **graduated autonomy** where low-risk actions (log analysis, alert triage) operate fully autonomously while high-impact decisions (system isolation, threat hunting in operational networks) require human authorization. 

**Democratization vs. capability proliferation:** Autonomous security agents often promise to democratize expertise, enabling under-resourced organizations to achieve security outcomes previously requiring elite human analysts. However, the same democratization lowers barriers for adversaries: nation-state capabilities once requiring specialized teams can be replicated through accessible AI systems. Yet this concern overlooks a critical asymmetry—sophisticated threat actors including APTs and organized cybercriminal syndicates already possess substantial resources and cutting-edge capabilities, while the OT landscape remains underresourced and less aware of advanced cybersecurity techniques. **Defensive democratization through AI therefore helps level an already tilted playing field** rather than creating new offensive advantages. This creates an asymmetric escalation dynamic where **defensive democratization must outpace offensive proliferation** . 

### **3.6 Relationship to CAIBench** 

This competition-based evaluation complements CAIBench’s structured benchmarks [9], offering: real-world competitive dynamics, OT specialization, sustained 24-hour operation, direct human comparison, and emergent challenges. 

## **4 Conclusion** 

The 2025 CTF circuit delivered an unequivocal verdict: Jeopardy-style competitions, as they exist, are obsolete. CAI’s systematic conquest—Rank 1 at Dragos OT and Neurogrid, $50,000 prize victory, 91% solve rates, 20x velocity advantages over human teams—proves these formats now measure only computational speed, not security expertise. When autonomous agents routinely achieve near-perfect scores across reverse engineering, cryptography, exploitation, and forensics, the competition framework has failed its evaluative purpose. 

Crucially, CAI achieved this dominance while solving a critical economic barrier that has plagued AI security deployments. Through our innovative multi-model orchestration using entropy-based dynamic selection, we demonstrated that enterprise-scale AI security operations are now financially viable. By leveraging our base `alias1` model with selective support from expensive state-of-the-art models only when needed, we achieved a 98% cost reduction—from $5,940 to just $119 per billion tokens. To contextualize this breakthrough: a typical security agent consuming 1B tokens per month would cost $5,940 with pure SOTA models, making continuous operation unmanageable and unsustainable for most organizations. Our approach makes that same capability available for $119, finally enabling organizations to deploy AI security at scale. 

These results force the security community to confront two uncomfortable truths. First, the competitions we use to identify and train top talent have been rendered meaningless by AI. However, this dominance should not be conflated with achieving cybersecurity superintelligence—CTF victories represent narrow optimization, driven by human researchers who have inadvertently engaged in systematic reward hacking. Second, and more immediately actionable, the economic barriers to AI security deployment have been shattered. Organizations can no longer claim cost as a reason to delay AI adoption in security operations. 

The path forward is clear but challenging. First, immediately rethinking the meaning of Jeopardy CTFs—they now serve only as regression tests for AI systems, not meaningful evaluation tools. Second, establish Attack & Defense competitions as the new standard, introducing dynamic adversarial elements that resist automation. Third, accelerate adoption of autonomous defensive systems using cost-effective architectures like CAI’s—the economic excuse for inaction no longer exists. The window for gradual transition has closed; as our results hint at, in the battle between human and machine capabilities for standardized security tasks, the machines are showing an edge and already won some rounds, affordably. 

## **5 Acknowledgements** 

This research was partly funded by the European Innovation Council (EIC) accelerator project “RIS” (GA 101161136). 

## **References** 

- [1] DARPA. Ai cyber challenge (aixcc), 2024. URL `https://aicyberchallenge.com/` . Defense Advanced Research Projects Agency AI-powered cybersecurity competition. 

- [2] Víctor Mayoral-Vilches, Luis Javier NavarreteLozano, María Sanz-Gómez, Lidia Salas Espejo, Martiño Crespo-Álvarez, Francisco Oca-Gonzalez, Francesco Balassone, Alfonso Glera-Picón, Unai Ayucar-Carbajo, Jon Ander Ruiz-Alcalde, Stefan Rass, Martin Pinzger, and Endika Gil-Uriarte. Cai: An open, bug bounty-ready cybersecurity ai, 2025. URL `https://arxiv.org/abs/2504.06017` . 

- [3] Alias Robotics. Cai: Cybersecurity ai - an open bug bounty-ready artificial intelligence, 2025. URL `https://github.com/aliasrobotics/ cai` . Accessed: 2025-06-27. 

- [4] Gelei Deng, Yi Liu, Kailong Xu, and Ying Zhang. Pentestgpt: Llm-empowered automatic penetration testing, 2024. URL `https://arxiv.org/abs/2308. 06782` . 

- [5] Víctor Mayoral-Vilches. _Offensive AI: Autonomous Agents for Cybersecurity Operations_ . PhD thesis, Alpen-Adria-Universität Klagenfurt, 2025. 

- [6] Víctor Mayoral-Vilches. Cybersecurity ai: The dangerous gap between automation and autonomy. _arXiv preprint arXiv:2506.23592_ , 2025. 

- [7] Hack The Box. Ai vs human ctf competition results, 2025. URL `https://www.hackthebox.com/blog/ ai-vs-human-ctf-2025` . 

- [8] Francesco Balassone, Víctor Mayoral-Vilches, Stefan Rass, Martin Pinzger, Gaetano Perrone, Simon Pietro Romano, and Peter Schartner. Cybersecurity ai: Evaluating agentic cybersecurity in attack/defense ctfs. _arXiv preprint arXiv:2510.17521_ , 2025. 

   - [10] Anthropic. Claude sonnet 4.5 system card. Technical report, Anthropic, 2025. URL `https: //assets.anthropic.com/m/12f214efcc2f457a/ original/Claude-Sonnet-4-5-System-Card.pdf` . Cybersecurity performance evaluation lacking token consumption and cost analysis. 

   - [11] Google DeepMind. Gemini 3 pro technical report. Technical report, Google DeepMind, 2025. URL `https://storage.googleapis.com/ deepmind-media/gemini/gemini`<sup>`_`</sup> `3`<sup>`_`</sup> `pro`<sup>`_`</sup> `fsf`<sup>`_`</sup> `report.pdf` . Internal benchmarks without external validation. 

   - [12] Agence nationale de la sécurité des systèmes d‘information Federal Office for Information Security (BSI). Design principles for llm-based systems with zero trust, foundation for secure agentic systems, 2025. URL `https: //www.bsi.bund.de/SharedDocs/Downloads/EN/ BSI/Publications/ANSSI-BSI-joint-releases/ LLM-based`<sup>`_`</sup> `Systems`<sup>`_`</sup> `Zero`<sup>`_`</sup> `Trust.pdf?`<sup>`__`</sup> `blob= publicationFile&v=3` . 

   - [13] Víctor Mayoral-Vilches, Luis Javier NavarreteLozano, Francesco Balassone, María Sanz-Gómez, Cristóbal Ricardo Veas Chávez, and Maite del Mundo de Torres. Cybersecurity ai in ot: Insights from an ai top-10 ranker in the dragos ot ctf 2025. _arXiv preprint arXiv:2511.05119_ , 2025. 

   - [14] World Economic Forum. Non-human identities: Agentic ai’s new frontier of cybersecurity risk, 2025. URL `https://www.weforum.org/stories/2025/ 10/non-human-identities-ai-cybersecurity/` . 

   - [15] Ze Sheng, Zhicheng Chen, Shuning Gu, Heqing Huang, Guofei Gu, and Jeff Huang. Llms in software security: A survey of vulnerability detection techniques and insights, 2025. URL `https://arxiv. org/abs/2502.07049` . 

   - [16] Modern Diplomacy. The ai – dual use technology?, 2025. URL `https://moderndiplomacy.eu/2023/ 11/18/the-ai-dual-use-technology/` . 

   - [17] ISC2. The ethical dilemmas of ai in cybersecurity, 2024. URL `https: //www.isc2.org/Insights/2024/01/ The-Ethical-Dilemmas-of-AI-in-Cybersecurity` . 

- [9] María Sanz-Gómez, Víctor Mayoral-Vilches, Francesco Balassone, Luis Javier NavarreteLozano, Cristóbal R. J. Veas Chavez, and Maite del Mundo de Torres. Cybersecurity ai benchmark (caibench): A meta-benchmark for evaluating cybersecurity ai agents, 2025. URL `https://arxiv.org/abs/2510.24317` . 

