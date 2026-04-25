import streamlit as st
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

from agents.scanner_agent import scanner_agent
from agents.quality_agent import quality_agent
from agents.readme_agent import readme_agent
from agents.planner_agent import planner_agent
from agents.reporter_agent import reporter_agent


class State(TypedDict, total=False):
    repo_url: str
    repo_path: str
    file_tree: str
    important_files: dict
    quality_report: dict
    readme_report: dict
    issues: list
    final_report: str
    errors: list


def build_graph():
    graph = StateGraph(State)

    graph.add_node("scanner_agent", scanner_agent)
    graph.add_node("quality_agent", quality_agent)
    graph.add_node("readme_agent", readme_agent)
    graph.add_node("planner_agent", planner_agent)
    graph.add_node("reporter_agent", reporter_agent)

    graph.add_edge(START, "scanner_agent")
    graph.add_edge("scanner_agent", "quality_agent")
    graph.add_edge("quality_agent", "readme_agent")
    graph.add_edge("readme_agent", "planner_agent")
    graph.add_edge("planner_agent", "reporter_agent")
    graph.add_edge("reporter_agent", END)

    return graph.compile()


st.set_page_config(page_title="RepoAgent Lite", page_icon="🤖", layout="wide")

st.title("🤖 RepoAgent Lite")
st.write("Agentic AI-style GitHub repository reviewer.")

repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/user/repo"
)

if st.button("Analyze Repository", type="primary"):
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
        st.stop()

    with st.spinner("Running RepoAgent workflow..."):
        graph = build_graph()
        result = graph.invoke({
            "repo_url": repo_url,
            "errors": []
        })

    if result.get("errors"):
        st.warning("Some errors occurred:")
        for err in result["errors"]:
            st.write(f"- {err}")

    report = result.get("final_report", "")

    st.markdown(report)

    st.download_button(
        "Download Report",
        report,
        file_name="repoagent_report.md",
        mime="text/markdown"
    )