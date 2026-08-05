import re

file_path = "docs/paper-research/md-downloaded-paper-curated/01-hackworld-evaluating-computer-use-agents-on-exploiting-web.md"

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    # Remove standalone page numbers
    if re.match(r'^\d+\s*$', line):
        continue
        
    new_lines.append(line)

content = "".join(new_lines)

# Replace the authors block
old_authors = """**Xiaoxue Ren**<sup>1</sup><sup>_∗_</sup> **Penghao Jiang**<sup>2</sup><sup>_∗_</sup> **Kaixin Li**<sup>3</sup><sup>_∗_</sup> **Zhiyong Huang**<sup>3</sup> **Xiaoning Du**<sup>4</sup> **Jiaojiao Jiang**<sup>2</sup> **Zhenchang Xing**<sup>5</sup><sup>_,_6</sup> **Jiamou Sun**<sup>5</sup> **Terry Yue Zhuo**<sup>4</sup><sup>_,_5</sup><sup>_∗†_</sup> 

1 Zhejiang University 2 University of New South Wales 3 National University of Singapore 4 Monash University 5 CSIRO’s Data61 6 Australian National University 

xxren@zju.edu.cn ; {penghao.jiang, jiaojiao.jiang}@unsw.edu.au likaixin@u.nus.edu ; {zhenchang.xing, frank.sun}@data61.csiro.au {xiaoning.du, terry.zhuo}@monash.edu"""

new_authors = """<div align="center">

**Xiaoxue Ren**<sup>1*</sup> &bull; **Penghao Jiang**<sup>2*</sup> &bull; **Kaixin Li**<sup>3*</sup> &bull; **Zhiyong Huang**<sup>3</sup> &bull; **Xiaoning Du**<sup>4</sup> <br>
**Jiaojiao Jiang**<sup>2</sup> &bull; **Zhenchang Xing**<sup>5,6</sup> &bull; **Jiamou Sun**<sup>5</sup> &bull; **Terry Yue Zhuo**<sup>4,5*†</sup>

<small>
<sup>1</sup> <i>Zhejiang University</i> &nbsp;&nbsp;&nbsp; <sup>2</sup> <i>University of New South Wales</i> &nbsp;&nbsp;&nbsp; <sup>3</sup> <i>National University of Singapore</i> <br>
<sup>4</sup> <i>Monash University</i> &nbsp;&nbsp;&nbsp; <sup>5</sup> <i>CSIRO’s Data61</i> &nbsp;&nbsp;&nbsp; <sup>6</sup> <i>Australian National University</i>
</small>

<small>
📧 `xxren@zju.edu.cn` &bull; `{penghao.jiang, jiaojiao.jiang}@unsw.edu.au` &bull; `likaixin@u.nus.edu` <br>
`{zhenchang.xing, frank.sun}@data61.csiro.au` &bull; `{xiaoning.du, terry.zhuo}@monash.edu`
</small>

</div>"""

content = content.replace(old_authors, new_authors)

with open(file_path, 'w') as f:
    f.write(content)

print("Done fixing 01-hackworld")
