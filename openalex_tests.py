from process_page import get_paper_by_title

titles = ["Fully Online Meta-Learning Without Task Boundaries", 
          "MEMO: Test Time Robustness via Adaptation and Augmentation", 
          "Mismatched No More: Joint Model-Policy Optimization for Model-Based RL", 
          "FitVid: Overfitting in Pixel-Level Video Prediction", 
          "ViKiNG: Vision-Based Kilometer-Scale Navigation with Geographic Hints", 
          "Context-Aware Language Modeling for Goal-Oriented Dialogue Systems", 
          "CHAI: A CHatbot AI for Task-Oriented Dialogue with Offline Reinforcement Learning", 
          "ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters", 
          "Lyapunov Density Models: Constraining Distribution Shift in Learning-Based Control", 
          "Bisimulation Makes Analogies in Goal-Conditioned Reinforcement Learning", 
          "Planning with Diffusion for Flexible Behavior Synthesis", 
          "How to Leverage Unlabeled Data in Offline Reinforcement Learning", 
          "Design-Bench: Benchmarks for Data-Driven Offline Model-Based Optimization", 
          "Offline Meta-Reinforcement Learning with Online Self-Supervision", 
          "Hybrid Imitative Planning with Geometric and Predictive Costs in Offroad Environments", 
          "ASHA: Assistive Teleoperation via Human-in-the-Loop Reinforcement Learning", 
          "Control-Aware Prediction Objectives for Autonomous Driving", 
          "Legged Robots that Keep on Learning: Fine-Tuning Locomotion Policies in the Real World", 
          "Offline Meta-Reinforcement Learning for Industrial Insertion", 
          "INFOrmation Prioritization through EmPOWERment in Visual Model-Based RL", 
          "When Should We Prefer Offline Reinforcement Learning Over Behavioral Cloning?", 
          "RvS: What is Essential for Offline RL via Supervised Learning?", 
          "Autonomous Reinforcement Learning: Formalism and Benchmarking", 
          "DR3: Value-Based Deep Reinforcement Learning Requires Explicit Regularization", 
          "CoMPS: Continual Meta Policy Search"
          ]

labels = ["https://openalex.org/W4221149559",
          "https://openalex.org/W3206798603",
          "https://openalex.org/W3204550979",
          "https://openalex.org/W3174394676",
          "https://openalex.org/W4221167405",
          "https://openalex.org/W4287889972",
          "https://openalex.org/W4287889738",
          "https://openalex.org/W6929470687",
          "https://openalex.org/W4283319080",
          "https://openalex.org/W4225134865",
          "https://openalex.org/W4281398962",
          "https://openalex.org/W4221150981",
          "https://openalex.org/W3131954206",
          "https://openalex.org/W3178748050",
          "https://openalex.org/W3217571039",
          "https://openalex.org/W4226029785",
          "https://openalex.org/W4285102474",
          "https://openalex.org/W3207033168",
          "https://openalex.org/W3206827162",
          "https://openalex.org/W4224256292",
          "https://openalex.org/W4223423875",
          "https://openalex.org/W4226395791",
          "https://openalex.org/W4225937903",
          "https://openalex.org/W4200634036",
          "https://openalex.org/W4226029999"]

def test_get_paper_by_title(titles, labels):
    count = 0
    for i in range(len(titles)):
        paper = get_paper_by_title(titles[i])
        if paper and paper.get("id", "") == labels[i]:
            count += 1
            print(f"Successfully retrieved work {i+1}: {titles[i]}")
        else:
            print(f"Failed to retrieve work {i+1}: {titles[i]}, instead returned {paper.get("id", "") if paper else "None"}")

test_get_paper_by_title(titles, labels)
        

