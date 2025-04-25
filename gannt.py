# grafico_escalonamento.py

from PIL import Image, ImageTk
import plotly.graph_objects as go
import plotly.colors as pc
import plotly.io as pio
import tempfile


def gerar_grafico_png(processos):
    nomes_unicos = list({p['Processo'] for p in processos})
    paleta = pc.qualitative.Plotly
    while len(paleta) < len(nomes_unicos):
        paleta += paleta

    cores_por_processo = {
        nome: paleta[i] for i, nome in enumerate(sorted(nomes_unicos))
    }

    fig = go.Figure()

    for p in processos:
        fig.add_trace(go.Bar(
            x=[p['Duracao']],
            y=["CPU"],
            base=p['Inicio'],
            name=p['Processo'],
            marker_color=cores_por_processo[p['Processo']],
            orientation='h',
            hovertemplate=f"{p['Processo']}: {p['Inicio']}s → {p['Inicio'] + p['Duracao']}s"
        ))

    fig.update_layout(
        barmode='stack',
        title='Simulação de Escalonamento de Processos no CPU',
        xaxis=dict(
            title='Tempo (segundos)',
            tickmode='linear',
            tick0=0,
            dtick=1
        ),
        yaxis=dict(
            title='',
            showticklabels=False
        ),
        height=300,
        width=800,
        legend_title_text='Processo'
    )

    # Guardar imagem
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    pio.write_image(fig, temp_file.name, format='png')
    return temp_file.name
