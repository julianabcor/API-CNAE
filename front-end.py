import html
import unicodedata
 
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
 
# ───────────────────────── Configuração ─────────────────────────
st.set_page_config(
    page_title="Painel CNAE · IBGE",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
BASE_URL = "https://servicodados.ibge.gov.br/api/v2/cnae"
 
# Tokens de design
NAVY = "#0B2545"
AZUL = "#1D4ED8"
TEXTO = "#1E293B"
TEXTO_SUAVE = "#64748B"
BORDA = "#E2E8F0"
FUNDO = "#F3F5F9"
 
# Paleta corporativa variada: uma cor por seção da CNAE
PALETA = [
    "#1D4ED8",  # azul royal
    "#0F766E",  # verde petróleo
    "#B45309",  # âmbar queimado
    "#7C3AED",  # violeta
    "#BE123C",  # carmim
    "#0369A1",  # azul aço
    "#4D7C0F",  # verde oliva
    "#A21CAF",  # magenta
    "#C2410C",  # laranja ferrugem
    "#0D9488",  # turquesa
    "#475569",  # grafite
]
 
 
def cor_da_secao(letra: str) -> str:
    if not letra:
        return "#475569"
    return PALETA[(ord(letra[0].upper()) - ord("A")) % len(PALETA)]
 
 
# ───────────────────────── Estilo ─────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
 
    html, body, [class*="css"], .stApp {{ font-family: 'Inter', sans-serif; color: {TEXTO}; }}
    .stApp {{ background: {FUNDO}; }}
    #MainMenu, footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1240px; }}
 
    /* Sidebar */
    [data-testid="stSidebar"] {{ background: {NAVY}; border-right: 1px solid rgba(255,255,255,.06); }}
    [data-testid="stSidebar"] * {{ color: #CBD5E1 !important; }}
    [data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,.12); }}
    [data-testid="stSidebar"] .stRadio label {{
        padding: .55rem .8rem; border-radius: 8px; width: 100%; font-weight: 500;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{ background: rgba(255,255,255,.07); }}
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {{
        background: rgba(255,255,255,.14); box-shadow: inset 3px 0 0 #60A5FA;
    }}
    [data-testid="stSidebar"] .stRadio label > div:first-child {{ display: none; }}
    [data-testid="stSidebar"] .stButton button {{
        background: transparent; border: 1px solid rgba(255,255,255,.25); color: #E2E8F0 !important;
    }}
    [data-testid="stSidebar"] .stButton button:hover {{ background: rgba(255,255,255,.1); }}
    .marca {{ font-size: 1.15rem; font-weight: 700; color: #fff !important; letter-spacing: .2px; }}
    .marca-sub {{ font-size: .78rem; color: #94A3B8 !important; margin-top: .15rem; }}
 
    /* Cabeçalho da página */
    .topo {{
        background: #fff; border: 1px solid {BORDA}; border-radius: 12px;
        padding: 1.4rem 1.7rem; margin-bottom: 1.4rem; border-top: 4px solid {AZUL};
    }}
    .topo .trilha {{ font-size: .78rem; color: {TEXTO_SUAVE}; margin-bottom: .3rem; }}
    .topo h1 {{ margin: 0; font-size: 1.6rem; font-weight: 700; color: {NAVY}; padding: 0; }}
    .topo p {{ margin: .35rem 0 0 0; color: {TEXTO_SUAVE}; font-size: .93rem; }}
 
    /* Indicadores */
    .kpi {{
        background: #fff; border: 1px solid {BORDA}; border-radius: 12px; padding: 1.1rem 1.3rem;
        position: relative; overflow: hidden;
    }}
    .kpi::before {{ content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px; background: var(--cor); }}
    .kpi .rotulo {{ font-size: .8rem; color: {TEXTO_SUAVE}; font-weight: 500; }}
    .kpi .valor {{ font-size: 1.9rem; font-weight: 700; color: {NAVY}; line-height: 1.2; }}
    .kpi .nota {{ font-size: .76rem; color: var(--cor); font-weight: 600; }}
 
    /* Painéis */
    .painel-titulo {{ font-size: 1rem; font-weight: 600; color: {NAVY}; margin: 0 0 .1rem 0; }}
    .painel-sub {{ font-size: .8rem; color: {TEXTO_SUAVE}; margin-bottom: .4rem; }}
    div[data-testid="stPlotlyChart"] {{
        background: #fff; border: 1px solid {BORDA}; border-radius: 12px; padding: .6rem;
    }}
    div[data-testid="stDataFrame"] {{ border: 1px solid {BORDA}; border-radius: 12px; overflow: hidden; }}
 
    /* Cards de seção */
    .card-secao {{
        background: #fff; border: 1px solid {BORDA}; border-radius: 12px; padding: 1.1rem 1.2rem;
        margin-bottom: 1rem; min-height: 158px; display: flex; flex-direction: column;
    }}
    .card-secao .cab {{ display: flex; align-items: center; gap: .7rem; margin-bottom: .7rem; }}
    .card-secao .letra {{
        width: 36px; height: 36px; border-radius: 8px; background: var(--cor); color: #fff;
        display: flex; align-items: center; justify-content: center; font-weight: 700;
    }}
    .card-secao .qtd {{ font-size: .78rem; font-weight: 600; color: var(--cor);
        background: color-mix(in srgb, var(--cor) 10%, white); padding: .15rem .6rem; border-radius: 999px; }}
    .card-secao .titulo {{ font-size: .9rem; font-weight: 500; color: {TEXTO}; line-height: 1.45; }}
 
    /* Resultados */
    .resultado {{
        background: #fff; border: 1px solid {BORDA}; border-left: 4px solid var(--cor);
        border-radius: 8px; padding: .75rem 1rem; margin-bottom: .5rem; font-size: .92rem;
    }}
    .resultado .cod {{ font-weight: 700; color: var(--cor); margin-right: .6rem; }}
    .resultado .caminho {{ font-size: .76rem; color: {TEXTO_SUAVE}; margin-top: .2rem; }}
    .tag {{
        display: inline-block; padding: .2rem .7rem; border-radius: 6px; margin-right: .4rem;
        font-size: .78rem; font-weight: 600; color: #fff; background: var(--cor);
    }}
 
    /* Controles */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{ border-radius: 8px; }}
    .stDownloadButton button {{
        background: {AZUL}; color: #fff; border: 0; border-radius: 8px; font-weight: 600;
    }}
    .stDownloadButton button:hover {{ background: #1E40AF; color: #fff; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 600; }}
    </style>
    """,
    unsafe_allow_html=True,
)
 
 
# ───────────────────────── Componentes ─────────────────────────
def cabecalho(trilha: str, titulo: str, descricao: str):
    st.markdown(
        f'<div class="topo"><div class="trilha">CNAE › {html.escape(trilha)}</div>'
        f"<h1>{html.escape(titulo)}</h1><p>{html.escape(descricao)}</p></div>",
        unsafe_allow_html=True,
    )
 
 
def kpi(rotulo: str, valor, cor: str, nota: str = ""):
    st.markdown(
        f'<div class="kpi" style="--cor:{cor}"><div class="rotulo">{rotulo}</div>'
        f'<div class="valor">{valor}</div><div class="nota">{nota}&nbsp;</div></div>',
        unsafe_allow_html=True,
    )
 
 
def painel(titulo: str, sub: str = ""):
    st.markdown(
        f'<div class="painel-titulo">{titulo}</div><div class="painel-sub">{sub}</div>',
        unsafe_allow_html=True,
    )
 
 
def estilizar(fig, altura=380):
    fig.update_layout(
        template="plotly_white",
        height=altura,
        font=dict(family="Inter, sans-serif", color=TEXTO, size=12),
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig
 
 
def baixar_csv(df: pd.DataFrame, nome: str, chave: str):
    st.download_button(
        "Exportar CSV",
        df.to_csv(index=False, sep=";").encode("utf-8-sig"),
        file_name=nome,
        mime="text/csv",
        key=chave,
    )
 
 
def normalizar(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return sem_acento.lower()
 
 
# ───────────────────────── Dados ─────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def buscar(endpoint: str):
    resposta = requests.get(f"{BASE_URL}/{endpoint}", timeout=20)
    resposta.raise_for_status()
    return resposta.json()
 
 
@st.cache_data(ttl=3600, show_spinner="Carregando dados do IBGE…")
def carregar_tudo():
    secoes_raw, divisoes_raw, grupos_raw = buscar("secoes"), buscar("divisoes"), buscar("grupos")
 
    secoes = pd.DataFrame(
        [
            {"codigo": s["id"], "descricao": s["descricao"], "qtd_divisoes": len(s.get("divisoes") or [])}
            for s in secoes_raw
        ]
    )
    divisoes = pd.DataFrame(
        [
            {
                "codigo": d["id"],
                "descricao": d["descricao"],
                "secao": (d.get("secao") or {}).get("id", ""),
                "secao_descricao": (d.get("secao") or {}).get("descricao", ""),
            }
            for d in divisoes_raw
        ]
    )
    grupos = pd.DataFrame(
        [
            {
                "codigo": g["id"],
                "descricao": g["descricao"],
                "divisao": (g.get("divisao") or {}).get("id", ""),
                "divisao_descricao": (g.get("divisao") or {}).get("descricao", ""),
                "secao": ((g.get("divisao") or {}).get("secao") or {}).get("id", ""),
            }
            for g in grupos_raw
        ]
    )
    return secoes, divisoes, grupos
 
 
try:
    df_secoes, df_divisoes, df_grupos = carregar_tudo()
except requests.RequestException as erro:
    st.error("Não foi possível acessar a API do IBGE. Verifique sua conexão e tente novamente.")
    st.caption(f"Detalhe técnico: {erro}")
    st.stop()
 
# ───────────────────────── Sidebar ─────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="marca">Painel CNAE</div>'
        '<div class="marca-sub">Classificação Nacional de Atividades Econômicas</div>',
        unsafe_allow_html=True,
    )
    st.divider()
    pagina = st.radio(
        "Navegação",
        ["Visão geral", "Seções", "Divisões", "Hierarquia", "Busca"],
        label_visibility="collapsed",
    )
    st.divider()
    if st.button("Atualizar dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("Fonte: IBGE · servicodados.ibge.gov.br")
 
# ───────────────────────── Páginas ─────────────────────────
if pagina == "Visão geral":
    cabecalho(
        "Visão geral",
        "Panorama da CNAE",
        "Estrutura oficial das atividades econômicas do Brasil, com dados em tempo real da API do IBGE.",
    )
 
    media = len(df_divisoes) / max(len(df_secoes), 1)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi("Seções", len(df_secoes), PALETA[0], "Nível 1")
    with k2:
        kpi("Divisões", len(df_divisoes), PALETA[1], "Nível 2")
    with k3:
        kpi("Grupos", len(df_grupos), PALETA[2], "Nível 3")
    with k4:
        kpi("Divisões por seção", f"{media:.1f}", PALETA[3], "Média")
    st.write("")
 
    contagem = df_divisoes.groupby("secao").size().reset_index(name="divisoes").sort_values("secao")
    cores = {s: cor_da_secao(s) for s in contagem["secao"]}
 
    c1, c2 = st.columns([3, 2])
    with c1:
        painel("Divisões por seção", "Quantidade de divisões em cada seção da CNAE")
        fig = px.bar(contagem, x="secao", y="divisoes", color="secao", color_discrete_map=cores,
                     text="divisoes", labels={"secao": "Seção", "divisoes": "Divisões"})
        fig.update_traces(textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False)
        st.plotly_chart(estilizar(fig), use_container_width=True)
    with c2:
        painel("Participação por seção", "Proporção do total de divisões")
        fig2 = px.pie(contagem, names="secao", values="divisoes", hole=0.6,
                      color="secao", color_discrete_map=cores)
        fig2.update_traces(textinfo="label", marker=dict(line=dict(color="white", width=2)))
        fig2.update_layout(showlegend=False)
        st.plotly_chart(estilizar(fig2), use_container_width=True)
 
    painel("Grupos por seção", "Seções com maior detalhamento na classificação")
    gps = df_grupos.groupby("secao").size().reset_index(name="grupos").sort_values("grupos")
    fig3 = px.bar(gps, x="grupos", y="secao", orientation="h", color="secao",
                  color_discrete_map={s: cor_da_secao(s) for s in gps["secao"]},
                  labels={"secao": "Seção", "grupos": "Grupos"})
    fig3.update_traces(marker_line_width=0)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(estilizar(fig3, 440), use_container_width=True)
 
elif pagina == "Seções":
    cabecalho("Seções", "Seções da CNAE", "Nível mais amplo da classificação, identificado por letras.")
    filtro = st.text_input("Filtrar seções", placeholder="Ex.: agricultura, comércio, saúde")
    dados = df_secoes
    if filtro:
        dados = dados[dados["descricao"].map(normalizar).str.contains(normalizar(filtro), regex=False)]
 
    if dados.empty:
        st.info("Nenhuma seção encontrada. Tente outro termo.")
    else:
        colunas = st.columns(3)
        for i, (_, s) in enumerate(dados.iterrows()):
            with colunas[i % 3]:
                st.markdown(
                    f"""<div class="card-secao" style="--cor:{cor_da_secao(s['codigo'])}">
                    <div class="cab"><div class="letra">{html.escape(s['codigo'])}</div>
                    <div class="qtd">{s['qtd_divisoes']} divisões</div></div>
                    <div class="titulo">{html.escape(s['descricao'])}</div></div>""",
                    unsafe_allow_html=True,
                )
        baixar_csv(dados, "cnae_secoes.csv", "dl_secoes")
 
elif pagina == "Divisões":
    cabecalho("Divisões", "Divisões da CNAE", "Segundo nível da classificação, identificado por 2 dígitos.")
    f1, f2 = st.columns([1, 2])
    with f1:
        secao_sel = st.selectbox("Seção", ["Todas"] + sorted(df_divisoes["secao"].unique()))
    with f2:
        termo = st.text_input("Buscar na descrição", placeholder="Ex.: fabricação, transporte")
 
    dados = df_divisoes
    if secao_sel != "Todas":
        dados = dados[dados["secao"] == secao_sel]
    if termo:
        dados = dados[dados["descricao"].map(normalizar).str.contains(normalizar(termo), regex=False)]
 
    m1, m2, _ = st.columns([1, 1, 2])
    with m1:
        kpi("Divisões exibidas", len(dados), PALETA[1])
    with m2:
        kpi("Seções envolvidas", dados["secao"].nunique(), PALETA[2])
    st.write("")
 
    if dados.empty:
        st.info("Nenhuma divisão encontrada com esses filtros.")
    else:
        tabela = dados.rename(columns={"codigo": "Divisão", "descricao": "Descrição",
                                       "secao": "Seção", "secao_descricao": "Descrição da seção"})
        st.dataframe(tabela, use_container_width=True, hide_index=True, height=470)
        baixar_csv(tabela, "cnae_divisoes.csv", "dl_divisoes")
 
elif pagina == "Hierarquia":
    cabecalho("Hierarquia", "Explorar hierarquia", "Escolha uma seção e uma divisão para ver os grupos que a compõem.")
    idx = df_secoes.set_index("codigo")
    secao_cod = st.selectbox("Seção", df_secoes["codigo"],
                             format_func=lambda c: f"{c} · {idx.loc[c, 'descricao']}")
    cor = cor_da_secao(secao_cod)
    divs = df_divisoes[df_divisoes["secao"] == secao_cod]
    didx = divs.set_index("codigo")
    div_cod = st.selectbox("Divisão", divs["codigo"],
                           format_func=lambda c: f"{c} · {didx.loc[c, 'descricao']}")
    grupos = df_grupos[df_grupos["divisao"] == div_cod]
 
    st.markdown(
        f'<span class="tag" style="--cor:{cor}">Seção {secao_cod}</span>'
        f'<span class="tag" style="--cor:#0369A1">Divisão {div_cod}</span>'
        f'<span class="tag" style="--cor:#475569">{len(grupos)} grupos</span>',
        unsafe_allow_html=True,
    )
    st.write("")
    if grupos.empty:
        st.info("Esta divisão não possui grupos cadastrados.")
    else:
        for _, g in grupos.iterrows():
            st.markdown(
                f'<div class="resultado" style="--cor:{cor}"><span class="cod">{html.escape(g["codigo"])}</span>'
                f'{html.escape(g["descricao"])}</div>',
                unsafe_allow_html=True,
            )
        baixar_csv(grupos, f"cnae_grupos_divisao_{div_cod}.csv", "dl_grupos")
 
else:  # Busca
    cabecalho("Busca", "Busca global", "Pesquise em seções, divisões e grupos ao mesmo tempo.")
    termo = st.text_input("Termo de busca", placeholder="Ex.: cultivo, restaurantes, software")
 
    if not termo:
        st.info("Digite um termo para começar. A busca ignora acentos e maiúsculas.")
    else:
        alvo = normalizar(termo)
        filtrar = lambda df: df[df["descricao"].map(normalizar).str.contains(alvo, regex=False)]
        r_secoes, r_divs, r_grupos = filtrar(df_secoes), filtrar(df_divisoes), filtrar(df_grupos)
 
        k1, k2, k3 = st.columns(3)
        with k1:
            kpi("Seções", len(r_secoes), PALETA[0])
        with k2:
            kpi("Divisões", len(r_divs), PALETA[1])
        with k3:
            kpi("Grupos", len(r_grupos), PALETA[2])
        st.write("")
 
        def mostrar(df, nivel, caminho):
            if df.empty:
                st.info(f"Nenhum resultado em {nivel}.")
                return
            for _, l in df.head(100).iterrows():
                secao = l["codigo"] if nivel == "seções" else l["secao"]
                st.markdown(
                    f'<div class="resultado" style="--cor:{cor_da_secao(secao)}">'
                    f'<span class="cod">{html.escape(l["codigo"])}</span>{html.escape(l["descricao"])}'
                    f'<div class="caminho">{html.escape(caminho(l))}</div></div>',
                    unsafe_allow_html=True,
                )
            if len(df) > 100:
                st.caption(f"Mostrando os 100 primeiros de {len(df)} resultados.")
 
        t1, t2, t3 = st.tabs(["Seções", "Divisões", "Grupos"])
        with t1:
            mostrar(r_secoes, "seções", lambda l: "Seção")
        with t2:
            mostrar(r_divs, "divisões", lambda l: f"Seção {l['secao']} › Divisão")
        with t3:
            mostrar(r_grupos, "grupos", lambda l: f"Seção {l['secao']} › Divisão {l['divisao']} › Grupo")