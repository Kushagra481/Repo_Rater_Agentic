from typing import TypedDict
import pandas as pd
import streamlit as st
from langgraph.graph import StateGraph, START, END

from agents.scanner_agent import scanner_agent
from agents.structure_agent import structure_agent
from agents.docs_agent import docs_agent
from agents.code_agent import code_agent
from agents.security_agent import security_agent
from agents.merge_agent import merge_agent
from agents.planner_agent import planner_agent
from agents.reporter_agent import reporter_agent


class State(TypedDict, total=False):
    repo_url: str
    repo_path: str
    file_tree: str
    important_files: dict
    extension_counts: dict
    source_stats: dict

    structure_report: dict
    docs_report: dict
    code_report: dict
    security_report: dict
    merged_report: dict

    issues: list
    final_report: str
    errors: list


def build_graph():
    graph = StateGraph(State)

    graph.add_node("scanner_agent", scanner_agent)
    graph.add_node("structure_agent", structure_agent)
    graph.add_node("docs_agent", docs_agent)
    graph.add_node("code_agent", code_agent)
    graph.add_node("security_agent", security_agent)
    graph.add_node("merge_agent", merge_agent)
    graph.add_node("planner_agent", planner_agent)
    graph.add_node("reporter_agent", reporter_agent)

    graph.add_edge(START, "scanner_agent")

    graph.add_edge("scanner_agent", "structure_agent")
    graph.add_edge("scanner_agent", "docs_agent")
    graph.add_edge("scanner_agent", "code_agent")
    graph.add_edge("scanner_agent", "security_agent")

    graph.add_edge("structure_agent", "merge_agent")
    graph.add_edge("docs_agent", "merge_agent")
    graph.add_edge("code_agent", "merge_agent")
    graph.add_edge("security_agent", "merge_agent")

    graph.add_edge("merge_agent", "planner_agent")
    graph.add_edge("planner_agent", "reporter_agent")
    graph.add_edge("reporter_agent", END)

    return graph.compile()


st.set_page_config(
    page_title="RepoAgent Lite",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 RepoAgent Lite")
st.caption("Multi-agent GitHub repository reviewer using LangGraph.")

repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/user/repo"
)

if st.button("Analyze Repository", type="primary"):
    if not repo_url.strip():
        st.error("Please enter a GitHub repository URL.")
        st.stop()

    with st.spinner("Running multi-agent workflow..."):
        graph = build_graph()
        result = graph.invoke({
            "repo_url": repo_url.strip(),
            "errors": []
        })

    if result.get("errors"):
        st.warning("Errors occurred during scanning:")
        for err in result["errors"]:
            st.write(f"- {err}")

    merged = result.get("merged_report", {})
    structure = result.get("structure_report", {})
    docs = result.get("docs_report", {})
    code = result.get("code_report", {})
    security = result.get("security_report", {})

    st.subheader("Final Score")
    st.metric("Multi-Agent Score", f"{merged.get('overall_score', 0)}/100")

    score_df = pd.DataFrame({
        "Agent": ["Structure", "Docs", "Code", "Security"],
        "Score": [
            structure.get("score", 0),
            docs.get("score", 0),
            code.get("score", 0),
            security.get("score", 0),
        ]
    })

    st.subheader("Agent Score Breakdown")
    st.bar_chart(score_df.set_index("Agent"))

    st.subheader("Detected Project Type")
    st.info(structure.get("project_type", "Unknown"))

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Final Report",
        "Structure",
        "Docs",
        "Code",
        "Security"
    ])

    with tab1:
        report = result.get("final_report", "")
        st.markdown(report)

        st.download_button(
            "Download Markdown Report",
            data=report,
            file_name="repoagent_multi_agent_report.md",
            mime="text/markdown"
        )

    with tab2:
        st.json(structure)

    with tab3:
        st.json(docs)

    with tab4:
        st.json(code)

    with tab5:
        st.json(security)

else:
    st.info("Paste a public GitHub repository URL and click Analyze Repository.")