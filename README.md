# Learning LangGraph

My notes and practice scripts while learning [LangGraph](https://github.com/langchain-ai/langgraph), one concept per file.

| # | File | What it covers |
|---|------|----------------|
| 1 | `01helloworld.py` | A single-node graph: state in, modified state out |
| 2 | `02multiple_inputs.py` | State with several fields (a list, a name, a result) |
| 3 | `03Sequential.py` | Several nodes running one after another |
| 4 | `04conditional.py` | Conditional edges: a router picks which node runs next |
| 5 | `05looping.py` | Looping: a node repeats until a condition is met |

## Running

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python 01helloworld.py
```
