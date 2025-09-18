import streamlit as st
import matplotlib.pyplot as plt
from peg_solitaire.board import Board
from peg_solitaire.astar import astar
from peg_solitaire.heuristics import h_min_moves

# UI del Peg Solitaire con Streamlit
# Uso: poetry run python -m streamlit run peg_solitaire/app.py

def plot_board(board: Board):
    """Renderiza el tablero como un grid de círculos con matplotlib"""
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")

    n = board.size
    for r in range(n):
        for c in range(n):
            val = board.grid[r][c]
            if val == -1:
                continue
            elif val == 1:  # peón
                circle = plt.Circle((c, n - r - 1), 0.4, color="blue")
            elif val == 0:  # vacío
                circle = plt.Circle((c, n - r - 1), 0.4, edgecolor="black", facecolor="white")
            ax.add_patch(circle)

    ax.set_xlim(-1, n)
    ax.set_ylim(-1, n)
    return fig


def main():
    st.set_page_config(page_title="Peg Solitaire A*", page_icon="🎮", layout="centered")
    st.title("🎮 Peg Solitaire con A*")

    if "solution" not in st.session_state:
        st.session_state.solution = None

    st.sidebar.header("⚙️ Configuración")
    n = st.sidebar.selectbox("Elige tamaño del tablero (n)", [3], index=0)  # solo n=3 por performance

    if st.sidebar.button("🔄 Resetear tablero"):
        st.session_state.solution = None

    if st.sidebar.button("✅ Resolver con A*", type="primary"):
        start = Board(n)
        path, boards, metrics = astar(start, h_func=h_min_moves)
        st.session_state.solution = (path, boards, metrics)

    if st.session_state.solution:
        path, boards, metrics = st.session_state.solution

        if metrics["success"]:
            st.success(f"✅ ¡Solución encontrada en {metrics['solution_length']} movimientos!")

            step = st.slider("Paso", 0, len(boards) - 1, 0)
            fig = plot_board(boards[step])
            st.pyplot(fig)

            st.subheader("📊 Métricas")
            st.json(metrics)
        else:
            st.error("❌ No se encontró solución 😢")


if __name__ == "__main__":
    main()
